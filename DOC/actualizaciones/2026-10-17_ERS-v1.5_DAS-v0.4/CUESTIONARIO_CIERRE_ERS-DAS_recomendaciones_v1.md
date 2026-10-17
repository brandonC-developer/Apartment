# Cuestionario de cierre de ambigüedades — ERS-SGA-001 v1.4 / DAS-SGA-001 v0.3

**Fecha:** 17 de octubre de 2026
**Estado:** Borrador de recomendaciones. No es aprobación del negocio ni asesoría legal.

Cada punto tiene una recomendación, su fundamento con fuente y su nivel de confianza.

- **Alta:** respaldada por texto primario que leí.
- **Media:** documentación de proveedor o patrón reconocido, con inferencia mía.
- **Diseño:** criterio de ingeniería sin fuente externa. Se declara como tal.

Las referencias `E:nnn` y `D:nnn` son líneas de la ERS y del DAS.

## 0. Límites de esta investigación

1. **Legal.** Leí el texto de la Ley 7527 (copia del SCIJ en `unpcr.com`, con reformas hasta la Ley 9354 de 2016 y notas de Sinalevi). No pude abrir Sinalevi (la página no entrega el texto) ni el PDF de la Asamblea (error de certificado). **Antes de aprobar, un abogado debe confirmar la versión vigente.** El texto lo extraje yo del PDF.
2. **Estudios universitarios.** No encontré estudios universitarios específicos sobre software de alquileres. La única evidencia universitaria que usé es Ancker et al. (Weill Cornell, 2017), que es clínica y la aplico por analogía. El resto son normas oficiales, documentación de proveedores y publicaciones técnicas de referencia.
3. **Lectura parcial.** Algunas fuentes las leí mediante la herramienta de resumen de páginas (NIST, Meta, W3C, Fowler, Stripe, OWASP, Python, AWS, Buildium, Landlord Studio). Citan frases textuales, pero no leí cada página completa. Ancker lo verifiqué solo por resultados de búsqueda (resumen), no por el artículo completo.

## Registro de fuentes y validación

| ID | Fuente | Qué usé | Cómo la validé | Limitación |
|---|---|---|---|---|
| F1 | Ley 7527, Ley General de Arrendamientos Urbanos y Suburbanos. https://unpcr.com/wp-content/uploads/2025/05/Ley-General-de-Arrendamientos-Urbanos-y-Suburbanos.pdf (copia del SCIJ, norma 23655) | Arts. 16, 56, 57, 58, 59, 60, 61, 62, 67, 70, 71, 72, 92 | Extraje el texto del PDF y lo leí | Es copia, no el sitio oficial. Falta confirmar vigencia. |
| F2 | Ley 8968, protección de datos personales. https://www.sutel.go.cr/sites/default/files/normativas/ley_proteccion_de_la_persona_frente_al_tratamiento_de_sus_ley_8968.pdf | Arts. 5 y 6 | Descargué el PDF y leí los artículos | Reglamento (Decreto 37554-JP) no revisado. |
| F3 | NIST SP 800-63B-4, https://pages.nist.gov/800-63-4/sp800-63b/aal/ , `/authenticators/`, `/events/` | Sesiones, contraseñas, recuperación | Resumen de página por herramienta con citas | Guía federal de EE. UU., aplicada por analogía. Los plazos de sesión son SHOULD. |
| F4 | Meta, WhatsApp Business Platform, https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages | Opt-in, plantillas, ventana de 24 h, estados de entrega | Resumen de página | No revisé la referencia de webhooks ni los estados `sent` y `read`. |
| F5 | AWS Architecture Blog, "Exponential Backoff And Jitter" (Marc Brooker, 2015). https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/ | Reintentos con jitter | Resumen de página | Escenario de alta concurrencia. Con un solo destinatario el beneficio es menor. |
| F6 | Stripe, "Idempotent requests". https://docs.stripe.com/api/idempotent_requests | Idempotencia en reintentos | Lectura completa de la página | Documentación de producto, patrón general. |
| F7 | OWASP File Upload Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html | Carga de cédulas | Resumen de página con citas | Los valores concretos (formatos y tamaños) son decisión nuestra. |
| F8 | W3C, "Working with Time and Timezones" (Group Draft Note, 26-jul-2025). https://www.w3.org/TR/timezone/ | Zona horaria | Resumen con secciones 3.4.7, 4.1, 4.2.2 | Nota en borrador, no es estándar. |
| F9 | M. Fowler, "Reversal Adjustment" (2006, borrador) https://martinfowler.com/eaaDev/ReversalAdjustment.html y "Money" https://martinfowler.com/eaaCatalog/money.html | Correcciones contables sin borrar historia | Resumen de página | El autor declara que es material en borrador. |
| F10 | Python, módulo `decimal`. https://docs.python.org/3/library/decimal.html | Redondeo | Resumen de página | Se cita como referencia técnica, sin implicar el lenguaje. |
| F11 | Ancker et al., *BMC Med Inform Decis Mak* 17:36 (2017), Weill Cornell Medicine. https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-017-0430-8 | Fatiga de alertas | Solo resultados de búsqueda (resumen) | Dominio clínico, no alquileres. |
| F12 | Buildium, "Introducing: Automatic prorated rent calculations" (2016). https://www.buildium.com/blog/introducing-prorated-rent-calculations | Prorrateo en software de alquileres | Resumen de página | Publicación de proveedor, de 2016. |
| F13 | Landlord Studio, "Managing rent arrears". https://help.landlordstudio.com/en/articles/4813815-managing-rent-arrears | Pagos parciales y saldos | Resumen de página | Documentación de proveedor. |
| F14 | ISO 4217 (CRC con unidad menor 2). Fuente secundaria: https://localizely.com/currency-code/CRC/ | Moneda | Resultado de búsqueda | **No consulté la lista oficial de ISO.** |

## 1. Hallazgos legales que cambian requisitos

Estos puntos salen de F1 y F2. Los cito primero porque modifican varias respuestas previas.

| ID | Qué dice la fuente | Efecto en la ERS |
|---|---|---|
| L1 | Art. 58: el pago es por períodos de un mes, salvo pacto. El arrendatario puede pagar **dentro de los siete días naturales siguientes al vencimiento** del período de pago. Art. 62: aceptar un pago tardío no modifica el día pactado. | El "vencido desde el día siguiente" de E:558-564 puede chocar con este plazo. Ver Q-13b. |
| L2 | Arts. 16, 56 y 58: el arrendador debe entregar **recibo o comprobante de pago**, y el inquilino tiene derecho irrenunciable a exigirlo. El art. 58 permite otros procedimientos que acrediten el pago de forma fehaciente. | La ERS no tiene requisito de comprobante. Falta (Q-17). |
| L3 | Art. 57: si el precio se pacta en moneda extranjera, el inquilino puede pagar en colones al **tipo de cambio de venta del BCCR a la fecha del pago**. | Contradice "sin conversión de monedas" de E:196. Ver Q-18. |
| L4 | Art. 67: en vivienda el precio se reajusta anualmente. Tope: inflación acumulada (INEC) hasta 10 %. Sobre 10 %, MIVAH fija el porcentaje. Rige **desde el período de pago siguiente** a la notificación. Cualquier reajuste mayor es nulo. En moneda extranjera no hay reajuste. | Afecta RF-10 y P10/P16 (actualizar vencidas). Ver Q-2. |
| L5 | Art. 70: la duración no puede ser menor a **tres años** (se entiende pactado así). Art. 71: prórroga tácita por tres años si el arrendador no avisa con tres meses. Art. 72: el inquilino termina con aviso de tres meses. | Afecta fin de contrato y generación de obligaciones. Ver Q-11. |
| L6 | Art. 60: el inquilino paga desde el día en que recibe el bien hasta el día en que lo entrega. | Respalda prorrateo por días de ocupación con ambos extremos. Ver Q-10. |
| L7 | Art. 61: si se paga con cheque u otro título, el descargo queda sujeto al recibo en efectivo. | Respalda anular movimientos (cheque rebotado). Ver Q-9. |
| L8 | Art. 92: no se puede obligar a pagar anticipado más de una mensualidad ni a rendir garantía mayor a una mensualidad; lo contrario es nulo. Art. 58 repite lo del pago anticipado para vivienda. | RF-29 no pone tope al depósito. Ver Q-15. No verifiqué si el art. 92 aplica solo a vivienda. |
| L9 | Ley 8968, art. 5: informar previamente ocho puntos y obtener **consentimiento expreso por escrito** (físico o electrónico), revocable. Art. 6: eliminar datos no pertinentes. En ningún caso conservar datos que puedan afectar al titular **más de diez años** desde los hechos, salvo norma especial; si hace falta, desasociarlos. | Base para DP-05 y para la foto de cédula. Ver Q-20. |

## 2. Respuestas a los bloqueantes (numeración de mi análisis anterior)

### Q-1 Período de alquiler
**Recomendación:** definir en el contrato `ancla_periodo` con dos valores. `mes_calendario` es el predeterminado, porque el propietario eligió prorratear por días reales del mes. `aniversario` cuenta de día de entrada a día de entrada, y no prorratea meses completos. El período siempre dura un mes (el art. 58 lo fija así salvo pacto). Agregar `fecha_entrega_bien` al contrato. El vencimiento es un día dentro de ese período (Q-13b define la gracia).
**Fundamento:** F1 art. 58 (períodos de un mes), art. 60 y art. 70 (cuenta desde la entrega). F12: el prorrateo automático solo aplica a alquiler recurrente mensual.
**Confianza:** Media.
**Requiere:** el propietario debe decir si cobra por mes calendario o por aniversario. Es la pregunta de mayor impacto.

### Q-2 Qué obligaciones afectan los cambios de condiciones
**Recomendación:** separar dos tipos de cambio.
- **Reajuste:** es prospectivo. Afecta las obligaciones cuyo período empieza en o después de la fecha efectiva. Guarda la fecha de notificación. La fecha efectiva se normaliza al inicio del período siguiente, y no se permiten fechas efectivas a mitad de período. Advierte (no bloquea) si el porcentaje supera el tope informado. No admite reajuste en moneda extranjera para vivienda.
- **Corrección:** es retroactiva, con motivo obligatorio y auditoría. Es la única que puede afectar vencidas no pagadas.
Si cambia el día de vencimiento, el estado se recalcula con la nueva fecha y las alertas ya emitidas se conservan en el historial.
**Fundamento:** F1 art. 67 (rige desde el período de pago siguiente a la notificación; excesos nulos).
**Confianza:** Alta en el principio, Media en la implementación.
**Requiere:** decisión del propietario. **Esto contradice en apariencia P10/P16** (actualizar también vencidas): para reajustes de vivienda la ley parece impedirlo. Validar con abogado.

### Q-3 Abonos existentes cuando el importe baja
**Recomendación:** bloquear cualquier cambio que deje el importe exigible por debajo de la suma de abonos válidos. El mensaje debe indicar el exceso y pedir anular o ajustar abonos antes.
**Fundamento:** RN-24 ya prohíbe saldo negativo. F13 muestra que el software de mercado trata el sobrante con una decisión explícita, no en silencio.
**Confianza:** Diseño.

### Q-4 CA-12 contra CA-22
**Recomendación:** unificar. "Histórica" significa obligación pagada o con período anterior a la fecha efectiva. Reescribir CA-12 y CA-22 con Q-2.
**Confianza:** Diseño.

### Q-5 ¿Pagada automáticamente o con confirmación?
**Recomendación:** el estado `pagada` se deriva: saldo cero implica pagada. Eliminar la "confirmación manual" adicional. Cada abono ya es la confirmación manual de recepción (RN-11).
**Fundamento:** F9 (derivar saldos desde los asientos, sin segundo estado manual). F13 (el sistema calcula el saldo restante).
**Confianza:** Media.

### Q-6 Fecha real única con varios abonos
**Recomendación:** la fecha de pago completo de una obligación es la fecha real del abono que llevó el saldo a cero. Se calcula, no se almacena en la obligación. RF-13 pasa a ser un abono por el saldo restante, con campo de importe.
**Confianza:** Diseño.

### Q-7 Entidades duplicadas y saldo almacenado
**Recomendación:** una sola entidad `Movimiento` (con tipo: abono de alquiler, abono de depósito) y saldos siempre derivados. Eliminar "Pago de alquiler" (D:372) y los atributos `saldo_pendiente` (E:588-589, D:359). Añadir la entidad a la ERS §6.
**Fundamento:** F9. El propio DAS ya exige que el saldo no sea fuente única (D:386).
**Confianza:** Media.

### Q-8 Estado `anulada`
**Recomendación:** añadir el estado `anulada` con motivo obligatorio. Solo se puede anular una obligación sin movimientos válidos. Al finalizar un contrato, las obligaciones futuras sin movimientos se anulan con auditoría. El último período parcial se recalcula según Q-10. Las alertas se detienen en `pagada` y en `anulada`.
**Fundamento:** F1 art. 72: el contrato termina con aviso de tres meses, así que se pueden haber generado obligaciones posteriores al fin real.
**Confianza:** Diseño con base legal parcial.

### Q-9 Anulación de pagos
**Recomendación:** nueva operación "anular movimiento": conserva el original, agrega la reversión con motivo, recalcula saldo y estado. Si la obligación vuelve a vencida, las alertas se reanudan el día siguiente. Los recordatorios pasados no se reenvían.
**Fundamento:** F9 (Reversal Adjustment: no se borra la entrada incorrecta, se postea una opuesta; costo: más filas). F1 art. 61 (el cheque no descarga hasta recibir el efectivo).
**Confianza:** Media.

### Q-10 Prorrateo
**Recomendación:**
- Base: días reales del mes (decisión R1 del propietario).
- Días cobrables: ambos extremos incluidos (día de entrega y día de devolución).
- Redondeo: una sola vez, al final, al colón entero, con `ROUND_HALF_UP` (empate se aleja de cero). Calcular con decimales exactos, nunca con flotantes.
- Vencimiento del período parcial: el día de vencimiento del contrato en ese mes.
- Permitir ajuste manual del importe, con auditoría.
**Fundamento:** F1 art. 60. F10: `ROUND_HALF_UP` y `ROUND_HALF_EVEN` definidos; el valor por defecto de Python es HALF_EVEN, así que hay que fijarlo. F12: el proveedor muestra los días usados y permite editar. F9 (Money): usar un tipo monetario y redondear a la unidad menor. F14 (secundaria): unidad menor del CRC es 2.
**Confianza:** Media. En los artículos que revisé no hay fórmula legal de prorrateo; **validar con abogado** (DP-01).
**Requiere:** el propietario confirma HALF_UP. La elección importa poco: solo afecta empates exactos de 0,5.

### Q-11 Generación de obligaciones y fin de contrato
**Recomendación:**
- Generar de forma rodante la obligación del período siguiente, 30 días antes de que empiece (valor propuesto). Así el calendario y los recordatorios funcionan sin generar años por adelantado. Un contrato sin fecha fin no necesita horizonte fijo.
- Si el contrato tiene `fecha_fin`, avisar al administrador 120 días antes (tres meses de aviso del art. 71 más margen). Si la fecha pasa sin acción, **no dejar de generar en silencio**: marcar el contrato `por_decidir` (posible prórroga tácita).
- Avisar si la vigencia pactada es menor a tres años.
- Contratos con inicio en el pasado: generar el historial como `histórica` sin alertas y dejar que el administrador registre movimientos. Las alertas empiezan desde hoy.
**Fundamento:** F1 arts. 70, 71, 72.
**Confianza:** Media (legal) y Diseño (valores 30 y 120 días).

### Q-12 "Incompatible" y solapamiento
**Recomendación:** definir el intervalo de un contrato como `[fecha_inicio, fecha_fin]`, ambos inclusive, y sin fecha fin = abierto. Dos contratos de una propiedad **no pueden compartir ningún día**. Un relevo exige que el nuevo inicio sea al menos el día siguiente al fin anterior. Reemplazar "incompatible" por esta definición en RF-08, RN-02, RF-36, CA-02 y CA-24.
**Fundamento:** F1 art. 60 (se paga hasta el día de entrega del bien).
**Confianza:** Diseño con apoyo legal.

### Q-13a Zona horaria
**Recomendación:** un solo nivel, **organización** (decisión R6 del propietario). Quitar la zona por propiedad del DAS (D:346, D:321, D:327, ADR-005). Las fechas de vencimiento son fechas de calendario sin hora. Las marcas de registro se guardan en UTC y se muestran en la zona de la organización. Guardar el identificador IANA (`America/Costa_Rica`), nunca un desfase. Reemplazar "Costa Rica" fijo en RF-14 y RNF-12 por "zona configurada".
**Fundamento:** F8, secciones 3.4.7 (preferir ID de zona), 4.1 (UTC para registros) y 4.2.2 (eventos futuros necesitan la zona, no solo el desfase).
**Confianza:** Media (nota en borrador).

### Q-13b Estado "vencido" y plazo de gracia
**Recomendación:** agregar `dias_gracia` por contrato, predeterminado **7** para vivienda en Costa Rica, ajustable. Calcular `fecha_limite = vencimiento + dias_gracia`. Los recordatorios se anclan al vencimiento. El estado `vencido` y las alertas diarias empiezan después de `fecha_limite`. Definir `vencido` como **derivado por fecha** (RF-14), no como resultado del proceso diario, y ajustar CA-05. Un pago tardío no mueve el día de vencimiento.
**Fundamento:** F1 arts. 58 y 62.
**Confianza:** Alta en el texto. Media en la interpretación: **requiere validación legal** de cómo se cuentan los siete días.

### Q-14 DP-10: ¿notificar cada abono?
**Recomendación:** no notificar. El administrador es quien registra el abono, y avisarle de su propia acción no añade información. Mostrar el saldo actualizado. Mantener el desacople que ya define el DAS (D:308-312).
**Fundamento:** F11: la aceptación de recordatorios cae 30 % por cada recordatorio adicional por encuentro (dominio clínico, analogía). Prevalece P8/P14 sobre P2.
**Confianza:** Diseño con apoyo por analogía.
**Requiere:** que el propietario confirme que P2 se refería al saldo visible.

### Q-15 Excepción de abonos y depósito
**Recomendación:**
- La "excepción" con una sola cuenta es una **confirmación explícita con motivo obligatorio** (texto libre, longitud mínima) y auditoría. No hay segundo aprobador en v1.
- "Efectivamente recibidos" = movimientos no anulados. El tope de tres incluye el abono que completa el depósito.
- Validar que el depósito total no supere una mensualidad de renta (advertencia o bloqueo configurable). Ver L8.
- Calendarios o acuerdos múltiples (R4, DP-13): **dejarlos fuera de v1**. El depósito tiene un importe total, una fecha límite acordada opcional y notas.
**Fundamento:** F1 arts. 59 y 92.
**Confianza:** Media.
**Requiere:** el propietario confirma retirar R4 de v1. Un proyecto de ley sobre retención de depósitos (expediente 25288) aparece en una búsqueda, pero **no lo verifiqué**.

### Q-16 Depósito: huecos
**Recomendación:**
- Sin alertas de depósito en v1. Se muestra el estado (pendiente, parcial, completado).
- El importe total solo se edita sin abonos, o con corrección auditada y nunca por debajo de lo abonado.
- Al cerrar el contrato el depósito mantiene su estado y se muestra "contrato cerrado, liquidación manual" (la devolución está fuera de alcance por R5).
- No se traslada automáticamente a un contrato nuevo (RF-36).
**Confianza:** Diseño.

## 3. Requisitos nuevos que salen de la investigación

### Q-17 Recibo o comprobante de pago
**Recomendación:** agregar un RF: cada abono o pago genera un comprobante numerado, consecutivo, imprimible y reimprimible, con datos del contrato, período, importe, fecha real y saldo. Los anulados quedan marcados, no se renumeran.
**Fundamento:** F1 arts. 16, 56 y 58 (el art. 58 admite otros procedimientos fehacientes, por lo que el formato exacto queda a validar).
**Confianza:** Alta en la obligación, Media en el formato.

### Q-18 Contratos en moneda extranjera
**Recomendación:** cambiar el alcance. El sistema no consulta tipos de cambio, pero permite registrar un movimiento en moneda distinta de la del contrato con **tipo de cambio ingresado a mano** y equivalente calculado. El saldo se mantiene siempre en la moneda del contrato. Fuera de v1: tipos de cambio automáticos.
**Fundamento:** F1 art. 57.
**Confianza:** Alta en la regla, Diseño en la forma.
**Requiere:** el propietario confirma si alquila en dólares.

### Q-19 Catálogo de monedas (DP-09)
**Recomendación:** CRC y USD en v1.
**Confianza:** Diseño, sin fuente. La ley solo habla de "moneda extranjera".

### Q-20 Datos personales y retención (DP-05)
**Recomendación:**
- Registrar el consentimiento escrito o electrónico del inquilino (fecha, versión del texto y medio) antes de guardar la foto de cédula.
- Mostrar o entregar la información previa de los ocho puntos del art. 5.
- Conservar la foto mientras el contrato esté vigente y hasta un plazo X tras su fin, con eliminación o desasociación a más tardar a los **diez años**.
- Implementar la revocación del consentimiento.
**Fundamento:** F2 arts. 5 y 6.
**Confianza:** Alta en las obligaciones, el valor X queda abierto.
**Requiere:** que el propietario y un abogado fijen X. No revisé el reglamento.

## 4. Notificaciones

### Q-21 Recordatorios (RF-21, DP-03)
**Recomendación:** lista de anticipaciones configurable con un máximo de tres valores y **un solo valor predeterminado** (por ejemplo, 3 días). Un cambio de configuración se aplica a las notificaciones futuras aún no procesadas y las reprograma sin duplicar. La clave única es obligación + tipo + anticipación + fecha. Con saldo parcial, el recordatorio indica el saldo, no el total.
**Fundamento:** F6 (claves de idempotencia para reintentos seguros). F11 (menos alertas).
**Confianza:** Diseño.

### Q-22 Destinatario y WhatsApp (DP-04)
**Recomendación:** el destinatario es el administrador. Se guarda su teléfono en configuración, con su aceptación registrada. Los avisos deben ser **plantillas aprobadas** de tipo utilidad, porque el negocio los inicia fuera de una ventana de 24 horas. La API que acepta el envío no prueba la entrega: se espera el estado `delivered` por webhook. Si no llega antes del TTL (30 días por defecto), se asume perdido. El estado `failed` puede llegar con retraso, así que se deja un margen.
**Fundamento:** F4.
**Confianza:** Alta.
**Requiere:** elegir proveedor. Los datos de inquilinos (teléfono y correo) no se usan para notificar en v1. Decidir si se siguen capturando o se hacen opcionales.

### Q-23 Reintentos (RF-24, CA-09)
**Recomendación:** backoff exponencial con jitter, máximo de cinco intentos, tope de intervalo (valores propuestos). Tras el último intento fallido, el resultado es `fallido` y la notificación web persiste.
**Fundamento:** F5: el jitter reparte los reintentos. Prefiere cualquier variante con jitter sobre ninguna. "Equal Jitter" es la peor.
**Confianza:** Media. Con un solo destinatario el beneficio del jitter es pequeño. Los números son de diseño.

### Q-24 Consolidación de alertas
**Recomendación:** mantener un registro de alerta por obligación y día (RF-22), pero **enviar un solo resumen diario por canal** con todas las vencidas. Así 10 vencidas no generan 10 mensajes.
**Fundamento:** F11: la aceptación baja con cada alerta adicional y con la proporción de repeticiones (clínico; analogía).
**Confianza:** Media.

### Q-25 Notificación web y hora del proceso (DP-02)
**Recomendación:** la notificación web tiene estados nueva, leída y archivada, y no se borra. El proceso corre cada día temprano en la zona de la organización y es idempotente. Si faltó algún día, recupera la generación pero **emite solo la alerta del día actual**, sin avalancha de atrasadas.
**Fundamento:** F6.
**Confianza:** Diseño.

## 5. Inquilinos, propiedades y contratos

| ID | Ambigüedad | Recomendación | Confianza |
|---|---|---|---|
| Q-26 | Identificación (RF-01) | Campos `tipo_documento` (cédula, DIMEX, pasaporte, otro) y número. Unicidad por tipo y número entre inquilinos activos; advertir duplicados. | Diseño |
| Q-27 | Foto de cédula | Frente obligatorio, reverso opcional. JPEG o PNG, hasta 5 MB (valores propuestos). Lista blanca de formatos, validación de firma real del archivo, nombre aleatorio, almacenamiento fuera del directorio público, límite de tamaño. | Alta (controles, F7), Diseño (valores) |
| Q-28 | Desactivar inquilino (RF-04) | Bloquear con contrato vigente o saldos pendientes. Permitir reactivar. No afecta el historial. | Diseño |
| Q-29 | Estados de propiedad y contrato | Propiedad: disponible, ocupada (derivada), inactiva. Contrato: futuro, vigente, por_decidir (Q-11), finalizado, derivados de las fechas, más `anulado`. | Diseño |
| Q-30 | Fecha real "válida" (CA-04, CA-21) | No futura (según la zona de la organización) y no anterior a la fecha de inicio del contrato. | Diseño |
| Q-31 | Saldos iniciales del piloto | Permitir un saldo de apertura por contrato, con fecha y auditoría. | Diseño |

## 6. Seguridad y no funcionales

### Q-32 Cuenta única (RF-27, RNF-01)
**Recomendación:** pasar a la ERS lo que hoy delega al diseño.
- MFA obligatorio con TOTP (un factor de código de un solo uso).
- Contraseña de al menos 15 caracteres si es el único factor; 8 si se usa solo dentro de MFA. Sin reglas de composición ni rotación periódica.
- Sesión: cierre total a las 24 horas e inactividad de 1 hora (el nivel AAL2 lo recomienda).
- Recuperación mediante **códigos de recuperación de un solo uso** guardados por el administrador. Cada recuperación envía una notificación al administrador o a un contacto designado.
**Fundamento:** F3. Los plazos son SHOULD y la guía es federal de EE. UU.
**Confianza:** Media.
**Por qué importa:** con una sola cuenta no hay otro administrador que recupere el acceso.

### Q-33 Otros no funcionales
- **RNF-08:** reescribir sobre el uso real (un administrador). Propuesta: consultas habituales en menos de 2 s en el percentil 95, con el volumen que fije el propietario (propiedades, contratos). *Diseño.*
- **RNF-10:** lista explícita de navegadores (las dos últimas versiones mayores de Chrome, Edge, Firefox y Safari en escritorio y móvil). *Diseño.*
- **Auditoría de acceso a cédulas:** registrar quién la vio y cuándo, sin guardar la imagen en el registro (el DAS ya lo propone). *Diseño.*
- **Idioma de la interfaz:** español en v1; textos externalizados para otros idiomas. *Diseño.*

## 7. Correcciones documentales que puedo aplicar sin decisión del negocio

1. Renumerar DP de la ERS y del DAS en una sola tabla con IDs únicos; cubrir DP-07 y DP-08 o retirarlos.
2. Corregir E:53 ("sección 14" debe decir sección 11) y la numeración de listas (§6.3, §12, §14, §15).
3. Eliminar o crear RNF-13 a RNF-17, citados en E:916, E:925, D:645 y D:650.
4. Reescribir RN-21: "los abonos al depósito no afectan el saldo ni el estado de las obligaciones de alquiler".
5. Quitar exclusiones duplicadas (E:190, E:193, E:203).
6. Completar la matriz §9 con RF-34 a RF-36, RN-23 a RN-28 y CA-19 a CA-24.
7. Mover el Anexo A antes de "Fin del documento".
8. Unificar "importe exigible" y "monto esperado"; separar "pendiente" (estado) de "saldo pendiente".
9. Incluir DP-10 a DP-16 en las condiciones de aprobación del DAS (§16).
10. Aclarar el estado de las decisiones de v1.1 frente a E:23-24.

## 8. Decisiones que siguen siendo del propietario

1. **Q-1:** mes calendario o aniversario.
2. **Q-2:** aceptar que los reajustes de vivienda no sean retroactivos (cambia P10/P16).
3. **Q-13b:** aceptar los 7 días de gracia como regla predeterminada.
4. **Q-14:** confirmar que P2 se refería al saldo visible.
5. **Q-15:** retirar R4 (calendarios de depósito) de v1.
6. **Q-18:** confirmar si se alquila en dólares.
7. **Q-20:** plazo X de retención de la foto de cédula.
8. **DP-14 (P11):** recuperar el enunciado original.
9. Nombrar propietario del producto y aprobador (hoy "Por designar").
10. **Validación legal** de L1 a L9 por un abogado.

## 9. Registro de respuestas del solicitante (17-oct-2026)

Respuestas dadas durante la sesión de validación. Siguen siendo respuestas del solicitante, no aprobación formal del propietario ni validación legal.

| Punto | Respuesta | Efecto en los documentos |
|---|---|---|
| Q-1 | El período va de un día X al mismo día X del mes siguiente (ejemplo: 10 ene a 10 feb es un mes). El prorrateo es un plan diferido. | Período por **aniversario**. Modifica RN-15, RN-17, §6.4, CA-14, R1 y R2. |
| Q-1b | El día 10 de febrero abre el segundo período (período 1: 10 ene al 9 feb). | Borde del período sin día compartido. |
| Q-10 / Q-10b | Se prorratea solo el último período, con respaldo en los arts. 60 y 72. | Prorrateo de v1 limitado al último período, con ajuste manual auditado. El prorrateo general queda diferido. DP-01 sigue abierto para la fórmula. |
| Q-2 | Reajuste (prospectivo) y corrección (retroactiva con motivo). | RF-10, RN-09, CA-12 y CA-22 se reescriben. Cambia P10/P16 para reajustes. |
| Q-13b | Gracia de 7 días, campo `dias_gracia` por contrato. | RF-14, RN-07, §5.2 y CA-05. Requiere validación legal del cómputo. |
| Q-18 | Colones y dólares, con tipo de cambio ingresado a mano. | Se retira "sin conversión" de E:196 para pagos en moneda distinta a la del contrato. Cierra DP-09 para CRC y USD. |
| Q-20 | Retención de la foto de cédula: 5 años tras fin del contrato. | Cierra DP-05 (un abogado debe validar el plazo). |
| Q-14 | No notificar cada abono de alquiler. | Cierra DP-10. |
| Q-15 | Excepción de abonos al depósito = confirmación con motivo obligatorio y auditoría. | Cierra DP-12. |
| Q-15b | Advertir si el depósito supera una mensualidad. | Nuevo control en RF-29. |
| Q-15c | Sin calendarios de abono del depósito en v1. | Cierra DP-13 para v1 y retira R4. |
| Q-5 | La obligación pasa a pagada sola con saldo cero. | RF-13, RF-35 y CA-20. |
| Q-9 | Anular con motivo (conserva el original). | Nueva operación "anular movimiento". |
| Q-8 | Estado `anulada` con motivo. | Cuarto estado de obligación. |
| Q-11 | Generación 30 días antes del período. | RF-11. |
| Q-11b | Aviso 120 días antes del fin y estado "por decidir". | Nuevos RF de fin de contrato. |
| Q-12 | Ningún día compartido entre contratos de una propiedad. | Define "incompatible". |
| Q-13a | Zona horaria solo a nivel de organización. | Corrige el DAS. |
| Q-17 | Comprobante de pago: **requisito diferido**. | Se registra como futuro. Riesgo legal del art. 56 anotado. |
| Q-21 | Un recordatorio configurable (3 días por defecto). | RF-21. |
| Q-24 | Resumen diario por WhatsApp. | RF-22 y RF-23. |
| Q-32 | MFA obligatorio con códigos de recuperación. | RF-27 y RNF-01. |
| Q-3 | Bloquear cambios que dejen saldo negativo. | Control en RF-10. |
| Q-28 | Bloquear desactivar con contrato vigente o saldos. | RF-04. |
| Q-27 | Frente obligatorio, reverso opcional. | RF-01 y RF-02. |

### Respuestas de la segunda tanda (17-oct-2026)

| Punto | Respuesta | Efecto en los documentos |
|---|---|---|
| Q-16 | El depósito conserva su estado y muestra "contrato cerrado, liquidación manual". Sin alertas de depósito en v1. El total solo se edita sin abonos, o con corrección auditada nunca por debajo de lo abonado. No se traslada solo a un contrato nuevo. | RF-29 a RF-32 y RF-36. |
| Q-22 | El proveedor de WhatsApp se elige en la fase de arquitectura. La ERS exige plantillas aprobadas, teléfono y aceptación del administrador, y distinguir aceptado de entregado. | DP-04 sigue abierto. No se compararon precios. |
| Q-23 | 5 intentos con backoff exponencial y jitter. | RF-24 y CA-09. |
| Q-25 | 07:00 en la zona de la organización (configurable). Tras una caída, solo se emite la alerta del día actual. | Cierra DP-02. |
| Q-26 | Tipo de documento (cédula, DIMEX, pasaporte, otro) más número, con advertencia de duplicados. | RF-01 y modelo de inquilino. |
| Q-29 | Estados derivados de fechas. Contrato: futuro, vigente, por decidir, finalizado, anulado. Propiedad: disponible, ocupada, inactiva. | RF-06 y RF-07. |
| Q-30 | La fecha real no puede ser futura ni anterior al inicio del contrato. | CA-04 y CA-21. |
| Q-31 | Saldo de apertura por contrato, con fecha y auditoría. Historial anterior como histórico sin alertas. | Nuevo requisito de carga inicial. |
| Q-33 | Hasta 50 propiedades. Consultas habituales en menos de 2 s (percentil 95). Navegadores: dos últimas versiones mayores de Chrome, Edge, Firefox y Safari. | RNF-08 y RNF-10. |

Q-4, Q-6 y Q-7 se resuelven con las respuestas anteriores (modelo de movimientos con saldo derivado).

### Pendientes abiertos

Todos los puntos Q-1 a Q-33 tienen respuesta. Quedan abiertos DP-14 (P11), el nombramiento del propietario del producto, la política de respaldo (RPO y RTO) y la validación legal de L1 a L9. La auditoría de acceso a cédulas y el idioma de la interfaz (Q-33) se asumieron sin preguntar.
