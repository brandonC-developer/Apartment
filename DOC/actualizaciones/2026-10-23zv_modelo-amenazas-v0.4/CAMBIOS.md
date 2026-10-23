# Actualización 2026-10-23 (zv) — Modelo de amenazas v0.4

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de amenazas v0.4](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.4_borrador.md) (nuevo; reemplaza a la [v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md), que no se edita), [DAS v0.15](../../fase-2-arquitectura/DAS_SGA_001_v0.15_borrador.md) (solo los tres enlaces al modelo, editado en su sitio), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Origen:** el modelo v0.3 listaba BR-05, BR-06, BR-07 (Nginx y Gunicorn), BR-09 y BR-10 como abiertas; se decidieron en las actualizaciones [(zo)](../2026-10-23zo_br-05-metadatos-imagenes/CAMBIOS.md), [(zp)](../2026-10-23zp_br-06-antivirus/CAMBIOS.md), [(zq)](../2026-10-23zq_br-07-registros-nginx-gunicorn/CAMBIOS.md), [(zr)](../2026-10-23zr_br-09-dispositivo-y-llave-ssh/CAMBIOS.md) y [(zs)](../2026-10-23zs_br-10-transferencia-a-proveedores/CAMBIOS.md); el solicitante pidió redactar la v0.4 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios
| Parte | Cambio |
|---|---|
| Encabezado e historial | Versión 0.4 |
| AM-02, AM-15 | Procedimiento del dispositivo y de la llave SSH en la fase 6 (BR-09); la llave física FIDO2 queda como mejora futura; ya no remiten a una brecha |
| AM-07 | Decodificación completa de la imagen (CA-83), sin antivirus (BR-06); queda el riesgo de una falla de la biblioteca de imágenes |
| AM-09 | Eliminación de metadatos en el servidor y medición de la E2 (BR-05, CA-82); DP-27 resuelta |
| AM-11, AM-20 | Remiten a la consulta al abogado DP-31 (BR-10) |
| AM-26 | Formato propio de Nginx, Gunicorn sin registro de acceso, 14 días (BR-07); sigue pendiente la rotación de journald, de la auditoría y de PostgreSQL |
| Sección 8 | BR-05, BR-06, BR-09 **decididas**; BR-07 **decidida en lo esencial**; BR-10 **remitida al abogado, sin resolver** |
| Fuentes, mantenimiento y sección 9 | Fuente nueva de las cinco decisiones; la revisión se dispara por DP-31, por la rotación de registros y por la medición de E2 |

**Sin amenazas nuevas y sin cambios de nivel:** siguen 28 amenazas, 1 alto (AM-02), 20 medios y 7 bajos. Es juicio del asistente: en una escala de tres niveles los controles nuevos no mueven ninguna casilla.

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** BR-05, BR-06, BR-07, BR-09 y consultar al abogado por BR-10 (actualizaciones (zo) a (zs)).
- **Propuesta del asistente, sin decidir:** que los niveles no cambien; que decodificar baste sin antivirus; los 14 días; la lista de prácticas del dispositivo.

## 3. Qué no se hizo
- No se añadió ninguna amenaza nueva (por ejemplo, la salida a internet o una falla de la biblioteca de imágenes como fila propia) ni se evaluó si hacen falta.
- No se verificó ningún control: no hay servidor. Sigue sin revisión de otra persona (DP-23): la pregunta «¿lo hicimos suficientemente bien?» sigue abierta.
- No se releyó la ERS v1.16 ni el DAS v0.15 enteros; los controles nuevos se tomaron de sus actualizaciones y de los ADR.
- El resumen para el abogado sigue en la ERS v1.8 y no incluye DP-31.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
