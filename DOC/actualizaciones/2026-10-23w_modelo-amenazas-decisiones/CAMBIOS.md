# Actualización 2026-10-23 (w) — Modelo de amenazas: decisiones previas a su redacción

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado ni creado; el documento del modelo de amenazas se redacta en una actualización posterior. [DOC/README.md](../../README.md)
**Origen:** recomendación 2 de la [investigación de la documentación núcleo](../2026-10-23u_investigacion-documentacion-nucleo/CAMBIOS.md); el solicitante pidió plantear el modelo de amenazas (23-oct-2026)
**Estado:** decisiones registradas; documento sin redactar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Qué técnica se usa? | "STRIDE + preguntas de privacidad de LINDDUN" (recomendada por el asistente) | STRIDE sobre un solo diagrama de flujo de datos, más una lista corta de preguntas de privacidad tomadas de LINDDUN (revelación de datos, identificación y vinculación, incumplimiento normativo); sin un segundo análisis completo |
| 2 | ¿Qué alcance tiene el diagrama? | "Producción de punta a punta, con exclusiones declaradas" (recomendada) | Entidades externas: administrador (con su dispositivo y navegador), Resend, DigitalOcean (respaldos) y DNS/Let's Encrypt. Procesos: Nginx, Gunicorn con Django y el proceso diario. Almacenes: PostgreSQL, documentos privados, archivo de secretos y respaldos cifrados. Flujos: sesión con segundo factor, subida y consulta de fotografías, correos, respaldo y restauración, administración por SSH. **Fuera, por escrito:** cadena de construcción (GitHub Actions y dependencias), interior de DigitalOcean y Resend, y la etapa A local |
| 3 | ¿Cómo se valora el riesgo? | "Probabilidad × impacto en 3 niveles, con justificación y riesgo residual" (recomendada) | Bajo, medio o alto, con una frase de justificación y una columna de riesgo residual aceptado, que acepta el solicitante y no el asistente |
| 4 | ¿Dónde vive el documento? | "Documento propio en la fase 3" (recomendada) | `MODELO_AMENAZAS_SGA_001_v0.1_borrador.md` en `fase-3-diseno-tecnico/`, listado en su README. **No es** el documento de seguridad con análisis de riesgos del Reglamento 37554-JP (ADR-021, fase 6, pendiente de abogado) |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| OWASP, Threat Modeling Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (23-oct-2026) | Cuatro preguntas; modelo del sistema con fronteras de confianza; STRIDE como ejemplo "aunque existen otras técnicas"; respuesta por amenaza (mitigar, eliminar, transferir, aceptar); documentar el riesgo residual, la técnica y sus limitaciones; mantenerlo actualizado; controlar el acceso a los artefactos | No fija formato ni tamaño |
| Microsoft, categorías de STRIDE: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats | Documentación del proveedor | Leída por resumen (23-oct-2026) | Las seis categorías de STRIDE y su descripción | Página de 2017, orientada a su herramienta |
| LINDDUN: https://linddun.org/ | Marco académico (KU Leuven) | Leída por resumen (23-oct-2026) | Siete categorías de amenazas a la privacidad; parte del mismo diagrama que STRIDE; variantes GO, PRO y MAESTRO | No hay una fuente que diga cuántas categorías usar en un sistema pequeño; usar solo tres es criterio del asistente |
| Manifiesto del modelado de amenazas: https://www.threatmodelingmanifesto.org/ | Declaración de expertos | Leída (23-oct-2026) | Hacerlo mejor que hablar de ello; refinamiento continuo; iteraciones acotadas; el diálogo crea entendimiento y los documentos lo registran | Declaración de valores, no un método |
| OWASP, Risk Rating Methodology: https://community.owasp.org/OWASP_Risk_Rating_Methodology | Guía de experto reconocido | Leída por resumen (23-oct-2026) | Riesgo = probabilidad × impacto; niveles bajo, medio y alto; lo de negocio prevalece; recomienda personalizar el modelo | Admite que existen metodologías más maduras (NIST SP 800-30, **no leída**) y que su ponderación ha sido debatida |
| NIST SP 800-218 (SSDF): https://csrc.nist.gov/pubs/sp/800/218/final | Estándar | Solo la ficha del catálogo (PDF no leído) | — | **No se pudo confirmar** que cubra la cadena de construcción ni el modelado de amenazas; por eso no se cita para esas afirmaciones |

## 3. Lo que propone el asistente y el solicitante no decidió
- Usar solo tres categorías de LINDDUN como preguntas: criterio del asistente, sin fuente.
- La consecuencia de impacto (la fuga de fotos de documentos y la pérdida de acceso o de datos financieros pesan más): se toma de la ERS y no de una fuente externa.
- El contenido y el tamaño del documento: una página de diagrama y una tabla (propuesta).
- Antes de subirlo a GitHub, **confirmar que el repositorio es privado** (no verificado; ADR-025).

## 4. Qué no se hizo
- No se redactó el modelo de amenazas ni se dibujó el diagrama.
- No se revisó con otra persona (DP-23; medida 9).
- No se evaluó ninguna amenaza concreta.
- No se leyó NIST SP 800-30 ni el PDF de SP 800-218.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
