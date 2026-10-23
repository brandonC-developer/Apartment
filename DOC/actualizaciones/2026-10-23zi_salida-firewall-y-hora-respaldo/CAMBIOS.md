# Actualización 2026-10-23 (zi) — Salida de los firewalls, hora del respaldo y aviso de fallo del respaldo

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; las decisiones se incorporarán en el DAS (ADR-032, ADR-024, ADR-013), en la ERS (extensión de RF-49, versión nueva), en el modelo de amenazas (versión nueva) y en el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** pendientes de la decisión 2 de ADR-032 ("la regla de salida queda sin decidir") y de ADR-024 ("hora del respaldo"), registrados en la [actualización 2026-10-23 (p)](../2026-10-23p_endurecimiento-02-firewall/CAMBIOS.md) y en el [DAS v0.13](../../fase-2-arquitectura/DAS_SGA_001_v0.13_borrador.md); AM-25 del [modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué tráfico saliente se permite? | "Denegar por defecto; permitir DNS, 80, 443, NTP, 2465/2587 e ICMP" (recomendada por el asistente) | En el Cloud Firewall y en UFW, con las mismas reglas: salida **denegada por defecto**, permitida solo por puerto para DNS (53), HTTP (80), HTTPS (443), NTP (123/UDP), SMTP de Resend (2465 o 2587) e ICMP; sin limitar por dirección de destino |
| 2 | ¿A qué hora corre el respaldo diario? | "05:00 hora de Costa Rica, después del reinicio" (recomendada) | A las 05:00 hora de Costa Rica (11:00 UTC), con un temporizador de systemd con `Persistent=yes`; después del reinicio de las 04:00 y antes del proceso diario de las 07:00 |
| 3 | ¿Se avisa si el respaldo falla o no corre? | "Sí, con el temporizador existente y un límite de 26 horas" (recomendada) | El temporizador de intervalo corto que ya vigila el proceso diario (ADR-013, cada minuto) comprueba una marca del **último respaldo correcto**; si tiene más de 26 horas registra un aviso, lo muestra como alerta web persistente y lo envía por correo. La marca se escribe solo cuando la subida a Spaces terminó bien. **Es un requisito nuevo** (extender RF-49), que se redacta en una ERS posterior |

## 2. Hallazgo que hizo obligatoria la decisión 1
Según la documentación de DigitalOcean, en un Cloud Firewall **"si no hay reglas de salida configuradas, no se permite ningún tráfico saliente"**. Con solo las reglas de entrada de ADR-032, el servidor no podría actualizar paquetes, enviar correo por Resend, renovar el certificado ni subir los respaldos. La regla de salida no podía seguir sin decidir.

## 3. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| DigitalOcean, configurar reglas de Cloud Firewalls: https://docs.digitalocean.com/products/networking/firewalls/how-to/configure-rules/ | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | Las reglas de salida limitan puertos y destinos; sin reglas de salida no se permite ningún tráfico saliente; lo que no coincide con ninguna regla se deniega | No indica qué reglas de salida trae un firewall nuevo |
| NIST SP 800-41 Rev. 1, *Guidelines on Firewalls and Firewall Policy* (2009): https://csrc.nist.gov/pubs/sp/800/41/r1/final | Estándar | PDF **leído en local con `pdftotext`** (secciones 2 y 4); texto citado: el tráfico entrante y saliente no permitido expresamente debe bloquearse ("deny by default"); la política debe basarse en un análisis de riesgo | Denegar por defecto en las dos direcciones | De 2009; no se leyó el documento completo; no trata nuestro caso de un Droplet |
| Manual de UFW, Ubuntu | Documentación oficial | Leído por resumen (actualización (p)) | La política de salida por defecto es permitir | El cambio a "denegar" en UFW no se probó |
| DigitalOcean, respaldos de Droplets: https://docs.digitalocean.com/products/backups/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Crear un respaldo o instantánea tarda unos 2 minutos por GB usado; los intervalos son de 4, 6 o 12 horas, diarios o semanales | **No dice a qué hora corre el respaldo semanal ni si se puede elegir** |
| PostgreSQL, `pg_dump` (ADR-024) | Documentación oficial | Leída por resumen (20-oct-2026) | Copias consistentes con la base en uso | — |
| Google SRE, respuesta a emergencias: https://sre.google/sre-book/emergency-response/ | Libro de expertos | Leída por resumen (23-oct-2026) | Solo respalda probar los procedimientos de recuperación; **no habla de vigilar respaldos** | — |

## 4. Lo que propone el asistente y el solicitante no decidió
- Que la salida se limite por puerto y no por dirección: criterio del asistente (las direcciones de los servicios cambian y mantenerlas sería un riesgo).
- La hora de las 05:00 y el límite de 26 horas: criterio del asistente, sin fuente.
- Una duración del respaldo: sin medir.
- La forma de la marca de éxito (archivo, tabla o registro): sin decidir.

## 5. Qué no se hizo
- No se configuró ningún firewall ni temporizador; es etapa B.
- No se probó la política de salida denegada en UFW ni que los destinos necesarios (Resend, Spaces, Let's Encrypt, repositorios) sean alcanzables solo por esos puertos.
- No se verificó a qué hora corre el respaldo semanal del Droplet ni si colisiona con el nuestro.
- No se midió cuánto tarda el respaldo, ni cuánto pesa una copia diaria completa de los documentos sin deduplicación (en el peor caso, unos 87 GiB en 35 días de los 250 GiB del plan, sin versionado; cálculo del asistente).
- El aviso de fallo del respaldo **no cubre un servidor caído** (la misma limitación que RF-49) y no comprueba que el respaldo se pueda restaurar; eso es la prueba trimestral.
- No se redactó la extensión de RF-49 ni su criterio de aceptación.

## 6. Qué falta hacer
1. ERS: extender RF-49 o crear un requisito para vigilar el respaldo, con su criterio de aceptación (versión nueva).
2. DAS: incorporar las tres decisiones (ADR-032, decisión 2; ADR-024; ADR-013).
3. Modelo de amenazas: AM-25 con el aviso de fallo.
4. Fase 6: tabla de reglas de salida, temporizador del respaldo y marca de éxito.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
