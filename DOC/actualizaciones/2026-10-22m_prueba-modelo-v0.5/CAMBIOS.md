# Actualización 2026-10-22 (m) — Prueba del modelo de datos v0.5 en PostgreSQL

**Fecha:** 2026-10-22
**Documentos afectados:** [Modelo de datos v0.5](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.5_borrador.md) (sección 12.1 nueva, hallazgo H18, una fila de transacción), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md). La v0.5 se edita en su sitio porque es un borrador del mismo día, no reemplazado ni aprobado.
**Origen:** pendiente de la [actualización 2026-10-22 (l)](../2026-10-22l_modelo-datos-v0.5/CAMBIOS.md) ("las entidades nuevas no están probadas")
**Estado:** autoverificación del asistente; no es revisión por otra persona

## 1. Qué se hizo
- Servidor PostgreSQL 18.4 desechable en el puerto 54329, con directorio de datos temporal; se arrancó, se probó y se borró. **No se tocó el servicio de PostgreSQL instalado**; al terminar el puerto quedó libre y no quedaron directorios temporales.
- Evidencia en [`evidencia/`](evidencia/): [`prueba_modelo_v0.5_postgres.sql`](evidencia/prueba_modelo_v0.5_postgres.sql), [`ejecutar_prueba_v0.5.ps1`](evidencia/ejecutar_prueba_v0.5.ps1) (arranca el servidor, corre el SQL, hace la concurrencia con dos sesiones reales y lo borra todo) y [`resultado_prueba_v0.5.txt`](evidencia/resultado_prueba_v0.5.txt).

## 2. Resultado
**36 de 36 comprobaciones de una sola sesión y 5 de 5 pruebas de concurrencia correctas** (la última ejecución).

| Probado | Resultado |
|---|---|
| R22, R23, R25 | Cumplen, incluido el reemplazo de una cédula tras marcar la anterior como eliminada |
| R24: segundo uso, vencido, inexistente, ya limpiado; archivo de contrato usado como cédula | Cumple; lo rechazado queda sin usar (la transacción se deshace) |
| Limpieza de temporales | Elimina solo lo vencido y no asociado |
| R11 (propuesta de CHECK), destino y cara, `expira_en` = `creado_en` + 24 horas, R12 de `ACCESO_DOCUMENTO` | Cumplen |
| RF-51: inquilino del contrato vigente con un contrato anulado solapado y uno futuro | Un solo inquilino |
| Concurrencia R24 (dos sesiones, mismo identificador) | La segunda espera el bloqueo 2,1 s y falla; queda una sola fotografía |
| Concurrencia R22 sin bloqueo del contrato | La segunda sesión recibe el mismo orden y R22 la rechaza con un error |
| Concurrencia R22 con bloqueo del contrato | Las dos se registran con órdenes distintos |

## 3. Hallazgo H18
Calcular el orden de la fotografía como "máximo más uno" falla bajo concurrencia: R22 protege los datos, pero la segunda sesión recibe un error. **Propuesta del asistente:** bloquear la fila del contrato antes de calcular el orden. Está en el modelo v0.5 (H18 y la transacción "Agregar la fotografía del contrato"); la decisión de adoptarla es del solicitante.

## 4. Errores de la propia prueba (no del modelo)
- El script colgó en el primer intento porque el servidor heredaba la salida de `pg_ctl`; se mató el proceso, se detuvo el servidor y se borró su directorio, y se corrigió el arranque.
- El script no leía los códigos de salida de las sesiones de concurrencia y el orden esperado estaba mal escrito (1,2,3 en lugar de 1,2,3,4); se corrigió y la prueba se repitió completa.

## 5. Límites de la prueba
- **No probado:** que la limpieza también borre el archivo del disco (aquí solo la fila), la ligadura a la sesión (`sesion_hash`, sin decidir), los tipos físicos con Django (`sqlmigrate`), el tope de 5 MB (no está fijada la unidad: 5 000 000 o 5 242 880 bytes) y carga con 50 propiedades.
- Los CHECK de R11, destino y cara y `expira_en` son propuestas del asistente para la prueba, no decisiones.
- Las entidades de apoyo del script (`inquilino`, `propiedad`, `contrato`) son versiones mínimas, no el modelo completo.
- Es autoverificación del asistente, no revisión por otra persona (DP-23).

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |

- **Corrección del 23-oct-2026:** la cifra "2,1 s" de espera de la tabla de la sección 2 salió de un cronómetro defectuoso del script (paraba el reloj de la segunda sesión después de esperar a la primera) y **no demuestra la espera**. Que la segunda sesión falle con "no válido" solo después de la confirmación de la primera sí demuestra el bloqueo. Ver la [actualización 2026-10-23 (h)](../2026-10-23h_prueba-modelo-v0.6/CAMBIOS.md). El script de esa actualización ya mide bien.
