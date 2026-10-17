# Actualización 2026-10-17 — ERS v1.5 y DAS v0.4

**Fecha:** 17 de octubre de 2026
**Documentos:** [ERS v1.5](../../fase-1-ers/ERS_SGA_001_v1.5_borrador.md) · [DAS v0.4](../../fase-2-arquitectura/DAS_SGA_001_v0.4_borrador.md)
**Versión anterior:** [actualización 2026-10-14](../2026-10-14_ERS-v1.4_DAS-v0.3/CAMBIOS.md) (ERS v1.4, DAS v0.3)
**Estado:** borrador; sin aprobación del negocio ni validación legal

## 1. Motivo

Un análisis de las dos versiones anteriores encontró 16 puntos bloqueantes y más de 45 ambigüedades en total. Se investigaron fuentes oficiales (Ley 7527, Ley 8968), estándares y documentación técnica, y el solicitante respondió un cuestionario de 33 puntos (Q-1 a Q-33). Esta actualización incorpora esas respuestas, las obligaciones legales identificadas y las correcciones de una revisión de coherencia.

## 2. Decisiones del solicitante incorporadas

| Punto | Decisión | Dónde queda |
|---|---|---|
| Q-1, Q-1b | Período de X a X (aniversario); el día X abre el período siguiente | ERS RN-03 |
| Q-10, Q-10b | Prorrateo solo del último período | ERS RN-12, RF-09 |
| Q-2 | Reajuste (prospectivo) y corrección (retroactiva con motivo) | ERS RF-10, RN-14 |
| Q-3 | Bloquear cambios que dejen saldo negativo | ERS RF-10 |
| Q-5 | Pagada automáticamente con saldo cero | ERS RF-13, RF-14 |
| Q-8 | Estado `anulada` con motivo | ERS RF-14, RN-17 |
| Q-9 | Anulación de movimientos con motivo, conservando el original | ERS RF-16 |
| Q-11, Q-11b | Generación 30 días antes; aviso a 120 días; estado `por decidir` | ERS RF-11, RF-42 |
| Q-12 | Ningún día compartido entre contratos de una propiedad | ERS RN-02 |
| Q-13a | Zona horaria solo a nivel de organización | ERS RF-33; DAS 7.6 |
| Q-13b | Gracia de 7 días | ERS RN-06, RN-07 |
| Q-14 | No se notifica cada abono | ERS CA-44 |
| Q-15, Q-15b, Q-15c, Q-16 | Depósito: excepción con motivo; advertencia sobre una mensualidad; sin calendarios; etiqueta al cerrar el contrato | ERS RF-29 a RF-32 |
| Q-17 | Comprobante: **diferido por el solicitante**; incluido luego por la instrucción de cubrir todas las obligaciones legales | ERS RF-37 (ver nota) |
| Q-18 | Colones y dólares con tipo de cambio manual | ERS RF-38 |
| Q-20 | Conservación de la foto de cédula: 5 años | ERS RF-41, RN-24 |
| Q-21 a Q-25 | Un recordatorio configurable; resumen diario por WhatsApp; 5 intentos; proveedor en fase de arquitectura; proceso a las 07:00 | ERS RF-21 a RF-24 |
| Q-26 a Q-31 | Documento de identidad con tipo y número; estados derivados; fecha real válida; saldo de apertura | ERS RF-01, RF-06, RF-34, RF-43 |
| Q-32 | MFA obligatorio con códigos de recuperación | ERS RF-27 |
| Q-33 | Hasta 50 propiedades; consultas en menos de 2 s | ERS RNF-08, RNF-10 |

**Nota sobre Q-17.** El solicitante respondió "requisito diferido". Después pidió redactar los documentos "con todas sus obligaciones legales". Se incluyó el comprobante (RF-37) como obligación legal de los arts. 16, 56 y 58 de la Ley 7527. El art. 58 admite otros procedimientos fehacientes. Si se vuelve a diferir, hay que registrar el riesgo (DP-20).

## 3. Requisitos nuevos

| ID | Origen |
|---|---|
| RF-37 Comprobante de pago | Ley 7527 arts. 16, 56, 58 |
| RF-38 Pago en moneda distinta | Ley 7527 art. 57 |
| RF-39 Consentimiento informado | Ley 8968 art. 5 |
| RF-40 Solicitudes del titular | Ley 8968 art. 7 |
| RF-41 Retención y eliminación | Ley 8968 art. 6 |
| RF-42 Aviso de vencimiento de contrato | Ley 7527 arts. 71 y 72 |
| RF-43 Saldo de apertura | Q-31 |
| RF-44 Datos mínimos en mensajes | Ley 8968 art. 14 |
| RF-45 Auditoría de acceso a cédulas | Ley 8968 arts. 10 y 11 |
| RNF-13 a RNF-17 | Referenciados antes sin definición |

**Requisitos que el solicitante no pidió expresamente y que fueron propuestos:** RN-05 (vencimiento dentro del período), RF-43 (detalle del saldo de apertura), RF-44, RF-45 y RF-40.

## 4. Cambios estructurales

- Identificadores DP unificados entre ERS y DAS (antes se repetían con distinto significado).
- Nueva sección 3 con las obligaciones legales OL-01 a OL-18.
- Entidad única "Movimiento" con saldos y estados derivados; se retira la entidad "Pago de alquiler".
- Correcciones documentales: referencia a la sección de decisiones, numeración de listas, RN-21 mal redactada, exclusiones duplicadas, matriz de trazabilidad completa y Anexo A antes del cierre.

## 5. Revisión de coherencia

Se comprobó con un script que todos los identificadores citados (RF, RN, RNF, CA, OL, DP, ADR) están definidos, y se releyó el contenido. Se corrigieron 8 fallas:

1. RN-05: el vencimiento podía caer fuera del período (caso inicio 31 de enero, vencimiento día 30). Añadido el criterio CA-50.
2. RN-15: impedía registrar abonos a obligaciones vencidas.
3. RN-17: podía anular la obligación del último período prorrateado.
4. RF-11: no generaba obligaciones para contratos *futuros*.
5. RF-43: el período en curso quedaba sin cubrir.
6. Gracia de 7 días: se limitaba a vivienda sin base en el texto leído del art. 58.
7. RF-41: el plazo de 5 años se contaba desde cualquier contrato.
8. RF-40: la supresión podía chocar con obligaciones de conservación.

## 6. Pendientes

| ID | Decisión | Responsable |
|---|---|---|
| DP-01 | Validar legalmente la fórmula del prorrateo | Propietario y abogado |
| DP-04 | Proveedor de WhatsApp | Propietario y responsable técnico |
| DP-07 | Respaldo: frecuencia, retención, RPO y RTO | Propietario y responsable técnico |
| DP-08 | Exposición pública de la aplicación | Responsable técnico |
| DP-14 | Pregunta P11 sin enunciado | Propietario |
| DP-17 a DP-21 | Validación legal y textos de consentimiento y comprobante | Abogado |
| DP-22 a DP-25 | Tope de reajuste, propietario del producto, regla de vencimiento y saldo de apertura | Propietario |

## 7. Evidencia y fuentes

- [CUESTIONARIO_CIERRE_ERS-DAS_recomendaciones_v1.md](CUESTIONARIO_CIERRE_ERS-DAS_recomendaciones_v1.md) — análisis de ambigüedades, recomendaciones, registro de fuentes y respuestas del solicitante.
- [Resumen para el abogado](../../legal/RESUMEN_PARA_ABOGADO_SGA_v1.md).
- [Evaluación de la metodología](../../metodologia/EVALUACION_METODOLOGIA_v1.md).

## 8. Limitaciones

- La lectura de las leyes fue propia, sobre copias de los textos. No es asesoría legal.
- La mayoría de las páginas técnicas se leyeron mediante una herramienta de resumen, no íntegramente.
- No hay revisión de pares ni ejecución de pruebas; los ejemplos numéricos se calcularon a mano.

## 9. Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | Por designar | Pendiente | Pendiente |
| Asesor legal | Por designar | Pendiente | Pendiente |
