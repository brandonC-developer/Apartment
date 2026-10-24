"""Respaldo cifrado y su restauración (ADR-024, ADR-032 decisiones 9 y 15; RNF-09).

Ejecutan de verdad `respaldo/respaldar.sh` y `respaldo/restaurar.sh` con `age`, `pg_dump`,
`pg_restore`, `tar` y bash contra la base de pruebas. Se omiten si falta alguna herramienta, si el
`pg_dump` no es de la misma versión mayor que el servidor o si el usuario no puede crear bases.
"""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.db import connection
from django.test import TransactionTestCase

from cuentas.models import Administrador
from nucleo.models import Organizacion

RESPALDO = Path(settings.BASE_DIR) / 'respaldo'
# Ruta completa: en Windows, `bash` a secas puede resolverse al lanzador de WSL de System32.
BASH = shutil.which('bash')


def _buscar(nombre, variable=None):
    if variable and os.environ.get(variable):
        return os.environ[variable]
    return shutil.which(nombre)


def _posix(ruta):
    """En Windows con Git Bash, `C:/x` lo toma tar por «equipo:ruta»; se pasa la forma /c/x."""
    ruta = str(ruta)
    if os.name == 'nt':
        return subprocess.run(['cygpath', '-u', ruta], capture_output=True, text=True, check=True).stdout.strip()
    return ruta


def _motivo_para_omitir():
    if BASH and 'system32' in BASH.lower():
        return 'bash es el lanzador de WSL, no uno de Git o del sistema'
    for programa in ('bash', 'pg_dump', 'pg_restore', 'psql', 'createdb', 'dropdb', 'tar', 'sha256sum'):
        if not shutil.which(programa):
            return f'falta {programa}'
    if not _buscar('age', 'SGA_AGE'):
        return 'falta age (instálelo o defina SGA_AGE)'
    if not _buscar('age-keygen') and not os.environ.get('SGA_AGE'):
        return 'falta age-keygen'
    try:
        local = subprocess.run(['pg_dump', '--version'], capture_output=True, text=True).stdout
        mayor_local = local.split()[-1].split('.')[0]
    except Exception:
        return 'no se pudo leer la versión de pg_dump'
    if str(connection.pg_version // 10000) != mayor_local:
        return f'pg_dump {mayor_local} no coincide con el servidor {connection.pg_version // 10000}'
    with connection.cursor() as c:
        c.execute('SELECT rolsuper OR rolcreatedb FROM pg_roles WHERE rolname = current_user')
        if not c.fetchone()[0]:
            return 'el usuario no puede crear bases'
    return None


class RespaldoYRestauracionTests(TransactionTestCase):
    """TransactionTestCase: los scripts son procesos aparte y solo ven datos confirmados.
    `serialized_rollback` repone los datos que crean las migraciones (la fila de la organización)."""
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.motivo = _motivo_para_omitir()

    def setUp(self):
        if self.motivo:
            self.skipTest(self.motivo)
        self.dir = Path(tempfile.mkdtemp(prefix='sga_respaldo_'))
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.age = _buscar('age', 'SGA_AGE')
        keygen = os.path.join(os.path.dirname(self.age), 'age-keygen') if os.path.dirname(self.age) else 'age-keygen'
        self.keygen = shutil.which(keygen) or shutil.which('age-keygen')
        self.privada = self.dir / 'privada.txt'
        self.publica = self.dir / 'publica.txt'
        self._clave(self.privada, self.publica)
        self.documentos = self.dir / 'documentos'
        self.documentos.mkdir()
        (self.documentos / 'foto con espacios.jpg').write_bytes(b'TEXTO-IDENTIFICABLE-DE-UNA-CEDULA ' * 50)
        (self.documentos / 'sub').mkdir()
        (self.documentos / 'sub' / 'otra.png').write_bytes(b'\x89PNG' + bytes(range(256)))
        self.destino = self.dir / 'respaldos'
        self.destino.mkdir()
        self.admin = Administrador.objects.crear_administrador('admin_de_respaldo_prueba', 'una contrasena larga de prueba')
        self.env = {
            **os.environ,
            'PGHOST': str(connection.settings_dict['HOST'] or ''), 'PGPORT': str(connection.settings_dict['PORT'] or ''),
            'PGUSER': connection.settings_dict['USER'] or '', 'PGPASSWORD': connection.settings_dict['PASSWORD'] or '',
            'SGA_BD_NOMBRE': connection.settings_dict['NAME'], 'SGA_AGE': _posix(self.age),
            'SGA_RESPALDO_DESTINO': _posix(self.destino), 'SGA_RESPALDO_CLAVE_PUBLICA': _posix(self.publica),
            'SGA_DOCUMENTOS': _posix(self.documentos),
        }
        self.bases_creadas = []
        self.addCleanup(self._borrar_bases)

    def _clave(self, privada, publica):
        subprocess.run([self.keygen, '-o', str(privada)], check=True, capture_output=True)
        salida = subprocess.run([self.keygen, '-y', str(privada)], check=True, capture_output=True, text=True).stdout
        Path(publica).write_text(salida)

    def _borrar_bases(self):
        for base in self.bases_creadas:
            subprocess.run(['dropdb', '--if-exists', base], env=self.env, capture_output=True)

    def correr(self, guion, *args, **entorno):
        return subprocess.run(
            [BASH, _posix(RESPALDO / guion), *args], env={**self.env, **entorno}, capture_output=True, text=True)

    def respaldar(self, **entorno):
        return self.correr('respaldar.sh', **entorno)

    def restaurar(self, fecha, base=None, privada=None, **extra):
        args = ['--fecha', fecha, '--clave-privada', _posix(privada or self.privada),
                '--origen', _posix(self.destino)]
        if base:
            args += ['--base-destino', base]
            self.bases_creadas.append(base)
        for clave, valor in extra.items():
            args += [f"--{clave.replace('_', '-')}"] + ([_posix(valor)] if valor is not True else [])
        return self.correr('restaurar.sh', *args)

    def fecha(self):
        return sorted(self.destino.glob('*.sha256'))[0].stem

    # ------------------------------------------------------------------
    def test_el_respaldo_deja_tres_archivos_cifrados_sus_sumas_y_la_marca(self):
        r = self.respaldar()
        self.assertEqual(r.returncode, 0, r.stderr)
        fecha = self.fecha()
        for parte in ('base.dump.age', 'globales.sql.age', 'documentos.tar.age'):
            contenido = (self.destino / f'{fecha}_{parte}').read_bytes()
            self.assertTrue(contenido.startswith(b'age-encryption.org/v1'), parte)
        self.assertTrue((self.destino / 'ultimo_respaldo_correcto').read_text().strip().endswith('Z'))
        self.assertEqual([p.name for p in self.destino.iterdir() if p.name.startswith('.en_curso')], [])

    def test_nada_queda_en_claro(self):
        self.respaldar()
        todo = b''.join(p.read_bytes() for p in self.destino.iterdir() if p.is_file())
        self.assertNotIn(b'TEXTO-IDENTIFICABLE-DE-UNA-CEDULA', todo)
        self.assertNotIn(b'admin_de_respaldo_prueba', todo)
        self.assertNotIn(b'PGDMP', todo)  # cabecera del formato personalizado de pg_dump
        self.assertNotIn(b'CREATE ROLE', todo)

    def test_restaurar_devuelve_la_base_y_los_documentos(self):
        self.respaldar()
        r = self.restaurar(self.fecha(), base='sga_restauracion_prueba', documentos_destino=self.dir / 'recuperados')
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertIn('restaurada', r.stdout)
        usuarios = subprocess.run(
            ['psql', '-X', '-tA', '-d', 'sga_restauracion_prueba', '-c', 'SELECT usuario FROM cuentas_administrador'],
            env=self.env, capture_output=True, text=True).stdout.split()
        self.assertEqual(usuarios, ['admin_de_respaldo_prueba'])
        for ruta in self.documentos.rglob('*'):
            if ruta.is_file():
                copia = self.dir / 'recuperados' / ruta.relative_to(self.documentos)
                self.assertEqual(copia.read_bytes(), ruta.read_bytes())

    def test_con_la_clave_equivocada_falla_y_no_deja_base(self):
        self.respaldar()
        otra = self.dir / 'otra_privada.txt'
        self._clave(otra, self.dir / 'otra_publica.txt')
        r = self.restaurar(self.fecha(), base='sga_restauracion_clave_mala', privada=otra)
        self.assertNotEqual(r.returncode, 0)
        existe = subprocess.run(['psql', '-X', '-tA', '-d', 'postgres', '-c',
                                 "SELECT 1 FROM pg_database WHERE datname = 'sga_restauracion_clave_mala'"],
                                env=self.env, capture_output=True, text=True).stdout.strip()
        self.assertEqual(existe, '')

    def test_un_archivo_alterado_se_detecta_por_su_suma(self):
        self.respaldar()
        archivo = next(self.destino.glob('*_base.dump.age'))
        datos = bytearray(archivo.read_bytes())
        datos[len(datos) // 2] ^= 0xFF
        archivo.write_bytes(bytes(datos))
        r = self.restaurar(self.fecha(), solo_verificar=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('no coinciden', r.stderr)

    def test_no_pisa_una_base_existente_ni_una_carpeta_con_contenido(self):
        self.respaldar()
        fecha = self.fecha()
        r = self.restaurar(fecha, base=connection.settings_dict['NAME'])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('ya existe', r.stderr)
        r = self.restaurar(fecha, base='sga_restauracion_carpeta', documentos_destino=self.documentos)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('no está vacía', r.stderr)

    def test_solo_verificar_no_crea_nada(self):
        self.respaldar()
        r = self.restaurar(self.fecha(), solo_verificar=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('se descifran', r.stdout)

    def test_si_el_respaldo_falla_no_se_toca_la_marca_ni_quedan_restos(self):
        self.respaldar()
        marca = (self.destino / 'ultimo_respaldo_correcto').read_text()
        r = self.respaldar(SGA_BD_NOMBRE='base_que_no_existe')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual((self.destino / 'ultimo_respaldo_correcto').read_text(), marca)
        self.assertEqual([p.name for p in self.destino.iterdir() if p.name.startswith('.en_curso')], [])

    def test_se_niega_si_la_clave_publica_falta_es_privada_o_no_hay_carpeta_de_documentos(self):
        r = self.respaldar(SGA_RESPALDO_CLAVE_PUBLICA=_posix(self.dir / 'no_existe.txt'))
        self.assertNotEqual(r.returncode, 0)
        r = self.respaldar(SGA_RESPALDO_CLAVE_PUBLICA=_posix(self.privada))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('PRIVADA', r.stderr)
        r = self.respaldar(SGA_DOCUMENTOS=_posix(self.dir / 'no_existe'))
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(list(self.destino.glob('*.age')), [])

    def test_la_retencion_borra_los_respaldos_viejos_y_solo_ellos(self):
        viejos = [self.destino / '2020-01-01_base.dump.age', self.destino / '2020-01-01.sha256']
        reciente = self.destino / '2026-10-10_base.dump.age'
        ajeno = self.destino / 'notas.txt'
        for ruta in (*viejos, reciente, ajeno):
            ruta.write_text('x')
        hace = 60 * 24 * 3600
        for ruta in (*viejos, ajeno):
            os.utime(ruta, (os.path.getmtime(ruta) - hace, os.path.getmtime(ruta) - hace))
        os.utime(reciente, (os.path.getmtime(reciente) - 10 * 24 * 3600,) * 2)
        r = self.respaldar()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(any(v.exists() for v in viejos))
        self.assertTrue(reciente.exists())
        self.assertTrue(ajeno.exists())

    def test_se_puede_respaldar_dos_veces_el_mismo_dia(self):
        self.assertEqual(self.respaldar().returncode, 0)
        self.assertEqual(self.respaldar().returncode, 0)
        self.assertEqual(len(list(self.destino.glob('*.sha256'))), 1)
        self.assertEqual(self.restaurar(self.fecha(), solo_verificar=True).returncode, 0)

    def test_si_la_restauracion_falla_a_medias_se_borra_la_base_nueva(self):
        """La consulta de cordura detecta una base sin organización y la restauración no queda a medias."""
        Organizacion.objects.all().delete()
        self.respaldar()
        r = self.restaurar(self.fecha(), base='sga_restauracion_a_medias')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('organización', r.stderr)
        existe = subprocess.run(['psql', '-X', '-tA', '-d', 'postgres', '-c',
                                 "SELECT 1 FROM pg_database WHERE datname = 'sga_restauracion_a_medias'"],
                                env=self.env, capture_output=True, text=True).stdout.strip()
        self.assertEqual(existe, '')

    def test_un_fallo_en_la_ultima_parte_no_deja_marca_ni_archivos(self):
        """Si el cifrado de los documentos falla, el respaldo no cuenta como correcto."""
        envoltorio = self.dir / 'age_que_falla.sh'
        envoltorio.write_text('\n'.join([
            '#!/usr/bin/env bash',
            'n=$(cat "$CONTADOR" 2>/dev/null || echo 0); n=$((n+1)); echo $n > "$CONTADOR"',
            'if [ "$n" -ge 3 ]; then echo "falla simulada" >&2; exit 1; fi',
            'exec "$AGE_REAL" "$@"',
            '',
        ]), newline='\n')
        envoltorio.chmod(0o755)
        r = self.respaldar(SGA_AGE=_posix(envoltorio), AGE_REAL=self.env['SGA_AGE'], CONTADOR=_posix(self.dir / 'contador'))
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse((self.destino / 'ultimo_respaldo_correcto').exists())
        self.assertEqual(list(self.destino.iterdir()), [])
