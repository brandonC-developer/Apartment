# Actualización 2026-10-21 (r) — ADR-031: esquema físico y migraciones (punto 1)

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-031 nuevo, corrección de ADR-027, sección 10.1, anexo A, referencia 33), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md) (sección 11 y nueva sección 13), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisiones (todas del solicitante, opción recomendada)
| # | Pregunta | Decisión | Fuentes (por resumen, 21-oct-2026) |
|---|---|---|---|
| 1 | ¿Cómo se impide en la base que dos contratos de una propiedad compartan un día (R2)? | Restricción de exclusión de PostgreSQL con `btree_gist` | Django, restricciones de PostgreSQL; PostgreSQL, `btree_gist` ("trusted") |
| 2 | ¿Qué tipo físico tienen los importes? | `DecimalField` de 14 dígitos y 2 decimales | Django, campos de modelo (primera mitad) |
| 3 | ¿Cómo se conceden los privilegios tras cada migración? | Archivo de privilegios idempotente ejecutado por el rol dueño, con una prueba de una entrada por tabla | PostgreSQL, privilegios (ADR-027) |

## 2. Corrección a una propuesta mía (ADR-027)
Había propuesto "ningún `DELETE` en ninguna tabla". Era incorrecta: Django guarda las sesiones en la base (`django_session`), no purga las expiradas por sí solo (`clearsessions`) y el solicitante adoptó cerrar las sesiones abiertas al restablecer la contraseña. El rol de la aplicación necesita `DELETE` en `django_session`. Corregido en el ADR-027, con la limpieza diaria en el paso 6 del proceso diario (DAS 10.1, propuesta). Fuente: Django, sesiones.

## 3. Cambios
- DAS v0.11: ADR-031; ADR-027 corregido; 10.1 con la limpieza de sesiones; anexo A; referencia 33.
- Modelo de datos v0.4: sección 13 con los tipos físicos decididos.
- Estrategia de pruebas v0.3: pruebas de la restricción de solape y del archivo de privilegios.

## 4. Pregunta de negocio abierta (no la resuelve el asistente)
RN-02 no decía si un contrato **anulado** cuenta para el solape de fechas. **Resuelta por el solicitante el 21-oct-2026: no cuenta** (era la propuesta del asistente). Recogida en la ERS v1.9 (RN-02, editada en su sitio), el DAS (ADR-031), el modelo de datos (R2 y sección 13) y la estrategia de pruebas.

## 5. Límites
- La expresión del rango con límite superior inclusivo no se verificó (la página solo muestra límites `[)`).
- Los tipos de columna que Django elige en PostgreSQL 18 (`numeric`, `timestamp with time zone`) son de memoria; se confirman con `sqlmigrate`.
- Los tamaños de los importes y del tipo de cambio son propuesta del asistente.

## 6. Pendiente del punto 1
Índices adicionales, nombres de tablas, orden de las migraciones entre las seis aplicaciones y formato del archivo de privilegios.

## 7. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.