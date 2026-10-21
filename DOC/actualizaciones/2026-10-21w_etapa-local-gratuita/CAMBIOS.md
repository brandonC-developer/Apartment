# Actualización 2026-10-21 (w) — Etapa local y gratuita antes de los servicios de pago

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) (sección 5.1 reescrita, E0, E6 y condición 6 de la definición de terminado), [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-023), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) (sección 4), README de la [fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Origen
El solicitante recordó que la implementación debe ir primero en local y gratis, con pruebas, y solo después usar los servicios ya mencionados (DigitalOcean, dominio, Resend). La decisión de contratar un Droplet de pruebas temporal desde la entrega E0 contradecía ese planteamiento y se corrigió.

## 2. Decisiones del solicitante
| # | Pregunta | Decisión | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo se despliega primero? | En local y gratis (etapa A); los servicios de pago después (etapa B) | Igual (planteamiento del solicitante) |
| 2 | ¿Qué camino sigue el entorno local y el servidor: Docker o no? | Sin contenedores en ambos lados: WSL 2 con Ubuntu-26.04 en local y el Droplet igual | Igual; se había preguntado antes por la pila local y el solicitante pidió el criterio de buenas prácticas, que se investigó |

## 3. Fuentes (por resumen, 21-oct-2026)
- The Twelve-Factor App, factor X: paridad entre desarrollo y producción; evitar servicios distintos en local y en producción.
- Docker, visión general: los contenedores dan consistencia entre entornos; el aislamiento es parcial y el estado de un contenedor eliminado se pierde si no es persistente.
- Microsoft, WSL: systemd (activo por defecto en la versión actual de Ubuntu; no mantiene viva la instancia) e instalación.
- Comprobación en la máquina del solicitante (solo lectura): Windows 11 compilación 26200, WSL 2.6.2.0, `Ubuntu-26.04` disponible, 15,7 GB de memoria, 18,6 GB libres en C:, solo `docker-desktop` instalado.

## 4. Cambios
- Plan: dos etapas, entorno de la etapa A y sustitutos locales de cada servicio; E0 se despliega en local; la E6 pasa a ser la etapa B (contratar, endurecer, probar en el Droplet y paso a producción); la condición 6 de la definición de terminado se refiere a la etapa A.
- DAS: nota en el ADR-023.
- Estrategia de pruebas: nuevo entorno de la etapa A en la sección 4.

## 5. Límites
- No se verificó que `Ubuntu-26.04` en WSL traiga systemd activo ni los paquetes de PostgreSQL 18 en esa versión.
- Espacio: 18,6 GB libres en C: pueden quedar justos; la distribución se puede mover a otra unidad.
- El correo local, el HTTPS autofirmado y los respaldos locales no prueban la entregabilidad, el certificado real ni Spaces.
- Los costos de los servicios no se contratan hasta terminar la etapa A: US$0 mientras tanto.
- Si el solicitante prefiere Docker en ambos lados, hay que reabrir el ADR-023 y revisar los ADR-013, 024 y 027.

## 6. Pendientes del plan
Versiones de Python y Django; registro de avance y regla ante una entrega Alta incompleta; revisión por otra persona; del plan de carga: formato del origen, consentimiento de los inquilinos actuales y fecha.

## 7. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.