# Actualización 2026-10-21 (v) — Entornos, región y tamaño del Droplet

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-023, anexo A), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 5.1 nueva, sección 8), README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Decisiones (opciones recomendadas por el asistente)
| # | Pregunta | Decisión del solicitante |
|---|---|---|
| 1 | ¿En qué región de DigitalOcean se aloja el SGA? | NYC3, Nueva York |
| 2 | ¿Qué tamaño tiene el Droplet de producción y cómo es el entorno de pruebas? | 2 GiB y 1 vCPU (US$12) y un Droplet de pruebas temporal |

## 2. Fuentes (por resumen, 21-oct-2026)
- DigitalOcean, disponibilidad regional: 16 centros de datos, ninguno en Latinoamérica; Atlanta es el más cercano a Centroamérica por geografía (la página no da distancias); NYC3 tiene Droplets, Spaces estándar y frío, y respaldos; ATL1 tiene Droplets "limitados".
- DigitalOcean, precios de Droplets: 2 GiB y 1 vCPU, US$12; 2 GiB y 2 vCPU, US$18; respaldos semanales 20 % y diarios 30 %; facturación por segundo desde el 1-ene-2026. La página no indica moneda ni fecha de publicación (se asume dólares).

## 3. Costo estimado en producción (a reconfirmar al contratar)
Droplet US$12 + respaldo semanal US$2,40 + Spaces US$5 = **US$19,40 al mes**, más el dominio (unos US$10 al año, por confirmar) y las horas de los Droplets de prueba.

## 4. Límites
- Sin medir: la latencia desde Costa Rica, el rendimiento real en 2 GiB y 1 vCPU y si 1 GiB sería insuficiente (criterio del asistente).
- No se verificó que el Droplet se pueda redimensionar sin perder datos ni los planes y precios de Atlanta.
- DP-19 (transferencia de datos al extranjero) aplica a cualquier región disponible.

## 5. Pendientes del plan
Versiones de Python y Django; registro de avance y regla ante una entrega Alta incompleta; revisión por otra persona; del punto de carga: formato del origen, consentimiento de los inquilinos actuales y fecha.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.