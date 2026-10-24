# Fase 5 — Plan de implementación

**Estado:** iniciada (plan v0.1 en borrador, sin revisar).

**Qué define:** módulos, tareas, dependencias, entregas y prioridades, con trazabilidad hasta los requisitos.

| Producto | Archivo | Estado |
|---|---|---|
| Plan de implementación (entregas E0 a E6, criterios de salida, condiciones antes de datos reales) | `PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md` (vigente) | Borrador v0.1; no aprobado |
| Lista de verificación de la revisión por otra persona (53 puntos en nueve áreas) | `LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md` (vigente) | Borrador v0.1; no aprobado; sin persona revisora designada |
| Registro de avance (una entrega a la vez; estados; bloqueo si falta una prueba Alta) | `AVANCE_IMPLEMENTACION.md` | Registro vivo, solo de adiciones; todas las entregas *no iniciada* |
| Lista de tareas por entrega (RF, RNF y CA generados de la ERS; E0 detallada; casillas para marcar) | `TAREAS_IMPLEMENTACION_SGA.md` | Lista viva; no versionada ni aprobada |

**Entradas:** ERS v1.16, DAS v0.15 (módulos de la sección 5 y ADR-002, 022 a 032), diseño técnico (fase 3) y estrategia de pruebas (fase 4).

**Decidido por el solicitante (21-oct-2026):** el orden de las entregas es esqueleto andante primero y rebanadas verticales por riesgo y dependencia, una entrega se da por terminada con una lista común de nueve condiciones más su criterio de salida propio (sección 3.1 del plan), y los datos iniciales se cargan digitándolos por las pantallas del sistema, con conciliación contra los registros actuales (sección 5). primero se despliega todo en local y gratis (etapa A: WSL 2 con Ubuntu-26.04, sin contenedores) y solo después se contratan los servicios de pago (etapa B: región NYC3, Droplet de producción de 2 GiB y 1 vCPU y un Droplet de pruebas temporal; sección 5.1). Las versiones son Django 5.2 LTS y Python 3.14 (sección 5.2). El avance se registra en `AVANCE_IMPLEMENTACION.md`, con una entrega a la vez y bloqueo si falta una prueba Alta (sección 3.2). Lo crítico (seguridad, datos personales y modelo financiero) lo revisa una persona distinta antes de cargar datos reales, y lo demás se autorevisa con herramientas (sección 3.3); falta designar a esa persona (la lista de verificación ya existe, LRC-SGA-001). Siguen pendientes los datos de la carga inicial y las versiones exactas.

**Elementos que deben incluirse y que no corresponden claramente a otra fase:**
- Plan de carga inicial de datos (saldo de apertura, RF-43): función en la E2; carga real por digitación con conciliación (sección 5 del plan); pendientes el formato del origen y el consentimiento de los inquilinos actuales.
- Integración con el canal de WhatsApp: fuera de la v1 (DP-04).
- Entregas incrementales, para poder iterar (ver `../metodologia/EVALUACION_METODOLOGIA_v1.md`).

**No se autoriza iniciar la implementación** hasta aprobar la ERS y la arquitectura.