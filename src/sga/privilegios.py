"""Privilegios del rol de la aplicación, tabla por tabla (ADR-027, ADR-031 decisión 3).

Este es «el archivo de privilegios» del ADR-031: el formato (un módulo de Python y no un script SQL)
es propuesta del asistente porque el ADR dejó el formato pendiente; así la prueba puede comparar las
tablas reales con las entradas. Una tabla sin entrada no recibe ningún privilegio: la aplicación
falla de forma visible en vez de quedar abierta, y una prueba exige una entrada por cada tabla.

Cada entrada: `tabla` son los privilegios de toda la tabla; `columnas` son privilegios solo sobre
las columnas indicadas. Lo que no consta no se concede. El rol de la aplicación nunca recibe
TRUNCATE, REFERENCES, TRIGGER ni la propiedad de ninguna tabla.
"""

# R12 (ADR-027): solo SELECT e INSERT en movimientos, ajustes de obligación, auditoría y accesos a
# documentos. Las tablas de las entregas E1 a E3 se agregan aquí con sus modelos.
PRIVILEGIOS = {
    # --- nucleo
    'nucleo_auditoria': {'tabla': ('SELECT', 'INSERT')},  # R12
    # Una sola fila: la crea la migración; INSERT solo por si faltara (organizacion.actual()).
    'nucleo_organizacion': {'tabla': ('SELECT', 'INSERT', 'UPDATE')},
    # --- cuentas
    # Sin DELETE: la cuenta única no se borra. UPDATE por el contador de intentos, el último
    # intervalo TOTP, el token de registro y last_login.
    'cuentas_administrador': {'tabla': ('SELECT', 'INSERT', 'UPDATE')},
    # DELETE porque emitir códigos nuevos y el rescate borran los anteriores. Excepción al ADR-027
    # (que proponía solo UPDATE de usado_en), DECIDIDA por el solicitante el 24-oct-2026 (actualización
    # 2026-10-24o): no es historia del negocio y no da más poder que marcarlos todos como usados.
    # Un código usado solo puede cambiar su marca de uso.
    'cuentas_codigorecuperacion': {'tabla': ('SELECT', 'INSERT', 'DELETE'), 'columnas': {'UPDATE': ('usado_en',)}},
    # --- Django
    # DELETE por clearsessions y por el cierre de sesiones (ADR-031, corrección a ADR-027).
    'django_session': {'tabla': ('SELECT', 'INSERT', 'UPDATE', 'DELETE')},
    # Solo el rol dueño las usa (migraciones y creación de permisos); la aplicación no.
    'django_migrations': {},
    'django_content_type': {},
    'auth_permission': {},
    'auth_group': {},
    'auth_group_permissions': {},
}
