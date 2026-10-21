# Actualización 2026-10-21 (q) — ADR-030: aplicaciones de Django y estructura del código

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-030 nuevo, sección 5, anexo A, referencia 32) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisión
Se presentó una propuesta de seis aplicaciones con tres opciones. El solicitante respondió: "quiero que propongas según buenas prácticas". El asistente investigó, ajustó la propuesta con las prácticas respaldadas y la registró **como propuesta del asistente, con la elección delegada**. El solicitante no revisó el reparto concreto.

## 2. Propuesta
Seis aplicaciones (`nucleo`, `cuentas`, `inquilinos`, `alquileres`, `notificaciones`, `privacidad`), claves foráneas solo hacia abajo, lógica de escritura en `services.py` y de lectura en `selectors.py`, vistas delgadas, URL y pruebas por aplicación. Detalle en el ADR-030.

## 3. Fuentes (por resumen, 21-oct-2026)
- Django, migraciones (dependencias y ciclos entre aplicaciones) y Django, aplicaciones (no dice cuántas crear).
- HackSoft, Django Styleguide (tercero; leída casi completa, 100.000 de 105.141 caracteres; no trata dependencias entre aplicaciones).
- Hostinger, guía de buenas prácticas (tercero comercial; solo resultados de búsqueda).
No hay norma ni estudio universitario sobre cuántas aplicaciones crear.

## 4. Límites
- Los nombres y el reparto son criterio del asistente.
- La tensión con el Styleguide (guardas de inmutabilidad en los modelos, ADR-027) está señalada en el ADR.
- Que el reparto no genere ciclos de migraciones se comprueba al escribir los modelos.

## 5. Quedan por revisar (punto 1)
Esquema físico y migraciones: tipos, índices, extensión `btree_gist`, orden de las migraciones por aplicación.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.