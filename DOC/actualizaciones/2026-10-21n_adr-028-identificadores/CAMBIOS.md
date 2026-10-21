# Actualización 2026-10-21 (n) — ADR-028: identificadores internos (H7)

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-028 nuevo, ADR-027, anexo A, referencia 29), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md) (convención de `id`, H7) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Qué formato tienen los identificadores internos de las entidades (H7)? | Entero de 64 bits autoincremental (`BigAutoField`); UUID solo en la clave de solicitud y los nombres de archivo de las cédulas | Igual |

**Fuentes (por resumen, 21-oct-2026):** Django, campos de modelo (primera mitad de la página: `BigAutoField` es el valor por defecto; `UUIDField` exige que la aplicación genere el valor); PostgreSQL 18, funciones de UUID (`uuidv4()`, `uuidv7()`).

## 2. Cambios
- DAS v0.11: ADR-028 nuevo; ADR-027 ya no deja el formato como abierto; anexo A; referencia 29.
- Modelo de datos v0.4: convención de `id` y hallazgo H7 resuelto.

## 3. Límites y propuestas
- Que el rendimiento de los índices no cambia a este volumen es afirmación del asistente.
- Los permisos de secuencia se conceden junto con los de cada tabla: propuesta, sin verificar contra Django en PostgreSQL 18.
- Los identificadores se pueden adivinar; la protección es la autorización en cada vista. No se verificó la guía de OWASP sobre referencias directas a objetos.

## 4. Quedan por revisar (puntos 1, 3, 4 y 6)
Esquema físico y migraciones; usuarios y permisos (tercer rol de respaldos y secreto del rol dueño); conexión; módulos del DAS como aplicaciones de Django.

## 5. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.