# Especificación de Requisitos de Software (ERS)

**Sistema de Gestión de Alquileres**

**Identificador:** ERS-SGA-001
**Versión:** 1.8 — Borrador para revisión
**Estado:** Borrador; pendiente de validación legal y aprobación formal
**Fecha:** 17 de octubre de 2026
**Idioma:** Español
**Configuración regional por defecto:** colones costarricenses (CRC) y dólares estadounidenses (USD) como monedas admitidas; zona horaria `America/Costa_Rica`.

**Nota de control:** Esta versión incorpora las respuestas del solicitante a la ronda de validación del 17 de octubre de 2026 (puntos Q-1 a Q-33 del documento `actualizaciones/2026-10-17_ERS-v1.5_DAS-v0.4/CUESTIONARIO_CIERRE_ERS-DAS_recomendaciones_v1.md`) y las obligaciones legales identificadas en la Ley 7527 y la Ley 8968. Las respuestas del solicitante no equivalen a aprobación formal del propietario del negocio. **Este documento no es asesoría legal**: las obligaciones de la sección 3 deben ser validadas por un abogado antes de aprobar la línea base. El documento no certifica conformidad con ninguna norma ISO/IEEE ni autoriza iniciar la implementación.

# Control del documento

| Campo | Valor |
|---|---|
| Nombre | Especificación de Requisitos de Software — Sistema de Gestión de Alquileres |
| Identificador | ERS-SGA-001 |
| Versión | 1.8 |
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
| **1.8** | **Cierre de DP-14 (P11 retirada por no recuperable), DP-23 (una sola persona ocupa los tres roles, identificada como brandonC-developer; el asesor legal sigue sin designar) y DP-26 (hora local más zona; el instante se calcula al ejecutar). H4: serie global de comprobantes, provisional hasta DP-20. Lectura del Reglamento 37554-JP (Archivo Nacional): nuevas obligaciones legales OL-19 a OL-21, requisito RF-46 (incidentes de seguridad) y RNF-18 (documentación de seguridad), criterios CA-56 y CA-57. Todo pendiente de abogado (DP-17).** Correcciones de QA del 17-oct-2026: entidad Incidente de seguridad en 7.1, alcance 2.3, lista de revisión y referencias; ver actualización 2026-10-17e.** |

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
- **Notificación WhatsApp:** mensaje enviado por un proveedor compatible; que el proveedor lo acepte no implica entrega ni lectura.
- **Titular de datos:** persona física cuyos datos personales se tratan (el inquilino).
- **Verificación:** comprobar que el producto cumple sus requisitos.
- **Validación:** comprobar que el producto satisface las necesidades del usuario y del negocio.

# 2. Contexto, objetivos y alcance

## 2.1 Objetivo general

Permitir al administrador registrar inquilinos y sus documentos de identificación, administrar propiedades y contratos, controlar obligaciones mensuales de alquiler, registrar abonos y pagos completos, visualizar el saldo pendiente, emitir comprobantes de pago, y consultar vencimientos en un calendario con recordatorios anticipados y alertas diarias de atraso, cumpliendo las obligaciones legales aplicables al arrendamiento y al tratamiento de datos personales.

## 2.2 Objetivos específicos

1. Mantener fichas de inquilinos con datos personales y fotografía de la cédula, con consentimiento informado.
2. Asociar cada contrato con un único inquilino y una única propiedad.
3. Generar como máximo una obligación por contrato y período, sin duplicados.
4. Registrar abonos y pagos completos, manteniendo visible el saldo pendiente.
5. Registrar la fecha real de recepción y conservar la fecha/hora en que el movimiento fue ingresado.
6. Consultar pagos y saldos en un calendario con filtros por inquilino y estado.
7. Configurar recordatorios anticipados y emitir alertas diarias de atraso.
8. Proteger datos personales, atender los derechos del titular y conservar trazabilidad de los cambios relevantes.
9. Emitir comprobantes de pago y aplicar las reglas legales de plazos, reajustes, garantía y moneda.

## 2.3 Incluido en la primera versión

- Registro, consulta, edición y desactivación lógica de inquilinos, con registro de consentimiento.
- Carga y consulta autorizada de la fotografía de cédula (frente obligatorio, reverso opcional).
- Registro de propiedades con estado derivado.
- Registro, modificación controlada (reajuste y corrección) y finalización de contratos.
- Monto mensual fijo por contrato, en CRC o USD.
- Período de alquiler por aniversario del día de inicio; vencimiento por día fijo con ajuste al último día del mes.
- Días de gracia por contrato.
- Generación de obligaciones 30 días antes de cada período.
- Prorrateo del último período cuando el contrato termina antes de completarlo.
- Registro de abonos y pagos completos con saldo derivado; anulación de movimientos con motivo.
- Pagos en moneda distinta de la del contrato con tipo de cambio ingresado manualmente.
- Comprobante de pago numerado.
- Saldo de apertura para contratos con historia previa.
- Depósito de garantía por contrato con abonos y saldo.
- Estados pendiente, vencida, pagada y anulada.
- Calendario mensual con filtros por inquilino y estado.
- Notificaciones web y WhatsApp; un recordatorio anticipado configurable; resumen diario de alertas de atraso.
- Una única cuenta administradora con autenticación multifactor.
- Atención de solicitudes del titular de datos; retención y eliminación de datos personales.
- Registro de auditoría de operaciones críticas y del acceso a cédulas.
- Registro de incidentes de seguridad con la fecha límite de aviso a titulares y a la Agencia (RF-46).

## 2.4 Fuera del alcance inicial

- Cobro o procesamiento automático de dinero, integración bancaria y conciliación automática.
- Consulta automática de tipos de cambio; conversión automática entre monedas.
- Cálculo automático de intereses, multas o penalizaciones.
- Prorrateo general de períodos al inicio del contrato y de meses intermedios; queda diferido a una versión futura (P1/R1/R2 y Q-1).
- Facturación electrónica o contabilidad completa.
- Acceso de inquilinos a un portal propio; notificaciones a inquilinos.
- Varias cuentas humanas con roles diferenciados.
- Correo electrónico y SMS como canales de notificación.
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
- El envío de WhatsApp depende de un proveedor externo aún no elegido.
- **S-01:** el vencimiento de una obligación cae dentro de su período (RN-05). Confirmado por el solicitante el 17-oct-2026 (DP-24).
- **S-02:** el destino del contrato (vivienda u otro) determina qué reglas legales se advierten; ver OL-06.

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
| Proveedor de WhatsApp | Acepta, procesa y reporta los estados disponibles de los mensajes. |

El inquilino no tiene acceso al sistema en esta versión. Las notificaciones se dirigen solo al administrador. Los datos de contacto del inquilino se capturan como parte de la ficha, pero no se usan para notificar en esta versión.

# 5. Requisitos funcionales

## 5.1 Gestión de inquilinos

**RF-01 — Registrar inquilino.** El sistema deberá permitir registrar nombre completo, tipo de documento (cédula, DIMEX, pasaporte u otro), número de documento, teléfono, correo electrónico y fotografía de la cédula (frente obligatorio, reverso opcional). Deberá advertir cuando exista otro inquilino activo con el mismo tipo y número de documento.

**RF-02 — Validar información.** El sistema deberá validar campos obligatorios, formato de contacto y archivo antes de aceptar el registro. Formatos permitidos: JPEG y PNG, hasta 5 MB. Deberá verificar el tipo real del archivo y no solo el tipo declarado por el navegador.

**RF-03 — Consultar y actualizar al inquilino.** El administrador deberá poder buscar, consultar y actualizar la ficha. Los cambios de identificación se validan y quedan auditados.

**RF-04 — Desactivar inquilino.** El sistema deberá permitir desactivar a un inquilino sin eliminar contratos, obligaciones ni historial. Deberá bloquear la desactivación si el inquilino tiene un contrato vigente o saldos pendientes, y permitir reactivarlo.

**RF-05 — Consultar ficha de inquilino.** El sistema deberá mostrar datos de contacto, contrato vigente cuando exista, obligaciones e historial asociado, respetando las restricciones de acceso a documentos.

## 5.2 Propiedades y contratos

**RF-06 — Registrar propiedad.** El sistema deberá permitir registrar una propiedad con identificador único, descripción y dirección. Su estado se deriva: *disponible* u *ocupada* (según tenga o no un contrato vigente), más *inactiva*, que marca el administrador.

**RF-07 — Crear contrato.** El sistema deberá permitir asociar un único inquilino con una única propiedad y registrar: destino (vivienda u otro), fecha de inicio (fecha de entrega del bien), fecha de fin si existe, monto mensual fijo, moneda (CRC o USD), día de vencimiento de 1 a 31 (por defecto, el día de inicio del período), días de gracia (7 por defecto) y, cuando corresponda, el depósito de garantía. El día de inicio ancla el período de alquiler (RN-03). **[Legal OL-01, OL-08, OL-10]** Deberá advertir, sin bloquear, cuando la vigencia pactada sea inferior a tres años.

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

**RF-42 — Avisar vencimiento de contrato.** El sistema deberá notificar al administrador 120 días antes de la fecha de fin de un contrato. Si la fecha de fin pasa sin que el contrato se cierre o se renueve, el contrato pasará al estado *por decidir* y el sistema continuará generando obligaciones hasta que el administrador lo cierre o lo renueve. **[Legal OL-09]**

**RF-43 — Registrar saldo de apertura.** Para un contrato cuyo inicio es anterior a la fecha de carga en el sistema, el administrador deberá poder registrar un saldo de apertura con fecha y auditoría. El saldo de apertura debe incluir lo adeudado por todos los períodos iniciados hasta la fecha de apertura; las obligaciones regulares se generan desde el primer período que inicia después de esa fecha. Las alertas de atraso comienzan desde la fecha de carga y no retroactivamente (confirmado por el solicitante el 17-oct-2026; DP-25).

## 5.3 Obligaciones y movimientos

**RF-11 — Generar obligaciones por período.** El sistema deberá generar la obligación de cada período 30 días antes de que inicie, mientras el contrato esté *futuro*, *vigente* o *por decidir*. Usará el monto, la moneda y la regla de vencimiento aplicables al período. El proceso es idempotente.

**RF-12 — Evitar duplicados.** El sistema deberá impedir más de una obligación por contrato y período, incluso si el proceso se ejecuta repetidamente o en paralelo.

**RF-13 — Registrar pago completo.** El administrador deberá poder registrar el pago que completa el saldo de una obligación como un movimiento por el saldo restante, con fecha real de recepción, medio de pago y observación opcional. No se exige comprobante adjunto. Al llegar el saldo a cero, la obligación pasa a *pagada* automáticamente.

**RF-14 — Determinar estado de obligación.** El sistema deberá derivar el estado de cada obligación a partir de su saldo, su fecha límite y la fecha local de la zona horaria de la organización: *pagada* si el saldo es cero; *vencida* si el saldo es mayor que cero y se superó la fecha límite de pago; *pendiente* en cualquier otro caso; *anulada* si fue anulada. **[Legal OL-01]**

**RF-15 — Consultar historial.** El sistema deberá permitir consultar obligaciones por inquilino, contrato, período y estado, mostrando importe exigible, vencimiento, saldo, estado y fecha de pago si existe.

**RF-16 — Anular movimiento.** El sistema deberá permitir anular un movimiento con motivo obligatorio. El movimiento original se conserva y se agrega una reversión. Se recalculan saldo y estado; si la obligación vuelve a *vencida*, las alertas se reanudan el día siguiente. Los recordatorios ya emitidos no se reenvían. Una corrección de importe o de fecha se realiza anulando el movimiento y registrando uno nuevo. **[Legal OL-04]**

**RF-34 — Registrar abono de alquiler.** El administrador deberá poder registrar uno o varios abonos asociados a una obligación, con importe positivo, fecha real de recepción, medio de pago (efectivo, transferencia, cheque u otro) y observación opcional. La fecha real no puede ser futura (según la zona de la organización) ni anterior a la fecha de inicio del contrato. El sistema conserva la fecha real y la fecha/hora de registro. Un abono no puede dejar saldo negativo. Para un cheque o título, la fecha real es la de recepción del efectivo. Cada envío lleva una clave de solicitud única: si el mismo envío se repite (doble clic o reintento), el sistema no crea otro movimiento y devuelve el ya registrado. **[Legal OL-04]**

**RF-35 — Calcular saldo de alquiler.** El sistema deberá calcular el saldo pendiente como importe exigible menos la suma de los movimientos válidos (no anulados). El saldo nunca es negativo.

**RF-37 — Emitir comprobante de pago.** El sistema deberá generar, por cada abono o pago, un comprobante numerado de forma consecutiva y sin huecos (la numeración no puede depender de un mecanismo que pierda números al fallar una operación), imprimible y reimprimible, con contrato, inquilino, período, importe, moneda, fecha real, medio de pago y saldo resultante, y deberá conservar copia. Los comprobantes de movimientos anulados quedan marcados y no se renumeran. **[Legal OL-03]** *Nota: el solicitante difirió este requisito en la respuesta Q-17; se incluye por la instrucción de incorporar todas las obligaciones legales. El art. 58 admite otros procedimientos fehacientes de acreditación; confirmar con abogado (DP-20) y, si se difiere, registrar el riesgo.*

**RF-38 — Registrar pago en moneda distinta.** Cuando el pago se reciba en una moneda distinta de la del contrato, el sistema deberá registrar la moneda recibida, el tipo de cambio ingresado manualmente por el administrador y el importe equivalente en la moneda del contrato. El saldo se mantiene en la moneda del contrato. El sistema no consulta tipos de cambio. **[Legal OL-05]**

## 5.4 Calendario

**RF-17 — Mostrar calendario mensual.** El sistema deberá mostrar las obligaciones en un calendario mensual e identificar inquilino, fecha de vencimiento y estado.

**RF-18 — Filtrar por inquilino.** El administrador deberá poder filtrar el calendario por inquilino y quitar el filtro conservando el mes consultado.

**RF-19 — Filtrar por estado.** El sistema deberá permitir filtrar por pendiente, vencida, pagada y anulada. Las anuladas no se muestran por defecto.

**RF-20 — Consultar detalle de evento.** Al seleccionar un evento, el sistema deberá mostrar contrato, período, importe exigible, vencimiento, fecha límite, saldo, estado, movimientos y observación.

## 5.5 Notificaciones

**RF-21 — Configurar recordatorios anticipados.** El administrador deberá poder configurar la anticipación del recordatorio en días antes del vencimiento (3 por defecto) y añadir hasta tres anticipaciones. Un cambio se aplica a las notificaciones futuras aún no procesadas, las reprograma y no genera duplicados. Si la obligación tiene abonos, el recordatorio indica el saldo pendiente.

**RF-22 — Generar alertas diarias de atraso.** El proceso diario deberá registrar una alerta por cada obligación *vencida* y por día. Las alertas se detienen cuando la obligación pasa a *pagada* o *anulada*. Si el proceso no se ejecutó algún día, solo se emite la alerta del día actual.

**RF-23 — Notificar por canales aprobados.** El sistema deberá admitir notificaciones web persistentes (estados nueva, leída y archivada, sin borrado) y envío de WhatsApp mediante un proveedor compatible. Las alertas de atraso se envían por WhatsApp en un **único resumen diario** que lista todas las obligaciones vencidas. El sistema no declarará entregado un mensaje que solo fue aceptado para procesamiento.

**RF-24 — Registrar intentos de notificación.** El sistema deberá conservar obligación asociada, canal, destinatario, fecha programada, fecha de intento, resultado, intentos y los identificadores y estados que exponga el proveedor. Ante un fallo de envío, hará hasta cinco intentos con espera creciente y aleatoria; después, el resultado es *fallido* y la notificación web persiste.

**RF-25 — Cancelar notificaciones futuras.** Cuando una obligación pase a *pagada* o *anulada*, el sistema deberá cancelar sus recordatorios y alertas futuros. Las notificaciones anteriores permanecen en el historial.

**RF-44 — Minimizar datos en mensajes externos.** Los mensajes enviados por WhatsApp no deberán incluir número de documento ni imagen alguna, y deberán limitar los datos del inquilino al mínimo necesario (por ejemplo, el alias de la propiedad y el importe). Los mensajes serán plantillas aprobadas. El destinatario es el teléfono del administrador, cuya aceptación de recibir mensajes queda registrada. **[Legal OL-17]**

## 5.6 Acceso y auditoría

**RF-26 — Autenticar administrador.** El sistema deberá requerir autenticación multifactor antes de permitir acceso a funciones administrativas y documentos privados.

**RF-27 — Administrar la cuenta.** La primera versión opera con una única cuenta administradora, con:
- contraseña de al menos 15 caracteres, sin reglas de composición ni cambio periódico obligatorio;
- un segundo factor de código de un solo uso (TOTP) obligatorio;
- sesión con cierre total a las 24 horas y por inactividad de 1 hora;
- códigos de recuperación de un solo uso, entregados al activar el segundo factor;
- notificación al administrador ante cada recuperación de acceso y cada emisión de nuevos códigos.

**RF-28 — Auditar operaciones críticas.** El sistema deberá registrar cambios relevantes en inquilinos, contratos, obligaciones, movimientos, anulaciones, depósitos y configuración de notificaciones, con actor, fecha/hora de registro, operación, campos modificados y valores anteriores y nuevos de los campos **no personales** (estados, importes, fechas, motivos). Para los campos personales (nombre, número de documento, teléfono, correo, imagen de cédula) solo registrará **que cambiaron**, nunca su valor. No almacenará secretos ni documentos completos. Así la auditoría no retiene datos que RF-41 manda desasociar. **[Legal OL-14]** *Nota: reescritura de la versión 1.6 (que pedía valores anteriores y nuevos sin distinguir); el efecto sobre la conservación de la auditoría se valida con abogado (DP-18).*

**RF-45 — Auditar acceso a cédulas.** El sistema deberá registrar cada consulta o descarga de una fotografía de cédula (actor, fecha/hora, inquilino), sin guardar la imagen en el registro. **[Legal OL-16]**

**RF-46 — Gestionar incidentes de seguridad.** El sistema deberá permitir registrar un incidente de seguridad (fecha y hora en que ocurrió y en que se conoció, naturaleza, datos comprometidos, acciones inmediatas, titulares afectados), calcular la fecha límite de aviso a los titulares y a la Agencia de cinco días hábiles y dejar constancia de cada aviso emitido y de la revisión posterior. El sistema no detecta el incidente: lo registra el administrador. **[Legal OL-19]** *Lectura propia del Reglamento 37554-JP, arts. 38 y 39; el momento desde el que corre el plazo y la obligación de avisar a la Agencia se validan con abogado (DP-17).*

## 5.7 Depósito de garantía

**RF-29 — Definir depósito de garantía.** El sistema deberá permitir registrar en el contrato el importe total del depósito, la moneda y una fecha límite acordada opcional, junto con notas. Un contrato tiene como máximo un depósito. El importe total solo se edita si no hay abonos, o mediante corrección auditada nunca inferior a lo abonado. **[Legal OL-11, OL-12]** Deberá advertir, sin bloquear, cuando el importe supere una mensualidad de renta.

**RF-30 — Registrar abonos al depósito.** El administrador deberá poder registrar abonos con importe, fecha real de recepción, medio de pago y observación opcional. El sistema bloquea importes nulos o negativos y abonos que superen el saldo. El flujo ordinario admite hasta tres abonos no anulados; para registrar más, el administrador confirma explícitamente una excepción con **motivo obligatorio**, que queda auditada. La moneda del abono debe ser la del depósito, salvo lo previsto en RF-38.

**RF-31 — Calcular saldo del depósito.** El sistema deberá calcular el saldo como importe total menos la suma de abonos válidos, y mostrar el estado pendiente, parcialmente pagado o completado.

**RF-32 — Consultar historial del depósito.** El sistema deberá mostrar importe acordado, abonos, fechas, observaciones, saldo, anulaciones y auditoría. Cuando el contrato esté finalizado, mostrará la etiqueta "contrato cerrado, liquidación manual". El depósito no genera recordatorios ni alertas en esta versión.

## 5.8 Configuración regional

**RF-33 — Configurar moneda y zona horaria.** El sistema deberá ofrecer CRC y `America/Costa_Rica` como valores predeterminados y admitir USD como segunda moneda por contrato. La zona horaria se configura solo a nivel de organización. Los vencimientos son fechas de calendario sin hora; las marcas de registro se almacenan en UTC y se presentan en la zona de la organización.

## 5.9 Datos personales

**RF-39 — Informar y registrar consentimiento.** Antes de guardar datos personales o la fotografía de cédula, el sistema deberá presentar al administrador el texto informativo con los ocho puntos del art. 5 de la Ley 8968 y registrar el consentimiento del inquilino (fecha, versión del texto y medio, físico o electrónico). El sistema deberá permitir registrar la revocación sin efecto retroactivo. **[Legal OL-13]**

**RF-40 — Atender solicitudes del titular.** El sistema deberá permitir registrar solicitudes de acceso, rectificación, actualización o supresión de un titular, con fecha de recepción y fecha límite de cinco días hábiles, y marcar su resolución. Deberá poder exportar los datos del titular en forma legible. La atención es gratuita. Una solicitud de supresión se atiende salvo que exista una obligación legal de conservar el dato (DP-18). **[Legal OL-15]**

**RF-41 — Retener y eliminar datos personales.** El sistema deberá conservar la fotografía de cédula mientras el contrato esté vigente y hasta cinco años después del fin del último contrato del inquilino (plazo configurable, nunca superior a diez años desde los hechos). Vencido el plazo, el sistema deberá eliminar la fotografía y desasociar los datos personales del inquilino, conservando los movimientos financieros sin datos de identificación. Deberá avisar al administrador antes de ejecutar la eliminación. **[Legal OL-14]**

# 6. Reglas de negocio

| ID | Regla |
|---|---|
| RN-01 | Cada contrato corresponde a un único inquilino y una única propiedad. |
| RN-02 | Una propiedad no puede tener dos contratos que compartan algún día. Cada contrato ocupa el intervalo `[fecha_inicio, fecha_fin]` con ambas fechas inclusive; sin fecha de fin es abierto. El relevo exige que el nuevo inicio sea al menos el día siguiente al fin anterior. |
| RN-03 | Un período de alquiler va desde un día X hasta el día anterior al mismo día X del mes siguiente. El día X es el día de `fecha_inicio`; si el mes no tiene ese día, el período inicia el último día de ese mes. Ejemplo: inicio el 10 de enero; período 1: 10 ene–9 feb; período 2: 10 feb–9 mar. El día 10 de febrero pertenece al segundo período. **[OL-01, OL-10]** |
| RN-04 | Se genera una sola obligación por contrato y período. |
| RN-05 | El vencimiento de una obligación es la fecha del `día de vencimiento` en el mes en que inicia el período (o el último día de ese mes si no existe); si esa fecha es anterior al inicio del período, se usa el mes siguiente; si esa fecha excede el último día del período, se usa el último día del período. Así el vencimiento siempre cae dentro del período. Confirmada por el solicitante (DP-24); el día de vencimiento por defecto es el día de inicio del período. |
| RN-06 | La fecha límite de pago es el vencimiento más los días de gracia del contrato (7 por defecto; el art. 58 no distingue destino en el texto leído). **[OL-01]** |
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
| RN-25 | La primera versión tiene una única cuenta administradora; no existen roles adicionales. |
| RN-26 | Un depósito superior a una mensualidad genera una advertencia; la garantía debe responder por alquileres y demás obligaciones del contrato. **[OL-11, OL-12]** |
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
| Inquilino | id, nombre, tipo y número de documento, teléfono, correo, referencias privadas a las fotografías, estado, consentimiento (fecha, versión, medio, revocación), fechas de creación y modificación. |
| Propiedad | id, descripción, dirección, marca de inactiva. |
| Contrato | id, inquilino_id, propiedad_id, destino, fecha_inicio, fecha_fin opcional, moneda, marca de anulado. El monto, el día de vencimiento y los días de gracia viven en la Condición del contrato. |
| Condición del contrato | id, contrato_id, monto_mensual, día_vencimiento, días_gracia, fecha efectiva, tipo (inicial, reajuste, corrección), fecha de notificación, porcentaje, tope digitado y fuente (reajustes de vivienda), motivo (correcciones), fecha de registro. Conserva el historial exigido por RF-10. |
| Obligación | id, contrato_id, período (inicio, fin), fecha_vencimiento, fecha_límite, importe_inicial, moneda, condición aplicada, datos del cálculo, anulación (motivo, fecha) y tipo (regular, apertura). El importe exigible vigente se deriva del importe inicial y sus ajustes. |
| Ajuste de obligación | id, obligacion_id, tipo (reajuste, corrección, prorrateo del último período, ajuste manual), importe con signo, condición que lo originó, motivo, fecha de registro. Inmutable. |
| Movimiento | id, tipo (abono de alquiler, abono de depósito, reversión), obligación o depósito asociado, importe, moneda recibida, tipo de cambio y equivalente cuando aplique, fecha real, fecha/hora de registro, medio de pago, observación, clave de solicitud, anulación (motivo, referencia al movimiento original), comprobante. |
| Organización | id, nombre y dirección del responsable de la base de datos, zona horaria, hora del proceso diario, teléfono y aceptación de WhatsApp del administrador, anticipaciones de recordatorio, años de retención de fotografías, días de gracia por defecto. Una sola fila en v1. |
| Comprobante | id, número consecutivo, movimiento_id, contenido, estado (vigente, anulado). |
| Depósito de garantía | id, contrato_id, importe_total, moneda, fecha límite acordada opcional, notas. |
| Notificación | id, obligación o contrato, canal, tipo, destinatario, fecha programada, intentos, resultado, referencia del proveedor, estado web (nueva, leída, archivada). |
| Solicitud del titular | id, inquilino_id, tipo, fecha de recepción, fecha límite, resolución. |
| Auditoría | id, entidad, registro, actor, acción, fecha, campos modificados y valores anteriores y nuevos solo de campos no personales. |
| Incidente de seguridad | id, fecha de ocurrencia y de conocimiento, naturaleza, datos comprometidos (descripción, sin copiarlos), acciones inmediatas, fecha límite de aviso, estado. Cada aviso emitido (a un titular o a la Agencia) se guarda con fecha, destinatario y contenido mínimo. |

El saldo de una obligación y el de un depósito, el estado de una obligación, de un contrato y de una propiedad **se derivan** y no se almacenan como fuente de verdad.

## 7.2 Relaciones

- Un inquilino puede tener varios contratos a lo largo del tiempo.
- Cada contrato referencia exactamente un inquilino y una propiedad.
- Un contrato tiene muchas obligaciones y, cuando corresponda, un depósito.
- Una obligación tiene muchos movimientos; un depósito tiene muchos movimientos.
- Un movimiento tiene como máximo un comprobante.
- Las operaciones relevantes producen registros de auditoría.

## 7.3 Restricciones de integridad

1. Identificadores únicos en todas las entidades.
2. Claves foráneas válidas entre contrato, inquilino y propiedad.
3. Monto mensual mayor que cero; día de vencimiento entre 1 y 31.
4. Unicidad de contrato y período en obligaciones.
5. Ausencia de días compartidos entre contratos de una propiedad.
6. Los movimientos no se borran ni se editan; se anulan.
7. Numeración de comprobantes única, consecutiva y sin huecos, asignada en la misma transacción que el movimiento.
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
| RNF-05 | Confiabilidad | Un fallo de WhatsApp no impide consultar ni registrar movimientos ni elimina la notificación web persistida. |
| RNF-06 | Trazabilidad | Los cambios relevantes de contrato, movimientos y configuración quedan auditados. |
| RNF-07 | Usabilidad | Los formularios validan entradas y muestran mensajes comprensibles. |
| RNF-08 | Rendimiento | Las consultas habituales (listados, calendario mensual, ficha) responden en menos de 2 s en el percentil 95, con hasta 50 propiedades y un administrador. Objetivo a validar, no medición. |
| RNF-09 | Recuperación | Un respaldo completo al día (pérdida tolerable de datos, RPO, de hasta 24 horas); recuperación del servicio (RTO) en hasta 24 horas; retención de respaldos de 35 días; prueba de restauración antes de producción y cada 3 meses, que abarque base de datos, archivos, contratos, movimientos, comprobantes y fotografías. Los respaldos se copian a otro lugar, cifrados. Valores de diseño elegidos por el solicitante (DP-07, 17-oct-2026), sin fuente externa. |
| RNF-10 | Compatibilidad | La interfaz funciona en las dos últimas versiones mayores de Chrome, Edge, Firefox y Safari, en escritorio y móvil. |
| RNF-11 | Mantenibilidad | Las responsabilidades de inquilinos, contratos, obligaciones, movimientos, calendario y notificaciones se mantienen separadas conceptualmente. |
| RNF-12 | Configuración regional | Fechas dd/mm/aaaa; moneda por contrato; fechas y tareas programadas interpretadas en la zona de la organización. Las tareas programadas se guardan como fecha y hora locales con la zona, y el instante se calcula al ejecutar (DP-26). |
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

**CA-01 — Registro de inquilino.** *Dado* un administrador autenticado, *cuando* registra los campos obligatorios, el consentimiento y el frente de la cédula en formato permitido, *entonces* se guarda el inquilino con identificador único. Si falta un campo, el consentimiento o el archivo no es válido, se muestra el error y no se guarda un registro incompleto.

**CA-25 — Documento duplicado.** *Dado* un inquilino activo con tipo y número de documento, *cuando* se intenta registrar otro con los mismos valores, *entonces* el sistema advierte del duplicado antes de guardar.

**CA-11 — Protección de cédula.** *Dado* un visitante sin autenticación válida, *cuando* intenta consultar una fotografía de cédula, *entonces* se deniega y el archivo no se recupera por una URL pública.

**CA-26 — Auditoría de acceso a cédula.** *Dado* un administrador autenticado, *cuando* consulta una fotografía de cédula, *entonces* queda un registro con actor y fecha/hora, sin la imagen.

**CA-27 — Solicitud del titular.** *Dado* una solicitud de acceso recibida un lunes, *cuando* se registra, *entonces* el sistema fija como fecha límite cinco días hábiles después y permite exportar los datos del titular.

**CA-28 — Retención.** *Dado* un contrato finalizado hace más de cinco años, *cuando* el proceso de retención se ejecuta tras el aviso al administrador, *entonces* se elimina la fotografía, se desasocian los datos personales y se conservan los movimientos sin datos de identificación.

**CA-29 — Desactivar con contrato vigente.** *Dado* un inquilino con contrato vigente o saldos pendientes, *cuando* se intenta desactivar, *entonces* el sistema lo bloquea.

## Contratos y obligaciones

**CA-02 — Creación de contrato.** *Dado* un inquilino y una propiedad disponible, *cuando* se crea un contrato con vigencia, monto válido y día de vencimiento válido, *entonces* queda registrado; se rechazan datos incoherentes y los solapamientos. Si la vigencia pactada es menor a tres años, se muestra una advertencia sin bloquear.

**CA-24 — Sustitución de inquilino.** *Dado* un contrato cuyo fin es el 9 de marzo, *cuando* se registra un nuevo contrato para la misma propiedad con inicio el 9 de marzo, *entonces* el sistema lo rechaza; con inicio el 10 de marzo lo acepta. Ambos contratos conservan su historial.

**CA-03 — Generación mensual y mes corto.** *Dado* un contrato de ₡180.000 con inicio el 10 de enero y vencimiento el día 31, *cuando* se generan las obligaciones, *entonces* los períodos son 10 ene–9 feb, 10 feb–9 mar y 10 mar–9 abr, y los vencimientos 31 de enero, 28 de febrero (29 en año bisiesto) y 31 de marzo. Ejecutar de nuevo el proceso no crea duplicados.

**CA-30 — Generación anticipada.** *Dado* un período que inicia el 10 de abril, *cuando* el proceso diario corre el 11 de marzo, *entonces* genera la obligación; el 10 de marzo aún no.

**CA-14 — Último período prorrateado.** *Dado* un período 10 mar–9 abr, un importe de ₡180.000 y fin de contrato el 25 de marzo, *cuando* se registra el fin, *entonces* el importe es ₡92.903 (16 de 31 días, redondeo al colón entero), con el cálculo registrado; los demás períodos no se prorratean.

**CA-31 — Fin de contrato con obligaciones futuras.** *Dado* un contrato con obligaciones futuras sin movimientos, *cuando* se registra su fecha de fin, *entonces* esas obligaciones quedan anuladas con auditoría y no generan alertas.

**CA-32 — Contrato por decidir.** *Dado* un contrato cuya fecha de fin expira sin cierre ni renovación, *cuando* corre el proceso diario, *entonces* el contrato pasa a *por decidir* y continúa generando obligaciones; 120 días antes del fin ya se había notificado al administrador.

## Movimientos y estados

**CA-04 — Registro de pago completo.** *Dado* una obligación con saldo pendiente, *cuando* el administrador registra el movimiento por el saldo con fecha real válida, *entonces* el saldo es cero, la obligación pasa a *pagada*, se cancelan los avisos futuros y se genera el comprobante. Una fecha inválida produce un error sin guardar.

**CA-19 — Abono parcial.** *Dado* una obligación de ₡180.000, *cuando* se registra un abono de ₡60.000, *entonces* el saldo es ₡120.000 y la obligación no queda pagada. La fecha real y la fecha/hora de registro se conservan por separado.

**CA-20 — Completar con abonos.** *Dado* una obligación con saldo, *cuando* los abonos válidos igualan el importe exigible, *entonces* el saldo es cero y la obligación pasa a *pagada* sin paso adicional. Un abono que exceda el saldo se rechaza.

**CA-21 — Fecha retroactiva.** *Dado* un pago recibido antes del día de registro, *cuando* se ingresa una fecha real anterior válida (no anterior al inicio del contrato), *entonces* se acepta, se conserva la fecha/hora de registro y no se exige observación.

**CA-33 — Fecha no válida.** *Dado* una fecha real futura o anterior al inicio del contrato, *cuando* se intenta registrar, *entonces* el sistema la rechaza con un mensaje claro.

**CA-34 — Anulación de movimiento.** *Dado* un abono que dejó una obligación en *pagada*, *cuando* se anula con motivo, *entonces* el movimiento original se conserva con su reversión, el saldo se recalcula, el estado vuelve a *pendiente* o *vencida* y el comprobante queda marcado como anulado.

**CA-35 — Anulación de obligación.** *Dado* una obligación sin movimientos válidos, *cuando* se anula con motivo, *entonces* pasa a *anulada* y deja de generar alertas. Una obligación con movimientos válidos no puede anularse.

**CA-50 — Vencimiento dentro del período.** *Dado* un contrato con inicio el 31 de enero y día de vencimiento 30, *cuando* se genera la obligación del período 31 ene–27 feb, *entonces* el vencimiento es el 27 de febrero (último día del período) y no el 28.

**CA-51 — Tope de reajuste digitado.** *Dado* una vivienda en colones y un reajuste del 5 %, *cuando* el administrador digita un tope vigente del 3,2 % y la fuente "certificación del INEC", *entonces* el sistema advierte que el porcentaje supera el tope, permite guardar y conserva el tope y la fuente junto al reajuste. Sin tope ni fuente digitados, el sistema los exige antes de guardar un reajuste de vivienda.

**CA-36 — Vencimiento y gracia.** *Dado* una obligación con vencimiento el 5 de febrero y 7 días de gracia, *cuando* se evalúa el 12 de febrero, *entonces* está *pendiente*; el 13 de febrero, *vencida*. Un pago recibido el 10 de febrero no cambia el día de vencimiento de los siguientes períodos.

**CA-37 — Comprobantes consecutivos.** *Dado* tres movimientos registrados en secuencia, *cuando* se emiten sus comprobantes, *entonces* la numeración es consecutiva y única; anular el segundo no renumera el tercero.

**CA-38 — Pago en moneda distinta de la del contrato.** *Dado* un contrato en USD con saldo de $300, *cuando* el inquilino paga ₡150.000 y el administrador ingresa un tipo de cambio de ₡500, *entonces* el sistema registra la moneda recibida, el tipo de cambio y el equivalente de $300, y el saldo se mantiene en USD.

## Cambios de condiciones

**CA-12 — Reajuste.** *Dado* un contrato con período vigente 10 mar–9 abr, *cuando* se registra un reajuste notificado el 20 de marzo, *entonces* la fecha efectiva se normaliza al 10 de abril, las obligaciones anteriores mantienen su monto y las posteriores aplican el nuevo.

**CA-39 — Reajuste sobre el tope o en moneda extranjera.** *Dado* una vivienda con porcentaje de reajuste superior al tope informado, *cuando* se registra, *entonces* el sistema advierte sin bloquear. Si la vivienda tiene precio en USD, *entonces* rechaza el reajuste.

**CA-22 — Corrección con obligaciones no pagadas.** *Dado* un contrato con obligaciones pagadas, pendientes y vencidas no pagadas, *cuando* se registra una corrección con motivo y fecha efectiva, *entonces* las pagadas no cambian, las no pagadas afectadas se actualizan, y el historial permite reconstruir los valores anteriores y nuevos.

**CA-40 — Cambio por debajo de lo abonado.** *Dado* una obligación con ₡100.000 abonados, *cuando* una corrección fija su importe en ₡80.000, *entonces* el sistema bloquea el cambio y muestra el exceso de ₡20.000.

## Calendario

**CA-06 — Calendario general.** *Dado* obligaciones de varios inquilinos en un mes, *cuando* se abre el calendario, *entonces* se identifican vencimiento, inquilino y estado; los eventos coincidentes permiten consultar cada obligación.

**CA-07 — Filtro por inquilino.** *Dado* obligaciones de al menos tres inquilinos, *cuando* se selecciona uno, *entonces* solo se muestran las suyas; al retirar el filtro se recupera la vista general y se conserva el mes.

## Notificaciones

**CA-08 — Recordatorio configurable.** *Dado* una obligación pendiente y una anticipación de 3 días, *cuando* llega la fecha calculada, *entonces* se crea la notificación web y se programa el envío de WhatsApp si el canal está configurado; intento y resultado quedan registrados. Si la obligación tiene abonos, el aviso indica el saldo.

**CA-41 — Cambio de anticipación.** *Dado* recordatorios programados, *cuando* el administrador cambia la anticipación, *entonces* los recordatorios futuros aún no procesados se reprograman sin duplicados.

**CA-05 — Alerta diaria y resumen.** *Dado* tres obligaciones vencidas, *cuando* corre el proceso diario, *entonces* se registra una alerta por obligación y se envía un único resumen por WhatsApp con las tres. No hay duplicados por obligación y día; tras pagarse una obligación, no se producen nuevas alertas para ella.

**CA-42 — Proceso omitido.** *Dado* que el proceso no corrió dos días, *cuando* se reanuda, *entonces* emite solo la alerta del día actual.

**CA-09 — Fallo de WhatsApp.** *Dado* un rechazo del proveedor, *cuando* el sistema intenta enviar, *entonces* registra el resultado, reintenta hasta cinco veces con espera creciente y aleatoria, no cambia el estado del pago y conserva la notificación web. Distingue aceptación, entrega y lectura según los estados disponibles.

**CA-43 — Contenido mínimo.** *Dado* un resumen de WhatsApp, *cuando* se inspecciona su contenido, *entonces* no contiene número de documento ni imágenes.

**CA-44 — Abono sin notificación individual.** *Dado* un abono registrado, *cuando* se guarda, *entonces* el sistema actualiza el saldo visible y no genera notificación individual.

## Depósito

**CA-15 — Abonos al depósito.** *Dado* un depósito acordado de ₡300.000, *cuando* se registra un abono de ₡100.000, *entonces* el saldo es ₡200.000 y el estado, parcialmente pagado.

**CA-16 — Completar depósito.** *Dado* un depósito con saldo, *cuando* un abono completa el total, *entonces* el saldo es cero y el depósito se muestra como completado, conservando los abonos por separado.

**CA-17 — Separación entre alquiler y depósito.** *Dado* un contrato con obligación y depósito, *cuando* se registra un abono al depósito, *entonces* el saldo y estado de la obligación no cambian.

**CA-23 — Excepción de abonos.** *Dado* un depósito con tres abonos no anulados, *cuando* el administrador intenta un cuarto, *entonces* el sistema exige confirmación con motivo; sin motivo, lo rechaza; con motivo, lo registra y deja auditoría.

**CA-45 — Depósito mayor a una mensualidad.** *Dado* una renta de ₡180.000, *cuando* se registra un depósito de ₡400.000, *entonces* el sistema muestra una advertencia legal sin bloquear el guardado.

**CA-46 — Depósito de contrato cerrado.** *Dado* un contrato finalizado con depósito, *cuando* se consulta, *entonces* se muestra el estado y la etiqueta "contrato cerrado, liquidación manual", sin alertas.

## Seguridad y configuración

**CA-13 — Una sola cuenta con segundo factor.** *Dado* el alcance de v1, *cuando* se configura el acceso, *entonces* solo existe una cuenta administradora, que requiere segundo factor. Las solicitudes sin autenticación válida son rechazadas.

**CA-47 — Recuperación de acceso.** *Dado* un administrador sin su segundo factor, *cuando* usa un código de recuperación válido, *entonces* accede una sola vez con ese código y el sistema le notifica la recuperación.

**CA-48 — Sesión.** *Dado* una sesión inactiva más de una hora o abierta más de 24 horas, *cuando* se realiza una acción, *entonces* se exige autenticarse de nuevo.

**CA-18 — Configuración regional.** *Dado* una configuración nueva, *cuando* se crean contratos y se programan procesos, *entonces* se usan CRC y `America/Costa_Rica`. Al configurar USD en un contrato o cambiar la zona de la organización, los registros históricos no cambian.

**CA-10 — Conservación del historial.** *Dado* un contrato con obligaciones previas, *cuando* se desactiva el inquilino o se finaliza el contrato, *entonces* el historial permanece consultable.

**CA-56 — Plazo de aviso de un incidente.** *Dado* un incidente de seguridad registrado el viernes 6 de noviembre de 2026 como ocurrido ese día, *cuando* se consulta, *entonces* el sistema muestra como fecha límite de aviso a titulares y a la Agencia el viernes 13 de noviembre de 2026 (cinco días hábiles), sin contar sábados ni domingos; los feriados oficiales se validan con abogado (DP-17).

**CA-57 — Constancia de avisos de un incidente.** *Dado* un incidente con dos titulares afectados, *cuando* el administrador registra el aviso a cada uno y a la Agencia, *entonces* queda constancia de fecha, destinatario y contenido mínimo (naturaleza, datos comprometidos, acciones, dónde obtener más información), y el incidente no se marca como atendido mientras falte un aviso.

**CA-52 — Envío repetido de un abono.** *Dado* un abono de ₡1.000 enviado con una clave de solicitud, *cuando* el mismo envío se repite con la misma clave, *entonces* el sistema no crea un segundo movimiento, devuelve el ya registrado y el saldo se descuenta una sola vez.

**CA-53 — Auditoría sin valores personales.** *Dado* un inquilino cuyo teléfono se modifica, *cuando* se consulta el registro de auditoría, *entonces* consta que el campo teléfono cambió, quién lo hizo y cuándo, pero no el teléfono anterior ni el nuevo; en un cambio de importe sí constan el valor anterior y el nuevo.

**CA-54 — Comprobantes sin huecos.** *Dado* que un registro de abono falla después de asignar un número de comprobante, *cuando* se registra el siguiente abono con éxito, *entonces* su número es el siguiente al último comprobante emitido, sin saltos.

**CA-55 — Ajuste que conserva el importe inicial.** *Dado* una obligación de ₡300.000 con una corrección de −₡100.000, *cuando* se consulta, *entonces* el importe exigible vigente es ₡200.000, el importe inicial de ₡300.000 y la corrección con su motivo siguen consultables, y ningún valor se sobrescribió.

**CA-49 — Saldo de apertura.** *Dado* un contrato con inicio hace dos años, *cuando* se registra un saldo de apertura de ₡360.000 con fecha de hoy, *entonces* se genera una obligación de apertura por ese importe, las obligaciones regulares se generan desde el primer período que inicia en o después de esa fecha, y no hay alertas retroactivas.

# 10. Matriz de trazabilidad

| Necesidad / objetivo | Requisitos | Criterios |
|---|---|---|
| Registrar inquilinos y cédulas | RF-01–RF-05, RF-39, RF-45, RNF-02, RNF-03 | CA-01, CA-11, CA-25, CA-26, CA-29 |
| Administrar propiedades y contratos | RF-06–RF-10, RF-36, RF-42, RN-01–RN-05, RN-16, RN-28, RN-30 | CA-02, CA-10, CA-24, CA-31, CA-32 |
| Generar obligaciones sin duplicados | RF-11, RF-12, RF-43, RN-04, RN-05, RN-13, RNF-04, RNF-16 | CA-03, CA-30, CA-49, CA-50 |
| Reajustes y correcciones | RF-10, RN-14, OL-06, OL-07 | CA-12, CA-22, CA-39, CA-40, CA-51, CA-55 |
| Prorratear el último período | RF-09, RN-12 | CA-14 |
| Movimientos, saldos y estados | RF-13–RF-16, RF-34, RF-35, RN-06–RN-09, RN-11, RN-17, RN-18, RN-21, RN-22, RN-29 | CA-04, CA-19–CA-21, CA-33–CA-36, CA-52 |
| Comprobantes y moneda | RF-37, RF-38, RN-23, OL-03, OL-05 | CA-37, CA-38, CA-54 |
| Calendario y filtros | RF-17–RF-20 | CA-06, CA-07 |
| Recordatorios y alertas | RF-21–RF-25, RF-44, RN-07, RN-08 | CA-05, CA-08, CA-09, CA-41–CA-44 |
| Restringir acceso y auditar | RF-26–RF-28, RF-45, RNF-01, RNF-02, RNF-06, RNF-14 | CA-11, CA-13, CA-26, CA-47, CA-48, CA-53 |
| Depósito de garantía | RF-29–RF-32, RN-19, RN-20, RN-26, RN-27 | CA-15–CA-17, CA-23, CA-45, CA-46 |
| Derechos del titular y retención | RF-39–RF-41, RN-24, RNF-13–RNF-15 | CA-27, CA-28 |
| Incidentes y documentación de seguridad | RF-46, RNF-14, RNF-18, OL-19–OL-21 | CA-56, CA-57 |
| Operar en varias regiones | RF-33, RN-23, RNF-12, RNF-17 | CA-18 |

# 11. Riesgos y dependencias

| Riesgo o dependencia | Respuesta requerida |
|---|---|
| Exposición de fotografías de cédula | Repositorio privado, acceso autenticado, auditoría de acceso, cifrado, retención de cinco años. |
| Incumplimiento legal por reglas no validadas | Validar la sección 3 con un abogado antes de aprobar (DP-17). |
| Duplicación de obligaciones | Unicidad por contrato y período, y generación idempotente. |
| Fallo de WhatsApp | Registro de resultados, reintentos y notificación web como canal interno. |
| Proveedor de WhatsApp no elegido | Diferido: depende de un proyecto aparte del solicitante (DP-04). El SGA define una interfaz de canal de salida y opera con el canal web mientras tanto. Los términos de servicio de WhatsApp para consumidores prohíben mensajería masiva o automática; los términos de la plataforma empresarial no se leyeron. |
| Vulneración de seguridad sin aviso a tiempo | Registro de incidentes con fecha límite de cinco días hábiles (RF-46) y procedimiento de respuesta en la fase 6; validación legal (DP-17, DP-19). |
| Servidor propio con datos de cédulas | El solicitante administra el servidor (DP-08). Recomendado antes de cargar datos reales: servidor endurecido, prueba de restauración superada y revisión legal cerrada. Las guías de endurecimiento no se han investigado. |
| Ejecución diaria interrumpida | Procesamiento independiente de la interfaz, idempotente; solo la alerta del día. |
| Reglas de reajuste y gracia mal aplicadas | Casos de prueba para fechas efectivas, gracia y tope; validación legal. |
| Pérdida de datos | Respaldo diario con copia independiente y prueba de restauración antes de producción y cada 3 meses (RNF-09). |
| Cuenta única comprometida | MFA, códigos de recuperación, sesión corta, notificación de recuperación. |
| Conservación contable de datos eliminados | Determinar obligaciones contables o tributarias de conservación antes de aplicar la eliminación (DP-18). |

# 12. Decisiones pendientes y registro de decisiones

## 12.1 Pendientes

| ID | Decisión pendiente | Responsable sugerido |
|---|---|---|
| DP-01 | Validar legalmente la fórmula del prorrateo del último período (días reales del período, ambos extremos, redondeo). | Propietario y abogado |
| DP-04 | Proveedor de WhatsApp: **diferida**, depende de un proyecto aparte del solicitante (aplicación propia que se conecte a WhatsApp). Se requiere revisión legal de ese proyecto frente a los términos de WhatsApp. | Propietario |
| DP-17 | Validación legal de las obligaciones OL-01 a OL-21 (OL-19 a OL-21 son lectura propia del Reglamento 37554-JP), incluido cómo se cuentan los siete días de gracia y la aplicabilidad del art. 92. | Abogado |
| DP-18 | Obligaciones contables y tributarias de conservación de registros y su efecto sobre la eliminación de datos. | Abogado y contador |
| DP-19 | Aplicabilidad de la Ley 8968 (arts. 2 y 21) y de su reglamento: si la base del SGA es "interna o doméstica" y por tanto no se inscribe (Reglamento, art. 44), si el historial de pagos es dato sensible, y si hay que informar a la Agencia ante incidentes (OL-19). | Abogado |
| DP-20 | Formato del comprobante y si los procedimientos pactados lo sustituyen (art. 58). Numeración: serie global continua, decisión provisional del solicitante (H4). | Abogado |
| DP-21 | Texto informativo y formato del consentimiento (art. 5). | Abogado |

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
☐ Comprobante de pago, consentimiento y atención del titular revisados (DP-20, DP-21).
☐ Retención de datos y obligaciones de conservación contable conciliadas (DP-18).
☐ Moneda, tipo de cambio manual y zona horaria verificados.
☐ Canales de notificación y límites de WhatsApp comprendidos.
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

Tras aprobar los requisitos y resolver los bloqueos relevantes, se producen artefactos separados y enlazados a esta ERS: documento de arquitectura (DAS-SGA-001), modelo lógico y físico de datos, especificación de API e interfaces, diseño del proceso de obligaciones y notificaciones, plan de verificación y pruebas, y plan de implementación por entregas. La ERS define **qué** debe cumplir el sistema; el DAS describe **cómo** se organiza la solución.

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
8. Meta, WhatsApp Business Platform, mensajes. https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages
9. Fuentes de investigación completas: `actualizaciones/2026-10-17_ERS-v1.5_DAS-v0.4/CUESTIONARIO_CIERRE_ERS-DAS_recomendaciones_v1.md`.

---

**Fin del documento — ERS-SGA-001, versión 1.8 (borrador no aprobado).**

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
| Q-17 | Comprobante de pago diferido. | **Incluido por instrucción de cubrir obligaciones legales** (RF-37). |
