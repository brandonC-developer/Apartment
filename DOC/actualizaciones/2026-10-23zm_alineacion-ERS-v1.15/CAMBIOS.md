# Actualización 2026-10-23 (zm) — ERS v1.15 y alineación de los documentos

**Fecha:** 2026-10-23
**Documentos afectados:** [ERS v1.15](../../fase-1-ers/ERS_SGA_001_v1.15_borrador.md) (nueva; reemplaza a la [v1.14](../../fase-1-ers/ERS_SGA_001_v1.14_borrador.md), que no se edita). Editados en su sitio, porque ninguno está reemplazado ni aprobado: [DAS v0.14](../../fase-2-arquitectura/DAS_SGA_001_v0.14_borrador.md) (cuatro frases que decían "requisito nuevo por redactar" y la ERS de referencia), [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md) y [Modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md) (solo la base), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md) (solo la base), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md), el [registro de avance](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), los README de las fases 1, 2, 4 y 5 y [DOC/README.md](../../README.md)
**Origen:** las decisiones de la [actualización 2026-10-23 (zl)](../2026-10-23zl_ers-requisitos-nuevos-decisiones/CAMBIOS.md); el solicitante pidió redactar la v1.15 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios en la ERS
| Elemento | Cambio |
|---|---|
| **RF-53** (nuevo) | Vigilar el respaldo diario: el reintentador comprueba que el último respaldo correcto tiene menos de 26 horas; si no, aviso, alerta web persistente y correo sin repetir. Aparte de RF-49. No cubre un servidor caído ni la restauración |
| **RNF-19** (nuevo) | Protección de las cuentas de servicios externos: mejor segundo factor disponible (nunca SMS), dos factores, códigos de respaldo fuera del dispositivo, un solo usuario, dirección dedicada, registro de cuentas sin secretos con revisión anual y bloqueo del dominio. Control de la fase 6 |
| **RNF-20** (nuevo) | Autenticación del correo saliente: subdominio dedicado con SPF y DKIM, DMARC de `p=none` a `p=reject` tras las pruebas, dominio raíz sin enviar correo |
| **CA-79, CA-80, CA-81** (nuevos) | Alerta de respaldo omitido (integración), registro de cuentas externas (inspección) y correo autenticado (cabeceras y registro `_dmarc`, etapa B) |
| Alcance 2.3, matriz (sección 10), sección 12.1h, lista de verificación | RF-53 en "Recordatorios y alertas"; fila nueva "Proteger las cuentas externas y el correo saliente"; registro de las tres decisiones; un punto nuevo en la lista del cierre |
| **Control del documento** | **Corrección de un error mío:** la tabla "Control del documento" decía versión 1.12 en las v1.13 y v1.14 (la edición se aplicó a una línea equivocada). En la v1.15 dice 1.15. Las v1.13 y v1.14 no se editan |

Totales: **53 RF, 30 RN, 20 RNF, 81 CA, 21 OL, 30 DP, 32 ADR, 11 RE.**

## 2. Alineación de los demás documentos
| Documento | Cambio |
|---|---|
| DAS v0.14 | La ERS de referencia pasa a v1.15; RF-53, CA-79, RNF-19 y RNF-20 reemplazan "requisito nuevo por redactar" en ADR-013, ADR-032 y la sección 11 |
| Estrategia de pruebas v0.3 | CA-79 (Integración, Media), CA-80 (inspección, Media) y CA-81 (verificación manual en la etapa B, Alta); recuento 81 de 81 (niveles propuestos por el asistente) |
| Plan v0.1 | RF-53 y CA-79 en la **E4**; RNF-19, RNF-20, CA-80 y CA-81 en la **E6** (propuesta del asistente: se comprueban con las cuentas y el dominio reales) |
| Registro de avance | E4 pasa de 0/12 a 0/13 CA; E6 de "sin CA" a 0/2 |
| Bases | Modelo de datos, modelo de amenazas, diseño técnico y lista de verificación declaran la ERS v1.15 |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** que existan RF-53, RNF-19 y RNF-20, con las reglas descritas en la actualización (zl).
- **Propuesta del asistente, sin decidir:** las 26 horas, la entrega E4 de RF-53, la entrega E6 de RNF-19, RNF-20, CA-80 y CA-81, los niveles de prueba, la clasificación como no funcionales y los textos exactos.

## 4. Qué no se hizo
- **El modelo de amenazas v0.2 no se actualizó con el contenido:** sigue listando BR-11 y BR-12 como abiertas y no cita RF-53, RNF-19 ni RNF-20. Es una v0.3 por redactar.
- No se diseñó cómo la aplicación lee la marca del respaldo.
- No se verificó qué segundo factor ofrece cada servicio ni que los receptores respeten DMARC.
- El script comprueba identificadores, enlaces, bases y cobertura, no el contenido; no se releyó la ERS entera.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
