# Actualización 2026-10-23 (f) — Alineación de los documentos con la ERS v1.12

**Fecha:** 2026-10-23
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado; mismo criterio que la [actualización 2026-10-22 (k)](../2026-10-22k_alineacion-ERS-v1.11/CAMBIOS.md)):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md), [Modelo de datos v0.5](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.5_borrador.md) (solo una nota), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md), [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md), el [registro de avance](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), los README de las fases 2 a 5 y [DOC/README.md](../../README.md)
**Origen:** [2026-10-23 (e)](../2026-10-23e_ERS-v1.12/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Tras publicar la ERS v1.12, seis documentos declaraban la v1.11 como base, CA-78 no estaba en la estrategia ni en el plan y varios describían la zona temporal que se descartó. El solicitante pidió alinearlos (23-oct-2026).

## 2. Cambios
| Documento | Cambio |
|---|---|
| DAS v0.11 | Base ERS v1.12; "5 MB" pasa a 5 MiB; la viñeta de archivos dice que no hay zona temporal y remite al diseño técnico; nota en el historial. **Sin ADR nuevos ni cambios de stack** |
| Modelo de datos v0.5 | Base ERS v1.12. **Solo una nota** (como se hizo con la v0.4 en la actualización (k)): `ARCHIVO_TEMPORAL`, R24, H16 y `sesion_hash` siguen descritos pero sin efecto, y se retiran en la v0.6. El modelo **sigue contradiciendo** la ERS v1.12 hasta entonces |
| Diseño técnico v0.7 | Base ERS v1.12. F-01 sin archivos (se guarda el inquilino y se audita); **F-02** rechaza el contrato sin frente; **F-10** directo al contrato con el bloqueo de H18; **F-11 nuevo** (agregar o reemplazar la fotografía del documento desde la ficha o el perfil); permisos con 5 MiB y la acción desactivada; pendientes 7 y condiciones de aprobación |
| Estrategia de pruebas v0.3 | Base ERS v1.12; CA-78 asignado (Integración, Alta, propuesta); prueba del límite de 5 242 880 / 5 242 881 bytes (propuesta); CA-75 con la acción desactivada y «Reemplazar»; recuento 78 de 78 |
| Plan de implementación v0.1 | Base ERS v1.12; CA-78 en la **E2**; HI-07 se cierra al quitarse la zona temporal; HI-08 ya no menciona la zona temporal |
| Lista de verificación v0.1 | Base ERS v1.12; RV-14 con 5 MiB; sin puntos nuevos |
| Registro de avance | E2 pasa de 0/23 a 0/24 CA; línea nueva en el historial |

## 3. Lo que propone el asistente y el solicitante no decidió
- Asignar CA-78 a la **E2** (necesita crear contratos) y su nivel y prioridad (Integración, Alta).
- Que el archivo ya escrito se borre en la misma petición si falla la base (F-10 y F-11).
- La prueba del límite de 5 242 880 y 5 242 881 bytes.
- Que F-11 sea un flujo aparte para el frente y el reverso.

## 4. Qué no se hizo
- **No se creó el modelo de datos v0.6.** El modelo vigente sigue con `ARCHIVO_TEMPORAL`, R24 y H16, y le falta la regla del contrato sin frente. Es el siguiente paso.
- No se repitió la prueba en PostgreSQL: varias de las 36 + 5 comprobaciones (R24, la limpieza de temporales, la concurrencia del identificador) dejan de aplicar.
- No se resolvió DP-30, DP-28, DP-29 ni DP-27.
- El script comprueba identificadores, enlaces, bases y cobertura, no el contenido; se revisó a mano el texto que citaba la zona temporal y "5 MB". No se releyeron enteros los documentos.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
