# Actualización 2026-10-21 (k) — Cierre de las cinco decisiones técnicas abiertas

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md), [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Cerrar, una por una y con fuentes, las decisiones técnicas que quedaban abiertas en el diseño técnico (sección 7) y en el DAS (ADR-023, ADR-026).

## 2. Decisiones (todas por el solicitante, con la opción recomendada por el asistente)
| # | Pregunta | Decisión | Fuentes y validación |
|---|---|---|---|
| 1 | Dominio y registrador | `.com` en Cloudflare Registrar, con el DNS de Cloudflare | Cloudflare (página de producto y comunicado de 2018) y una reseña de terceros de julio de 2026 (unos US$10,44 al año); **solo resultados de búsqueda**, páginas no abiertas. El precio y el nombre exacto se confirman al comprar |
| 2 | Segunda dirección de los avisos de seguridad | Dos direcciones del propio solicitante, en proveedores distintos; no constan en los documentos | NIST SP 800-63B-4, sec. 4.6 (al menos dos direcciones), leído por resumen el 20-oct. **Cambia** la decisión del 20-oct (ADR-026: "una puede ser de una persona de confianza"); ya no hay dato de un tercero en este punto |
| 3 | Intervalo del reintentador | Cada 1 minuto | AWS Architecture Blog (backoff con aleatoriedad) respalda la espera creciente, no el intervalo; la primera espera de 1 minuto es propuesta del asistente |
| 4 | Protecciones del enlace de restablecimiento | Las tres: respuesta y tiempo idénticos; invalidar enlaces y sesiones al cambiar la contraseña; 3 solicitudes por hora | OWASP, Forgot Password Cheat Sheet, leída por resumen el 21-oct. El cierre automático de sesiones y el límite de 3 por hora son propuestas del asistente (la fuente no fija números) |
| 5 | Qué lecturas se auditan | Fotos de cédula y exportación del titular; no las lecturas ordinarias | OWASP, Logging Cheat Sheet, leída por resumen el 21-oct (acceso a datos sensibles y exportaciones sí; no guardar datos personales en los registros) |

## 3. Cambios
- **ERS v1.9:** dominio en 2.5; RF-27 (dos direcciones del solicitante; protecciones adoptadas); RF-45 amplía su título y alcance a las exportaciones del titular (el ID no cambia); CA-27 y CA-59 ajustados; DP-19 sin la dirección de un tercero; sección 12.1b con una fila nueva.
- **DAS v0.11:** ADR-013 (1 minuto), ADR-023 (dominio), ADR-026 (direcciones, protecciones, pendientes), secciones 7.7 y 9, DP-19 y condiciones de aprobación.
- **Modelo de datos v0.4:** `correo_aviso_persona_confianza` pasa a `correo_aviso_secundario`; `destinatario_tipo` con valores `administrador` y `secundaria`; R17 invalida los demás tokens y las sesiones; R18 (límite de solicitudes); retención ajustada; H14 coherente.
- **Diseño técnico v0.7:** secciones 3.4.1, 3.5, 3.6 y 4.2 y la sección 7.
- **Estrategia de pruebas v0.3:** CA-27 (auditoría de la exportación) y CA-59 (protecciones).

## 4. Impacto
- Un cambio de requisito (RF-45 y RF-27) hecho sin nueva versión de la ERS: aceptable porque la ERS v1.9 no está reemplazada ni aprobada, pero conviene registrarlo en la próxima revisión.
- El resumen para el abogado v2 no se tocó; sigue describiendo la segunda dirección como de una persona de confianza. El solicitante declaró que el abogado ya lo verificó todo (ver [2026-10-21 (i)](../2026-10-21i_registro-validacion-legal/CAMBIOS.md)); si esa revisión incluyó a un tercero, ahora es innecesaria en ese punto.
- **Propuestas del asistente no revisadas una por una:** el límite de 3 solicitudes por hora, el cierre automático de sesiones, la primera espera de 1 minuto y la forma de R17 y R18.

## 5. Pendientes
- Comprar el dominio y confirmar nombre y precio; configurar las dos direcciones en el servidor.
- Verificar la entregabilidad, los términos de servicio y los registros DNS de Resend (fase 6).
- Procedimiento de reacción ante un aviso de seguridad inesperado (fase 6).
- Añadir el TOTP al reemplazo del segundo factor (futuro).

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.