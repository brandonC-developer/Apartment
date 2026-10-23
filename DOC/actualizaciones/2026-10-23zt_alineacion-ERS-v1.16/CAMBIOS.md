# Actualización 2026-10-23 (zt) — ERS v1.16 y alineación de los documentos

**Fecha:** 2026-10-23
**Documentos afectados:** [ERS v1.16](../../fase-1-ers/ERS_SGA_001_v1.16_borrador.md) (nueva; reemplaza a la [v1.15](../../fase-1-ers/ERS_SGA_001_v1.15_borrador.md), que no se edita). Editados en su sitio, porque ninguno está reemplazado ni aprobado: [DAS v0.14](../../fase-2-arquitectura/DAS_SGA_001_v0.14_borrador.md), [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md), [Modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md) y [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md) (solo la base), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md), el [registro de avance](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), los README de las fases 1, 2, 4 y 5 y [DOC/README.md](../../README.md)
**Origen:** las decisiones de las actualizaciones [(zo)](../2026-10-23zo_br-05-metadatos-imagenes/CAMBIOS.md) (BR-05), [(zp)](../2026-10-23zp_br-06-antivirus/CAMBIOS.md) (BR-06) y [(zs)](../2026-10-23zs_br-10-transferencia-a-proveedores/CAMBIOS.md) (BR-10); el solicitante pidió redactar la v1.16 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios en la ERS
| Elemento | Cambio |
|---|---|
| **RF-02** (nota v1.16) | El servidor decodifica la imagen completa y rechaza el archivo si falla (BR-06: sin antivirus); y elimina los metadatos de todo original que reciba sin reducir y, si la medición de la E2 lo exige, también de los reducidos (BR-05) |
| **RF-50** | Sustituye «metadatos pendientes en DP-27» por una remisión a RF-02 |
| **CA-82** (nuevo) | Metadatos: un JPEG con ubicación enviado sin reducir se guarda sin ella; se registra la medición de la E2 con tres teléfonos |
| **CA-83** (nuevo) | Imagen truncada o dañada: rechazada con mensaje y sin guardar |
| **DP-27** | Pasa de la lista de pendientes a las resueltas |
| **DP-31** (nueva) | Transferencia de datos a Resend y DigitalOcean, con las tres preguntas para el abogado; bloquea cargar datos reales |
| Sección 12.1i, matriz (sección 10), lista de verificación | Registro de las tres decisiones; CA-82 y CA-83 en «Registrar inquilinos y cédulas»; el punto de DP-27 pasa a CA-82 y se añade un punto para DP-31 |

Totales: **53 RF, 30 RN, 20 RNF, 83 CA, 21 OL, 31 DP, 32 ADR, 11 RE.**

## 2. Alineación de los demás documentos
| Documento | Cambio |
|---|---|
| DAS, modelo de datos, diseño técnico, estrategia, plan, lista de verificación, modelo de amenazas v0.3 | La ERS de referencia pasa a v1.16 en su base y en las líneas que la citan como vigente. Las frases del DAS que citan la v1.15 como origen de RF-53, CA-79, RNF-19 y RNF-20 no cambian: es correcto |
| Estrategia de pruebas v0.3 | CA-82 y CA-83 (Integración, Media); recuento 83 de 83 |
| Plan v0.1 | CA-83 a la **E1** (validación de la subida); CA-82 a la **E2** (donde se mide con fotos reales); propuesta del asistente |
| Registro de avance | E1 pasa de 0/7 a 0/8 CA; E2 de 0/24 a 0/25 |
| README de las fases 1, 2, 4 y 5 y DOC/README.md | Vigencia de la v1.16; el de la fase 4 corrige además «cubre los 78» (era una cifra antigua) |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** el tratamiento de los metadatos, la ausencia de antivirus con decodificación, y consultar al abogado por la transferencia (actualizaciones (zo), (zp) y (zs)).
- **Propuesta del asistente, sin decidir:** que existan CA-82 y CA-83 y su redacción; su asignación a la E1 y la E2; el número y las preguntas de DP-31; el método y la biblioteca para quitar metadatos.

## 4. Qué no se hizo
- **BR-07 (registros de Nginx y Gunicorn) y BR-09 (dispositivo y llave SSH) no entran en la ERS:** quedan en el DAS (ADR-032, ADR-017) y en la fase 6. No se preguntó si deben ser requisitos.
- El DAS v0.14 no refleja todavía las decisiones BR-05, BR-06, BR-07, BR-09 ni BR-10 (ADR-003, ADR-017, ADR-032): es un DAS v0.15 por redactar. El modelo de amenazas v0.3 tampoco: es una v0.4.
- El resumen para el abogado sigue en la ERS v1.8 y no incluye DP-31.
- El CA-82 mezcla dos comprobaciones (una automática y una medición en la E2); si hace falta separarlas, sería un criterio nuevo.
- El script comprueba identificadores, enlaces, bases y cobertura, no el contenido; no se releyó la ERS entera.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
