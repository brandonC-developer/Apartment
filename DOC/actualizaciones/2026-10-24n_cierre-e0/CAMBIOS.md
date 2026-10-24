# Actualización 2026-10-24 (n) — Cierre de la entrega E0

**Fecha:** 2026-10-24
**Documentos afectados:** [`AVANCE_IMPLEMENTACION.md`](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [README de la fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md). El plan de implementación v0.1 **no se modifica** (no se versiona por esto). Ningún código cambia.
**Origen:** plan de implementación, secciones 3.1 y 3.2 (definición de terminado y seguimiento); mensaje del solicitante del 24-oct-2026: «Todas las corridas salieron en verde» (informe suyo sobre las Actions de GitHub, sin captura; el asistente no puede verlas); respuesta del solicitante a la pregunta sobre CA-18 (ver sección 3)
**Estado:** E0 *terminada*; no aprobada (ningún documento está aprobado)

## 1. Las nueve condiciones comunes de terminado
| # | Condición | Evidencia |
|---|---|---|
| 1 | Pruebas de los CA asignados en la integración continua; ninguna Alta sin escribir | Corridas en verde informadas por el solicitante; 196 pruebas, también 196 sin omitir en WSL con Python 3.14.4 |
| 2 | Integración continua en verde | Informado por el solicitante: los tres trabajos (`pruebas`, `respaldo`, `auditoria-dependencias`) |
| 3 | `verificar_coherencia.ps1` sin problemas | Sin problemas el 24-oct-2026 |
| 4 | Tablas nuevas en el archivo de privilegios, con su prueba | Actualización 2026-10-24g; una prueba exige una entrada por tabla |
| 5 | Código sin cubrir de los módulos críticos revisado | Actualización 2026-10-24m (**autorrevisión**) |
| 6 | Desplegada en la etapa A con datos ficticios y criterio de salida cumplido | Actualización 2026-10-24j |
| 7 | Ningún dato personal ni secreto en los registros ni en la auditoría | Pruebas de los registros del programa, de la auditoría y del registro de Nginx. En la E0 aún no hay datos personales de terceros; se repite en cada entrega |
| 8 | `CAMBIOS.md` de la entrega y trazabilidad al día | Actualizaciones 2026-10-23zy a 2026-10-24n |
| 9 | Ningún defecto conocido de prioridad Alta abierto | Hasta donde el asistente sabe; las decisiones abiertas de la sección 4 no son defectos |

## 2. Los ocho criterios de aceptación
| CA | Prio. | Resultado | Pruebas principales |
|---|---|---|---|
| CA-13 Una sola cuenta con segundo factor | Alta | Cumplido | Una sola fila por restricción de la tabla; una prueba recorre **todas** las rutas y exige sesión |
| CA-18 Configuración regional | Media | **Parcial: parte de contratos diferida a la E2** | Zona de la organización, formato, instantes en UTC, histórico intacto al cambiar la zona |
| CA-48 Sesión | Alta | Cumplido | Cierre a las 24 h y tras 1 h de inactividad |
| CA-53 Auditoría sin valores personales | Alta | Cumplido | El teléfono consta como cambiado sin su valor; un importe, con anterior y nuevo |
| CA-68 Límite de intentos | Alta | Cumplido en el alcance de la E0 | Espera creciente, reinicio, contador compartido, concurrencia; aviso en la auditoría y alerta web |
| CA-69 Segundo factor y códigos | Alta | Cumplido en el alcance de la E0 | 10 códigos de un solo uso, TOTP sin repetición y con tolerancia, códigos nuevos con la contraseña |
| CA-70 Creación y rescate por el servidor | Alta | Cumplido en el alcance de la E0 | Comandos, registro en el primer ingreso con token, constancia en la auditoría |
| CA-71 Auditoría de autenticación y su consulta | Alta | Cumplido | Fallo y acierto con fecha, hora e IP, sin secretos; consulta de solo lectura que no genera registros |

**«En el alcance de la E0»** significa lo que el plan fijó en HI-01 y HI-05: el aviso de seguridad se **registra y se muestra como alerta en la web**; el envío por correo a las dos direcciones se verifica en la E4. No es un cumplimiento completo del texto de esos tres CA.

## 3. Decisión del solicitante sobre CA-18 (24-oct-2026)
**Pregunta:** CA-18 mezcla la configuración de la organización y el formato (probados) con los contratos en USD, que no existen hasta la E2. El plan exige aceptación escrita del solicitante para diferir un criterio de prioridad Media. **Respuesta:** «Diferir su parte de contratos a la E2 (Recomendado)». **Decisión:** la E0 se da por terminada con CA-18 verificado en lo que le toca; su parte de contratos en USD (y la creación de contratos con CRC y `America/Costa_Rica`) se verifica en la E2. Igual que con CA-47 (HI-02), se anota en el registro de avance en lugar de crear una versión nueva del plan; si prefieres una versión nueva del plan que lo recoja, se hace.

## 4. Lo que la E0 deja abierto (no son condiciones, pero no se pierden)
- **Decisiones del solicitante:** decimales que se muestran en colones; en qué entrega va la pantalla de la organización (propuesta: E4); si los códigos de recuperación mantienen `DELETE` o se marcan como invalidados con una columna propia; si la clave Fernet se guarda también fuera de línea.
- **Alerta persistente por aviso de correo fallido** y el envío por correo de los avisos: E4.
- **Revisión por otra persona** de la seguridad y los datos personales antes de cargar datos reales (plan, sección 3.3): **sin persona designada**.
- Todo lo de la etapa B (Droplet, Spaces, Resend, dominio, Certbot, HSTS y cifrados TLS, rendimiento y el tiempo de restauración con datos reales): E6.
- ERS y DAS siguen sin aprobar; DP-17 a DP-21 y DP-31 (abogado) abiertos; ningún documento está aprobado.

## 5. Lo que cambia ahora
- **No empieza la E1.** CLAUDE.md autoriza la implementación solo para la E0; las demás entregas necesitan la autorización expresa del solicitante, y el plan exige una entrega a la vez.
- El registro de avance muestra E0 *terminada*, 9 de 9 condiciones, 7 de 8 CA.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
