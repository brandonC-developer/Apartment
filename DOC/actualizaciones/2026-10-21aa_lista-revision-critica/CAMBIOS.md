# Actualización 2026-10-21 (aa) — Lista de verificación de la revisión por otra persona

**Fecha:** 2026-10-21
**Documentos afectados:** [Lista de verificación LRC-SGA-001 v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md) (nueva), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 3.3 y 8; editado en su sitio), README de la [fase 5](../../fase-5-implementacion/README.md), [DOC/README.md](../../README.md) y `herramientas/verificar_coherencia.ps1`
**Estado:** borrador; no aprobado

## 1. Motivo
El solicitante pidió preparar la lista de verificación antes de empezar la fase 6, tras decidir que una persona distinta revise lo crítico antes de cargar datos reales (actualización 2026-10-21 (z)).

## 2. Qué se creó
- **LRC-SGA-001 v0.1:** 47 puntos (RV-01 a RV-47) en nueve áreas: cuenta y restablecimiento, autorización, documentos privados, datos personales y registros, base de datos y roles, integridad financiera, configuración de Django y del servidor, respaldos y trazabilidad. Cada punto indica qué verificar, su referencia (RF, RN, CA, ADR), el momento (A diseño, B código, C servidor) y deja el resultado y la evidencia en blanco. Incluye los datos de la persona revisora, una tabla de hallazgos y un cierre firmado.
- **Script:** el documento entra en la comprobación de citas, base declarada, vigencia y README de la fase.

## 3. Fuentes
- OWASP ASVS (página del proyecto, por resumen: versión estable 5.0.0). **No se leyeron sus capítulos ni niveles; no se cita ningún número de requisito.**
- OWASP, Django Security Cheat Sheet (por resumen): ajustes de despliegue, HTTPS, cookies, CSRF, XSS. La política de seguridad de contenido usa el middleware de Django 6.0 o posterior, que no existe en la 5.2 LTS: queda como punto RV-36.
- Las demás: las ya citadas en el DAS y el diseño técnico; NIST SSDF por páginas de terceros.

## 4. Límites
- Los puntos son propuesta del asistente, derivados de las decisiones del proyecto; el solicitante no los revisó uno por uno.
- La lista no sustituye a una auditoría de seguridad ni a pruebas de penetración.
- No hay persona revisora ni nivel de verificación decididos.
- Una revisión hecha por el asistente no es independiente.

## 5. Pendientes
Designar a la persona revisora; decidir el nivel de verificación (por ejemplo de ASVS, tras leerlo); versiones exactas (micro) y forma de instalar Django; del plan de carga: formato del origen, consentimiento de los inquilinos actuales y fecha.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.