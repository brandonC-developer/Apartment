# Actualización 2026-10-23 (x) — Modelo de amenazas v0.1

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de amenazas v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md) (nuevo); [README de la fase 3](../../fase-3-diseno-tecnico/README.md); [DOC/README.md](../../README.md); una fila nueva en la sección 12 (riesgos) del [DAS v0.12](../../fase-2-arquitectura/DAS_SGA_001_v0.12_borrador.md), editado en su sitio por ser un borrador del mismo día, solo para enlazar el modelo
**Origen:** decisiones de la [actualización 2026-10-23 (w)](../2026-10-23w_modelo-amenazas-decisiones/CAMBIOS.md); el solicitante pidió redactarlo (23-oct-2026)
**Estado:** borrador; no aprobado; **autoverificación del asistente, sin revisión de otra persona**

## 1. Qué contiene
- Alcance (producción de punta a punta, con exclusiones por escrito), método, **diagrama de flujo de datos** con cinco fronteras de confianza, activos y supuestos.
- **28 amenazas STRIDE** con controles decididos, probabilidad, impacto, nivel y respuesta propuesta: 5 de nivel alto, 16 medios y 7 bajos.
- Preguntas de privacidad (LINDDUN reducido), **11 brechas con propuesta** y una tabla de riesgo residual con todas las aceptaciones **pendientes**.

## 2. Los cinco riesgos altos
| ID | Qué | Por qué es alto |
|---|---|---|
| AM-02 | Dispositivo y sesión del administrador comprometidos | El sistema no puede impedirlo; el riesgo se asumió en parte al elegir el restablecimiento por correo (ADR-026) |
| AM-16 | Software sin parchear, sobre todo las dependencias de Python | `unattended-upgrades` no actualiza lo que se instale con `pip` (inferencia del asistente) y no hay un proceso para ello |
| AM-21 | Correo falsificado con el aspecto de un aviso o de un restablecimiento | SPF, DKIM y DMARC no están decididos |
| AM-23 | Toma de control de las cuentas de los proveedores (dominio, servidor, correo, repositorio) | Ningún documento exige protegerlas |
| AM-24 | Robo del respaldo o de su clave | Herramienta y custodia de la clave sin definir |

## 3. Hallazgos que no estaban en los documentos
1. **No hay ningún requisito sobre las cuentas de los proveedores** (BR-01): una de ellas da control sobre el servidor, el DNS, el correo o los respaldos.
2. **Las dependencias de Python no tienen proceso de actualización** (BR-04).
3. **La autenticación del correo del dominio (SPF, DKIM, DMARC) no está decidida** (BR-02).
4. El contador por cuenta de RF-27 puede usarse para dejar fuera al administrador (AM-04); depende del límite por IP de Nginx, aún sin decidir (BR-08).

## 4. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** técnica, alcance, forma de valorar el riesgo y ubicación del documento (actualización (w)).
- **Propuesta del asistente, sin decidir:** todos los niveles de probabilidad, impacto y riesgo; todas las respuestas; las 11 brechas y sus propuestas. **Ningún riesgo está aceptado.**

## 5. Qué no se hizo
- **No se revisó con otra persona**; la cuarta pregunta ("¿lo hicimos suficientemente bien?") queda abierta (medida 9).
- No se verificó ningún control: no hay servidor. Los niveles son juicio del asistente, sin datos de ataques reales.
- No se cubrió la cadena de construcción, el interior de los proveedores ni un adversario con acceso de `root`.
- No se usó una herramienta de modelado de amenazas ni se leyó NIST SP 800-30.
- Las características de Django que se citan (escape automático y protección CSRF) no se verificaron en esta sesión.
- Antes de subirlo a GitHub hay que confirmar que el repositorio sea privado (no verificado).
- **No es** el documento de seguridad del Reglamento 37554-JP (ADR-021).
- No se cambió ninguna ERS, modelo de datos ni diseño técnico; las brechas son propuestas que, si se adoptan, requieren una versión nueva de la ERS.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
