# Actualización 2026-10-24 (c) — Lista de tareas de la implementación

**Fecha:** 2026-10-24
**Documentos afectados:** nuevo [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md) (TAR-SGA-001), [README de la fase 5](../../fase-5-implementacion/README.md) y [DOC/README.md](../../README.md). La ERS, el DAS y el plan no cambian.
**Origen:** instrucción del solicitante (24-oct-2026): «Antes de continuar crea un archivo de tarea a cumplir en la implementación según la documentación oficial para no inventar tareas en el proceso y poder ir marcando. Analiza toda la documentación»
**Estado:** lista viva, no versionada ni aprobada (como `AVANCE_IMPLEMENTACION.md`)

## 1. Qué se hizo
- Se leyó el plan de implementación v0.1 completo, el registro de avance, la ERS v1.16 (títulos de los 53 RF, los 20 RNF y los 83 CA, y el texto de RF-27, RF-28, RF-33 y de los CA de la E0), el DAS v0.15 (ADR-022 a ADR-032 y las 18 decisiones del ADR-032), la estrategia de pruebas v0.3 (prioridad de cada CA, secciones 6 y 7) y el README de la fase 6.
- Las listas de RF, RNF y CA por entrega **se generaron con un script** a partir de esos textos y de la tabla de entregas del plan, no a mano. Comprobación: 53 RF repartidos (4+8+14+11+8+7+1 en la fase posterior), 83 CA con prioridad y título, y los totales por entrega coinciden con `AVANCE_IMPLEMENTACION.md` (8, 8, 25, 17, 13, 8, 2).
- La **E0 se detalló en tareas** (proyecto, cuenta y autenticación, auditoría, configuración regional, base de datos, despliegue en WSL, respaldo, integración continua y pruebas de seguridad), cada una con su fuente, y se marcó lo ya hecho con su commit: lo hecho es sobre todo la sección B.
- Para E1 a E6 se añadieron las tareas del criterio de salida, de los hallazgos (HI-xx) y de las secciones del plan, y para la E6 las 18 decisiones del ADR-032. También constan las condiciones antes de cargar datos reales, la carga inicial y las pendientes de la fase 6.

## 2. Qué es propuesta del asistente (sin aprobar)
- La **agrupación** de la E0 en las secciones A a L y el orden sugerido dentro de ella: el plan no lo fija.
- Varias tareas de la E0 que **no están escritas en el plan con ese detalle** y que derivan de un ADR o de un requisito: la pantalla para emitir códigos nuevos (CA-69), la prueba de concurrencia del contador, obtener la IP de origen detrás de Nginx, `CONN_MAX_AGE = 0` y `BigAutoField`, el almacenamiento privado de archivos y `pip-audit` en la integración continua. Cada una cita su origen.
- El **marcado de «hecho»**: lo marcó el asistente con base en lo implementado; un CA solo se marca cuando pase su prueba en la integración continua, que aún no existe.

## 3. Puntos por decidir (también en el archivo)
1. El plan **no asigna a ninguna entrega el reemplazo del segundo factor con la sesión iniciada** (RF-27). Propuesta: E4.
2. El orden interno de la E0.
3. Hasta repetir todo con Python 3.14 en WSL, ninguna tarea de la E0 debería darse por terminada.

## 4. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`: sin problemas.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
