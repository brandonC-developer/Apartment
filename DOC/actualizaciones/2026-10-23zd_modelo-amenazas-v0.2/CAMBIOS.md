# Actualización 2026-10-23 (zd) — Modelo de amenazas v0.2

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md) (nuevo; reemplaza a la [v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md), que no se edita); [README de la fase 3](../../fase-3-diseno-tecnico/README.md); [DOC/README.md](../../README.md); el enlace de la sección 12 del [DAS v0.12](../../fase-2-arquitectura/DAS_SGA_001_v0.12_borrador.md), editado en su sitio para apuntar a la v0.2
**Origen:** decisiones de las actualizaciones [(y)](../2026-10-23y_br-01-cuentas-proveedores/CAMBIOS.md), [(z)](../2026-10-23z_br-02-autenticacion-correo/CAMBIOS.md), [(za)](../2026-10-23za_br-03-respaldos-clave-spaces/CAMBIOS.md), [(zb)](../2026-10-23zb_br-04-dependencias-python/CAMBIOS.md) y [(zc)](../2026-10-23zc_br-08-limite-solicitudes-nginx/CAMBIOS.md); el solicitante pidió redactar la v0.2 (23-oct-2026)
**Estado:** borrador; no aprobado; **autoverificación del asistente, sin revisión de otra persona**

## 1. Cambios en el modelo
| Elemento | Cambio |
|---|---|
| AM-01 | Control nuevo: límite de 6 solicitudes por minuto por IP (BR-08). Nivel: medio (sin cambio) |
| AM-03 | Brecha nueva **BR-12**: las direcciones de correo del administrador no tienen requisito de segundo factor. Nivel: medio (sin cambio) |
| AM-04 | **Aceptar**, decidido el 23-oct-2026. Se corrige el control: el límite por IP de Nginx reduce el volumen pero no evita el efecto. Nivel: medio |
| AM-10 | Control: zona general de 10 por segundo (BR-08). Nivel: bajo |
| AM-16 | Pasa de alto a **medio**: `pip` con versiones fijadas, plazos de 3 y 14 días, django-announce, `pip-audit` y Dependabot (BR-04); sigue habiendo una sola persona |
| AM-21 | Pasa de alto a **medio**: subdominio de envío y DMARC (BR-02); supone que el receptor respeta DMARC |
| AM-23 | Pasa de alto a **medio**: segundo factor, correo dedicado, registro de cuentas (BR-01); el TOTP sigue siendo vulnerable al phishing |
| AM-24 | Pasa de alto a **medio**: `age` con clave pública y custodia fuera de línea (BR-03) |
| AM-25 | Sigue en medio; se actualiza el control (llave limitada, versionado, copia mensual, respaldo semanal del Droplet) |
| Sección 8 | Columna "Estado": BR-01, BR-02, BR-03, BR-04 y BR-08 **decididas**; BR-05, 06, 07, 09, 10 y 11 abiertas; **BR-12 nueva** |
| Sección 9 | AM-04 **aceptado**; AM-23 y AM-25 con residual propuesto; el resto, pendiente |
| Resumen | De 5 altos, 16 medios y 7 bajos a **1 alto (AM-02), 20 medios y 7 bajos** |

## 2. Qué conviene saber
- **Los niveles bajan solo en el papel:** las decisiones del 23-oct-2026 no están aplicadas; no hay servidor ni cuentas. La v0.2 lo dice en el resumen y en los supuestos.
- **La única amenaza alta es AM-02** (dispositivo y sesión del administrador), que el sistema no puede impedir; su brecha (BR-09) sigue abierta.
- **Hallazgo de esta versión (BR-12):** la dirección que recibe el enlace de restablecimiento y los avisos no tiene ningún requisito de segundo factor; quien controle ese buzón controla el restablecimiento. Es una propuesta abierta, no una decisión.
- **Se corrigió un error de la v0.1 y de la actualización (t):** el límite por IP de Nginx no mitiga AM-04.

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** lo recogido en BR-01, BR-02, BR-03, BR-04 y BR-08, y aceptar AM-04.
- **Propuesta del asistente, sin decidir:** todos los niveles recalculados; BR-12 y su propuesta; BR-05, 06, 07, 09, 10 y 11. **Ningún otro riesgo está aceptado.**

## 4. Qué no se hizo
- **No se revisó con otra persona**; la cuarta pregunta ("¿lo hicimos suficientemente bien?") sigue abierta (medida 9).
- No se aplicó ni verificó ningún control.
- No se resolvieron BR-05, 06, 07, 09, 10, 11 ni BR-12.
- No se editaron la ERS ni el DAS (solo el enlace del DAS al modelo): las decisiones de BR-01 a BR-04 y BR-08 aún no están en el ADR-032 ni en la ERS.
- Se mantienen los límites de la v0.1: no cubre la cadena de construcción ni el interior de los proveedores.

## 5. Qué falta hacer
1. DAS: incorporar las decisiones de BR-01 a BR-04 y BR-08 al ADR-032 (y completar ADR-022, ADR-024 y ADR-025) en una versión nueva.
2. ERS: decidir si algunas pasan a requisito (por ejemplo, el segundo factor de las cuentas de los proveedores).
3. Decidir BR-07, BR-12 y las demás abiertas.
4. Revisión con otra persona.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
