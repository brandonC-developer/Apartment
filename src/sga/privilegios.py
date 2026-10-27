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
    # --- inquilinos (E1)
    # Sin DELETE: la retención desasocia con UPDATE (RF-41) y el inquilino se desactiva, no se borra.
    'inquilinos_inquilino': {'tabla': ('SELECT', 'INSERT', 'UPDATE')},
    # Textos informativos: cada versión es inmutable (RF-39).
    'inquilinos_textoconsentimiento': {'tabla': ('SELECT', 'INSERT')},
    # Solo se puede registrar la revocación (sin efecto retroactivo).
    'inquilinos_consentimiento': {'tabla': ('SELECT', 'INSERT'), 'columnas': {'UPDATE': ('revocado_en',)}},
    # Reemplazar una fotografía solo marca la anterior como eliminada (R25).
    'inquilinos_documentoidentidad': {'tabla': ('SELECT', 'INSERT'), 'columnas': {'UPDATE': ('eliminado_en',)}},
    # R12: solo inserción.
    'inquilinos_accesodocumento': {'tabla': ('SELECT', 'INSERT')},
    # --- alquileres (E2)
    # Sin DELETE: la propiedad se marca inactiva, no se borra (RF-06).
    'alquileres_propiedad': {'tabla': ('SELECT', 'INSERT', 'UPDATE')},
    # Del contrato solo cambian la fecha de fin (RF-09 y su renovación), el cierre y la anulación, que se completan una sola vez (R21; disparador).
    'alquileres_contrato': {'tabla': ('SELECT', 'INSERT'), 'columnas': {'UPDATE': ('fecha_fin', 'cerrado_en', 'anulado_en', 'motivo_anulacion')}},
    # El historial de condiciones no se edita: una corrección es una fila nueva (ADR-014).
    'alquileres_condicioncontrato': {'tabla': ('SELECT', 'INSERT')},
    # `importe_inicial` no se actualiza nunca (R12); solo se completa la anulación, una vez.
    'alquileres_obligacion': {'tabla': ('SELECT', 'INSERT'), 'columnas': {'UPDATE': ('anulada_en', 'motivo_anulacion')}},
    # R12: los ajustes de importe son solo inserción (ADR-016).
    'alquileres_ajusteobligacion': {'tabla': ('SELECT', 'INSERT')},
    # Sin eliminado_en: la conservación depende de DP-28 (abierta).
    'alquileres_documentocontrato': {'tabla': ('SELECT', 'INSERT')},
    # R12: solo inserción (decisión 1 de la E2).
    'alquileres_accesodocumentocontrato': {'tabla': ('SELECT', 'INSERT')},
    # Al terminar solo se completan el instante, el resultado y el detalle.
    'alquileres_ejecucionproceso': {'tabla': ('SELECT', 'INSERT'), 'columnas': {'UPDATE': ('terminada_en', 'resultado', 'detalle')}},
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
