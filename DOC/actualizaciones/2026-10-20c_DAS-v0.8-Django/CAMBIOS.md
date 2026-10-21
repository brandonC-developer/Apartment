# Actualización 2026-10-20 (c) — DAS v0.8: Python y Django

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [DAS v0.8](../../fase-2-arquitectura/DAS_SGA_001_v0.8_borrador.md) (nuevo) y los README de las fases 2, 3, 5 y 6 y de `DOC/`.
**Versión anterior:** [DAS v0.7](../../fase-2-arquitectura/DAS_SGA_001_v0.7_borrador.md), que se conserva sin cambios.
**Estado:** borrador; no aprobado.

## 1. Motivo
RE-04 decía que no se fijaba lenguaje ni framework porque el solicitante no tenía preferencia. El 20-oct-2026 se investigaron frameworks (evidencia en la sección 5) y el solicitante decidió usar Django.

## 2. Cambios
| ID | Tipo | Descripción | Origen (pregunta → respuesta → decisión) |
|---|---|---|---|
| S1 | añadido | ADR-022: Python y Django, monolito modular, interfaz renderizada por el servidor, sin API pública en la v1 | Pregunta del asistente: "¿Interfaz renderizada por el servidor (Django), o Next.js con una API aparte?" → solicitante: "Entonces con django" → decisión del solicitante |
| S2 | modificado | RE-04: lenguaje y framework fijados; el motor de base de datos sigue sin fijarse. El texto anterior se conserva dentro de la restricción para no cambiar el significado de un ID | Ídem |
| S3 | modificado | Introducción, historial y sección 5 del DAS | Ídem |
| S4 | añadido | Referencias 17 a 19 y fila en el anexo A | Regla 8 de `CLAUDE.md` |
| S5 | modificado | README de las fases 2, 3, 5 y 6 y de `DOC/` apuntan al DAS v0.8; en la fase 3 los "contratos de API" pasan a interfaces internas | Regla 3 de `CLAUDE.md` |

## 3. Impacto
- **Arquitectura:** la interfaz se renderiza en el servidor; no hay aplicación de frontend separada ni API pública en la versión 1.
- **Fase 3:** desaparecen los contratos de API públicos. Quedan permisos por operación y flujos de negocio.
- **ERS:** sin cambios; sus requisitos no describen tecnología (ERS sección 1.2).
- **Modelo de datos v0.3 y resumen para el abogado v2:** siguen citando el DAS v0.7; los enlaces siguen siendo válidos y no se editan (documentos de otras fases, sin cambio de contenido).

## 4. Decisiones
- **Resuelta (solicitante, 20-oct-2026):** lenguaje y framework (Python y Django) e interfaz renderizada por el servidor.
- **Pendientes, sin decidir:** versión de Django y de Python (propuesta: Django 6.2 LTS, prevista para abril de 2027), motor de base de datos (ADR-002), servidor de aplicaciones y proxy con HTTPS, tareas programadas, almacenamiento de archivos privados, contenedores, integración continua. Las propuestas hechas en la conversación sobre estos puntos (PostgreSQL 18, Caddy, systemd, `pg_dump` hacia almacenamiento externo) no están decididas ni verificadas con fuentes completas.
- **No decidido:** el proveedor de alojamiento. Se investigó DigitalOcean, pero no consta una decisión del solicitante.

## 5. Evidencia y fuentes
Detalle y nivel de validación en el ADR-022 y en las referencias 17 a 19 del DAS v0.8. Resumen:
- Documentación oficial de Django (ExclusionConstraint, Argon2, lista de despliegue, versiones con soporte): leída por resumen.
- Stack Overflow Developer Survey 2025 (uso de frameworks): leída por resumen; mide popularidad, no calidad.
- Estudio de la Universidad de Kabul (2026, Django frente a Laravel): solo el resumen; compara dos frameworks; método basado en documentación y CVE.
- Estudio de rendimiento en JCSI (2025) y tesis de EAFIT (2022): solo resultados de búsqueda; no se pudo leer el texto. No se citan cifras.
- Fowler, MonolithFirst (2015): leída por resumen.
- No se encontró un estudio universitario que compare modular monolito y microservicios con datos de equipos.
- Se descartó Next.js para la v1 con base en su documentación de autoalojamiento y en el aviso CVE-2025-29927 (ambos leídos por resumen o resultados de búsqueda); no hay estudios sobre Next.js para este tipo de sistema.
- La investigación sobre DigitalOcean de esta sesión (precios del 20-oct-2026, VPC, respaldos, regiones) no se ha registrado en un documento; queda pendiente si el solicitante lo pide.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. Revisión de pares: no realizada.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
