# Actualización 2026-10-21 (l) — HT-06 (actor del proceso diario) y HT-07 (bloqueo de fila)

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md) (RF-28), [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (secciones 6, 8 y 10.2), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md) (AUDITORIA, R19), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md) (HT-06, HT-07), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisiones
| # | Pregunta | Decisión del solicitante | Recomendación | Fuentes |
|---|---|---|---|---|
| 1 | Actor de las operaciones del proceso diario (HT-06) | Actor `sistema`, tipo de actor `proceso` y la ejecución que lo originó | Igual | OWASP, Logging Cheat Sheet (leída por resumen): el "quién" puede ser "human or machine user" y conviene clasificar a los actores conocidos que no son personas. La propuesta concreta es del asistente |
| 2 | Espera ante un bloqueo de fila (HT-07) | Esperar a que termine la primera operación (comportamiento por defecto, sin `nowait`) | Igual | Django, `select_for_update()` (leída por resumen, primera mitad: la segunda mitad de la página no se leyó); PostgreSQL, bloqueos de fila (leída por resumen) |

**Verificación de HT-07:** el DAS 10.2 decía "bloquea la obligación" sin técnica. Ahora consta: `select_for_update()` dentro de `transaction.atomic()`, que en PostgreSQL genera `SELECT ... FOR UPDATE`; fuera de una transacción lanza error; en SQLite no tiene efecto; varias filas se bloquean siempre en el mismo orden para evitar interbloqueos. No se ejecutó ninguna prueba: la de concurrencia sigue siendo trabajo de la implementación.

## 2. Ideas del solicitante registradas (sin decisión)
- **Dos cuentas** (administrador y servicio, o dos personas con roles) y **un sistema aparte tipo CMS**: el solicitante preguntó su opinión y se le recomendó no adoptarlas para HT-06 ni para la v1 (dos cuentas humanas están fuera de alcance en la ERS 2.4 y exigirían cambiar RF-26 a RF-28 y RNF-01; el sitio de administración de Django es una herramienta interna del propio framework y no sustituye las vistas propias; un sistema aparte duplicaría autenticación, despliegue y auditoría). Se anotan junto con la idea del portal del inquilino (2026-10-20h) como ideas futuras. No se eligió ninguna.

## 3. Cambios
- ERS v1.9, RF-28: actor `sistema` y ejecución en las operaciones del proceso diario.
- DAS v0.11: bloques de auditoría, entidad Auditoría y paso 3 de 10.2.
- Modelo de datos v0.4: `AUDITORIA` con `tipo_actor` y `ejecucion_id`; restricción R19; no hay cuenta `sistema`.
- Diseño técnico v0.7: HT-06 y HT-07 resueltos.
- Estrategia de pruebas v0.3: prueba de dos abonos simultáneos en la fila de concurrencia.

## 4. Propuestas del asistente, no revisadas una por una
La forma de `tipo_actor` y `ejecucion_id`, la restricción R19 y la redacción de la prueba de concurrencia.

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.