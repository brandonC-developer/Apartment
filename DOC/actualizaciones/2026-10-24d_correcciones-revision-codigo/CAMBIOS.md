# Actualización 2026-10-24 (d) — Correcciones de la revisión de código del registro del segundo factor

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/cuentas/`](../../../src/cuentas/views.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** hallazgos de `/code-review` sobre el commit a097789 (24-oct-2026); instrucción del solicitante: «sí, corrige los 6 defectos con el token» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Hallazgos y corrección
| # | Hallazgo | Corrección | Prueba |
|---|---|---|---|
| 1 | Con solo la contraseña se podía registrar un segundo factor propio y entrar (cuenta nueva o tras el rescate) | **Token de registro** de un solo uso: lo generan `crear_administrador` y `rescatar_segundo_factor`, se imprime una vez, se guarda solo su hash y vale 24 horas. La pantalla de registro pide primero el token; no muestra la clave hasta que es correcto. `activar_segundo_factor` lo vuelve a comprobar bajo bloqueo y lo consume. Un token incorrecto suma al contador compartido de intentos | `TokenDeRegistroTests` |
| 2 | El código con espacios internos («123 456») fallaba y contaba como fallo | `_intervalo_aceptado` quita todo el espacio interno, igual que el segundo paso | `test_codigo_con_espacios_internos_se_acepta` |
| 3 | La respuesta con los 10 códigos podía guardarse en caché | `@never_cache` en la vista de registro (`Cache-Control: no-store`) | `test_los_codigos_no_se_guardan_en_cache` |
| 4 | Cuenta borrada o clave de cifrado cambiada a mitad: error 500 | La vista busca la cuenta sin lanzar error y, si el secreto guardado no se puede descifrar, genera otro | `test_cuenta_borrada_a_mitad_no_da_error`, `test_secreto_guardado_ilegible_se_regenera` |
| 5 | El secreto propuesto sobrevivía a un nuevo primer paso | `_olvidar_primer_paso` descarta también el secreto y la marca del token | `test_el_secreto_no_sobrevive_a_un_nuevo_primer_paso` |
| 6 | El aviso de cinco fallos se ignoraba en el registro (y en el primer paso) | Una función común registra el aviso en el registro del servidor, sin datos personales, en el primer paso, el segundo paso, el token y el registro. **Es provisional**: la alerta en la web y la auditoría dependen de la auditoría base (E0, sección C), y el correo, de la E4 | `test_el_quinto_fallo_deja_aviso_en_el_registro_del_servidor` |

También se unificó la comprobación del primer paso (`_administrador_pendiente`) en el segundo paso y el registro, con una sola consulta.

## 2. Propuestas del asistente (sin aprobar)
- El token en sí: formato (`secrets.token_urlsafe(16)`, 128 bits), vigencia de **24 horas** y hash SHA-256. La ERS dice que el segundo factor se activa «en el primer ingreso» sin decir con qué prueba; esto la añade.
- Un token correcto no reinicia el contador de intentos (solo lo reinicia un segundo factor correcto).
- Cambia el flujo de las actualizaciones 2026-10-24a y 2026-10-24b: la cuenta recién creada o rescatada imprime un token que hay que escribir antes del código.

## 3. Verificación
- **78 pruebas pasan** (14 nuevas de esta actualización, incluida una del flujo con los comandos) en PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows.
- **Mutaciones manuales:** quitar la comprobación del token en `activar_segundo_factor`, quitar `never_cache` y no limpiar el secreto en el primer paso hicieron fallar sus pruebas; se restauró el código. Con la primera mutación solo falla la prueba de la función, porque la vista también bloquea (doble barrera).
- No se probó en navegador. Si la respuesta con los códigos se pierde (cierre del navegador), no se puede recuperar: hay que emitir códigos nuevos, y esa pantalla aún no existe (tarea pendiente de la E0).

## 4. Qué no está hecho
Auditoría base, alerta web del quinto fallo y de los avisos, aviso por correo (E4), pantalla de códigos nuevos, roles de PostgreSQL, WSL, respaldo y CI. 0 de 8 CA de la E0 cumplidos.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
