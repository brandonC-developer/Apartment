# Actualización 2026-10-23 (n) — Prueba del modelo de datos v0.7 en PostgreSQL

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md) (sección 12.3 nueva), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md). La v0.7 se edita en su sitio porque es un borrador del mismo día, no reemplazado ni aprobado.
**Origen:** pendiente de la [actualización 2026-10-23 (m)](../2026-10-23m_modelo-datos-v0.7/CAMBIOS.md) ("sin probar en PostgreSQL")
**Estado:** autoverificación del asistente; no es revisión por otra persona

## 1. Qué se hizo
- Servidor PostgreSQL 18.4 desechable en el puerto 54329, con directorio de datos temporal; se arrancó, se probó y se borró. **No se tocó el servicio de PostgreSQL instalado**; al terminar el puerto quedó libre y no quedaron directorios temporales.
- Evidencia en [`evidencia/`](evidencia/): [`prueba_modelo_v0.7_postgres.sql`](evidencia/prueba_modelo_v0.7_postgres.sql), [`ejecutar_prueba_v0.7.ps1`](evidencia/ejecutar_prueba_v0.7.ps1) y [`resultado_prueba_v0.7.txt`](evidencia/resultado_prueba_v0.7.txt). Parten de los de la [prueba de la v0.6](../2026-10-23h_prueba-modelo-v0.6/CAMBIOS.md) con el cronómetro ya corregido.

## 2. Resultado
**44 de 44 comprobaciones de una sola sesión y 7 de 7 pruebas de concurrencia y de archivo huérfano correctas**, a la primera ejecución. Todo lo probado en la v0.6 (R22, R23, R25, R26, R27, H18, H19b, R2, R11, R12, RF-51) se repitió y cumple igual.

| Probado | Resultado |
|---|---|
| R28: las 10 fotografías de un contrato | Se aceptan, órdenes 1 a 10 |
| R28: la fotografía número 11 | La rechaza el servicio con el mensaje de R28 (se comprobó el texto, para distinguirlo del `CHECK`); las 10 anteriores se conservan |
| R28: `INSERT` directo con `orden` 11 | Lo rechaza el `CHECK` |
| R28: otro contrato | No se ve afectado |
| Concurrencia R28 (9 fotografías, dos sesiones a la vez) | La primera registra la 10; la segunda espera y el servicio la rechaza con el mensaje de R28; quedan 10 filas |
| H20 (borrar una fotografía de un contrato lleno y agregar otra) | Con 9 filas, `max(orden) + 1` da 11 y el `CHECK` lo rechaza: el hallazgo es real |

## 3. Qué se aprendió
- **H20 es real, no teórico:** mientras no haya borrado (DP-28) el máximo funciona; si se permite borrar una fotografía, hay que contar las filas y reutilizar el menor `orden` libre. La solución propuesta **no se probó**; solo se comprobó que hace falta.
- El servicio y el `CHECK` se complementan: el usuario ve un mensaje claro y la base impide el estado imposible aunque falle la aplicación.

## 4. Cambios al modelo durante la prueba
Ninguno en el diseño. Solo se agregó la sección 12.3 y se actualizó el estado de la v0.7 en su cabecera y control.

## 5. Límites de la prueba
- **No probado:** el borrado del archivo con Django y el disco real (el patrón se probó en PowerShell con un archivo simulado); el tipo real del archivo; tipos físicos con `sqlmigrate`; carga con 50 propiedades; la solución de H20.
- R26 y R28 se aplican aquí con funciones SQL; en la aplicación real las aplica el servicio (propuesta). Los `CHECK` de R11, R27 y R28 son propuestas del asistente.
- Las entidades de apoyo son versiones mínimas, no el modelo completo.
- Es autoverificación del asistente, no revisión por otra persona (DP-23).

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
