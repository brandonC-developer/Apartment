# Actualización 2026-10-20 (h) — HT-05: aviso de recuperación de acceso

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [DAS v0.10](../../fase-2-arquitectura/DAS_SGA_001_v0.10_borrador.md) (nuevo), [diseño técnico v0.2](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.2_borrador.md) (nuevo) y los README de las fases 2, 3, 5 y 6 y de `DOC/`.
**Versiones anteriores:** [DAS v0.9](../../fase-2-arquitectura/DAS_SGA_001_v0.9_borrador.md) y [diseño técnico v0.1](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.1_borrador.md), que se conservan sin cambios.
**Estado:** borrador; no aprobado.

## 1. Motivo
Hallazgo HT-05 del diseño técnico v0.1: RF-27 exige notificar al administrador cada recuperación de acceso y cada emisión de nuevos códigos, pero no dice por qué canal. Una notificación dentro de la misma web no es independiente de la sesión: quien use un código de recuperación robado la vería antes que el administrador. El solicitante pidió resolverlo "uno por uno según buenas prácticas y recomendación".

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| C1 | añadido | ADR-026 en el DAS: avisos de seguridad de la cuenta por correo a dos direcciones, cuatro eventos, Resend por API con django-anymail, aviso guardado con el evento, reintentos y recuperación que procede si el envío falla | Preguntas 1 a 4 |
| C2 | modificado | ADR-013 (segundo temporizador de intervalo corto) y ADR-023 (el dominio también lo exige el correo) | Preguntas 2 y 4 |
| C3 | modificado | Diseño técnico v0.2: sección 3.5, catálogo de operaciones, flujo F-05, HT-05 resuelto, nuevos HT-08 y HT-09 y sección 7 | Todas |
| C4 | modificado | README de las fases 2, 3, 5 y 6 y de `DOC/` | Regla 3 de `CLAUDE.md` |

## 3. Impacto
- **ERS (no modificada; cambios pendientes para su próxima versión):**
  - Excepción en la sección 2.4, que excluye "Correo electrónico y SMS como canales de notificación", solo para alertas de seguridad al administrador (HT-09).
  - Ampliar RF-27 con dos eventos: registro o cambio del segundo factor y cambio o restablecimiento de la contraseña.
  - Definir cómo se cambia o restablece la contraseña del administrador (HT-08).
  - Estos cambios se agrupan con el CA de la segunda mitad de RN-15 (actualización 2026-10-20 (f)) en la ERS v1.9.
- **Arquitectura:** una dependencia externa nueva (Resend), un dominio propio y un segundo temporizador.
- **Legal:** la dirección de la segunda persona es un dato personal de un tercero y Resend recibe esas direcciones (DP-19, pendiente de abogado).
- **Pruebas (fase 4):** hay que probar el aviso guardado con el evento, los reintentos, la alerta persistente y que el aviso no contenga códigos ni enlaces.

## 4. Decisiones del solicitante (pregunta → respuesta)
En las preguntas 1 a 4 eligió la opción recomendada por el asistente. Antes de la pregunta 1 propuso crear otra web para el administrador y otra para el cliente; el asistente explicó que no da independencia al aviso. La pregunta 1 se corrigió porque el asistente no había advertido la exclusión de la sección 2.4 de la ERS. La pregunta 4 se añadió durante la ronda.
## Tabla de decisiones (sección 4)
| # | Pregunta | Respuesta | Fecha | Fuentes y validación |
|---|---|---|---|---|
| 1 | Canal del aviso | Correo, solo para alertas de seguridad al administrador, y WhatsApp como segundo canal cuando exista (opción recomendada, tras corregir una omisión del asistente). Antes, el solicitante preguntó si bastaba crear otra web para el administrador y otra para el cliente; el asistente explicó que no da independencia al aviso y que el portal del inquilino está fuera del alcance (ERS 2.4) | 20-oct-2026 | NIST SP 800-63B-4, sec. 4.6 (la recuperación de cuenta debe causar una notificación; al menos dos direcciones; instrucciones si no se reconoce el evento) y OWASP, Multifactor Authentication Cheat Sheet (notificar por canal fuera de la sesión; el correo depende de la seguridad de esa cuenta), por resumen; DigitalOcean bloquea los puertos 25, 465 y 587 en los Droplets (por resumen). **Cambio de alcance:** la ERS 2.4 excluye "Correo electrónico y SMS como canales de notificación"; esta decisión requiere una excepción explícita, solo para alertas de seguridad al administrador, en la próxima versión de la ERS |
| 2 | Servicio de correo | Resend, por su API HTTPS con django-anymail (opción recomendada) | 20-oct-2026 | Página de precios de Resend (plan gratis: 3.000 correos al mes y 100 al día, 3 dominios, API y SMTP) y su documentación de dominios (exige un dominio propio verificado), Mailgun (100 al día; 1 día de retención de registros), Amazon SES ($0,10 por 1.000; créditos de $200 por 6 meses) y django-anymail (licencia BSD, 14 proveedores), todas por resumen. Brevo (300 al día) solo por páginas del propio Brevo en una búsqueda. DigitalOcean bloquea los puertos 25, 465 y 587: el envío debe ir por la API HTTPS. **Dependencias:** nombre de dominio con DNS verificado (pendiente en ADR-023; su costo no se investigó). **No verificado:** entregabilidad, términos de servicio sobre datos personales (DP-19, abogado), registros DNS exactos y estabilidad del plan gratis. |
| 3 | Eventos de la cuenta que generan aviso | Cuatro: uso de un código de recuperación, emisión de nuevos códigos, registro o cambio del segundo factor y cambio o restablecimiento de la contraseña (opción recomendada). El aviso lleva qué ocurrió, fecha y hora local y qué hacer si no fue el administrador; no lleva códigos, contraseñas ni enlaces de acceso | 20-oct-2026 | NIST SP 800-63B-4, sec. 4.6 (debe notificarse la recuperación y el reemplazo de un código de recuperación, y añadir un autenticador, por un mecanismo independiente; debería notificarse la invalidación; el aviso debe traer instrucciones y contacto; cambio de contraseña y de dirección no figuran en su lista; no dice qué no debe llevar el aviso) y OWASP, Forgot Password Cheat Sheet (aviso por correo tras restablecer la contraseña, sin la contraseña; avisar a todas las direcciones si hay sospecha), por resumen. Los eventos 3 y 4 y la regla de no incluir códigos ni enlaces son propuesta del asistente, aceptada por el solicitante; los eventos 3 y 4 amplían RF-27 en la próxima ERS. Los pasos concretos de reacción dependen de un procedimiento operativo de la fase 6 que no existe. |

## Idea registrada, sin decisión
Portal del inquilino y sitio de administración separado: fuera del alcance de la v1 (ERS 2.4). No resuelve HT-05. Se podría considerar en una versión futura como cambio de alcance.

## 5. Pendientes
- Nombre de dominio con DNS verificado y su costo (no investigado).
- Cuáles son las dos direcciones de correo; protegerlas con segundo factor.
- Intervalo del temporizador de reintentos.
- Registros DNS exactos que pide Resend; entregabilidad, términos de servicio y estabilidad del plan gratis.
- Procedimiento de reacción ante un aviso inesperado (fase 6).
- HT-08: procedimiento de cambio y restablecimiento de contraseña y de segundo factor.
- Cambios de la ERS descritos en la sección 3.
- DP-19 y DP-17: abogado.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. La investigación se leyó por resumen (la herramienta devuelve un resumen, no el texto completo); en cada fila se indica qué se leyó y qué quedó solo como resultado de búsqueda. Revisión de pares: no realizada. Ninguna fuente decide si bloquear o dejar pasar la recuperación ante un fallo del envío: es un equilibrio de riesgo del solicitante y del asistente.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |