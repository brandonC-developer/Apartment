# Actualización 2026-10-21 — Diseño técnico v0.3 (HT-08)

**Fecha:** 2026-10-21
**Documentos afectados:** [Diseño técnico v0.3](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.3_borrador.md); README de la [fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Versión anterior:** [Diseño técnico v0.2](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.2_borrador.md) (se conserva sin cambios)
**Estado:** borrador; no aprobado

## 1. Motivo
Hallazgo HT-08 del diseño técnico: la ERS v1.8 no describe cómo se cambia o restablece la contraseña del administrador ni cómo se sustituye el segundo factor (RF-27 solo define sus reglas y la recuperación con códigos). Se resolvió una pregunta a la vez, con fuentes.

## 2. Cambios
| ID | Tipo | Descripción | Origen (pregunta → respuesta) |
|---|---|---|---|
| DTE 3.6 | añadido | Procedimiento de cambio y restablecimiento de contraseña y de segundo factor | P1–P4 de la tabla siguiente |
| DTE 4.2 | modificado | Dos filas del catálogo remiten a la sección 3.6 | — |
| DTE 6 (HT-08), 7 | modificado | HT-08 resuelto a nivel de diseño; pendientes actualizados | — |
| DTE 2 | modificado | Fila nueva con la OWASP Authentication Cheat Sheet | — |

## 3. Impacto
- **ERS (próxima versión):** describir el procedimiento (3.6), ampliar RF-27 con los eventos de cambio de contraseña y de segundo factor, y registrar la excepción del correo en la sección 2.4 (HT-09).
- **DAS:** debe describir el correo con enlace de restablecimiento, distinto de los avisos del ADR-026 (que no llevan enlaces). Aún no se hizo; el ADR-026 y el ADR-023 siguen sin cambios.
- **Pruebas:** habrá que cubrir enlace de un solo uso, caducidad de 15 minutos y que el restablecimiento no inicie sesión. Aún sin CA.
- **Seguridad:** dos decisiones contra la recomendación; riesgos en el punto 4.

## 4. Decisiones
| # | Pregunta | Respuesta del solicitante | Recomendación del asistente |
|---|---|---|---|
| P1 | ¿Qué exige cambiar la contraseña o reemplazar el TOTP con sesión iniciada? | "Por el momento solo contraseña, a futuro TOTP" | Contraseña actual y TOTP actual |
| P2 | ¿La regla aplica también al reemplazo del segundo factor? | Aplica a ambos: solo contraseña | Reemplazo del TOTP con contraseña y código de recuperación |
| P3 | ¿Cómo restablece la contraseña olvidada? | Con un enlace por correo | Código de recuperación y TOTP en la web |
| P4 | ¿Cuánto dura el enlace? | 15 minutos (valor propuesto por el asistente) | 15 minutos |

**Riesgos asumidos por el solicitante** (P1–P3): sesión secuestrada más contraseña permite reemplazar el segundo factor; el correo pasa a ser llave para restablecer la contraseña y el inicio de sesión depende de Resend y del dominio.

**Condiciones que se siguen recomendando:** TOTP o código de recuperación para reemplazar el segundo factor (futuro); respuesta que no revele si la dirección existe; invalidar enlaces y sesiones al cambiar la contraseña; limitar solicitudes. Las tres últimas no están decididas.

**Pendientes:** fecha o versión en que se añadirá el TOTP; las tres propuestas anteriores; dominio, direcciones e intervalo del reintentador (de HT-05).

## 5. Evidencia y fuentes
- OWASP Authentication Cheat Sheet y Multifactor Authentication Cheat Sheet ("Changing MFA Factors"), consultadas el 21-oct-2026 con WebFetch; validación: leídas por resumen. La primera no pide aviso tras cambiar la contraseña.
- La duración de 15 minutos y el valor por defecto de Django (3 días) no se verificaron en una fuente: el primero es propuesta, el segundo es de memoria y se presentó como tal.
- La guía OWASP Forgot Password no se volvió a leer en esta sesión.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1` (resultado en el cierre de la sesión). El script no revisa el diseño técnico.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
