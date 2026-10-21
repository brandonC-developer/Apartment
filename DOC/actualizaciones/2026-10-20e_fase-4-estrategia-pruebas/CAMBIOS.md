# Actualización 2026-10-20 (e) — Fase 4: estrategia de pruebas v0.1

**Fecha:** 20 de octubre de 2026
**Documentos afectados:** [Estrategia de pruebas v0.1](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.1_borrador.md) (nuevo), [README de la fase 4](../../fase-4-pruebas/README.md) y [DOC/README.md](../../README.md).
**Versión anterior:** ninguna; la fase 4 no estaba iniciada.
**Estado:** borrador; no aprobado.

## 1. Motivo
El solicitante pidió iniciar la fase 4 ("empieza la fase 4") tras validar las entradas: los CA-01 a CA-57 de la [ERS v1.8](../../fase-1-ers/ERS_SGA_001_v1.8_borrador.md) y las decisiones del [DAS v0.9](../../fase-2-arquitectura/DAS_SGA_001_v0.9_borrador.md).

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| P1 | añadido | Estrategia de pruebas EPP-SGA-001 v0.1: niveles, entornos, cobertura de los 57 CA, verificación de los RNF sin CA, pruebas de operación, casos límite, criterios de entrada y salida, hallazgos HP-01 a HP-04 y decisiones pendientes | "empieza la fase 4" |
| P2 | modificado | README de la fase 4 (estado, producto y entradas) | Regla 3 de `CLAUDE.md` |
| P3 | modificado | `DOC/README.md`: mapa de fases e historial | Regla 3 de `CLAUDE.md` |

## 3. Impacto
Ningún requisito, regla ni identificador compartido cambia. El documento es una propuesta: niveles, herramientas, prioridades y criterios de salida son del asistente hasta que el solicitante decida (sección 11 del documento).

## 4. Decisiones
- **Resueltas:** ninguna en esta actualización.
- **Pendientes del solicitante:** ejecutor de pruebas, herramientas de extremo a extremo y de carga, umbral de cobertura, responsable de la restauración trimestral, CA para la segunda mitad de RN-15 y prioridades aceptables sin probar.
- **Hallazgos:** HP-01 (RN-15 sin CA para su segunda mitad), HP-02 (los CA no citan requisitos), HP-03 (el script no revisa este documento) y HP-04 (CA con resultado provisional por depender de obligaciones legales sin validar).

## 5. Evidencia y fuentes
- Vocke, *The Practical Test Pyramid* (2018): leída por resumen.
- Documentación de pruebas de Django (visión general y herramientas): leída por resumen; la segunda, hasta el carácter 100.000 de 113.245; sin cobertura de pruebas con el tiempo.
- OWASP Web Security Testing Guide: solo la página de presentación; sus categorías y casos no se leyeron.
- ISO/IEC/IEEE 29119-3: **no se pudo abrir** (error 403). No se afirma nada sobre su contenido.
- No se encontraron estudios universitarios sobre estrategias de pruebas para sistemas de saldos y comprobantes, ni una fuente para un umbral de cobertura de código.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. El script no revisa el contenido del documento nuevo (HP-03). Se contó a mano que los 57 CA aparecen asignados una sola vez. Revisión de pares: no realizada.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
