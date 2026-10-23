# Actualización 2026-10-22 (j) — ERS v1.11: cédula desde el perfil de la propiedad y fotografía del contrato

**Fecha:** 2026-10-22
**Documentos afectados:** [ERS v1.11](../../fase-1-ers/ERS_SGA_001_v1.11_borrador.md) (nueva; reemplaza a la [v1.10](../../fase-1-ers/ERS_SGA_001_v1.10_borrador.md), que no se edita), [README de la fase 1](../../fase-1-ers/README.md) y [DOC/README.md](../../README.md)
**Origen:** [2026-10-22 (i)](../2026-10-22i_cedula-y-contrato-desde-propiedad/CAMBIOS.md)
**Estado:** borrador; no aprobado

## 1. Motivo
El solicitante decidió que la cédula se agrega desde el perfil de la propiedad, que la fotografía del contrato es un documento nuevo y que son **dos fotos distintas** (22-oct-2026), y pidió redactar la ERS v1.11.

## 2. Cambios
| Dónde | Cambio |
|---|---|
| Control del documento | Versión 1.11, nota de control y fila de historial |
| Sección 1.3 | Términos nuevos: "Perfil de la propiedad" y "Fotografía del contrato" |
| Sección 2.3 | Perfil de la propiedad con las dos acciones |
| **RF-51 (nuevo)** | Agregar la cédula desde el perfil de una propiedad con contrato vigente; la fotografía se guarda en la ficha del inquilino y sigue RF-39, RF-02, RF-50, RF-45 y RN-24 |
| **RF-52 (nuevo)** | Fotografía del contrato asociada al contrato: JPEG o PNG, hasta 5 MB por archivo, un archivo por petición, reducción en el navegador con la mecánica de RF-50, repositorio privado, acceso y auditoría de la consulta; no se extrae la cédula de ella |
| **CA-75 a CA-77 (nuevos)** | Cédula desde el perfil; fotografía del contrato; protección y auditoría de la fotografía del contrato |
| Sección 7.1 | Entidad nueva: Documento del contrato |
| Matriz (sección 10) | RF-51 y CA-75 en "Registrar inquilinos y cédulas"; RF-52, CA-76 y CA-77 en "Administrar propiedades y contratos" |
| Sección 11 | Riesgo de exposición ampliado a la fotografía del contrato |
| Sección 12 | DP-28 y DP-29 nuevas; sección 12.1d con las decisiones; casilla nueva en la lista de aprobación |
| Totales | 52 RF y 77 CA (antes 50 y 74); DP pasa de 27 a 29. RN, RNF, OL, ADR y RE no cambian |

## 3. Trazabilidad
| Pregunta | Respuesta | Decisión | Dónde |
|---|---|---|---|
| ¿Dónde queda la foto de la cédula? | "Botón en el perfil de la propiedad, y se guarda en el inquilino" | Atajo desde el perfil; la foto es del inquilino | RF-51, CA-75 |
| ¿La foto del contrato es un documento nuevo? | "Sí, foto del contrato asociada al contrato" | Documento nuevo asociado al contrato | RF-52, CA-76, CA-77 |
| ¿Se reduce en el navegador? | "Sí, igual que la cédula pero con otra cifra a medir" | Misma mecánica, cifra por medir | RF-52, DP-29 |
| ¿Una o dos imágenes? | "son dos fotos distintas" | Dos fotos distintas; no se extrae la cédula del contrato | RF-52 |

## 4. Lo que propone el asistente y el solicitante no decidió
- Que la acción de RF-51 solo se ofrezca con un **contrato vigente** y que reemplazar una fotografía ya cargada se haga desde la ficha (RF-03).
- Que el contrato admita **varias fotografías** (páginas), un registro por fotografía y su número de orden (DP-29).
- La **auditoría de la consulta** de la fotografía del contrato (equivalente a RF-45) y que quede **sin retención ni eliminación** hasta DP-28.
- El **contenido del perfil de la propiedad**: solo se definió lo que necesitan estas dos acciones.
- Que en el **perfil** solo se vea el contrato vigente (no los futuros ni los anulados).
- Los ejemplos de CA-75 a CA-77 (JPEG de 3 MB, etc.) son del asistente.

## 5. Lo que no se verificó ni se resolvió
- **Privacidad:** la fotografía del contrato contiene datos personales del inquilino y del arrendador; no se ha consultado al abogado (DP-17, DP-28).
- **Cifras de reducción para un contrato:** no existen; un contrato tiene texto pequeño y 2048 px pueden no bastar (DP-29).
- **Desasociación y exportación del titular (RF-40, RF-41):** no se ampliaron a la fotografía del contrato; dependen de DP-28.
- **Tipo de contrato en el perfil cuando hay varios inquilinos:** no se trató; hoy un contrato tiene un solo inquilino (sección 7).

## 6. Documentos que quedan desalineados
El script de coherencia lo señala:
- **DAS v0.11, modelo de datos v0.4, diseño técnico v0.7, estrategia de pruebas v0.3, plan de implementación v0.1 y lista de verificación v0.1:** declaran la ERS v1.10 como base.
- **Estrategia de pruebas:** CA-75, CA-76 y CA-77 sin asignar.
- **Plan de implementación:** RF-51, RF-52 y CA-75 a CA-77 sin entrega (RF-51 y CA-75, E1; RF-52, CA-76 y CA-77, E2, donde existen los contratos; propuesta).
- **Modelo de datos:** falta la entidad Documento del contrato y la ampliación de la zona temporal (HT-10).
- **Diseño técnico:** faltan el perfil de la propiedad, las dos operaciones y sus permisos.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
