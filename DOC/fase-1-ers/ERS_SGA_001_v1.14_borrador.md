# Especificación de Requisitos de Software (ERS)

**Sistema de Gestión de Alquileres**

**Identificador:** ERS-SGA-001
**Versión:** 1.14 — Borrador para revisión
**Estado:** Borrador; pendiente de validación legal y aprobación formal
**Fecha:** 23 de octubre de 2026
**Idioma:** Español
**Configuración regional por defecto:** colones costarricenses (CRC) y dólares estadounidenses (USD) como monedas admitidas; zona horaria `America/Costa_Rica`.

**Nota de control (v1.14):** esta versión incorpora las decisiones del solicitante del 23 de octubre de 2026 sobre DP-29 (actualización `actualizaciones/2026-10-23k_dp-29-fotos-contrato/CAMBIOS.md`): (1) un contrato admite como máximo **10 fotografías** (RF-52, CA-76); el 10 es criterio del asistente, sin fuente sobre el largo de un contrato, aceptado por el solicitante; (2) la reducción de la fotografía del contrato **parte de un lado mayor de 3508 px y calidad 0,85** (unos 300 ppp en el largo de una hoja A4, según guías de OCR leídas por resumen), no de los 2048 px de RF-50, que se pensaron para una cédula; los valores definitivos y el peso objetivo se fijan al medir en la entrega E2 con fotos reales. DP-29 queda **dividida**: el máximo está resuelto; las cifras siguen abiertas hasta medir. Sin RF nuevos. Nada de esto está aprobado ni validado por abogado.

**Nota de control (v1.13):** esta versión incorpora la decisión del solicitante del 23 de octubre de 2026 sobre DP-30 (actualización `actualizaciones/2026-10-23i_dp-30-inquilinos-sin-frente/CAMBIOS.md`): los inquilinos guardados sin frente que nunca se completan se tratan con la retención sin contrato que ya existe (RF-41, CA-66), sin plazo nuevo; y se hacen visibles con una indicación en la ficha y un filtro «Sin frente» en la lista de inquilinos, sin alertas (RF-03, CA-78). DP-30 queda resuelta. Sin RF ni CA nuevos. Que un año sea plazo razonable para este caso lo valida el abogado (DP-17). Nada de esto está aprobado ni validado por abogado.

**Nota de control (v1.12):** esta versión incorpora las decisiones del solicitante del 23 de octubre de 2026 (actualizaciones `2026-10-23_ht-11-perfil-propiedad`, `2026-10-23c_unidad-tope-5mb` y `2026-10-23d_quitar-zona-temporal`): (1) el tope de subida pasa de "5 MB" a **5 MiB = 5 242 880 bytes** en todo requisito normativo (RF-02, RF-50, RF-52, CA-73, CA-74, CA-76); donde las notas de control o el historial de versiones anteriores dicen "5 MB", léase 5 MiB; (2) **no hay zona temporal de archivos**: el inquilino se registra primero (datos y consentimiento) y las fotografías se suben después a su ficha, y el frente es obligatorio **antes de asignar un contrato**, no para guardar al inquilino (RF-01, RF-03, RF-07, CA-01, nuevo CA-78, nueva DP-30); (3) en el perfil de la propiedad, sin contrato vigente las acciones se ven **desactivadas** con el aviso "No hay contrato vigente", y con una cara de la cédula ya cargada la acción dice "Reemplazar" (RF-51, RF-52, CA-75). La regla "sin contrato hasta tener el frente" fue propuesta por el asistente y aceptada por el solicitante, sin fuente. Nada de esto está aprobado ni validado por abogado.

**Nota de control (v1.11):** esta versión incorpora las decisiones del solicitante del 22 de octubre de 2026 sobre la fotografía de la cédula y del contrato (actualización `actualizaciones/2026-10-22i_cedula-y-contrato-desde-propiedad/CAMBIOS.md`): la cédula se agrega desde el perfil de la propiedad y se guarda en el inquilino (nuevo RF-51, CA-75); la fotografía del contrato es un documento nuevo, asociado al contrato y distinto de la de la cédula (nuevo RF-52, CA-76, CA-77, entidad Documento del contrato). Quedan abiertas DP-28 (conservación de la fotografía del contrato, con el abogado y el contador) y DP-29 (número de fotografías y cifras de reducción, tras medir). El "perfil de la propiedad" no existía en los documentos: su contenido completo es propuesta. Nada de esto está aprobado ni validado por abogado.

**Nota de control (v1.10):** esta versión incorpora la decisión del solicitante del 22 de octubre de 2026 de reducir en el navegador la fotografía del documento antes de enviarla (nuevo RF-50, nuevos CA-73 y CA-74) y de enviar el frente y el reverso en peticiones separadas (RF-02). Las cifras (2048 px, calidad 0,85, objetivo de 2 MB, tope de 5 MB) fueron propuestas por el asistente con fuentes de terceros, adoptadas por el solicitante como valores de diseño y **no se han medido con fotos reales**; ver `actualizaciones/2026-10-22f_ERS-v1.10/CAMBIOS.md`. Nada de esto está aprobado ni validado por abogado.

**Nota de control (v1.9):** esta versión incorpora las decisiones del solicitante del 20 y 21 de octubre de 2026 sobre el diseño técnico (hallazgos HT-01, HT-02, HT-03, HT-05 y HT-08, ver `actualizaciones/2026-10-21e_ERS-v1.9/CAMBIOS.md`). Varias cambian el alcance respecto de la v1.8: notificaciones por correo en lugar de WhatsApp, y recibos de papel fuera del sistema antes del comprobante generado por el sistema. Lo marcado "propuesta" no fue decidido por el solicitante. Nada de esto está aprobado ni validado por abogado.

**Nota de control (v1.8):** Esta versión incorpora las respuestas del solicitante a la ronda de validación del 17 de octubre de 2026 (puntos Q-1 a Q-33 del documento `actualizaciones/2026-10-17_ERS-v1.5_DAS-v0.4/CUESTIONARIO_CIERRE_ERS-DAS_recomendaciones_v1.md`) y las obligaciones legales identificadas en la Ley 7527 y la Ley 8968. Las respuestas del solicitante no equivalen a aprobación formal del propietario del negocio. **Este documento no es asesoría legal**: las obligaciones de la sección 3 deben ser validadas por un abogado antes de aprobar la línea base. El documento no certifica conformidad con ninguna norma ISO/IEEE ni autoriza iniciar la implementación.

# Control del documento

| Campo | Valor |
|---|---|
| Nombre | Especificación de Requisitos de Software — Sistema de Gestión de Alquileres |
| Identificador | ERS-SGA-001 |
| Versión | 1.12 |
| Estado | Borrador para revisión, validación legal y aprobación |
| Propietario del producto | brandonC-developer (identificador de Git del solicitante; no es necesariamente su nombre legal) |
| Responsable de requisitos | brandonC-developer (misma persona; sin revisión independiente) |
| Aprobador | brandonC-developer, como propietario del producto |
| Revisión siguiente | Tras resolver las decisiones pendientes de la sección 12 |

## Historial de versiones

| Versión | Descripción |
|---|---|
| 0.1 | Idea inicial: registro de inquilinos, calendario y recordatorios. |
| 1.0 | Primera especificación con requisitos funcionales y no funcionales, reglas, modelo conceptual y criterios de aceptación. |
| 1.1 | Decisiones: último día del mes para fechas inexistentes, recordatorios configurables, web y WhatsApp, alertas diarias, vigencia contractual, fecha real de pago, una cuenta administradora. |
| 1.2 | Consolidación documental, trazabilidad, criterios verificables, riesgos y referencias. |
| 1.3 | Prorrateo, abonos al depósito, almacenamiento privado de cédulas, configuración regional. |
| 1.4 | Abonos de alquiler, período por contrato, depósito con máximo de tres abonos, fecha real retroactiva, cambio de inquilino por nuevo contrato. |
| **1.5** | **Período por aniversario; prorrateo limitado al último período; reajuste distinto de corrección; días de gracia; estados derivados y estado `anulada`; movimientos con anulación; moneda USD con tipo de cambio manual; saldo de apertura; MFA con códigos de recuperación; sección de obligaciones legales (Ley 7527 y Ley 8968); comprobante de pago; derechos del titular de datos y retención; decisiones pendientes unificadas con IDs únicos; correcciones documentales.** |
| **1.6** | **Cierre de DP-22, DP-24 y DP-25 con las respuestas del solicitante: vencimiento configurable con día de inicio por defecto; saldo de apertura que incluye todos los períodos iniciados; tope de reajuste digitado en cada reajuste con su fuente. DP-23 parcialmente resuelta: el solicitante es propietario del producto y aprobador (falta registrar el nombre). Nuevo criterio CA-51.** |
| **1.7** | **Cierre de DP-07 (respaldo: RPO y RTO de 24 h, retención de 35 días) y DP-08 (acceso por internet; servidor virtual administrado por el solicitante); DP-04 sigue abierta, ligada a un proyecto externo. Cambios que surgieron del modelo de datos (MDD-SGA-001 v0.2): el saldo de apertura es una obligación y no un movimiento (glosario); nuevas entidades Condición del contrato, Ajuste de obligación y Organización; los cambios de importe se registran como ajustes y no sobrescriben; comprobantes consecutivos sin huecos; registro de movimientos idempotente por clave de solicitud; la auditoría no guarda valores personales (reescritura de RF-28). Nuevos criterios CA-52 a CA-55 y DP-26.** |
| **1.8** | **Cierre de DP-14 (P11 retirada por no recuperable), DP-23 (una sola persona ocupa los tres roles, identificada como brandonC-developer; el asesor legal sigue sin designar) y DP-26 (hora local más zona; el instante se calcula al ejecutar). H4: serie global de comprobantes, provisional hasta DP-20. Lectura del Reglamento 37554-JP (Archivo Nacional): nuevas obligaciones legales OL-19 a OL-21, requisito RF-46 (incidentes de seguridad) y RNF-18 (documentación de seguridad), criterios CA-56 y CA-57. Todo pendiente de abogado (DP-17).** Correcciones de QA del 17-oct-2026: entidad Incidente de seguridad en 7.1, alcance 2.3, lista de revisión y referencias; ver actualización 2026-10-17e. Corrección de la matriz de trazabilidad del 20-oct-2026 (RN-10, RN-15, RN-25 y seis RNF sin criterio); ver actualización 2026-10-20b.** |
| **1.9** | **Decisiones del solicitante del 20 y 21-oct-2026: notificaciones al administrador por web y correo en la v1 y WhatsApp futuro (RF-23, RF-24, RF-44, sección 2.4, CA-05, CA-08, CA-09, CA-43); avisos de seguridad de la cuenta a dos direcciones, cambio y restablecimiento de contraseña y de segundo factor (RF-27, CA-47, nuevos CA-59 y CA-60); exportación de todo el registro del titular en informe web imprimible (RF-40, CA-27); comprobante en dos fases, con recibo de papel fuera del sistema primero (RF-37 dividido, nuevo RF-47, CA-04, CA-34, CA-37 y CA-54 pasan a la fase posterior, nuevo CA-61). Nuevo CA-58 (segunda mitad de RN-15). Texto de API de la sección 15 ajustado. Difiere requisitos de prioridad Alta; ver actualización 2026-10-21e. Revisión guiada por módulos (21-oct-2026, actualización 2026-10-21ab): nuevos RF-48 (anular contrato) y RF-49 (vigilar el proceso diario) y CA-62 a CA-72; ajustes a RF-06, RF-17, RF-18, RF-21, RF-23, RF-27, RF-28, RF-29, RF-34, RF-38, RF-39, RF-40, RF-41, RF-42, RF-43, RN-06, RN-25, RN-26, RNF-12 y CA-45, CA-49. Totales: 49 RF y 72 CA.** |
| **1.10** | **Decisión del solicitante del 22-oct-2026 (actualización 2026-10-22f): la fotografía del documento se reduce en el navegador antes de enviarla (nuevo RF-50, nuevos CA-73 y CA-74, supuesto S-03, nueva DP-27 sobre los metadatos de la imagen) y el frente y el reverso se envían en peticiones separadas (nota en RF-02). RF-02 conserva su regla: JPEG y PNG, hasta 5 MB, verificados en el servidor. Se actualiza el riesgo del servidor propio (el endurecimiento se investigó el 22-oct-2026). Totales: 50 RF y 74 CA.** |
| **1.14** | **Decisiones del solicitante del 23-oct-2026 (actualización 2026-10-23k): máximo de 10 fotografías por contrato (RF-52, CA-76) y punto de partida de 3508 px y calidad 0,85 para reducir la fotografía del contrato, a confirmar al medir en la E2; DP-29 dividida (máximo resuelto, cifras abiertas). Sin RF ni CA nuevos. Totales: 52 RF y 78 CA.** |
| **1.13** | **Decisión del solicitante del 23-oct-2026 (actualización 2026-10-23i): DP-30 resuelta; los inquilinos sin frente se tratan con RF-41 y CA-66 (sin plazo nuevo) y se hacen visibles con una indicación en la ficha y un filtro «Sin frente» en la lista de inquilinos (RF-03, CA-78). Sin RF ni CA nuevos. Totales: 52 RF y 78 CA.** |
| **1.12** | **Decisiones del solicitante del 23-oct-2026 (actualizaciones 2026-10-23, 23c y 23d): tope de subida fijado en 5 MiB = 5 242 880 bytes; se descarta la zona temporal de archivos (registro del inquilino en dos pasos, frente obligatorio antes de asignar un contrato: RF-01, RF-03, RF-07, CA-01); contenido del perfil de la propiedad, acciones desactivadas sin contrato vigente y "Reemplazar" (RF-51, RF-52, CA-75); nuevos CA-78 y DP-30. Sin RF nuevos. Totales: 52 RF y 78 CA.** |
| **1.11** | **Decisiones del solicitante del 22-oct-2026 (actualización 2026-10-22i): cédula agregada desde el perfil de la propiedad y guardada en el inquilino (nuevo RF-51, CA-75, término "perfil de la propiedad"); fotografía del contrato como documento nuevo, asociada al contrato, distinta de la cédula y reducida en el navegador como ella (nuevo RF-52, CA-76, CA-77, entidad Documento del contrato). Nuevas DP-28 y DP-29. RF-01 a RF-50 no cambian. Totales: 52 RF y 77 CA.** |

# 1. Propósito y organización

## 1.1 Propósito

Definir de forma verificable el comportamiento esperado, las restricciones y las condiciones de aceptación de la primera versión del Sistema de Gestión de Alquileres (SGA), antes de tomar decisiones de arquitectura técnica o iniciar la implementación.

La ERS es la referencia común para el propietario del producto, analista, diseñador/arquitecto, desarrollador y responsable de pruebas. Todo cambio aprobado se registra en el historial de versiones y se evalúa por su impacto en requisitos, reglas, datos y pruebas.

## 1.2 Convención de redacción

- **"El sistema deberá"** expresa un requisito obligatorio.
- Cada requisito tiene un identificador único y es comprobable mediante prueba, inspección, análisis o demostración.
- Las recomendaciones y las decisiones pendientes se identifican por separado; no son requisitos aprobados.
- Los requisitos describen el comportamiento del producto, no una tecnología.
- Los requisitos con origen legal llevan la marca **[Legal OL-xx]**, que remite a la sección 3.

## 1.3 Términos

- **Inquilino:** persona que alquila una propiedad.
- **Propiedad:** vivienda, unidad o inmueble objeto del alquiler.
- **Contrato:** acuerdo que asocia a un inquilino con una propiedad durante una vigencia y define monto, moneda, día de vencimiento y destino (vivienda u otro).
- **Período de alquiler:** mes de alquiler que va desde un día X hasta el día anterior al mismo día X del mes siguiente (RN-03).
- **Obligación:** importe exigible de un contrato para un período de alquiler.
- **Importe exigible:** importe que el inquilino debe pagar por una obligación. Es el único término para este concepto; "monto esperado" e "importe esperado" quedan en desuso.
- **Movimiento:** registro inmutable de un abono de alquiler, un abono al depósito o una anulación (reversión).
- **Saldo de apertura:** deuda previa cargada al registrar en el sistema un contrato antiguo. Se modela como una **obligación** de tipo apertura, no como un movimiento (RF-43, CA-49).
- **Ajuste de obligación:** registro inmutable que suma o resta importe a una obligación (reajuste, corrección, prorrateo del último período o ajuste manual). El importe exigible vigente es el importe inicial más sus ajustes.
- **Saldo pendiente:** importe exigible menos la suma de movimientos válidos. No debe confundirse con el estado "pendiente".
- **Vencimiento:** fecha pactada de pago de una obligación.
- **Fecha límite de pago:** vencimiento más los días de gracia del contrato.
- **Estados de una obligación:** *pendiente* (saldo mayor que cero y fecha límite no superada), *vencida* (saldo mayor que cero y fecha límite superada), *pagada* (saldo cero) y *anulada* (cancelada con motivo).
- **Notificación web:** aviso persistente dentro de la aplicación para el administrador.
- **Notificación por correo:** mensaje enviado al administrador por un servicio de correo; que el servicio lo acepte no implica entrega ni lectura.
- **Notificación WhatsApp (futuro, fuera de la v1):** mensaje enviado por un proveedor compatible; que el proveedor lo acepte no implica entrega ni lectura.
- **Aviso de seguridad de la cuenta:** correo a dos direcciones que informa un evento de la cuenta administradora (RF-27).
- **Fotografía del documento de identidad:** imagen del documento (cédula, DIMEX, pasaporte u otro); en el modelo y las pruebas se conserva el nombre histórico "cédula". El "frente" es la cara con la fotografía y los datos principales.
- **Perfil de la propiedad:** pantalla del administrador con los datos de una propiedad (RF-06), el inquilino y el contrato vigente, y las acciones sobre él, entre ellas agregar la fotografía de la cédula del inquilino (RF-51) y la del contrato (RF-52). Sin historial de contratos en la v1. *Término nuevo de la v1.11; el contenido de esta definición lo decidió el solicitante el 23-oct-2026; la maquetación y los textos son propuesta.*
- **Fotografía del contrato:** imagen de una página del contrato firmado, asociada al contrato (RF-52); es distinta de la fotografía del documento de identidad.
- **Recibo físico:** recibo de papel hecho fuera del sistema; el sistema solo anota su número (RF-47).
- **Titular de datos:** persona física cuyos datos personales se tratan (el inquilino).
- **Verificación:** comprobar que el producto cumple sus requisitos.
- **Validación:** comprobar que el producto satisface las necesidades del usuario y del negocio.

# 2. Contexto, objetivos y alcance

## 2.1 Objetivo general

Permitir al administrador registrar inquilinos y sus documentos de identificación, administrar propiedades y contratos, controlar obligaciones mensuales de alquiler, registrar abonos y pagos completos, visualizar el saldo pendiente, anotar el número del recibo de papel (los comprobantes generados por el sistema, en una fase posterior), y consultar vencimientos en un calendario con recordatorios anticipados y alertas diarias de atraso, cumpliendo las obligaciones legales aplicables al arrendamiento y al tratamiento de datos personales.

## 2.2 Objetivos específicos

1. Mantener fichas de inquilinos con datos personales y fotografía de la cédula, con consentimiento informado.
2. Asociar cada contrato con un único inquilino y una única propiedad.
3. Generar como máximo una obligación por contrato y período, sin duplicados.
4. Registrar abonos y pagos completos, manteniendo visible el saldo pendiente.
5. Registrar la fecha real de recepción y conservar la fecha/hora en que el movimiento fue ingresado.
6. Consultar pagos y saldos en un calendario con filtros por inquilino y estado.
7. Configurar recordatorios anticipados y emitir alertas diarias de atraso.
8. Proteger datos personales, atender los derechos del titular y conservar trazabilidad de los cambios relevantes.
9. Anotar el recibo de papel (y, en una fase posterior, emitir comprobantes de pago) y aplicar las reglas legales de plazos, reajustes, garantía y moneda.

## 2.3 Incluido en la primera versión

- Registro, consulta, edición y desactivación lógica de inquilinos, con registro de consentimiento.
- Carga y consulta autorizada de la fotografía de cédula (frente obligatorio antes de asignar un contrato, reverso opcional), con reducción previa en el navegador (RF-50) y un archivo por petición (RF-02).
- Perfil de la propiedad con acciones para agregar la cédula del inquilino del contrato vigente (RF-51) y la fotografía del contrato (RF-52).
- Registro de propiedades con alias y estado derivado, y marca de inactiva con sus reglas (RF-06).
- Registro, modificación controlada (reajuste y corrección), finalización y anulación (sin movimientos, RF-48) de contratos.
- Monto mensual fijo por contrato, en CRC o USD.
- Período de alquiler por aniversario del día de inicio; vencimiento por día fijo con ajuste al último día del mes.
- Días de gracia por contrato.
- Generación de obligaciones 30 días antes de cada período.
- Prorrateo del último período cuando el contrato termina antes de completarlo.
- Registro de abonos y pagos completos con saldo derivado; anulación de movimientos con motivo.
- Pagos en moneda distinta de la del contrato con tipo de cambio ingresado manualmente.
- Recibo de pago de papel fuera del sistema, con anotación opcional de su número (RF-47); el comprobante numerado generado por el sistema (RF-37) queda para una fase posterior.
- Saldo de apertura para contratos con historia previa.
- Depósito de garantía por contrato con abonos y saldo.
- Estados pendiente, vencida, pagada y anulada.
- Calendario mensual con filtros por inquilino, propiedad y estado, y eventos informativos de fin de contrato y de fecha límite del depósito.
- Notificaciones web y por correo al administrador; un recordatorio anticipado configurable; resumen diario de alertas de atraso.
- Una única cuenta administradora con autenticación multifactor, cambio y restablecimiento de contraseña y avisos de seguridad por correo a dos direcciones.
- Atención de solicitudes del titular de datos (con desasociación a petición); retención y eliminación de datos personales, incluida la de inquilinos sin contrato.
- Registro de auditoría de operaciones críticas, de los eventos de autenticación y de seguridad, del acceso a cédulas y de las exportaciones del titular, con una pantalla de consulta de solo lectura (RF-28, RF-45).
- Vigilancia del proceso diario, con alerta y aviso si no corre o falla (RF-49).
- Registro de incidentes de seguridad con la fecha límite de aviso a titulares y a la Agencia (RF-46).

## 2.4 Fuera del alcance inicial

- Cobro o procesamiento automático de dinero, integración bancaria y conciliación automática.
- Consulta automática de tipos de cambio; conversión automática entre monedas.
- Cálculo automático de intereses, multas o penalizaciones.
- Prorrateo general de períodos al inicio del contrato y de meses intermedios; queda diferido a una versión futura (P1/R1/R2 y Q-1).
- Facturación electrónica o contabilidad completa. Si la normativa tributaria exige factura electrónica por el alquiler no está verificado en fuente oficial; es una consulta para el contador o abogado (DP-20).
- Comprobante de pago generado, numerado y reimpreso por el sistema (RF-37): fase posterior, por decisión del solicitante del 21-oct-2026.
- Acceso de inquilinos a un portal propio; notificaciones a inquilinos.
- Varias cuentas humanas con roles diferenciados.
- SMS y WhatsApp como canales de notificación. WhatsApp queda para una versión futura, ligado a DP-04; en la v1 las notificaciones al administrador salen por la web y por correo (RF-23), y el correo también se usa para los avisos de seguridad de la cuenta y el enlace de restablecimiento de contraseña (RF-27). El correo no se usa para notificar a inquilinos.
- Varios inquilinos bajo un mismo contrato.
- Calendarios o acuerdos de cuotas del depósito de garantía (Q-15c).
- Devoluciones, deducciones y liquidación del depósito de garantía.
- Consulta automática del índice de precios (INEC) o de los porcentajes publicados por el MIVAH.

## 2.5 Supuestos

- El primer piloto se usa en Costa Rica; el producto se diseña para configurarse en otras regiones.
- Las monedas admitidas son CRC y USD; la moneda se define por contrato.
- La zona horaria predeterminada es `America/Costa_Rica` y se configura a nivel de organización, no por propiedad.
- El administrador registra manualmente la recepción de cada pago.
- El monto mensual permanece fijo salvo reajuste o corrección registrados con fecha efectiva.
- Volumen esperado el primer año: hasta 50 propiedades y un administrador.
- El envío de correo depende de un servicio externo y de un dominio propio verificado (DAS, ADR-026); el dominio será un `.com` registrado en Cloudflare Registrar (decisión del solicitante del 21-oct-2026; el nombre y el precio exacto se confirman al comprarlo). Cuando WhatsApp vuelva, depende de un proveedor externo aún no elegido.
- **S-01:** el vencimiento de una obligación cae dentro de su período (RN-05). Confirmado por el solicitante el 17-oct-2026 (DP-24).
- **S-02:** el destino del contrato (vivienda u otro) determina qué reglas legales se advierten; ver OL-06.
- **S-03:** el administrador usa un navegador con JavaScript y con soporte de canvas y de JPEG (RF-50). Es un supuesto sin verificar; si no se cumple, aplica el envío del original de CA-74.

# 3. Obligaciones legales

Esta sección recoge las obligaciones legales identificadas y los requisitos que las implementan. **Fuentes leídas:** texto de la Ley 7527, Ley General de Arrendamientos Urbanos y Suburbanos (copia del SCIJ, con reformas hasta la Ley 9354 de 2016), y texto de la Ley 8968, Protección de la Persona frente al Tratamiento de sus Datos Personales. **Leído parcialmente (v1.8):** el Reglamento a la Ley 8968, Decreto 37554-JP (copia del Archivo Nacional con reformas del decreto 40008 de 2016): arts. 3, 32, 34 a 39 y 44; no se confirmó en el SCIJ que no existan reformas posteriores. **No se revisaron:** el resto del reglamento, normativa tributaria, contable ni de facturación, ni otras normas aplicables. La lista no es exhaustiva. Todo su contenido está **pendiente de validación por un abogado** (DP-17).

## 3.1 Ley 7527 — Arrendamientos

| ID | Fuente | Obligación o regla | Requisitos que la implementan |
|---|---|---|---|
| OL-01 | Art. 58 | El pago es por períodos de un mes, salvo pacto. El inquilino puede pagar dentro de los siete días naturales siguientes al vencimiento del período de pago. | RF-07, RF-14, RN-03, RN-07 |
| OL-02 | Art. 62 | Aceptar un pago en fecha posterior no modifica el día o el período de pago pactados, salvo pacto escrito. | RN-09 |
| OL-03 | Arts. 16, 56, 58 | El arrendador debe entregar recibo o comprobante de pago, salvo que se pacten otros procedimientos que acrediten el pago de forma fehaciente. El inquilino tiene derecho irrenunciable a exigirlo y el arrendador conserva copia. | RF-37 |
| OL-04 | Art. 61 | El pago con cheque, título valor u otra modalidad solo descarga la obligación con el recibo del efectivo. | RF-34, RF-16, RN-11 |
| OL-05 | Art. 57 | Si el precio se pacta en moneda extranjera, el inquilino puede pagar en colones al tipo de cambio de venta del Banco Central de Costa Rica a la fecha del pago. | RF-38 |
| OL-06 | Art. 67 | En vivienda, el precio se actualiza al final de cada año del contrato, con tope: inflación acumulada de 12 meses (INEC) si es menor o igual a 10 %; si supera 10 %, el porcentaje lo fija el MIVAH entre 10 % y la inflación. El reajuste rige desde el período de pago siguiente a la notificación. Un reajuste mayor es nulo. Es válido pactar uno menor. | RF-10, RN-14 |
| OL-07 | Art. 67 | Si el precio de una vivienda está en moneda extranjera, se mantiene la suma convenida durante todo el plazo, sin derecho a reajuste. | RF-10, RN-14 |
| OL-08 | Art. 70 | La duración del arrendamiento no puede ser inferior a tres años; si se pactó menos o no se pactó, se entiende de tres años. | RF-07 |
| OL-09 | Arts. 71, 72 | Prórroga tácita por tres años si el arrendador no notifica con al menos tres meses de anticipación su voluntad de no renovar. El inquilino extingue el contrato avisando con tres meses de anticipación, salvo pacto escrito en contrario. | RF-09, RF-42, RN-16 |
| OL-10 | Art. 60 | El inquilino paga el alquiler desde el día en que recibe el bien hasta el día en que lo entrega. | RN-03, RN-12 |
| OL-11 | Arts. 58, 92 | En vivienda no se puede exigir pago anticipado de más de una mensualidad (art. 58). No se puede obligar a pagar anticipadamente más de una mensualidad ni a rendir garantía mayor a una mensualidad; lo contrario es nulo (art. 92). | RF-29, RN-15, RN-26 |
| OL-12 | Art. 59 | Las garantías responden por el pago de los alquileres y por las demás obligaciones del contrato, salvo pacto expreso en contrario. | RF-29 |

## 3.2 Ley 8968 — Datos personales

| ID | Fuente | Obligación o regla | Requisitos que la implementan |
|---|---|---|---|
| OL-13 | Art. 5 | Antes de recolectar datos, informar de modo expreso, preciso e inequívoco ocho puntos: existencia de la base de datos, fines, destinatarios, carácter obligatorio o facultativo de las respuestas, tratamiento, consecuencias de negarse, derechos del titular, e identidad y dirección del responsable. Obtener consentimiento expreso por escrito (físico o electrónico), revocable sin efecto retroactivo. Se prohíbe acopiar datos sin consentimiento informado. | RF-39 |
| OL-14 | Art. 6 | Datos actuales, veraces, exactos y adecuados a su fin. Eliminar los que dejen de ser pertinentes. En ningún caso conservar datos que puedan afectar al titular pasados diez años de los hechos, salvo norma especial; si hace falta conservarlos, desasociarlos del titular. | RF-41, RN-24 |
| OL-15 | Art. 7 | Derecho de acceso, rectificación, actualización y supresión. El responsable debe cumplir lo solicitado gratuitamente y resolver en cinco días hábiles desde la recepción. | RF-40 |
| OL-16 | Arts. 10, 11 | Medidas técnicas y de organización para garantizar la seguridad e impedir alteración, pérdida, tratamiento o acceso no autorizado. Deber de confidencialidad de quien intervenga en el tratamiento, aun después de finalizar su relación con la base. | RNF-14, RNF-15 |
| OL-17 | Art. 14 | Los datos solo pueden transferirse con autorización expresa y válida del titular. | RF-44 |
| OL-18 | Arts. 2, 3, 21 | La ley no aplica a bases con fines exclusivamente internos, personales o domésticos que no se comercialicen. Se define "dato sensible" con ejemplos que incluyen la condición socioeconómica. Las bases administradas con fines de distribución, difusión o comercialización deben inscribirse ante la Prodhab. **Aplicabilidad al SGA por determinar** (DP-19). | DP-19, RNF-14 |
| OL-19 | Reglamento, arts. 38 y 39 | Ante una vulnerabilidad de seguridad que afecte datos personales (pérdida, destrucción, extravío u otra), informar al titular dentro de cinco días hábiles y a la Agencia (Prodhab), con la naturaleza del incidente, los datos comprometidos, las acciones inmediatas y dónde obtener más información; iniciar en ese plazo una revisión exhaustiva. Desde cuándo corre el plazo y cuándo hay que notificar a la Agencia se validan (DP-17). | RF-46, CA-56 |
| OL-20 | Reglamento, arts. 32 y 33 | Confeccionar un protocolo mínimo de actuación (políticas de privacidad, capacitación, control interno, procedimientos gratuitos para consultas, acceso, rectificación, bloqueo, supresión y revocación, y un historial de los datos durante su tratamiento), que la Agencia puede verificar; se inscribe ante ella. | RNF-18, RF-40 |
| OL-21 | Reglamento, arts. 34 a 37 | Establecer y mantener medidas de seguridad administrativas, físicas y lógicas, documentadas: descripción de datos, inventario de infraestructura, análisis de riesgos, medidas aplicadas, riesgo residual y plan de trabajo; actualizarlas ante cambios o vulneraciones y, si hay datos sensibles, al menos una vez al año. | RNF-14, RNF-18 |

# 4. Actores y límites del sistema

| Actor o sistema externo | Responsabilidad |
|---|---|
| Administrador | Gestiona inquilinos, propiedades, contratos, movimientos, configuración y notificaciones. |
| Servicio programado de procesos | Genera obligaciones, avisos y alertas y aplica retención, sin depender de que la interfaz esté abierta. |
| Servicio de correo | Acepta los correos que envía el sistema (notificaciones al administrador, avisos de seguridad y enlace de restablecimiento). La API de envío informa la aceptación; la v1 no recibe estados posteriores. |
| Proveedor de WhatsApp (futuro) | Acepta, procesa y reporta los estados disponibles de los mensajes. No forma parte de la v1. |

El inquilino no tiene acceso al sistema en esta versión. Las notificaciones se dirigen solo al administrador. Los datos de contacto del inquilino (teléfono y correo, opcionales) se capturan como parte de la ficha, para que el administrador lo contacte por su cuenta, pero no se usan para notificar en esta versión.

# 5. Requisitos funcionales

## 5.1 Gestión de inquilinos

**RF-01 — Registrar inquilino.** El sistema deberá permitir registrar nombre completo, tipo de documento (cédula, DIMEX, pasaporte u otro), número de documento, teléfono, correo electrónico y fotografía del documento de identidad (frente obligatorio antes de asignarle un contrato, reverso opcional). Son **obligatorios para guardar** el nombre completo, el tipo y el número de documento y el consentimiento (RF-39); el frente de la fotografía es obligatorio **antes de asignar un contrato** al inquilino (RF-07), no para guardarlo; el teléfono y el correo son **opcionales**: sirven al administrador para contactar al inquilino por su cuenta y el sistema no los usa para notificar. La fotografía es del documento de identidad de cualquier tipo, y el "frente" es la cara con la fotografía y los datos principales (en un pasaporte, la página de datos). *Nota v1.9 (revisión por módulos, 21-oct-2026): decisiones del solicitante; en la v1.8 no se decía cuáles campos eran obligatorios ni que la fotografía fuese del documento de cualquier tipo.* Deberá advertir cuando exista otro inquilino activo con el mismo tipo y número de documento. *Nota v1.12 (23-oct-2026): el registro es en dos pasos: primero se guarda el inquilino (datos y consentimiento) y después cada fotografía se sube a su ficha (RF-03), en una petición propia (RF-02); por eso no hay archivos a la espera de un inquilino que aún no existe. Es decisión del solicitante; la regla "no se asigna contrato hasta tener el frente" fue propuesta del asistente y aceptada por él, sin fuente. Lo que se hace con quien nunca completa el frente: RF-41 y CA-66, sin plazo nuevo (DP-30, resuelta en la v1.13).*

**RF-02 — Validar información.** El sistema deberá validar campos obligatorios, formato de contacto y archivo antes de aceptar el registro. Formatos permitidos: JPEG y PNG, hasta **5 MiB (5 242 880 bytes)** por archivo. Deberá verificar el tipo real del archivo y no solo el tipo declarado por el navegador. *Nota v1.10 (22-oct-2026): el frente y el reverso se envían cada uno en una petición propia; el límite de 5 MiB y la verificación del tipo real se aplican siempre en el servidor, con o sin la reducción del navegador (RF-50).*

**RF-50 — Reducir la fotografía antes de enviarla.** El sistema deberá reducir, en el navegador del administrador y antes de enviarla, cada fotografía del documento de identidad: (1) escalarla de modo que su lado mayor no pase de **2048 píxeles**, sin ampliar una imagen más pequeña; (2) codificarla como JPEG con calidad inicial de **0,85**; (3) si el resultado pesa más de **2 MB** (objetivo), probar calidades menores sin bajar de **0,70**; (4) si aun así pesa más de **5 MiB**, reducir el lado mayor hasta que no lo pase; y (5) conservar la orientación visible de la imagen. Si el navegador no puede reducirla, deberá enviar el original solo si es JPEG o PNG de hasta 5 MiB; en otro caso, informar al administrador antes de enviar. La reducción **no es un control de seguridad**: el servidor aplica siempre RF-02. *Valores de diseño: las cifras fueron propuestas por el asistente con fuentes de terceros (guía de un proveedor de verificación de identidad, documentación de MDN) y adoptadas por el solicitante el 22-oct-2026; no se han medido con fotos reales y se confirman en la entrega E1 con al menos un iPhone y dos teléfonos Android. Los pasos intermedios de calidad entre 0,85 y 0,70 son propuesta.* *No se cita ninguna obligación legal para esta reducción; el tratamiento de los metadatos de la imagen está pendiente en DP-27.*

**RF-51 — Agregar la cédula desde el perfil de la propiedad.** El sistema deberá ofrecer, en el perfil de una propiedad con un contrato vigente, una acción para agregar la fotografía del documento de identidad (frente o reverso) del inquilino de ese contrato; si esa cara ya está cargada, la acción dice «Reemplazar» y la fotografía anterior se marca como eliminada. La fotografía **se guarda en la ficha del inquilino**, no en la propiedad, y sigue las mismas reglas que si se hubiera cargado desde la ficha: consentimiento previo (RF-39), validación (RF-02), reducción en el navegador (RF-50), acceso restringido y auditado (RF-45) y retención (RN-24). Si la propiedad no tiene un contrato vigente (está libre o solo tiene un contrato futuro), la acción se muestra **desactivada** con el aviso «No hay contrato vigente». *Nota v1.12: la acción desactivada con aviso y el «Reemplazar» desde el perfil son decisiones del solicitante del 23-oct-2026 (opciones recomendadas por el asistente); los textos exactos son propuesta.* *Nota v1.11: es una decisión del solicitante del 22-oct-2026 (atajo desde el perfil de la propiedad). Son propuesta del asistente: que solo se ofrezca con un contrato vigente y que reemplazar una fotografía ya cargada se haga desde la ficha del inquilino (RF-03).*

**RF-03 — Consultar y actualizar al inquilino.** El administrador deberá poder buscar, consultar y actualizar la ficha, incluido agregar o reemplazar el frente y el reverso de la fotografía del documento (con las reglas de RF-02, RF-39, RF-45 y RF-50; la fotografía reemplazada se marca como eliminada). La ficha indica cuándo falta el frente y la lista de inquilinos permite filtrar los que están «Sin frente»; no hay alertas ni correos por este motivo. *Nota v1.13: indicación y filtro son decisión del solicitante del 23-oct-2026 (opción recomendada por el asistente); los textos exactos son propuesta.* Los cambios de identificación se validan y quedan auditados.

**RF-04 — Desactivar inquilino.** El sistema deberá permitir desactivar a un inquilino sin eliminar contratos, obligaciones ni historial. Deberá bloquear la desactivación si el inquilino tiene un contrato vigente o saldos pendientes, y permitir reactivarlo.

**RF-05 — Consultar ficha de inquilino.** El sistema deberá mostrar datos de contacto, contrato vigente cuando exista, obligaciones e historial asociado, respetando las restricciones de acceso a documentos.

## 5.2 Propiedades y contratos

**RF-06 — Registrar propiedad.** El sistema deberá permitir registrar una propiedad con identificador único, **alias** (nombre corto obligatorio y único, que se muestra en listas, calendario y correos), descripción y dirección. Su estado se deriva: *disponible* u *ocupada* (según tenga o no un contrato vigente), más *inactiva*, que marca el administrador. Marcar inactiva una propiedad se **bloquea** si tiene un contrato vigente, futuro o por decidir; se puede reactivar; y una propiedad inactiva no admite contratos nuevos. *Nota v1.9 (revisión por módulos, 21-oct-2026): alias y regla de propiedad inactiva por decisión del solicitante; RF-44 ya hablaba de un "alias" que no estaba definido.*

**RF-07 — Crear contrato.** El sistema deberá permitir asociar un único inquilino con una única propiedad y registrar: destino (vivienda u otro), fecha de inicio (fecha de entrega del bien), fecha de fin si existe, monto mensual fijo, moneda (CRC o USD), día de vencimiento de 1 a 31 (por defecto, el día de inicio del período), días de gracia (7 por defecto) y, cuando corresponda, el depósito de garantía. El día de inicio ancla el período de alquiler (RN-03). **[Legal OL-01, OL-08, OL-10]** Deberá advertir, sin bloquear, cuando la vigencia pactada sea inferior a tres años. Deberá **rechazar** la creación de un contrato con un inquilino cuyo frente de la fotografía del documento aún no esté cargado (RF-01). *Nota v1.12: regla propuesta por el asistente y aceptada por el solicitante el 23-oct-2026, sin fuente.*

**RF-08 — Validar solapamiento contractual.** El sistema deberá rechazar un contrato que comparta al menos un día con otro contrato de la misma propiedad, considerando ambas fechas inclusive y la vigencia sin fecha de fin como abierta (RN-02).

**RF-09 — Finalizar contrato.** El sistema deberá permitir registrar la fecha de fin (inclusive). **[Legal OL-09]** Al registrarla:
- las obligaciones futuras sin movimientos válidos se anulan con auditoría (RN-17);
- si la fecha de fin cae dentro de un período, el importe de ese último período se prorratea (RN-12) y puede ajustarse manualmente con motivo;
- se conservan las obligaciones y movimientos existentes;
- el sistema advierte, sin bloquear, si la fecha de fin dista menos de tres meses de la fecha de registro.

**RF-10 — Modificar condiciones contractuales.** El sistema deberá distinguir dos tipos de cambio, ambos con auditoría del valor anterior, el nuevo valor, la fecha efectiva y el motivo:
- **Reajuste.** Registra la fecha de notificación al inquilino, el nuevo monto y el porcentaje resultante. La fecha efectiva se normaliza al inicio del período siguiente a la notificación; no se admiten fechas efectivas a mitad de período. Aplica solo a obligaciones cuyo período inicia en o después de la fecha efectiva. Para vivienda, el administrador digita en cada reajuste el porcentaje máximo vigente y su fuente (certificación del INEC o publicación del MIVAH), que el sistema conserva junto al reajuste; el sistema deberá advertir, sin bloquear, cuando el porcentaje supere ese tope, y deberá rechazar el reajuste de una vivienda con precio en moneda extranjera. **[Legal OL-06, OL-07]**
- **Corrección.** Corrige un error de monto, vencimiento o período. Es retroactiva, requiere motivo obligatorio y puede actualizar obligaciones no pagadas, incluidas las vencidas.

El importe de una obligación **no se sobrescribe**: cada reajuste, corrección o ajuste manual se registra como un ajuste inmutable, y el importe exigible vigente se deriva (H9 del modelo de datos).

En ambos casos, las obligaciones pagadas no se modifican y el sistema deberá **bloquear** cualquier cambio que deje el importe exigible por debajo de la suma de movimientos válidos ya registrados, mostrando el exceso.

**RF-36 — Sustituir inquilino mediante nuevo contrato.** Cuando cambie el inquilino de una propiedad, el administrador deberá cerrar el contrato anterior y crear uno nuevo. El sistema conserva el historial y valida el solapamiento (RF-08). El depósito del contrato anterior no se traslada automáticamente al nuevo.

**RF-48 — Anular contrato.** El administrador deberá poder anular un contrato **solo si no tiene movimientos válidos** (ni de alquiler ni de depósito), con **motivo obligatorio**. Al anularlo, el sistema anula sus obligaciones (que no tienen movimientos, RN-17) y su depósito si no tiene abonos, deja constancia en la auditoría, y el contrato deja de contar para el solape (RN-02) y de figurar como vigente de la propiedad. Un contrato que ya recibió pagos no se anula: se finaliza (RF-09) y su historial se conserva (RN-10). *Nota v1.9 (revisión por módulos, 21-oct-2026): requisito nuevo por decisión del solicitante; el estado "anulado" existía en RN-30 y en el modelo de datos sin una operación que lo produjera.*


**RF-49 — Vigilar el proceso diario.** Si no hay una ejecución correcta del proceso diario del día una hora después de la hora programada, o si la última ejecución falló, el sistema deberá registrar un aviso, mostrar una **alerta web persistente** en cada inicio de sesión hasta que haya una ejecución correcta y enviarlo por correo al administrador. La comprobación la hace el reintentador de intervalo corto, no el proceso diario. No detecta un servidor caído (monitoreo externo, fase 6). *Nota v1.9 (revisión por módulos, 21-oct-2026): requisito nuevo por decisión del solicitante; la hora de la comprobación (una hora después) es propuesta del asistente.*

**RF-52 — Registrar la fotografía del contrato.** El sistema deberá permitir al administrador agregar, desde el perfil de la propiedad, una o más fotografías del contrato firmado, hasta un **máximo de 10 por contrato**, **asociadas al contrato** (no al inquilino ni a la propiedad); la fotografía número 11 se rechaza con un mensaje. Formatos JPEG y PNG, hasta 5 MiB por archivo, con verificación del tipo real y cada archivo en su propia petición (RF-02). Antes de enviarla, el navegador reduce cada fotografía con la mecánica de RF-50, pero con un **lado mayor de 3508 px** y calidad inicial de **0,85** como punto de partida; el peso objetivo, los pasos de calidad y los valores definitivos se fijan al medir con fotos reales en la entrega E2 (DP-29). *Nota v1.14: el máximo de 10 y los valores de partida son decisiones del solicitante del 23-oct-2026 (opciones recomendadas por el asistente). El 10 no tiene fuente; los 3508 px (unos 300 ppp en una hoja A4) se apoyan en guías de OCR de escáneres leídas por resumen, que no son prueba para fotos con teléfono.* La fotografía del contrato es una imagen **distinta** de la de la cédula: el sistema no extrae ni recorta la cédula a partir de ella. Se guarda en un repositorio privado, sin URL pública, y solo la consulta la cuenta administradora autenticada (RNF-02). El sistema deberá registrar cada consulta o descarga (actor, fecha/hora, contrato), sin guardar la imagen. Su conservación y eliminación están pendientes (DP-28). Sin contrato vigente, la acción se muestra desactivada con el aviso «No hay contrato vigente» (decisión del solicitante del 23-oct-2026, que se tomó para el perfil de la propiedad; aplicarla a RF-52 por igual es propuesta del asistente). *Nota v1.11: la fotografía del contrato como documento nuevo es decisión del solicitante del 22-oct-2026. Son propuesta del asistente: que el contrato admita varias fotografías (páginas), la auditoría de la consulta (equivalente a RF-45) y que no se retenga ni se elimine con las reglas de RN-24 hasta DP-28.*

**RF-42 — Avisar vencimiento de contrato.** El sistema deberá notificar al administrador 120 días antes de la fecha de fin de un contrato. Si la fecha de fin pasa sin que el contrato se cierre o se renueve, el contrato pasará al estado *por decidir* y el sistema continuará generando obligaciones hasta que el administrador lo cierre o lo renueve. Mientras esté *por decidir*, el sistema mantendrá una **notificación web persistente** y una **línea en el resumen diario por correo** hasta que se cierre o se renueve. **[Legal OL-09]** *Nota v1.9 (revisión por módulos, 21-oct-2026): el recordatorio mientras el contrato está por decidir es decisión del solicitante.*

**RF-43 — Registrar saldo de apertura.** Para un contrato cuyo inicio es anterior a la fecha de carga en el sistema, el administrador deberá poder registrar un saldo de apertura con fecha y auditoría. El saldo de apertura debe incluir lo adeudado por todos los períodos iniciados hasta la fecha de apertura; las obligaciones regulares se generan desde el primer período que inicia después de esa fecha. Las alertas de atraso comienzan desde la fecha de carga y no retroactivamente (confirmado por el solicitante el 17-oct-2026; DP-25). La obligación de apertura no tiene período: su **fecha de vencimiento la digita el administrador** al registrarla (por defecto, la fecha de apertura más los días de gracia del contrato) y su fecha límite es esa misma fecha. Aparece en el calendario ese día y pasa a *vencida* al superarla. *Nota v1.9 (revisión por módulos, 21-oct-2026): decisión del solicitante; la regla RN-05 no aplica a una obligación sin período.*

## 5.3 Obligaciones y movimientos

**RF-11 — Generar obligaciones por período.** El sistema deberá generar la obligación de cada período 30 días antes de que inicie, mientras el contrato esté *futuro*, *vigente* o *por decidir*. Usará el monto, la moneda y la regla de vencimiento aplicables al período. El proceso es idempotente.

**RF-12 — Evitar duplicados.** El sistema deberá impedir más de una obligación por contrato y período, incluso si el proceso se ejecuta repetidamente o en paralelo.

**RF-13 — Registrar pago completo.** El administrador deberá poder registrar el pago que completa el saldo de una obligación como un movimiento por el saldo restante, con fecha real de recepción, medio de pago y observación opcional. No se exige comprobante adjunto. Al llegar el saldo a cero, la obligación pasa a *pagada* automáticamente.

**RF-14 — Determinar estado de obligación.** El sistema deberá derivar el estado de cada obligación a partir de su saldo, su fecha límite y la fecha local de la zona horaria de la organización: *pagada* si el saldo es cero; *vencida* si el saldo es mayor que cero y se superó la fecha límite de pago; *pendiente* en cualquier otro caso; *anulada* si fue anulada. **[Legal OL-01]**

**RF-15 — Consultar historial.** El sistema deberá permitir consultar obligaciones por inquilino, contrato, período y estado, mostrando importe exigible, vencimiento, saldo, estado y fecha de pago si existe.

**RF-16 — Anular movimiento.** El sistema deberá permitir anular un movimiento con motivo obligatorio. El movimiento original se conserva y se agrega una reversión. Se recalculan saldo y estado; si la obligación vuelve a *vencida*, las alertas se reanudan el día siguiente. Los recordatorios ya emitidos no se reenvían. Una corrección de importe o de fecha se realiza anulando el movimiento y registrando uno nuevo. **[Legal OL-04]**

**RF-34 — Registrar abono de alquiler.** El administrador deberá poder registrar uno o varios abonos asociados a una obligación, con importe positivo, fecha real de recepción, medio de pago (efectivo, transferencia, cheque u otro) y observación opcional. La fecha real no puede ser futura (según la zona de la organización) ni anterior a la fecha de inicio del contrato. El sistema conserva la fecha real y la fecha/hora de registro. Un abono no puede dejar saldo negativo: si excede el saldo de la obligación, se **rechaza** (el sistema no reparte un pago entre obligaciones ni guarda saldo a favor) y el administrador registra un abono por cada obligación; el mensaje de rechazo sugiere registrar el resto como abono de la obligación siguiente (RN-15). Para un cheque o título, la fecha real es la de recepción del efectivo. Cada envío lleva una clave de solicitud única: si el mismo envío se repite (doble clic o reintento), el sistema no crea otro movimiento y devuelve el ya registrado. **[Legal OL-04]**

**RF-35 — Calcular saldo de alquiler.** El sistema deberá calcular el saldo pendiente como importe exigible menos la suma de los movimientos válidos (no anulados). El saldo nunca es negativo.

**RF-37 — Emitir comprobante de pago (fase posterior; fuera de la v1 por decisión del solicitante del 21-oct-2026, HT-02).** En la v1 el recibo es de papel, hecho fuera del sistema (RF-47). Este requisito se conserva sin cambios de fondo para cuando se integre el comprobante del sistema. El sistema deberá generar, por cada abono o pago, un comprobante numerado de forma consecutiva y sin huecos (la numeración no puede depender de un mecanismo que pierda números al fallar una operación), imprimible y reimprimible, con contrato, inquilino, período, importe, moneda, fecha real, medio de pago y saldo resultante, y deberá conservar copia. Los comprobantes de movimientos anulados quedan marcados y no se renumeran. **[Legal OL-03]** *Nota: el solicitante difirió este requisito en la respuesta Q-17; se incluye por la instrucción de incorporar todas las obligaciones legales. El art. 58 admite otros procedimientos fehacientes de acreditación; confirmar con abogado (DP-20) y, si se difiere, registrar el riesgo.*

**RF-38 — Registrar pago en moneda distinta.** Cuando el pago se reciba en una moneda distinta de la del contrato, el sistema deberá registrar la moneda recibida, el tipo de cambio ingresado manualmente por el administrador (expresado en colones por dólar) y el importe equivalente en la moneda del contrato. El **sistema calcula** el equivalente con aritmética decimal exacta (multiplica por el tipo de cambio al pasar de dólares a colones y divide al pasar de colones a dólares), lo redondea a dos decimales con empate hacia arriba (`ROUND_HALF_UP`), lo muestra antes de guardar y conserva el cálculo. El saldo se mantiene en la moneda del contrato. *Nota v1.9 (revisión por módulos, 21-oct-2026): regla de cálculo y redondeo por decisión del solicitante; en la v1.8 no se decía quién calculaba el equivalente ni cómo se redondeaba.* El sistema no consulta tipos de cambio. **[Legal OL-05]**

**RF-47 — Anotar el número del recibo físico.** El sistema deberá permitir anotar en cada movimiento de abono, de forma opcional, el número del recibo de papel entregado al inquilino fuera del sistema. El número es un texto único entre todos los movimientos cuando se llena. El administrador conserva la copia en papel. El sistema no valida el formato, no genera ni numera el recibo y no marca el papel como anulado cuando se anula el movimiento. **[Legal OL-03]** *Nota v1.9: requisito nuevo, derivado de la decisión del solicitante del 21-oct-2026 (HT-02); el campo es propuesta del asistente, aceptada. Riesgos asumidos: numeración a mano y posibles errores, papel sin marca de anulado y sin copia electrónica. Si el recibo de papel basta frente al art. 58 y si Hacienda exige factura electrónica quedan con el abogado o contador (DP-20).*

## 5.4 Calendario

**RF-17 — Mostrar calendario mensual.** El sistema deberá mostrar las obligaciones en un calendario mensual e identificar inquilino, fecha de vencimiento y estado. Además muestra, como eventos **informativos** (sin recordatorios ni alertas), la fecha de fin de cada contrato y la fecha límite acordada del depósito cuando exista. *Nota v1.9 (revisión por módulos, 21-oct-2026): eventos añadidos por decisión del solicitante.*

**RF-18 — Filtrar por inquilino o por propiedad.** El administrador deberá poder filtrar el calendario por inquilino o por propiedad (por su alias) y quitar el filtro conservando el mes consultado. *Nota v1.9 (revisión por módulos, 21-oct-2026): el filtro por propiedad se añade por decisión del solicitante; el ID no cambia.*

**RF-19 — Filtrar por estado.** El sistema deberá permitir filtrar por pendiente, vencida, pagada y anulada. Las anuladas no se muestran por defecto.

**RF-20 — Consultar detalle de evento.** Al seleccionar un evento, el sistema deberá mostrar contrato, período, importe exigible, vencimiento, fecha límite, saldo, estado, movimientos y observación.

## 5.5 Notificaciones

**RF-21 — Configurar recordatorios anticipados.** El administrador deberá poder configurar la anticipación del recordatorio en días antes del vencimiento (3 por defecto) y añadir hasta tres anticipaciones. Un cambio se aplica a las notificaciones futuras aún no procesadas, las reprograma y no genera duplicados. Si la obligación tiene abonos, el recordatorio indica el saldo pendiente. Los recordatorios del día se envían por correo **dentro del resumen diario** (RF-23), no como correos individuales; cada uno conserva su notificación web. *Nota v1.9 (revisión por módulos, 21-oct-2026): decisión del solicitante.*

**RF-22 — Generar alertas diarias de atraso.** El proceso diario deberá registrar una alerta por cada obligación *vencida* y por día. Las alertas se detienen cuando la obligación pasa a *pagada* o *anulada*. Si el proceso no se ejecutó algún día, solo se emite la alerta del día actual.

**RF-23 — Notificar por canales aprobados.** El sistema deberá admitir notificaciones web persistentes (estados nueva, leída y archivada, sin borrado) y envío de **correo al administrador**. Los correos de recordatorio y de atraso se envían en un **único resumen diario** con tres secciones: los recordatorios del día, las obligaciones vencidas y los contratos *por decidir* (RF-42); se envía si hay al menos un elemento. El sistema no declarará entregado un correo que solo fue aceptado por el servicio de envío. WhatsApp queda para una versión futura (DP-04). *Nota v1.9: cambio de alcance por decisión del solicitante del 21-oct-2026 (HT-01); la v1.8 exigía WhatsApp.*

**RF-24 — Registrar intentos de notificación.** El sistema deberá conservar obligación asociada, canal, destinatario, fecha programada, fecha de intento, resultado, intentos y los identificadores y estados que exponga el servicio de envío. Ante un fallo de envío, hará hasta cinco intentos con espera creciente y aleatoria; después, el resultado es *fallido* y la notificación web persiste. La v1 no recibe estados de entrega posteriores a la aceptación.

**RF-25 — Cancelar notificaciones futuras.** Cuando una obligación pase a *pagada* o *anulada*, el sistema deberá cancelar sus recordatorios y alertas futuros. Las notificaciones anteriores permanecen en el historial.

**RF-44 — Minimizar datos en mensajes externos.** Los mensajes enviados por correo (y, en el futuro, por WhatsApp) no deberán incluir número de documento ni imagen alguna, y deberán limitar los datos del inquilino al mínimo necesario (por ejemplo, el alias de la propiedad y el importe). El destinatario es el administrador: en el correo, su dirección; en WhatsApp, cuando exista, su teléfono, con la aceptación de recibir mensajes registrada y plantillas aprobadas. **[Legal OL-17]** *Nota v1.9 (propuesta): extender estos límites al correo; OL-17 y la redacción original trataban WhatsApp y la validez de su aplicación al correo debe confirmarla el abogado (DP-17).*

## 5.6 Acceso y auditoría

**RF-26 — Autenticar administrador.** El sistema deberá requerir autenticación multifactor antes de permitir acceso a funciones administrativas y documentos privados.

**RF-27 — Administrar la cuenta.** La primera versión opera con una única cuenta administradora, con:
- contraseña de al menos 15 caracteres, sin reglas de composición ni cambio periódico obligatorio;
- un segundo factor de código de un solo uso (TOTP) obligatorio;
- sesión con cierre total a las 24 horas y por inactividad de 1 hora;
- **10 códigos de recuperación** de un solo uso, entregados (y mostrados una sola vez) al activar el segundo factor y guardados con hash; emitir códigos nuevos exige la contraseña actual e invalida los anteriores; un código TOTP ya aceptado no se reutiliza y se tolera una diferencia de reloj de un intervalo de 30 segundos a cada lado (cifras propuestas por el asistente y aceptadas por el solicitante el 21-oct-2026; OWASP no las fija);
- **límite de intentos fallidos** por cuenta, compartido por la contraseña, el TOTP y los códigos de recuperación: tras 5 fallos seguidos hay una espera de 1 minuto que se duplica con cada fallo adicional hasta un máximo de 1 hora, sin bloqueo permanente; un inicio de sesión correcto reinicia el contador y el restablecimiento de contraseña sigue disponible (cifras propuestas por el asistente);
- **creación y rescate por el servidor:** la cuenta se crea con un comando de gestión ejecutado por el solicitante en el servidor y el segundo factor se activa en el primer ingreso; si se pierden el TOTP y los códigos, otro comando desactiva el segundo factor y obliga a registrarlo de nuevo, deja constancia en la auditoría y avisa a las dos direcciones; no hay pantalla pública de alta ni de rescate;
- aviso de seguridad por correo, a dos direcciones del propio solicitante, en proveedores de correo distintos (decisión del 21-oct-2026; ninguna es de un tercero), ante: el uso de un código de recuperación, la emisión de nuevos códigos, el registro o reemplazo del segundo factor, el cambio o restablecimiento de la contraseña, el cambio de una dirección de correo, llegar a cinco intentos fallidos seguidos y el rescate por el servidor. El aviso dice qué ocurrió, la fecha y hora local y qué hacer si no fue el administrador, y **no** lleva códigos, contraseñas ni enlaces de acceso. Si el envío falla, la operación **procede**: el aviso se guarda con el evento, se reintenta hasta cinco veces con espera creciente y aleatoria, y si sigue fallando queda como *fallido*, con una alerta persistente en cada inicio de sesión y un registro de auditoría (ADR-026);
- cambio de contraseña con la sesión iniciada: exige la contraseña actual;
- reemplazo del segundo factor con la sesión iniciada: exige la contraseña actual (decisión del solicitante del 21-oct-2026, contra la recomendación de exigir además un factor ya registrado; añadir el TOTP queda para el futuro);
- cambio de una de las dos direcciones de correo (con la sesión iniciada): exige la contraseña actual y la **confirmación en la dirección nueva** (enlace de un solo uso, válido 15 minutos); mientras no se confirme, sigue vigente la dirección anterior; el aviso de seguridad va a las dos direcciones anteriores. Decisión del solicitante del 21-oct-2026 (revisión por módulos), contra la recomendación de exigir además el código del segundo factor: una sesión robada con la contraseña podría cambiar la dirección si controla también la nueva;
- restablecimiento de la contraseña olvidada (sin sesión): un enlace enviado por correo **solo a la dirección del administrador**, de un solo uso y válido 15 minutos (el valor es propuesta del asistente, aceptada). El enlace solo permite fijar una contraseña nueva y no inicia sesión: el acceso sigue exigiendo el segundo factor (RF-26).

*Nota v1.9: el cambio de contraseña y de segundo factor y el restablecimiento por correo son decisiones del solicitante del 21-oct-2026 (HT-08); las dos primeras y el restablecimiento por correo van contra la recomendación. Riesgos asumidos: una sesión secuestrada con la contraseña puede reemplazar el segundo factor, y el correo del administrador pasa a ser llave de restablecimiento y depende del servicio de correo y del dominio. Las dos direcciones son del solicitante y no constan en los documentos, solo en la configuración del servidor. Protecciones adoptadas por el solicitante el 21-oct-2026, siguiendo la recomendación: respuesta y tiempo de respuesta idénticos exista o no la cuenta; al fijar la contraseña nueva se invalidan los demás enlaces pendientes y se cierran las sesiones abiertas (el cierre automático es propuesta del asistente); y un máximo de 3 solicitudes de restablecimiento por hora para la cuenta (el número es propuesta del asistente). Fuente: OWASP, Forgot Password Cheat Sheet (leída por resumen el 21-oct-2026), que no fija la duración ni el límite numérico.*

**RF-28 — Auditar operaciones críticas.** El sistema deberá registrar cambios relevantes en inquilinos, contratos, obligaciones, movimientos, anulaciones, depósitos y configuración de notificaciones, con actor, fecha/hora de registro, operación, campos modificados y valores anteriores y nuevos de los campos **no personales** (estados, importes, fechas, motivos). Para los campos personales (nombre, número de documento, teléfono, correo, imagen de cédula) solo registrará **que cambiaron**, nunca su valor. No almacenará secretos ni documentos completos. Así la auditoría no retiene datos que RF-41 manda desasociar. Cuando la operación la hace el proceso diario y no el administrador, el actor es el **sistema** (tipo de actor: proceso) y el registro incluye la ejecución que lo originó (decisión del solicitante del 21-oct-2026, HT-06; no se crea otra cuenta). Registra también los **eventos de autenticación y de seguridad de la cuenta**: inicios de sesión correctos y fallidos, cierres de sesión y los siete eventos de RF-27, con la dirección IP de origen y sin contraseñas, códigos ni tokens. El administrador puede **consultar la auditoría** en una pantalla de solo lectura con filtros por fecha, tipo de evento, entidad y actor; esa consulta no se audita. La auditoría **no se borra automáticamente** en la v1 (la aplicación no puede borrarla, ADR-027); su plazo de conservación se define con DP-18. *Nota v1.9 (revisión por módulos, 21-oct-2026): eventos de autenticación, consulta y conservación por decisión del solicitante.* **[Legal OL-14]** *Nota: reescritura de la versión 1.6 (que pedía valores anteriores y nuevos sin distinguir); el efecto sobre la conservación de la auditoría se valida con abogado (DP-18).*

**RF-45 — Auditar acceso a cédulas y exportaciones del titular.** El sistema deberá registrar cada consulta o descarga de una fotografía de cédula y cada exportación de los datos de un titular (RF-40) (actor, fecha/hora, inquilino), sin guardar la imagen ni el contenido de la exportación en el registro. No se auditan las lecturas ordinarias de fichas, saldos o calendario. **[Legal OL-16]** *Nota v1.9: la exportación se añade por decisión del solicitante del 21-oct-2026 (HT-03 y auditoría de lecturas); el título cambió, el ID no.*

**RF-46 — Gestionar incidentes de seguridad.** El sistema deberá permitir registrar un incidente de seguridad (fecha y hora en que ocurrió y en que se conoció, naturaleza, datos comprometidos, acciones inmediatas, titulares afectados), calcular la fecha límite de aviso a los titulares y a la Agencia de cinco días hábiles y dejar constancia de cada aviso emitido y de la revisión posterior. El sistema no detecta el incidente: lo registra el administrador. **[Legal OL-19]** *Lectura propia del Reglamento 37554-JP, arts. 38 y 39; el momento desde el que corre el plazo y la obligación de avisar a la Agencia se validan con abogado (DP-17).*

## 5.7 Depósito de garantía

**RF-29 — Definir depósito de garantía.** El sistema deberá permitir registrar en el contrato el importe total del depósito y una fecha límite acordada opcional, junto con notas. **La moneda del depósito es siempre la del contrato.** Un contrato tiene como máximo un depósito. El importe total solo se edita si no hay abonos, o mediante corrección auditada nunca inferior a lo abonado. **[Legal OL-11, OL-12]** Deberá advertir, sin bloquear, cuando el importe supere una mensualidad de renta **en un contrato de vivienda** (no se advierte en otros destinos, S-02). *Nota v1.9 (revisión por módulos, 21-oct-2026): moneda única y advertencia solo para vivienda, por decisión del solicitante.*

**RF-30 — Registrar abonos al depósito.** El administrador deberá poder registrar abonos con importe, fecha real de recepción, medio de pago y observación opcional. El sistema bloquea importes nulos o negativos y abonos que superen el saldo. El flujo ordinario admite hasta tres abonos no anulados; para registrar más, el administrador confirma explícitamente una excepción con **motivo obligatorio**, que queda auditada. La moneda del abono debe ser la del depósito (la del contrato), salvo lo previsto en RF-38.

**RF-31 — Calcular saldo del depósito.** El sistema deberá calcular el saldo como importe total menos la suma de abonos válidos, y mostrar el estado pendiente, parcialmente pagado o completado.

**RF-32 — Consultar historial del depósito.** El sistema deberá mostrar importe acordado, abonos, fechas, observaciones, saldo, anulaciones y auditoría. Cuando el contrato esté finalizado, mostrará la etiqueta "contrato cerrado, liquidación manual". El depósito no genera recordatorios ni alertas en esta versión.

## 5.8 Configuración regional

**RF-33 — Configurar moneda y zona horaria.** El sistema deberá ofrecer CRC y `America/Costa_Rica` como valores predeterminados y admitir USD como segunda moneda por contrato. La zona horaria se configura solo a nivel de organización. Los vencimientos son fechas de calendario sin hora; las marcas de registro se almacenan en UTC y se presentan en la zona de la organización.

## 5.9 Datos personales

**RF-39 — Informar y registrar consentimiento.** Antes de guardar datos personales o la fotografía de cédula, el sistema deberá presentar al administrador el texto informativo con los ocho puntos del art. 5 de la Ley 8968 y registrar el consentimiento del inquilino (fecha, versión del texto y medio, físico o electrónico). El sistema deberá permitir registrar la revocación sin efecto retroactivo. Cada versión del texto informativo se **conserva** en el sistema y el consentimiento apunta a la versión mostrada. Al registrar una revocación, el sistema muestra un aviso en la ficha del inquilino, **no permite crear contratos nuevos** con él y **abre de oficio una solicitud de supresión** (RF-40) con la fecha de la revocación como recepción; la revocación no borra datos por sí sola. *Nota v1.9 (revisión por módulos, 21-oct-2026): conservación del texto y efecto de la revocación por decisión del solicitante; interpretación del proyecto, validada por abogado según el solicitante, sin dictamen aportado.* **[Legal OL-13]**

**RF-40 — Atender solicitudes del titular.** El sistema deberá permitir registrar solicitudes de acceso, rectificación, actualización o supresión de un titular, con fecha de recepción y fecha límite de cinco días hábiles, y marcar su resolución. Deberá poder exportar **todo el registro del titular, incluida la fotografía de la cédula**, como un informe web imprimible, completo, claro y sin codificaciones, con la finalidad y el uso de los datos y la explicación de los términos técnicos, y sin datos de terceros. La atención es gratuita. *Nota v1.9: alcance y formato por decisión del solicitante del 21-oct-2026 (HT-03), como propuesta hasta que el abogado valide el alcance, la foto de la cédula y qué cuenta como dato de tercero (DP-17); lectura propia de la Ley 8968, art. 7.1.* Una solicitud de supresión se atiende salvo que exista una obligación legal de conservar el dato (DP-18). Para atenderla, el administrador dispone de la operación **desasociar a petición**: elimina las fotografías, anula nombre, número de documento, teléfono y correo, marca la desasociación (como en RF-41) y conserva los movimientos sin identificación, la solicitud y la auditoría. Se **bloquea** si el inquilino tiene un contrato vigente, futuro o por decidir, o saldos pendientes (como RF-04); entonces la solicitud se resuelve como *denegada* con un motivo escrito. **[Legal OL-15]**

**RF-41 — Retener y eliminar datos personales.** El sistema deberá conservar la fotografía de cédula mientras el contrato esté vigente y hasta cinco años después del fin del último contrato del inquilino (plazo configurable, nunca superior a diez años desde los hechos). Vencido el plazo, el sistema deberá eliminar la fotografía y desasociar los datos personales del inquilino, conservando los movimientos financieros sin datos de identificación. Deberá avisar al administrador antes de ejecutar la eliminación. Si el inquilino **no tiene ningún contrato o todos están anulados**, no hay fin de contrato: el plazo es **corto y configurable (propuesta de 1 año)** y corre desde el registro del inquilino o desde la última anulación, el posterior; con el mismo aviso previo. *Nota v1.9 (revisión por módulos, 21-oct-2026): decisión del solicitante; el valor de un año es propuesta del asistente, sin fuente.* **[Legal OL-14]**

# 6. Reglas de negocio

| ID | Regla |
|---|---|
| RN-01 | Cada contrato corresponde a un único inquilino y una única propiedad. |
| RN-02 | Una propiedad no puede tener dos contratos que compartan algún día. Cada contrato ocupa el intervalo `[fecha_inicio, fecha_fin]` con ambas fechas inclusive; sin fecha de fin es abierto. El relevo exige que el nuevo inicio sea al menos el día siguiente al fin anterior. Un contrato **anulado** no cuenta para el solape (decisión del solicitante del 21-oct-2026; regla de negocio, no validada por abogado). |
| RN-03 | Un período de alquiler va desde un día X hasta el día anterior al mismo día X del mes siguiente. El día X es el día de `fecha_inicio`; si el mes no tiene ese día, el período inicia el último día de ese mes. Ejemplo: inicio el 10 de enero; período 1: 10 ene–9 feb; período 2: 10 feb–9 mar. El día 10 de febrero pertenece al segundo período. **[OL-01, OL-10]** |
| RN-04 | Se genera una sola obligación por contrato y período. |
| RN-05 | El vencimiento de una obligación es la fecha del `día de vencimiento` en el mes en que inicia el período (o el último día de ese mes si no existe); si esa fecha es anterior al inicio del período, se usa el mes siguiente; si esa fecha excede el último día del período, se usa el último día del período. Así el vencimiento siempre cae dentro del período. Confirmada por el solicitante (DP-24); el día de vencimiento por defecto es el día de inicio del período. |
| RN-06 | La fecha límite de pago es el vencimiento más los días de gracia del contrato (7 por defecto; el art. 58 no distingue destino en el texto leído). En la obligación de apertura, la fecha límite es la misma fecha de vencimiento digitada (RF-43). **[OL-01]** |
| RN-07 | Una obligación está *vencida* cuando su saldo es mayor que cero y la fecha local supera la fecha límite de pago; está *pendiente* si su saldo es mayor que cero y no la ha superado. Los recordatorios se anclan al vencimiento. **[OL-01]** |
| RN-08 | Una obligación *pagada* o *anulada* no genera recordatorios ni alertas. |
| RN-09 | Aceptar un pago tardío no modifica el día de vencimiento ni el período pactados. **[OL-02]** |
| RN-10 | Desactivar un inquilino o finalizar un contrato no elimina su historial financiero. La eliminación de datos personales se rige por RF-41 y RN-24. |
| RN-11 | La recepción se confirma manualmente por el administrador mediante movimientos. El vencimiento o una notificación no prueban el pago. Un pago con cheque o título solo descarga la obligación con el recibo del efectivo. **[OL-04]** |
| RN-12 | Los períodos completos no se prorratean. Solo el último período, cuando `fecha_fin` cae dentro de él, se prorratea por días: `importe = importe mensual × días cobrables / días del período`, con ambos extremos inclusivos, calculado con aritmética decimal exacta y redondeado una sola vez al final a la unidad monetaria entera con empate hacia arriba (`ROUND_HALF_UP`) para CRC y a dos decimales para USD. Debe quedar registrado el cálculo y puede ajustarse manualmente con motivo y auditoría. **[OL-10]** |
| RN-13 | Cada obligación conserva período, importe final, vencimiento y datos para reconstruir la regla de cálculo. |
| RN-14 | Un reajuste de vivienda rige desde el período de pago siguiente a la notificación y no puede exceder el tope legal informado; una vivienda con precio en moneda extranjera no se reajusta. Una corrección es retroactiva con motivo. **[OL-06, OL-07]** |
| RN-15 | El sistema no genera obligaciones de períodos que inicien a más de 30 días, y no acepta movimientos sobre obligaciones cuyo período aún no ha iniciado salvo la del período inmediato siguiente, de modo que no se admite pago anticipado de más de una mensualidad. Las obligaciones de períodos pasados con saldo siguen aceptando movimientos. **[OL-11]** |
| RN-16 | La vigencia de un contrato con fecha de fin que expira sin acción pasa a *por decidir*; el sistema no deja de generar obligaciones en silencio. El inquilino puede terminar el contrato con tres meses de aviso salvo pacto escrito. **[OL-09]** |
| RN-17 | Al finalizar un contrato, las obligaciones cuyo período inicia después de la fecha de fin y no tienen movimientos válidos se anulan; la obligación del período que contiene la fecha de fin se conserva con su importe prorrateado. Solo se puede anular una obligación sin movimientos válidos; la anulación requiere motivo. |
| RN-18 | Un saldo nunca es negativo. Un abono que lo exceda se rechaza. |
| RN-19 | El depósito de garantía es independiente de las obligaciones de alquiler. Un abono al depósito no modifica el saldo ni el estado de ninguna obligación. |
| RN-20 | El saldo del depósito es el importe total menos la suma de abonos válidos. |
| RN-21 | Un abono de alquiler no se considera pagada la obligación mientras exista saldo pendiente. |
| RN-22 | Un movimiento anulado no se borra; se conserva con su reversión. Un movimiento *válido* es el no anulado. |
| RN-23 | Las monedas admitidas son CRC y USD por contrato. No se mezclan importes de monedas distintas en sumas. El pago en otra moneda usa un tipo de cambio ingresado manualmente. **[OL-05]** |
| RN-24 | Los datos personales se conservan solo mientras sean pertinentes; el plazo ordinario de la fotografía de cédula es de cinco años tras el fin del contrato y en ningún caso se conservan datos que puedan afectar al titular pasados diez años desde los hechos, salvo norma especial. **[OL-14]** |
| RN-25 | La primera versión tiene una única cuenta administradora; no existen roles adicionales. La cuenta se crea y se rescata solo desde el servidor (RF-27). |
| RN-26 | Un depósito superior a una mensualidad en un contrato de vivienda genera una advertencia; la garantía debe responder por alquileres y demás obligaciones del contrato. **[OL-11, OL-12]** |
| RN-27 | Un depósito tiene como máximo tres abonos no anulados en el flujo ordinario; más abonos requieren confirmación con motivo. |
| RN-28 | El cambio de inquilino cierra el contrato anterior y crea uno nuevo. |
| RN-29 | La fecha real de recepción no puede ser futura ni anterior al inicio del contrato; el sistema conserva siempre la fecha/hora de registro y no exige observación solo por ser retroactiva. |
| RN-30 | El estado de contrato se deriva de las fechas: *futuro*, *vigente*, *por decidir*, *finalizado* o *anulado*. |

## 6.1 Ejemplos

**Vencimiento.** Contrato con inicio el 10 de enero y día de vencimiento 31: períodos 10 ene–9 feb, 10 feb–9 mar y 10 mar–9 abr; vencimientos 31 de enero, 28 de febrero (29 en año bisiesto) y 31 de marzo.

**Fecha límite.** Vencimiento el 5 de febrero con 7 días de gracia: la fecha límite es el 12 de febrero y la obligación pasa a *vencida* el 13 de febrero.

**Último período.** Período 10 mar–9 abr (31 días), importe ₡180.000, contrato que termina el 25 de marzo: días cobrables del 10 al 25 = 16; 180.000 × 16 / 31 = 92.903,22…; importe final ₡92.903.

# 7. Modelo de información conceptual

## 7.1 Entidades

| Entidad | Atributos conceptuales principales |
|---|---|
| Inquilino | id, nombre, tipo y número de documento, teléfono, correo, referencias privadas a las fotografías, estado, consentimiento (fecha, versión con el texto mostrado, medio, revocación), fechas de creación y modificación. |
| Propiedad | id, alias (obligatorio y único), descripción, dirección, marca de inactiva. |
| Contrato | id, inquilino_id, propiedad_id, destino, fecha_inicio, fecha_fin opcional, moneda, anulación (fecha y motivo). El monto, el día de vencimiento y los días de gracia viven en la Condición del contrato. |
| Documento del contrato | id, contrato_id, referencia privada al archivo, número de orden dentro del contrato, fecha de carga. Una fotografía por registro (propuesta). |
| Condición del contrato | id, contrato_id, monto_mensual, día_vencimiento, días_gracia, fecha efectiva, tipo (inicial, reajuste, corrección), fecha de notificación, porcentaje, tope digitado y fuente (reajustes de vivienda), motivo (correcciones), fecha de registro. Conserva el historial exigido por RF-10. |
| Obligación | id, contrato_id, período (inicio, fin), fecha_vencimiento, fecha_límite, importe_inicial, moneda, condición aplicada, datos del cálculo, anulación (motivo, fecha) y tipo (regular, apertura). El importe exigible vigente se deriva del importe inicial y sus ajustes. |
| Ajuste de obligación | id, obligacion_id, tipo (reajuste, corrección, prorrateo del último período, ajuste manual), importe con signo, condición que lo originó, motivo, fecha de registro. Inmutable. |
| Movimiento | id, tipo (abono de alquiler, abono de depósito, reversión), obligación o depósito asociado, importe, moneda recibida, tipo de cambio y equivalente cuando aplique, fecha real, fecha/hora de registro, medio de pago, observación, clave de solicitud, anulación (motivo, referencia al movimiento original), número de recibo físico (opcional, único), comprobante (fase posterior). |
| Organización | id, nombre y dirección del responsable de la base de datos, zona horaria, hora del proceso diario, correo del administrador y segunda dirección de avisos de seguridad, teléfono y aceptación de WhatsApp del administrador (futuro), anticipaciones de recordatorio, años de retención de fotografías, plazo de retención sin contrato (1 año por defecto), días de gracia por defecto. Una sola fila en v1. |
| Comprobante (fase posterior, RF-37) | id, número consecutivo, movimiento_id, contenido, estado (vigente, anulado). No existe en la v1. |
| Depósito de garantía | id, contrato_id, importe_total, fecha límite acordada opcional, notas. La moneda es la del contrato. |
| Notificación | id, obligación o contrato (ninguno en los avisos de seguridad), canal (web o correo), tipo (recordatorio, alerta de atraso, vencimiento o contrato por decidir, aviso de seguridad, proceso diario fallido), destinatario, fecha programada, intentos, resultado, referencia del servicio de envío, estado web (nueva, leída, archivada). |
| Solicitud del titular | id, inquilino_id, tipo, fecha de recepción, fecha límite, resolución. |
| Auditoría | id, entidad, registro, actor, acción, fecha, campos modificados y valores anteriores y nuevos solo de campos no personales. |
| Incidente de seguridad | id, fecha de ocurrencia y de conocimiento, naturaleza, datos comprometidos (descripción, sin copiarlos), acciones inmediatas, fecha límite de aviso, estado. Cada aviso emitido (a un titular o a la Agencia) se guarda con fecha, destinatario y contenido mínimo. |

El saldo de una obligación y el de un depósito, el estado de una obligación, de un contrato y de una propiedad **se derivan** y no se almacenan como fuente de verdad.

## 7.2 Relaciones

- Un inquilino puede tener varios contratos a lo largo del tiempo.
- Cada contrato referencia exactamente un inquilino y una propiedad.
- Un contrato tiene muchas obligaciones y, cuando corresponda, un depósito.
- Una obligación tiene muchos movimientos; un depósito tiene muchos movimientos.
- Un movimiento tiene como máximo un comprobante (fase posterior) y como máximo un número de recibo físico.
- Las operaciones relevantes producen registros de auditoría.

## 7.3 Restricciones de integridad

1. Identificadores únicos en todas las entidades.
2. Claves foráneas válidas entre contrato, inquilino y propiedad.
3. Monto mensual mayor que cero; día de vencimiento entre 1 y 31.
4. Unicidad de contrato y período en obligaciones.
5. Ausencia de días compartidos entre contratos de una propiedad.
6. Los movimientos no se borran ni se editan; se anulan.
7. Numeración de comprobantes única, consecutiva y sin huecos, asignada en la misma transacción que el movimiento (fase posterior, RF-37). El número de recibo físico, si se anota, es único (RF-47).
8. El estado financiero no se infiere de una notificación.
9. Las fotografías de cédula se almacenan en un repositorio privado; la base guarda una referencia protegida, no una URL pública.
10. La información sensible no aparece en registros técnicos ni mensajes de error.
11. Cada obligación y depósito conserva su moneda; la conversión es solo la registrada manualmente en un movimiento.
12. Una fecha real de recepción no puede ser futura ni anterior al inicio del contrato.
13. Los ajustes de obligación son inmutables y nunca dejan el importe vigente por debajo de lo abonado.
14. La clave de solicitud de un movimiento es única; un reintento no crea otro movimiento.
15. La auditoría no almacena valores de campos personales ni secretos.

# 8. Requisitos no funcionales

| ID | Categoría | Requisito verificable |
|---|---|---|
| RNF-01 | Autenticación | Todas las funciones administrativas requieren sesión autenticada con segundo factor. Solo existe una cuenta administradora. |
| RNF-02 | Autorización | Solo la cuenta administradora autenticada puede consultar cédulas, modificar contratos, registrar movimientos o cambiar la configuración. |
| RNF-03 | Privacidad | Los datos personales y documentos se protegen en tránsito y mediante controles de acceso. Los archivos no son públicos. |
| RNF-04 | Integridad | La generación de obligaciones es idempotente y tiene restricción de unicidad por contrato y período. |
| RNF-05 | Confiabilidad | Un fallo del servicio de correo (o, en el futuro, de WhatsApp) no impide consultar ni registrar movimientos ni elimina la notificación web persistida. |
| RNF-06 | Trazabilidad | Los cambios relevantes de contrato, movimientos y configuración quedan auditados. |
| RNF-07 | Usabilidad | Los formularios validan entradas y muestran mensajes comprensibles. |
| RNF-08 | Rendimiento | Las consultas habituales (listados, calendario mensual, ficha) responden en menos de 2 s en el percentil 95, con hasta 50 propiedades y un administrador. Objetivo a validar, no medición. |
| RNF-09 | Recuperación | Un respaldo completo al día (pérdida tolerable de datos, RPO, de hasta 24 horas); recuperación del servicio (RTO) en hasta 24 horas; retención de respaldos de 35 días; prueba de restauración antes de producción y cada 3 meses, que abarque base de datos, archivos, contratos, movimientos, comprobantes y fotografías. Los respaldos se copian a otro lugar, cifrados. Valores de diseño elegidos por el solicitante (DP-07, 17-oct-2026), sin fuente externa. |
| RNF-10 | Compatibilidad | La interfaz funciona en las dos últimas versiones mayores de Chrome, Edge, Firefox y Safari, en escritorio y móvil. |
| RNF-11 | Mantenibilidad | Las responsabilidades de inquilinos, contratos, obligaciones, movimientos, calendario y notificaciones se mantienen separadas conceptualmente. |
| RNF-12 | Configuración regional | Fechas dd/mm/aaaa; números con punto de miles y coma decimal, con el símbolo de la moneda delante (₡180.000,50) y porcentajes con coma (3,2 %), formato propio sin depender del idioma por defecto de la plataforma (decisión del solicitante del 21-oct-2026); moneda por contrato; fechas y tareas programadas interpretadas en la zona de la organización. Las tareas programadas se guardan como fecha y hora locales con la zona, y el instante se calcula al ejecutar (DP-26). |
| RNF-13 | Protección de datos | El sistema registra el consentimiento, atiende solicitudes del titular y aplica la retención de las secciones 5.9 y 3.2. **[OL-13 a OL-15]** |
| RNF-14 | Seguridad de los datos | Se aplican medidas técnicas y de organización que impidan alteración, pérdida, tratamiento o acceso no autorizado: cifrado en tránsito y, cuando la infraestructura lo permita, en reposo; almacenamiento privado; nombres de archivo aleatorios; límites de tamaño y formato; validación del tipo real. El historial de pagos puede considerarse dato sensible por su relación con la condición socioeconómica; su tratamiento se valida legalmente (DP-19). **[OL-16, OL-18]** |
| RNF-15 | Confidencialidad | Quien intervenga en el tratamiento de datos personales mantiene confidencialidad aun después de terminada su relación con el sistema. **[OL-16]** |
| RNF-16 | Idempotencia de procesos | Todos los procesos programados pueden reejecutarse sin producir duplicados ni efectos adicionales. |
| RNF-17 | Zona horaria y moneda | Los registros históricos no cambian al modificar la configuración regional; las marcas temporales se almacenan en UTC; las monedas se calculan con aritmética decimal exacta. |
| RNF-18 | Documentación de seguridad | Debe existir y mantenerse actualizado un documento de seguridad con descripción de los datos tratados, inventario de infraestructura, análisis de riesgos, medidas aplicadas, riesgo residual y plan de trabajo, revisado al menos una vez al año y ante cambios de plataforma o vulneraciones, y un protocolo mínimo de actuación. Es un entregable de la fase 6, no una función del sistema. **[OL-20, OL-21]** |

Los valores de rendimiento son objetivos propuestos, no resultados medidos.

# 9. Criterios de aceptación

Los criterios se formulan para ejecutarse como pruebas funcionales o revisiones de aceptación.

## Inquilinos y datos personales

**CA-01 — Registro de inquilino.** *Dado* un administrador autenticado, *cuando* registra los campos obligatorios (nombre completo, tipo y número de documento) y el consentimiento, *entonces* se guarda el inquilino con identificador único, aunque todavía no tenga fotografía (v1.12; el frente se exige antes de asignar un contrato, ver CA-78). Si falta un campo obligatorio o el consentimiento, se muestra el error y no se guarda el registro. Un inquilino sin teléfono ni correo se guarda sin error.

**CA-25 — Documento duplicado.** *Dado* un inquilino activo con tipo y número de documento, *cuando* se intenta registrar otro con los mismos valores, *entonces* el sistema advierte del duplicado antes de guardar.

**CA-73 — Reducción de la fotografía en el navegador (RF-50).** *Dado* un administrador que selecciona una fotografía de 4032 × 3024 píxeles y 6 MB (ejemplo), *cuando* el navegador la reduce antes de enviarla, *entonces* lo enviado es un JPEG de 2048 × 1536 píxeles, con la misma orientación visible que la original y de **no más de 5 MiB**. Una imagen de 1200 × 800 píxeles no se amplía. El peso obtenido con fotos reales de al menos tres teléfonos (un iPhone y dos Android) se **registra** en las pruebas de la entrega E1 y se compara con el objetivo de 2 MB; superar ese objetivo no es motivo de rechazo mientras no pase de 5 MiB.

**CA-74 — Envío sin reducción y un archivo por petición (RF-50, RF-02).** *Dado* un navegador que no puede reducir la imagen, *cuando* el administrador elige un JPEG o PNG de hasta 5 MiB, *entonces* se envía el original y el servidor lo valida (RF-02); si el original pesa más de 5 MiB, se informa al administrador antes de enviarlo. *Dado* un archivo de más de 5 MiB o de un tipo real distinto de JPEG y PNG que llega al servidor sin haber pasado por la reducción, *entonces* el servidor lo rechaza con un mensaje y no lo guarda. El frente y el reverso se envían cada uno en una petición propia: el rechazo de un archivo no descarta el otro ya aceptado.

**CA-75 — Cédula desde el perfil de la propiedad (RF-51).** *Dado* una propiedad con un contrato vigente cuyo inquilino tiene consentimiento registrado, *cuando* el administrador agrega desde el perfil de la propiedad la fotografía del frente de su cédula, *entonces* la fotografía queda en la ficha del inquilino (se consulta desde ella, con el mismo acceso restringido y la misma auditoría de CA-11 y CA-26) y no queda asociada a la propiedad. *Dado* una propiedad sin contrato vigente (libre o solo con un contrato futuro), *entonces* el perfil muestra la acción desactivada con el aviso «No hay contrato vigente». *Dado* un inquilino que ya tiene cargado el frente, *cuando* el administrador usa la acción del perfil para el frente, *entonces* la acción dice «Reemplazar», el frente nuevo queda activo y el anterior se marca como eliminado (queda uno solo activo por cara).

**CA-11 — Protección de cédula.** *Dado* un visitante sin autenticación válida, *cuando* intenta consultar una fotografía de cédula, *entonces* se deniega y el archivo no se recupera por una URL pública.

**CA-26 — Auditoría de acceso a cédula.** *Dado* un administrador autenticado, *cuando* consulta una fotografía de cédula, *entonces* queda un registro con actor y fecha/hora, sin la imagen.

**CA-27 — Solicitud del titular.** *Dado* una solicitud de acceso recibida un lunes, *cuando* se registra, *entonces* el sistema fija como fecha límite cinco días hábiles después y permite exportar el informe imprimible con todo el registro del titular, incluida la fotografía de su cédula, sin datos de terceros y con la finalidad y el uso de los datos, y la exportación queda registrada en la auditoría (RF-45).

**CA-28 — Retención.** *Dado* un contrato finalizado hace más de cinco años, *cuando* el proceso de retención se ejecuta tras el aviso al administrador, *entonces* se elimina la fotografía, se desasocian los datos personales y se conservan los movimientos sin datos de identificación.

**CA-29 — Desactivar con contrato vigente.** *Dado* un inquilino con contrato vigente o saldos pendientes, *cuando* se intenta desactivar, *entonces* el sistema lo bloquea.

## Contratos y obligaciones

**CA-02 — Creación de contrato.** *Dado* un inquilino y una propiedad disponible, *cuando* se crea un contrato con vigencia, monto válido y día de vencimiento válido, *entonces* queda registrado; se rechazan datos incoherentes y los solapamientos. Si la vigencia pactada es menor a tres años, se muestra una advertencia sin bloquear. Si el inquilino no tiene cargado el frente de la fotografía del documento, se rechaza (CA-78).

**CA-24 — Sustitución de inquilino.** *Dado* un contrato cuyo fin es el 9 de marzo, *cuando* se registra un nuevo contrato para la misma propiedad con inicio el 9 de marzo, *entonces* el sistema lo rechaza; con inicio el 10 de marzo lo acepta. Ambos contratos conservan su historial.

**CA-03 — Generación mensual y mes corto.** *Dado* un contrato de ₡180.000 con inicio el 10 de enero y vencimiento el día 31, *cuando* se generan las obligaciones, *entonces* los períodos son 10 ene–9 feb, 10 feb–9 mar y 10 mar–9 abr, y los vencimientos 31 de enero, 28 de febrero (29 en año bisiesto) y 31 de marzo. Ejecutar de nuevo el proceso no crea duplicados.

**CA-30 — Generación anticipada.** *Dado* un período que inicia el 10 de abril, *cuando* el proceso diario corre el 11 de marzo, *entonces* genera la obligación; el 10 de marzo aún no.

**CA-14 — Último período prorrateado.** *Dado* un período 10 mar–9 abr, un importe de ₡180.000 y fin de contrato el 25 de marzo, *cuando* se registra el fin, *entonces* el importe es ₡92.903 (16 de 31 días, redondeo al colón entero), con el cálculo registrado; los demás períodos no se prorratean.

**CA-31 — Fin de contrato con obligaciones futuras.** *Dado* un contrato con obligaciones futuras sin movimientos, *cuando* se registra su fecha de fin, *entonces* esas obligaciones quedan anuladas con auditoría y no generan alertas.

**CA-32 — Contrato por decidir.** *Dado* un contrato cuya fecha de fin expira sin cierre ni renovación, *cuando* corre el proceso diario, *entonces* el contrato pasa a *por decidir* y continúa generando obligaciones; 120 días antes del fin ya se había notificado al administrador; mientras esté por decidir hay una notificación web persistente y una línea en el resumen diario, que se detienen cuando el contrato se cierra o se renueva.

**CA-76 — Fotografía del contrato (RF-52).** *Dado* un contrato, *cuando* el administrador agrega desde el perfil de la propiedad una fotografía JPEG de 3 MB, *entonces* queda asociada al contrato y se consulta desde él; una fotografía de más de 5 MiB o de un tipo real distinto de JPEG y PNG se rechaza con un mensaje y no se guarda (como en CA-74). Agregar la fotografía del contrato no crea ni modifica la fotografía de la cédula del inquilino, ni al revés. *Dado* un contrato que ya tiene 10 fotografías, *cuando* el administrador intenta agregar otra, *entonces* el sistema la rechaza con un mensaje que indica el máximo, no la guarda y conserva las 10 anteriores.

**CA-77 — Protección y auditoría de la fotografía del contrato (RF-52).** *Dado* un visitante sin autenticación válida, *cuando* intenta consultar una fotografía de un contrato, *entonces* se deniega y el archivo no se recupera por una URL pública. *Dado* un administrador autenticado, *cuando* la consulta, *entonces* queda un registro con actor, fecha/hora y contrato, sin la imagen.

**CA-78 — Registro en dos pasos y contrato sin frente (RF-01, RF-03, RF-07).** *Dado* un inquilino guardado con datos y consentimiento pero sin fotografía, *cuando* el administrador intenta crear un contrato con él, *entonces* el sistema lo rechaza con un mensaje que indica que falta el frente de la fotografía del documento, y el inquilino se conserva. *Cuando* el administrador sube desde la ficha un frente JPEG o PNG válido, *entonces* el inquilino queda con el frente activo y ya se le puede crear un contrato. *Dado* que el archivo del frente se rechaza (por ejemplo, un tipo real distinto de JPEG y PNG o más de 5 MiB), *entonces* no se guarda, el inquilino sigue sin frente y los demás datos no se pierden. La ficha indica que falta el frente. *Dado* que existen inquilinos con y sin frente, *cuando* el administrador aplica en la lista de inquilinos el filtro «Sin frente», *entonces* la lista muestra solo los que no tienen un frente activo (los que solo tienen el reverso incluidos), sin que se envíe ninguna alerta ni correo. *Dado* un inquilino sin frente y sin contrato desde hace más de un año (valor configurable), *entonces* se le aplica la retención de CA-66 sin regla distinta.

## Movimientos y estados

**CA-04 — Registro de pago completo.** *Dado* una obligación con saldo pendiente, *cuando* el administrador registra el movimiento por el saldo con fecha real válida, *entonces* el saldo es cero, la obligación pasa a *pagada* y se cancelan los avisos futuros; en la fase posterior (RF-37) también se genera el comprobante. Una fecha inválida produce un error sin guardar.

**CA-19 — Abono parcial.** *Dado* una obligación de ₡180.000, *cuando* se registra un abono de ₡60.000, *entonces* el saldo es ₡120.000 y la obligación no queda pagada. La fecha real y la fecha/hora de registro se conservan por separado.

**CA-20 — Completar con abonos.** *Dado* una obligación con saldo, *cuando* los abonos válidos igualan el importe exigible, *entonces* el saldo es cero y la obligación pasa a *pagada* sin paso adicional. Un abono que exceda el saldo se rechaza.

**CA-21 — Fecha retroactiva.** *Dado* un pago recibido antes del día de registro, *cuando* se ingresa una fecha real anterior válida (no anterior al inicio del contrato), *entonces* se acepta, se conserva la fecha/hora de registro y no se exige observación.

**CA-33 — Fecha no válida.** *Dado* una fecha real futura o anterior al inicio del contrato, *cuando* se intenta registrar, *entonces* el sistema la rechaza con un mensaje claro.

**CA-34 — Anulación de movimiento.** *Dado* un abono que dejó una obligación en *pagada*, *cuando* se anula con motivo, *entonces* el movimiento original se conserva con su reversión, el saldo se recalcula, el estado vuelve a *pendiente* o *vencida*; en la fase posterior (RF-37) el comprobante queda marcado como anulado.

**CA-35 — Anulación de obligación.** *Dado* una obligación sin movimientos válidos, *cuando* se anula con motivo, *entonces* pasa a *anulada* y deja de generar alertas. Una obligación con movimientos válidos no puede anularse.

**CA-50 — Vencimiento dentro del período.** *Dado* un contrato con inicio el 31 de enero y día de vencimiento 30, *cuando* se genera la obligación del período 31 ene–27 feb, *entonces* el vencimiento es el 27 de febrero (último día del período) y no el 28.

**CA-51 — Tope de reajuste digitado.** *Dado* una vivienda en colones y un reajuste del 5 %, *cuando* el administrador digita un tope vigente del 3,2 % y la fuente "certificación del INEC", *entonces* el sistema advierte que el porcentaje supera el tope, permite guardar y conserva el tope y la fuente junto al reajuste. Sin tope ni fuente digitados, el sistema los exige antes de guardar un reajuste de vivienda.

**CA-36 — Vencimiento y gracia.** *Dado* una obligación con vencimiento el 5 de febrero y 7 días de gracia, *cuando* se evalúa el 12 de febrero, *entonces* está *pendiente*; el 13 de febrero, *vencida*. Un pago recibido el 10 de febrero no cambia el día de vencimiento de los siguientes períodos.

**CA-37 — Comprobantes consecutivos (fase posterior, RF-37; no aplica a la v1).** *Dado* tres movimientos registrados en secuencia, *cuando* se emiten sus comprobantes, *entonces* la numeración es consecutiva y única; anular el segundo no renumera el tercero.

**CA-38 — Pago en moneda distinta de la del contrato.** *Dado* un contrato en USD con saldo de $300, *cuando* el inquilino paga ₡150.000 y el administrador ingresa un tipo de cambio de ₡500, *entonces* el sistema registra la moneda recibida, el tipo de cambio y el equivalente de $300, y el saldo se mantiene en USD. Con un pago de ₡100.000 y un tipo de cambio de ₡512,35, el sistema calcula el equivalente en $195,18 (100.000 ÷ 512,35 = 195,179…, redondeado a dos decimales).

## Cambios de condiciones

**CA-12 — Reajuste.** *Dado* un contrato con período vigente 10 mar–9 abr, *cuando* se registra un reajuste notificado el 20 de marzo, *entonces* la fecha efectiva se normaliza al 10 de abril, las obligaciones anteriores mantienen su monto y las posteriores aplican el nuevo.

**CA-39 — Reajuste sobre el tope o en moneda extranjera.** *Dado* una vivienda con porcentaje de reajuste superior al tope informado, *cuando* se registra, *entonces* el sistema advierte sin bloquear. Si la vivienda tiene precio en USD, *entonces* rechaza el reajuste.

**CA-22 — Corrección con obligaciones no pagadas.** *Dado* un contrato con obligaciones pagadas, pendientes y vencidas no pagadas, *cuando* se registra una corrección con motivo y fecha efectiva, *entonces* las pagadas no cambian, las no pagadas afectadas se actualizan, y el historial permite reconstruir los valores anteriores y nuevos.

**CA-40 — Cambio por debajo de lo abonado.** *Dado* una obligación con ₡100.000 abonados, *cuando* una corrección fija su importe en ₡80.000, *entonces* el sistema bloquea el cambio y muestra el exceso de ₡20.000.

## Calendario

**CA-06 — Calendario general.** *Dado* obligaciones de varios inquilinos en un mes, *cuando* se abre el calendario, *entonces* se identifican vencimiento, inquilino y estado; los eventos coincidentes permiten consultar cada obligación. Un contrato que termina en el mes y un depósito con fecha límite acordada aparecen como eventos informativos, sin alertas.

**CA-07 — Filtro por inquilino.** *Dado* obligaciones de al menos tres inquilinos, *cuando* se selecciona uno, *entonces* solo se muestran las suyas; al retirar el filtro se recupera la vista general y se conserva el mes. Lo mismo al filtrar por una propiedad (por su alias).

## Notificaciones

**CA-08 — Recordatorio configurable.** *Dado* una obligación pendiente y una anticipación de 3 días, *cuando* llega la fecha calculada, *entonces* se crea la notificación web y el recordatorio se incluye en el resumen diario por correo al administrador si el canal está configurado; intento y resultado quedan registrados. Si la obligación tiene abonos, el aviso indica el saldo.

**CA-41 — Cambio de anticipación.** *Dado* recordatorios programados, *cuando* el administrador cambia la anticipación, *entonces* los recordatorios futuros aún no procesados se reprograman sin duplicados.

**CA-05 — Alerta diaria y resumen.** *Dado* tres obligaciones vencidas, *cuando* corre el proceso diario, *entonces* se registra una alerta por obligación y se envía un único resumen por correo con las tres y con los recordatorios del día. No hay duplicados por obligación y día; tras pagarse una obligación, no se producen nuevas alertas para ella.

**CA-42 — Proceso omitido.** *Dado* que el proceso no corrió dos días, *cuando* se reanuda, *entonces* emite solo la alerta del día actual.

**CA-09 — Fallo del envío de correo.** *Dado* un rechazo del servicio de correo, *cuando* el sistema intenta enviar, *entonces* registra el resultado, reintenta hasta cinco veces con espera creciente y aleatoria, no cambia el estado del pago y conserva la notificación web. Distingue el correo aceptado por el servicio del no aceptado y no declara entregado uno solo aceptado; la v1 no recibe estados posteriores.

**CA-43 — Contenido mínimo.** *Dado* un resumen enviado por correo, *cuando* se inspecciona su contenido, *entonces* no contiene número de documento ni imágenes.

**CA-44 — Abono sin notificación individual.** *Dado* un abono registrado, *cuando* se guarda, *entonces* el sistema actualiza el saldo visible y no genera notificación individual.

## Depósito

**CA-15 — Abonos al depósito.** *Dado* un depósito acordado de ₡300.000, *cuando* se registra un abono de ₡100.000, *entonces* el saldo es ₡200.000 y el estado, parcialmente pagado.

**CA-16 — Completar depósito.** *Dado* un depósito con saldo, *cuando* un abono completa el total, *entonces* el saldo es cero y el depósito se muestra como completado, conservando los abonos por separado.

**CA-17 — Separación entre alquiler y depósito.** *Dado* un contrato con obligación y depósito, *cuando* se registra un abono al depósito, *entonces* el saldo y estado de la obligación no cambian.

**CA-23 — Excepción de abonos.** *Dado* un depósito con tres abonos no anulados, *cuando* el administrador intenta un cuarto, *entonces* el sistema exige confirmación con motivo; sin motivo, lo rechaza; con motivo, lo registra y deja auditoría.

**CA-45 — Depósito mayor a una mensualidad.** *Dado* una renta de ₡180.000, *cuando* se registra un depósito de ₡400.000, *entonces* el sistema muestra una advertencia legal sin bloquear el guardado, si el contrato es de vivienda; en un contrato de destino "otro" no advierte.

**CA-46 — Depósito de contrato cerrado.** *Dado* un contrato finalizado con depósito, *cuando* se consulta, *entonces* se muestra el estado y la etiqueta "contrato cerrado, liquidación manual", sin alertas.

## Seguridad y configuración

**CA-13 — Una sola cuenta con segundo factor.** *Dado* el alcance de v1, *cuando* se configura el acceso, *entonces* solo existe una cuenta administradora, que requiere segundo factor. Las solicitudes sin autenticación válida son rechazadas.

**CA-47 — Recuperación de acceso.** *Dado* un administrador sin su segundo factor, *cuando* usa un código de recuperación válido, *entonces* accede una sola vez con ese código y el sistema envía el aviso de seguridad por correo a las dos direcciones (RF-27).

**CA-48 — Sesión.** *Dado* una sesión inactiva más de una hora o abierta más de 24 horas, *cuando* se realiza una acción, *entonces* se exige autenticarse de nuevo.

**CA-18 — Configuración regional.** *Dado* una configuración nueva, *cuando* se crean contratos y se programan procesos, *entonces* se usan CRC y `America/Costa_Rica`. Al configurar USD en un contrato o cambiar la zona de la organización, los registros históricos no cambian.

**CA-10 — Conservación del historial.** *Dado* un contrato con obligaciones previas, *cuando* se desactiva el inquilino o se finaliza el contrato, *entonces* el historial permanece consultable.

**CA-56 — Plazo de aviso de un incidente.** *Dado* un incidente de seguridad registrado el viernes 6 de noviembre de 2026 como ocurrido ese día, *cuando* se consulta, *entonces* el sistema muestra como fecha límite de aviso a titulares y a la Agencia el viernes 13 de noviembre de 2026 (cinco días hábiles), sin contar sábados ni domingos; los feriados oficiales se validan con abogado (DP-17).

**CA-57 — Constancia de avisos de un incidente.** *Dado* un incidente con dos titulares afectados, *cuando* el administrador registra el aviso a cada uno y a la Agencia, *entonces* queda constancia de fecha, destinatario y contenido mínimo (naturaleza, datos comprometidos, acciones, dónde obtener más información), y el incidente no se marca como atendido mientras falte un aviso.

**CA-52 — Envío repetido de un abono.** *Dado* un abono de ₡1.000 enviado con una clave de solicitud, *cuando* el mismo envío se repite con la misma clave, *entonces* el sistema no crea un segundo movimiento, devuelve el ya registrado y el saldo se descuenta una sola vez.

**CA-53 — Auditoría sin valores personales.** *Dado* un inquilino cuyo teléfono se modifica, *cuando* se consulta el registro de auditoría, *entonces* consta que el campo teléfono cambió, quién lo hizo y cuándo, pero no el teléfono anterior ni el nuevo; en un cambio de importe sí constan el valor anterior y el nuevo.

**CA-54 — Comprobantes sin huecos (fase posterior, RF-37; no aplica a la v1).** *Dado* que un registro de abono falla después de asignar un número de comprobante, *cuando* se registra el siguiente abono con éxito, *entonces* su número es el siguiente al último comprobante emitido, sin saltos.

**CA-55 — Ajuste que conserva el importe inicial.** *Dado* una obligación de ₡300.000 con una corrección de −₡100.000, *cuando* se consulta, *entonces* el importe exigible vigente es ₡200.000, el importe inicial de ₡300.000 y la corrección con su motivo siguen consultables, y ningún valor se sobrescribió.

**CA-49 — Saldo de apertura.** *Dado* un contrato con inicio hace dos años, *cuando* se registra un saldo de apertura de ₡360.000 con fecha de hoy, *entonces* se genera una obligación de apertura por ese importe, las obligaciones regulares se generan desde el primer período que inicia **después** de esa fecha (un período que inicia el mismo día de la apertura queda dentro del saldo de apertura y no se genera de nuevo), y no hay alertas retroactivas. La fecha de vencimiento de la apertura es la que digita el administrador (por defecto, la fecha de apertura más los días de gracia del contrato) y la obligación aparece en el calendario ese día.

**CA-58 — Movimientos sobre períodos futuros (RN-15, segunda mitad).** *Dado* el 10 de enero y una obligación cuyo período inicia el 5 de febrero (el período inmediato siguiente), *cuando* el administrador registra un abono sobre ella, *entonces* el sistema lo acepta. *Dado* una obligación cuyo período inicia el 5 de marzo, *cuando* intenta registrar un abono sobre ella, *entonces* lo rechaza con un mensaje y no guarda nada. Sobre una obligación de un período pasado con saldo, el abono se acepta. *Nota v1.9 (propuesta de redacción, HP-01 de la estrategia de pruebas): la regla se verifica directamente en la operación de registro, aunque la generación a 30 días normalmente no cree la obligación de marzo.*

**CA-59 — Restablecer la contraseña olvidada (RF-27).** *Dado* un administrador sin sesión que olvidó su contraseña, *cuando* solicita restablecerla, *entonces* el sistema envía un enlace solo a la dirección del administrador, válido 15 minutos y de un solo uso; un enlace usado o con más de 15 minutos es rechazado; al fijar la contraseña nueva no queda ninguna sesión iniciada, los demás enlaces pendientes dejan de valer y el acceso exige el segundo factor; el sistema envía el aviso de seguridad a las dos direcciones. La respuesta y su tiempo son iguales exista o no la cuenta, y una cuarta solicitud dentro de una hora es rechazada. *Dado* una sesión iniciada, *cuando* cambia la contraseña o reemplaza el segundo factor, *entonces* el sistema exige la contraseña actual y envía el aviso de seguridad.

**CA-60 — Fallo del aviso de seguridad (RF-27).** *Dado* que el servicio de correo rechaza el aviso de un evento de seguridad, *cuando* el administrador usa un código de recuperación, *entonces* accede (la recuperación procede), el aviso queda guardado con el evento, se reintenta hasta cinco veces con espera creciente y aleatoria y, si sigue fallando, queda como *fallido*, se muestra una alerta persistente en cada inicio de sesión y se registra en la auditoría. El aviso no contiene códigos, contraseñas ni enlaces de acceso.

**CA-61 — Número de recibo físico (RF-47).** *Dado* dos abonos, *cuando* el administrador anota el número "R-0001" en el primero e intenta anotar el mismo número en el segundo, *entonces* el sistema rechaza el segundo; un abono sin número se guarda sin error; anular un abono conserva su número anotado.

**CA-62 — Anular un contrato (RF-48).** *Dado* un contrato sin movimientos válidos, *cuando* el administrador lo anula con un motivo, *entonces* el contrato queda anulado, sus obligaciones y su depósito sin abonos quedan anulados, queda constancia en la auditoría y otro contrato puede ocupar esas fechas. *Dado* un contrato con al menos un movimiento válido, *cuando* intenta anularlo, *entonces* el sistema lo rechaza y propone finalizarlo. Sin motivo, no se anula.

**CA-63 — Propiedad inactiva (RF-06).** *Dado* una propiedad con un contrato vigente, futuro o por decidir, *cuando* el administrador intenta marcarla inactiva, *entonces* el sistema lo bloquea. *Dado* una propiedad sin contratos activos, *cuando* la marca inactiva, *entonces* no admite contratos nuevos hasta que se reactive; la reactivación es posible. Dos propiedades no pueden tener el mismo alias.


**CA-64 — Cambiar una dirección de correo (RF-27).** *Dado* un administrador con la sesión iniciada, *cuando* pide cambiar una de las dos direcciones de aviso, *entonces* el sistema exige la contraseña actual, envía un enlace de confirmación de un solo uso y 15 minutos a la dirección nueva, mantiene vigente la anterior hasta la confirmación, y al confirmar envía el aviso de seguridad a las dos direcciones anteriores. Un enlace usado o vencido no cambia nada.


**CA-65 — Desasociar a petición del titular (RF-40).** *Dado* una solicitud de supresión de un inquilino sin contratos vigentes, futuros ni por decidir y sin saldos pendientes, *cuando* el administrador ejecuta "desasociar a petición", *entonces* se eliminan sus fotografías, se anulan sus datos personales, se conservan los movimientos sin identificación y la solicitud queda resuelta con auditoría. *Dado* un inquilino con un contrato vigente o con saldo pendiente, *cuando* intenta ejecutarla, *entonces* el sistema la bloquea y la solicitud solo puede resolverse como denegada con un motivo escrito.

**CA-66 — Retención sin contrato (RF-41).** *Dado* un inquilino registrado hace más de un año sin ningún contrato, o cuyo único contrato se anuló hace más de un año, *cuando* corre el proceso de retención tras avisar al administrador, *entonces* se eliminan sus fotografías y se desasocian sus datos personales. Un inquilino con un contrato no anulado no se elimina por esta regla.

**CA-67 — Consentimiento y revocación (RF-39).** *Dado* un inquilino con consentimiento otorgado sobre la versión 2 del texto informativo, *cuando* se consulta, *entonces* se puede ver el texto exacto de esa versión. *Cuando* el administrador registra la revocación, *entonces* la ficha muestra el aviso, el sistema rechaza crear un contrato nuevo con ese inquilino, se abre una solicitud de supresión de oficio y no se borra ningún dato por la revocación.


**CA-68 — Límite de intentos fallidos (RF-27).** *Dado* cinco intentos fallidos seguidos de iniciar sesión (con contraseña, TOTP o código de recuperación), *cuando* se intenta un sexto, *entonces* el sistema exige esperar un minuto, y la espera se duplica con cada fallo adicional hasta una hora; no hay bloqueo permanente. Un inicio de sesión correcto reinicia el contador, el restablecimiento de contraseña sigue disponible y al llegar a cinco fallos se envía un aviso de seguridad a las dos direcciones.

**CA-69 — Segundo factor y códigos de recuperación (RF-27).** *Dado* un segundo factor recién activado, *cuando* se muestran los códigos de recuperación, *entonces* son 10, se muestran una sola vez y cada uno sirve una sola vez. Un código TOTP ya aceptado se rechaza si se repite; uno de un intervalo de 30 segundos anterior o posterior se acepta. Emitir códigos nuevos exige la contraseña actual, invalida los anteriores y envía el aviso de seguridad.

**CA-70 — Creación de la cuenta y rescate por el servidor (RF-27).** *Dado* un sistema recién desplegado sin cuenta, *cuando* el solicitante ejecuta el comando de creación en el servidor y entra por primera vez, *entonces* activa el segundo factor y recibe los 10 códigos; no existe ninguna pantalla pública para crear la cuenta. *Dado* un administrador sin TOTP ni códigos, *cuando* el solicitante ejecuta el comando de rescate, *entonces* el segundo factor queda desactivado, se exige registrarlo de nuevo, queda constancia en la auditoría y se avisa a las dos direcciones.


**CA-71 — Auditoría de autenticación y su consulta (RF-28).** *Dado* un inicio de sesión fallido y uno correcto, *cuando* el administrador consulta la auditoría filtrando por tipo de evento, *entonces* constan ambos con fecha, hora y dirección IP de origen, y no aparecen contraseñas, códigos ni tokens. La pantalla es de solo lectura y consultarla no genera un registro nuevo.

**CA-72 — Alerta de proceso diario omitido o fallido (RF-49).** *Dado* un día en que el proceso diario no se ejecutó correctamente, *cuando* pasa una hora de la hora programada, *entonces* el sistema registra un aviso, muestra una alerta web persistente en cada inicio de sesión y lo envía por correo; la alerta desaparece cuando hay una ejecución correcta, y no se repite el correo en cada comprobación.

# 10. Matriz de trazabilidad

| Necesidad / objetivo | Requisitos | Criterios |
|---|---|---|
| Registrar inquilinos y cédulas | RF-01–RF-05, RF-39, RF-45, RF-50, RF-51, RNF-02, RNF-03 | CA-01, CA-11, CA-25, CA-26, CA-29, CA-73, CA-74, CA-75, CA-78 |
| Administrar propiedades y contratos | RF-06–RF-10, RF-36, RF-42, RF-48, RF-52, RN-01–RN-05, RN-10, RN-16, RN-28, RN-30 | CA-02, CA-10, CA-24, CA-31, CA-32, CA-62, CA-63, CA-76, CA-77 |
| Generar obligaciones sin duplicados | RF-11, RF-12, RF-43, RN-04, RN-05, RN-13, RN-15, RNF-04, RNF-16 | CA-03, CA-30, CA-49, CA-50, CA-58 |
| Reajustes y correcciones | RF-10, RN-14, OL-06, OL-07 | CA-12, CA-22, CA-39, CA-40, CA-51, CA-55 |
| Prorratear el último período | RF-09, RN-12 | CA-14 |
| Movimientos, saldos y estados | RF-13–RF-16, RF-34, RF-35, RN-06–RN-09, RN-11, RN-17, RN-18, RN-21, RN-22, RN-29 | CA-04, CA-19–CA-21, CA-33–CA-36, CA-52 |
| Comprobantes, recibos y moneda | RF-37 (fase posterior), RF-47, RF-38, RN-23, OL-03, OL-05 | CA-37 y CA-54 (fase posterior), CA-61, CA-38 |
| Calendario y filtros | RF-17–RF-20 | CA-06, CA-07 |
| Recordatorios y alertas | RF-21–RF-25, RF-44, RF-49, RN-07, RN-08 | CA-05, CA-08, CA-09, CA-41–CA-44, CA-72 |
| Restringir acceso y auditar | RF-26–RF-28, RF-45, RN-25, RNF-01, RNF-02, RNF-06, RNF-14 | CA-11, CA-13, CA-26, CA-47, CA-48, CA-53, CA-59, CA-60, CA-64, CA-68, CA-69, CA-70, CA-71 |
| Depósito de garantía | RF-29–RF-32, RN-19, RN-20, RN-26, RN-27 | CA-15–CA-17, CA-23, CA-45, CA-46 |
| Derechos del titular y retención | RF-39–RF-41, RN-24, RNF-13–RNF-15 | CA-27, CA-28, CA-65, CA-66, CA-67 |
| Incidentes y documentación de seguridad | RF-46, RNF-14, RNF-18, OL-19–OL-21 | CA-56, CA-57 |
| Operar en varias regiones | RF-33, RN-23, RNF-12, RNF-17 | CA-18 |
| Requisitos no funcionales sin criterio de aceptación | RNF-05, RNF-07, RNF-08, RNF-09, RNF-10, RNF-11 | Ninguno; se verifican en la estrategia de pruebas (fase 4) |

# 11. Riesgos y dependencias

| Riesgo o dependencia | Respuesta requerida |
|---|---|
| Exposición de fotografías de cédula y de contrato | Repositorio privado, acceso autenticado, auditoría de acceso, cifrado; retención de cinco años de la cédula; la del contrato queda sin plazo hasta DP-28. |
| Incumplimiento legal por reglas no validadas | Validar la sección 3 con un abogado antes de aprobar (DP-17). |
| Duplicación de obligaciones | Unicidad por contrato y período, y generación idempotente. |
| Fallo del servicio de correo | Registro de resultados, reintentos y notificación web como canal interno; los avisos de seguridad fallidos dejan alerta persistente (RF-23, RF-24, RF-27). |
| Dependencia del correo y del dominio | El correo envía notificaciones, avisos de seguridad y el enlace de restablecimiento de contraseña; requiere dominio propio verificado y un servicio externo (DAS, ADR-026). Sin ellos no hay restablecimiento por correo; la entrada sigue posible con el segundo factor. Entregabilidad y términos del servicio sin verificar. |
| Cuenta de correo del administrador comprometida | Con el enlace de restablecimiento un tercero podría fijar la contraseña, pero no entra sin el segundo factor (RF-26). Aviso a dos direcciones. Riesgo asumido por el solicitante. |
| Recibos de papel fuera del sistema | Numeración a mano, sin marca de anulado y sin copia electrónica. Riesgo asumido por el solicitante hasta integrar el comprobante del sistema (RF-37, RF-47). |
| Proveedor de WhatsApp no elegido | Diferido y fuera de la v1: WhatsApp es futuro y depende de un proyecto aparte del solicitante (DP-04). Los términos de servicio de WhatsApp para consumidores prohíben mensajería masiva o automática; los términos de la plataforma empresarial no se leyeron. |
| Vulneración de seguridad sin aviso a tiempo | Registro de incidentes con fecha límite de cinco días hábiles (RF-46) y procedimiento de respuesta en la fase 6; validación legal (DP-17, DP-19). |
| Servidor propio con datos de cédulas | El solicitante administra el servidor (DP-08). Recomendado antes de cargar datos reales: servidor endurecido, prueba de restauración superada y revisión legal cerrada. Las guías de endurecimiento se investigaron el 22-oct-2026 (actualizaciones 2026-10-22 a 2026-10-22e): el solicitante decidió no depender del PDF de CIS y auditar con Lynis; las medidas concretas siguen sin decidir. |
| Ejecución diaria interrumpida | Procesamiento independiente de la interfaz, idempotente; solo la alerta del día. |
| Reglas de reajuste y gracia mal aplicadas | Casos de prueba para fechas efectivas, gracia y tope; validación legal. |
| Pérdida de datos | Respaldo diario con copia independiente y prueba de restauración antes de producción y cada 3 meses (RNF-09). |
| Cuenta única comprometida | MFA, códigos de recuperación, sesión corta, avisos de seguridad por correo a dos direcciones. |
| Conservación contable de datos eliminados | Determinar obligaciones contables o tributarias de conservación antes de aplicar la eliminación (DP-18). |

# 12. Decisiones pendientes y registro de decisiones

## 12.1 Pendientes

| ID | Decisión pendiente | Responsable sugerido |
|---|---|---|
| DP-01 | Validar legalmente la fórmula del prorrateo del último período (días reales del período, ambos extremos, redondeo). | Propietario y abogado |
| DP-04 | Proveedor de WhatsApp: **diferida**, depende de un proyecto aparte del solicitante (aplicación propia que se conecte a WhatsApp). Desde la v1.9, WhatsApp queda fuera de la v1 y es un canal futuro. Se requiere revisión legal de ese proyecto frente a los términos de WhatsApp. | Propietario |
| DP-17 | Validación legal de las obligaciones OL-01 a OL-21 (OL-19 a OL-21 son lectura propia del Reglamento 37554-JP), incluido cómo se cuentan los siete días de gracia y la aplicabilidad del art. 92. | Abogado |
| DP-18 | Obligaciones contables y tributarias de conservación de registros y su efecto sobre la eliminación de datos. | Abogado y contador |
| DP-19 | Aplicabilidad de la Ley 8968 (arts. 2 y 21) y de su reglamento: si la base del SGA es "interna o doméstica" y por tanto no se inscribe (Reglamento, art. 44), si el historial de pagos es dato sensible, y si hay que informar a la Agencia ante incidentes (OL-19). Desde la v1.9, también el alcance de la exportación del titular y, por la auditoría de las exportaciones, qué conserva el registro. La segunda dirección de los avisos de seguridad es del propio solicitante (decisión del 21-oct-2026), por lo que no es dato de un tercero. | Abogado |
| DP-20 | Contenido del comprobante y si los procedimientos pactados, incluido el recibo de papel, lo sustituyen (art. 58). Desde la v1.9, también si el recibo de papel fuera del sistema basta para OL-03 y si la normativa tributaria exige factura electrónica por el alquiler (solo hay notas de prensa que citan la resolución DGT-R-012-2018; sin fuente oficial leída). Numeración: serie global continua, decisión provisional del solicitante (H4), aplicable a la fase del comprobante del sistema. | Abogado y contador |
| DP-21 | Texto informativo y formato del consentimiento (art. 5). | Abogado |
| DP-27 | Metadatos de la fotografía (por ejemplo, la ubicación): si volver a codificar la imagen en el navegador los elimina (no verificado) y si el sistema debe exigir o garantizar que no se guarden; se decide tras la prueba de la entrega E1. | Solicitante |
| DP-28 | Conservación, eliminación y desasociación de la fotografía del contrato (contiene datos personales del inquilino y del arrendador): plazo, si entra en la exportación del titular (RF-40) y relación con las obligaciones de conservación de DP-18. | Abogado y contador |
| DP-29 | **Dividida el 23-oct-2026 (v1.14).** *Resuelto:* máximo de 10 fotografías por contrato y punto de partida de 3508 px y calidad 0,85. *Abierto:* cifras definitivas de reducción (lado mayor, calidad, peso objetivo) de la fotografía del contrato, tras medirlas con fotos reales (un iPhone y dos Android) en la entrega E2. | Solicitante |

## 12.1b Decisiones del solicitante del 20 y 21-oct-2026 incorporadas en la v1.9

Cada fila indica el hallazgo del diseño técnico y la decisión; el detalle y los riesgos están en `actualizaciones/2026-10-20h_ht-05-recuperacion-acceso/`, `2026-10-21_ht-08-contrasena-segundo-factor/`, `2026-10-21b_ht-01-canal-correo/`, `2026-10-21c_ht-03-exportacion-titular/` y `2026-10-21d_ht-02-comprobante-fisico/`. No son aprobación del negocio.

| Hallazgo | Decisión | Requisitos afectados | ¿Contra la recomendación? |
|---|---|---|---|
| HT-05 | Avisos de seguridad por correo a dos direcciones; recuperación procede si falla el envío | RF-27, CA-47, CA-60 | No |
| HT-08 | Cambio de contraseña y reemplazo del segundo factor con la contraseña actual; restablecimiento por enlace de correo de 15 minutos | RF-27, CA-59 | Sí (las tres primeras) |
| HT-01 | La v1 notifica al administrador por web y correo; WhatsApp futuro; sin punto de recepción de estados | RF-23, RF-24, RF-44, CA-05, CA-08, CA-09, CA-43, sección 2.4 | No |
| HT-03 | Exportación del titular: todo su registro con la foto de la cédula, informe web imprimible; auditoría de la exportación | RF-40, RF-45, CA-27 | No (rectificó una primera elección) |
| Pendientes del diseño técnico (21-oct-2026) | Dominio `.com` en Cloudflare Registrar; dos direcciones del solicitante en proveedores distintos; reintentador cada 1 minuto; protecciones del enlace de restablecimiento; auditar fotos de cédula y exportaciones, no las lecturas ordinarias | RF-27, RF-45, CA-27, CA-59 | No |
| HT-02 | Recibo de papel fuera del sistema primero; comprobante del sistema después | RF-37, RF-47, CA-04, CA-34, CA-37, CA-54, CA-61 | No; difiere una prioridad Alta |
| HP-01 | Segunda mitad de RN-15 con criterio de aceptación | RN-15, CA-58 | No |

## 12.1c Decisión del solicitante del 22-oct-2026 incorporada en la v1.10

Detalle y fuentes en `actualizaciones/2026-10-22d_limite-subida-foto-cedula/` y `2026-10-22e_decision-limite-subida/`. No es aprobación del negocio.

| Pregunta | Decisión | Requisitos afectados | ¿Contra la recomendación? |
|---|---|---|---|
| ¿Se reduce la foto en el navegador, y con qué cifras? | Reducción con canvas; 2048 px, calidad 0,85, objetivo de 2 MB, tope del servidor de 5 MiB (el de RF-02) | RF-50, CA-73, CA-74, S-03 | No |
| ¿Frente y reverso en una o dos peticiones? | Por separado | RF-02, CA-74 | No |

La propuesta de formalizar la reducción en la ERS (propuesta 25 de la actualización 2026-10-22d) queda cumplida con esta versión; las pruebas en teléfonos reales y la verificación de los metadatos siguen pendientes.

## 12.1d Decisiones del solicitante del 22-oct-2026 incorporadas en la v1.11

Detalle en `actualizaciones/2026-10-22i_cedula-y-contrato-desde-propiedad/`. No son aprobación del negocio.

| Pregunta | Decisión | Requisitos afectados | ¿Contra la recomendación? |
|---|---|---|---|
| ¿Dónde queda la foto de la cédula? | Botón en el perfil de la propiedad; la fotografía se guarda en el inquilino | RF-51, CA-75 | No |
| ¿La foto del contrato es un documento nuevo? | Sí, asociada al contrato | RF-52, CA-76, CA-77, entidad Documento del contrato | No |
| ¿La foto del contrato se reduce en el navegador? | Sí, con la misma mecánica; la cifra se mide | RF-52, DP-29 | No |
| ¿La cédula y el contrato son una imagen o dos? | Dos fotos distintas | RF-52 | No |

La retención de la fotografía del contrato (DP-28) y las cifras de reducción (DP-29) quedan abiertas.

## 12.1e Decisiones del solicitante del 23-oct-2026 incorporadas en la v1.12

Detalle en `actualizaciones/2026-10-23_ht-11-perfil-propiedad/`, `2026-10-23c_unidad-tope-5mb/` y `2026-10-23d_quitar-zona-temporal/`. No son aprobación del negocio.

| Pregunta | Decisión | Requisitos afectados | ¿Contra la recomendación? |
|---|---|---|---|
| ¿Qué muestra el perfil de la propiedad? | Datos de la propiedad (RF-06), inquilino y contrato vigente, y las acciones de cédula y foto del contrato; sin historial de contratos | glosario, RF-51, RF-52 | No |
| ¿Qué pasa con los botones sin contrato vigente? | Desactivados con el aviso «No hay contrato vigente» | RF-51, RF-52, CA-75 | No |
| ¿Cómo se comporta «Agregar cédula» si ya existe la cara? | Dice «Reemplazar»; la anterior se marca eliminada | RF-51, CA-75 | No |
| ¿Qué unidad tiene el tope de subida? | 5 MiB = 5 242 880 bytes | RF-02, RF-50, RF-52, CA-73, CA-74, CA-76 | No |
| ¿Se necesita una zona temporal de archivos? | No: el inquilino se registra primero y las fotos se suben después a su ficha; sin contrato hasta tener el frente (regla propuesta por el asistente y aceptada) | RF-01, RF-03, RF-07, CA-01, CA-02, CA-78, DP-30 | No (la primera recomendación del asistente era mantenerla solo en el registro; la cambió tras la pregunta del solicitante) |

La adopción del bloqueo del contrato al ordenar las fotografías (H18) es una decisión del modelo de datos y no cambia la ERS.

## 12.1f Decisión del solicitante del 23-oct-2026 incorporada en la v1.13

Detalle en `actualizaciones/2026-10-23i_dp-30-inquilinos-sin-frente/`. No es aprobación del negocio.

| Pregunta | Decisión | Requisitos afectados | ¿Contra la recomendación? |
|---|---|---|---|
| ¿Qué se hace con los inquilinos sin frente que nunca se completan? | Aplicar RF-41 tal como está (retención sin contrato, 1 año configurable), sin plazo nuevo | RF-41, CA-66, CA-78 | No |
| ¿Cómo se hace visible un inquilino sin frente? | Indicación en la ficha y filtro «Sin frente» en la lista; sin alertas ni correos | RF-03, CA-78 | No |

## 12.1g Decisiones del solicitante del 23-oct-2026 incorporadas en la v1.14

Detalle en `actualizaciones/2026-10-23k_dp-29-fotos-contrato/`. No son aprobación del negocio.

| Pregunta | Decisión | Requisitos afectados | ¿Contra la recomendación? |
|---|---|---|---|
| ¿Cuántas fotografías como máximo por contrato? | 10 | RF-52, CA-76, DP-29 | No |
| ¿Con qué cifras se empieza a medir la reducción de la foto del contrato? | Lado mayor de 3508 px y calidad 0,85, a confirmar al medir en la E2 | RF-52, DP-29 | No |

DP-29 queda dividida: el máximo está resuelto y las cifras definitivas siguen abiertas.

## 12.2 Resueltas en esta versión (respuestas del solicitante, 17-oct-2026)

| ID | Resolución |
|---|---|
| DP-02 | Proceso diario a las 07:00 en la zona de la organización; tras una caída solo se emite la alerta del día. |
| DP-03 | Un cambio de anticipación reprograma las notificaciones futuras sin duplicar. |
| DP-05 | Cinco años tras el fin del contrato, tope de diez años (sujeto a DP-17). |
| DP-06 | Hasta 50 propiedades; consultas en menos de 2 s en el percentil 95. |
| DP-07 | Respaldo: RPO de 24 h, RTO de 24 h, respaldo diario, retención de 35 días, prueba de restauración antes de producción y cada 3 meses (17-oct-2026; RNF-09). |
| DP-08 | Acceso desde cualquier lugar por internet (HTTPS, contraseña larga, segundo factor); servidor virtual (VPS) administrado por el solicitante, con datos reales desde el inicio. Decisión contra la recomendación de nube gestionada, por aprendizaje y costo; riesgo asumido por el solicitante (17-oct-2026). |
| DP-09 | Monedas admitidas: CRC y USD. |
| DP-10 | No se notifica cada abono de alquiler. |
| DP-11 | Período por aniversario del día de inicio; sin prorrateo en períodos completos. |
| DP-12 | La excepción de abonos al depósito es una confirmación con motivo obligatorio y auditoría. |
| DP-13 | Sin calendarios de abono del depósito en v1. |
| DP-15 | La corrección de una fecha se hace anulando el movimiento y registrando uno nuevo, con motivo en ambos. |
| DP-16 | Se bloquea todo cambio que deje el importe exigible por debajo de lo abonado. |
| DP-14 | Pregunta P11: sin enunciado ni respuesta recuperables; cerrada por el solicitante (17-oct-2026). No se inventó su contenido; si reaparece se reabre con un ID nuevo. |
| DP-22 | El administrador digita el tope de reajuste y su fuente en cada reajuste; el sistema advierte sin bloquear (17-oct-2026). |
| DP-24 | El día de vencimiento es configurable (1 a 31) y por defecto es el día de inicio del período; RN-05 confirmada (17-oct-2026). |
| DP-25 | El saldo de apertura incluye todo lo adeudado por los períodos ya iniciados, incluido el período en curso; las alertas comienzan desde la carga (17-oct-2026). |
| DP-23 | El solicitante ocupa los tres roles (propietario del producto, responsable de requisitos y responsable técnico) y se registra como brandonC-developer. El asesor legal sigue sin designar (17-oct-2026). |
| DP-26 | Hora local más zona, y el instante se calcula al ejecutar; fundamento: W3C, Working with Time Zones (17-oct-2026). |
| DP-30 | Inquilinos guardados sin el frente de la fotografía (23-oct-2026, ERS v1.13): no hay plazo nuevo, se aplica la retención sin contrato de RF-41 y CA-66; se hacen visibles con una indicación en la ficha y un filtro «Sin frente» en la lista de inquilinos, sin alertas (RF-03, CA-78). Que el plazo de un año sea razonable para este caso lo valida el abogado (DP-17). |

# 13. Gestión de requisitos y control de cambios

1. Todo requisito tiene identificador único, descripción, fuente, prioridad, estado y método de verificación.
2. Los cambios se solicitan con justificación y análisis de impacto sobre requisitos, reglas, modelo de datos, criterios, seguridad, cumplimiento legal y planificación.
3. El responsable designado aprueba o rechaza cada cambio antes de considerarlo parte de la línea base.
4. Las versiones aprobadas no se sobrescriben sin registrar el cambio.
5. Los requisitos ambiguos o bloqueados se resuelven antes de construir lo que dependa de ellos.
6. La matriz de trazabilidad se actualiza con cada cambio aprobado.
7. Una versión se considera aprobada solo con responsable, fecha y aceptación formal.
8. Un cambio legal que afecte la sección 3 requiere revisión de un abogado.

# 14. Revisión y condiciones de aprobación

Antes de aprobar esta ERS, los revisores deben confirmar:

☐ Objetivos y alcance comprensibles.
☐ Requisitos necesarios, no contradictorios y verificables.
☐ Reglas de período, vencimiento, gracia y generación consistentes (RN-03 a RN-07).
☐ Regla de prorrateo del último período validada (DP-01).
☐ Reajustes y correcciones validados legalmente (OL-06, OL-07).
☐ Obligaciones legales de la sección 3 validadas por un abogado (DP-17).
☐ Recibo de papel y comprobante del sistema, factura electrónica, consentimiento y atención del titular revisados (DP-20, DP-21).
☐ Retención de datos y obligaciones de conservación contable conciliadas (DP-18).
☐ Moneda, tipo de cambio manual y zona horaria verificados.
☐ Canales de notificación (web y correo en la v1; WhatsApp futuro) y sus límites comprendidos.
☐ Cambios de alcance de la v1.9 aceptados por escrito, incluido el diferimiento de RF-37 (prioridad Alta) y los riesgos de las decisiones contra la recomendación (RF-27).
☐ Fotografía del contrato: conservación decidida (DP-28), y cifras de reducción medidas con fotos reales en la E2 (DP-29; el máximo de 10 ya está decidido).
☐ Cifras de la reducción de la fotografía (RF-50) confirmadas con fotos reales en un iPhone y dos teléfonos Android, y metadatos de la imagen decididos (DP-27).
☐ Documento de seguridad, protocolo de actuación y procedimiento de incidentes revisados (OL-19 a OL-21, RF-46, RNF-18).
☐ Prueba de restauración de respaldos superada y servidor endurecido antes de cargar datos reales (RNF-09, DP-08).
☐ Asesor legal designado.
☐ Protección de cédulas y datos personales aceptada.
☐ Criterios de aceptación suficientes; matriz de trazabilidad revisada.
☐ Dependencias, riesgos y decisiones pendientes asignados.
☐ Aprobación formal del propietario del producto.

## Registro de aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
| Responsable de requisitos | brandonC-developer (misma persona; sin revisión independiente) | Pendiente | Pendiente |
| Responsable técnico | brandonC-developer | Pendiente | Pendiente |
| Asesor legal | Por designar | Pendiente | Pendiente |

**Estado actual:** línea base propuesta para revisión. No debe describirse como "oficialmente aprobada" hasta completar el registro de aprobación.

# 15. Próxima fase: arquitectura y diseño técnico

Tras aprobar los requisitos y resolver los bloqueos relevantes, se producen artefactos separados y enlazados a esta ERS: documento de arquitectura (DAS-SGA-001), modelo lógico y físico de datos, diseño técnico con las interfaces (la versión 1 no tiene API pública; ver DAS, ADR-022, y el diseño técnico DTE-SGA-001), diseño del proceso de obligaciones y notificaciones, plan de verificación y pruebas, y plan de implementación por entregas. La ERS define **qué** debe cumplir el sistema; el DAS describe **cómo** se organiza la solución.

# 16. Base metodológica y referencias

Las referencias orientan el método de documentación; no significan que el proyecto haya sido auditado ni certificado.

1. ISO/IEC/IEEE 29148:2018 — Requirements engineering. https://www.iso.org/standard/72089.html
2. NASA Systems Engineering Handbook, apéndices C, D y E. https://www.nasa.gov/reference/system-engineering-handbook-appendix/
3. Ley 7527, Ley General de Arrendamientos Urbanos y Suburbanos (SCIJ, norma 23655).
4. Ley 8968, Protección de la Persona frente al Tratamiento de sus Datos Personales. https://www.sutel.go.cr/sites/default/files/normativas/ley_proteccion_de_la_persona_frente_al_tratamiento_de_sus_ley_8968.pdf
4b. Reglamento a la Ley 8968, Decreto 37554-JP (copia del Archivo Nacional, con reformas del decreto 40008 de 2016; lectura parcial: arts. 3, 32, 34 a 39 y 44). https://www.archivonacional.go.cr/web/normativa/reglamento37554.docx
5. NIST SP 800-63B-4, Digital Identity Guidelines (autenticación, sesiones, recuperación). https://pages.nist.gov/800-63-4/sp800-63b/aal/
6. W3C, Working with Time and Timezones (Group Draft Note, 2025). https://www.w3.org/TR/timezone/
7. OWASP File Upload Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
8. Meta, WhatsApp Business Platform, mensajes (canal futuro, fuera de la v1). https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages
8b. OWASP, Authentication Cheat Sheet y Multifactor Authentication Cheat Sheet ("Changing MFA Factors"); NIST SP 800-63B-4, sec. 4.6 (avisos de recuperación). Leídos por resumen; ver diseño técnico DTE-SGA-001 v0.3, sec. 2 y 3.6. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
8c. Ley 8968, art. 7, y Reglamento 37554-JP, arts. 21 y 22 (derecho de acceso); copias .docx del Archivo Nacional, leídas en esos artículos; ver DTE-SGA-001 v0.5, sec. 3.4.1.
9. Fuentes de investigación completas: `actualizaciones/2026-10-17_ERS-v1.5_DAS-v0.4/CUESTIONARIO_CIERRE_ERS-DAS_recomendaciones_v1.md`.

---

**Fin del documento — ERS-SGA-001, versión 1.14 (borrador no aprobado).**

# Anexo A. Estado de las respuestas de las rondas de aclaración

Este anexo registra respuestas del solicitante y no sustituye la aprobación formal del propietario.

| Pregunta | Respuesta registrada | Tratamiento en v1.8 |
|---|---|---|
| P1, R1, R2 | Prorratear períodos parciales por días reales con redondeo al colón. | Acotado al último período (RN-12); prorrateo general diferido. |
| P2, P8, P14 | Abonos manuales con saldo visible; notificación por abono contradictoria. | Abonos y saldo incorporados; no se notifica cada abono (DP-10). |
| P3, P9 | Un depósito por contrato; máximo ordinario de tres abonos. | RN-27, RF-30. |
| P4 | Un inquilino por contrato. | RN-01. |
| P5, P13 | El administrador define el período por contrato. | Período por aniversario (RN-03). |
| P6, P17 | Fecha real retroactiva sin observación obligatoria. | RN-29, RF-34. |
| P7 | Fecha mensual acordada; si termina antes, prorratear. | RN-12. |
| P10, P16 | Actualizar obligaciones no pagadas, incluso vencidas. | **Modificado:** reajuste solo prospectivo; corrección retroactiva (RF-10). |
| P11 | Sin enunciado ni respuesta recuperables. | Cerrada por el solicitante el 17-oct-2026 (DP-14); si reaparece, se reabre con un ID nuevo. |
| P12 | Cerrar contrato y crear uno nuevo al cambiar de inquilino. | RF-36, RN-28. |
| P15 | Excepción administrativa para abonos adicionales al depósito. | Confirmación con motivo (RF-30). |
| R3 | Bloquear abonos que superen el saldo del depósito. | RF-30. |
| R4 | Varios acuerdos o calendarios para un depósito. | **Retirado de v1** (Q-15c). |
| R5 | Devoluciones y deducciones fuera del alcance inicial. | Se mantiene. |
| R6 | Zona horaria a nivel de organización. | RF-33. |
| R7 | Bloquear solapamientos incompatibles. | RN-02 (definición precisa). |
| Q-17 | Comprobante de pago diferido. | **Incluido por instrucción de cubrir obligaciones legales** (RF-37). **v1.9:** el solicitante lo difiere de nuevo a una fase posterior (HT-02, 21-oct-2026), con recibo de papel fuera del sistema (RF-47). |
