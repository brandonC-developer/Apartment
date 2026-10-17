Especificación de Requisitos de Software (ERS)

**Sistema de Gestión de Alquileres**

**Identificador:** ERS-SGA-001

**Versión:** 1.4 --- Borrador actualizado para revisión

**Estado:** Borrador actualizado; pendiente de validación y aprobación
formal

**Fecha:** 14 de octubre de 2026

**Idioma:** Español

**Configuración regional por defecto:** Colones costarricenses (CRC);
zona horaria `America/Costa_Rica`. La plataforma deberá permitir
configurar moneda y zona horaria para operar en otras regiones.

**Nota de control:** Esta versión incorpora las respuestas del solicitante
a las rondas de aclaración, incluidas reglas sobre abonos de alquiler,
períodos contractuales, modificaciones de obligaciones no pagadas, depósitos
y fechas retroactivas. Las respuestas del solicitante no equivalen por sí
solas a aprobación formal del propietario del negocio. Se mantienen
identificadas las contradicciones y decisiones pendientes. Este documento no
certifica conformidad integral con una norma ISO/IEEE ni autoriza comenzar
la implementación.

# Control del documento

  -----------------------------------------------------------------------
  **Campo**           **Valor**
  ------------------- ---------------------------------------------------
  **Nombre**          Especificación de Requisitos de Software ---
                      Sistema de Gestión de Alquileres

  **Identificador**   ERS-SGA-001

  **Versión**         1.4

  **Estado**          Borrador actualizado para revisión y aprobación

  **Propietario del   Por designar
  producto**          

  **Responsable de    Por designar
  requisitos**        

  **Aprobador**       Administrador/propietario del negocio, por
                      confirmar

  **Revisión          Tras resolver las decisiones pendientes de la
  siguiente**         sección 14
  -----------------------------------------------------------------------

## Historial de versiones

  ---------------------------------------------------------------------------------
  **Versión**   **Descripción**
  ------------- -------------------------------------------------------------------
  **0.1**       Idea inicial: registro de inquilinos, calendario y recordatorios.

  **1.0**       Primera especificación con requisitos funcionales y no funcionales,
                reglas, modelo conceptual y criterios de aceptación.

  **1.1**       Decisiones aprobadas: último día del mes para fechas inexistentes,
                recordatorios configurables, web y WhatsApp, alertas diarias,
                vigencia contractual, fecha real de pago y una cuenta
                administradora.

  **1.2**       Consolidación documental, normalización de términos, trazabilidad,
                criterios verificables, riesgos y referencias metodológicas.

  **1.3**       Incorporación de prorrateo, abonos al depósito de garantía,
                almacenamiento privado de cédulas y configuración regional global
                con valores predeterminados de Costa Rica.

  **1.4**       Incorporación de respuestas a rondas de aclaración: abonos de
                alquiler con saldo pendiente; período de alquiler definido por
                contrato; máximo ordinario de tres abonos al depósito con excepción
                administrativa; actualización de obligaciones no pagadas desde la
                fecha efectiva; fecha real retroactiva con marca temporal de registro;
                y cambio de inquilino mediante cierre y nuevo contrato. Se conserva
                el estado de borrador y se documentan contradicciones y pendientes.
  ---------------------------------------------------------------------------------

# 1. Propósito y organización

## 1.1 Propósito

Definir de forma verificable el comportamiento esperado, las
restricciones y las condiciones de aceptación de la primera versión del
Sistema de Gestión de Alquileres (SGA), antes de tomar decisiones de
arquitectura técnica o iniciar la implementación.

La ERS será la referencia común para el propietario del producto,
analista, diseñador/arquitecto, desarrollador y responsable de pruebas.
Cualquier cambio aprobado deberá registrarse en el historial de
versiones y evaluarse por su impacto en requisitos, reglas, datos y
pruebas.

## 1.2 Convención de redacción

-   **"El sistema deberá"** expresa un requisito obligatorio.
-   Cada requisito tiene un identificador único y debe ser comprobable
    mediante prueba, inspección, análisis o demostración.
-   Las recomendaciones y decisiones pendientes se identifican por
    separado; no se tratan como requisitos aprobados.
-   Los requisitos de esta versión describen el comportamiento del
    producto, no una tecnología específica.

## 1.3 Términos

-   **Inquilino:** persona que alquila una propiedad.
-   **Propiedad:** vivienda, unidad o inmueble objeto del alquiler.
-   **Contrato:** acuerdo que asocia a un inquilino con una propiedad
    durante un período y define el monto y vencimiento.
-   **Obligación de pago:** importe mensual esperado según un contrato y
    un período determinado.
-   **Pago recibido:** confirmación manual del administrador de que
    recibió el importe debido.
-   **Vencimiento:** fecha límite definida para una obligación.
-   **Pendiente:** obligación no marcada como pagada cuyo vencimiento no
    ha pasado.
-   **Vencido:** obligación no marcada como pagada cuyo vencimiento ha
    pasado.
-   **Notificación web:** aviso persistente visible dentro de la
    aplicación para el administrador.
-   **Notificación WhatsApp:** mensaje enviado a través de un proveedor
    compatible; la aceptación del envío no implica necesariamente
    entrega o lectura.
-   **Verificación:** comprobar que un producto cumple sus requisitos
    especificados.
-   **Validación:** comprobar que el producto satisface las necesidades
    del usuario y del negocio.

# 2. Contexto, objetivos y alcance

## 2.1 Objetivo general

Permitir al administrador registrar inquilinos y sus documentos de
identificación, administrar propiedades y contratos, controlar
obligaciones mensuales de alquiler, registrar manualmente pagos completos y abonos de alquiler, visualizar el
saldo pendiente y consultar vencimientos mediante un calendario con
notificaciones anticipadas y alertas diarias de atraso.

## 2.2 Objetivos específicos

1.  Mantener fichas de inquilinos con datos personales y fotografía de
    la cédula.
2.  Asociar cada contrato con un único inquilino y una única propiedad.
3.  Generar como máximo una obligación por contrato y período de alquiler
    configurado, sin duplicados.
4.  Registrar pagos completos y abonos de alquiler, manteniendo visible el
    saldo pendiente hasta completar el importe exigible.
5.  Registrar la fecha real de recepción y conservar la fecha/hora en que
    el movimiento fue ingresado al sistema.
6.  Consultar pagos y saldos en un calendario, con filtros por inquilino
    y estado.
7.  Configurar recordatorios anticipados y emitir alertas diarias de
    obligaciones vencidas.
8.  Proteger datos personales y conservar la trazabilidad de cambios
    relevantes.

## 2.3 Incluido en la primera versión

-   Registro, consulta, edición y desactivación lógica de inquilinos.
-   Carga y consulta autorizada de fotografía de cédula.
-   Registro de propiedades.
-   Registro, modificación controlada y finalización de contratos.
-   Monto mensual fijo por contrato.
-   Vencimiento por día fijo del mes; si el día no existe, usar el
    último día del mes.
-   Generación de obligaciones conforme a la vigencia y al período de
    alquiler configurado por contrato.
-   Registro manual de pagos completos y abonos de alquiler, con cálculo
    del saldo pendiente.
-   Gestión del depósito de garantía asociado al contrato, incluyendo
    registro de abonos y saldo pendiente.
-   Estados pendiente, vencido y pagado.
-   Historial de obligaciones y pagos.
-   Calendario mensual general y filtros por inquilino y estado.
-   Notificaciones dentro del sistema web.
-   Notificaciones de WhatsApp mediante un proveedor compatible.
-   Recordatorios anticipados configurables y alertas diarias de atraso.
-   Una única cuenta administradora.
-   Registro de auditoría de operaciones críticas.

## 2.4 Fuera del alcance inicial

-   Cobro o procesamiento automático de dinero.
-   Integración bancaria y conciliación automática.
-   Procesamiento automático de dinero, conciliación bancaria o cobro
    automatizado. Los abonos de alquiler se registran manualmente y no
    liquidan la obligación hasta que el saldo pendiente sea cero.
-   Conversión automática entre monedas o gestión de tipos de cambio.
-   Cálculo automático de intereses, multas o penalizaciones.
-   Facturación electrónica o contabilidad completa.
-   Acceso de inquilinos a un portal propio.
-   Varias cuentas humanas con roles diferenciados.
-   Correo electrónico y SMS como canales de notificación.
-   Gestión simultánea de varios inquilinos bajo un mismo contrato.
-   Cobros automáticos o procesamiento de dinero.
-   Reembolsos, devoluciones o aplicación de deducciones al depósito de
    garantía, hasta que se definan reglas de negocio específicas.

## 2.5 Supuestos

-   El primer piloto se utilizará en Costa Rica, pero el producto se
    diseñará para poder configurarse para otras regiones.
-   La moneda predeterminada será el colón costarricense (CRC); podrá
    configurarse la moneda por contrato.
-   La zona horaria predeterminada será `America/Costa_Rica`; deberá
    poder configurarse según la región o ubicación de la propiedad.
-   La plataforma conservará los importes en la moneda contractual
    original. La conversión automática de monedas queda fuera del
    alcance inicial.
-   El administrador es responsable de registrar manualmente la
    recepción de cada pago.
-   El monto mensual permanece fijo durante la vigencia del contrato,
    excepto cuando se registre una modificación contractual con fecha
    efectiva.
-   La primera versión tendrá una única cuenta administradora.
-   El envío de WhatsApp depende de la contratación y configuración de
    un proveedor externo compatible.

# 3. Actores y límites del sistema

  --------------------------------------------------------------------------
  **Actor o sistema   **Responsabilidad**
  externo**           
  ------------------- ------------------------------------------------------
  **Administrador**   Gestiona inquilinos, propiedades, contratos, pagos,
                      configuración y consulta notificaciones.

  **Servicio          Ejecuta la generación/control periódico de
  programado de       obligaciones y alertas, sin depender de que la
  procesos**          interfaz esté abierta.

  **Proveedor de      Acepta, procesa y reporta los estados disponibles de
  WhatsApp**          los mensajes externos.
  --------------------------------------------------------------------------

El inquilino no tendrá acceso directo al sistema en esta versión. Las
notificaciones se dirigen al administrador, salvo que una decisión
futura apruebe expresamente notificar también al inquilino.

# 4. Requisitos funcionales

## 4.1 Gestión de inquilinos

**RF-01 --- Registrar inquilino.** El sistema deberá permitir registrar
nombre completo, número de identificación, teléfono, correo electrónico
y fotografía de la cédula.

**RF-02 --- Validar información.** El sistema deberá validar campos
obligatorios, formato de contacto, tipo de archivo y tamaño máximo
configurado antes de aceptar el registro.

**RF-03 --- Consultar y actualizar al inquilino.** El administrador
deberá poder buscar, consultar y actualizar la ficha del inquilino. Los
cambios de identificación deberán validarse y quedar auditados.

**RF-04 --- Desactivar inquilino.** El sistema deberá permitir
desactivar a un inquilino sin eliminar contratos, obligaciones ni
historial relacionado.

**RF-05 --- Consultar ficha de inquilino.** El sistema deberá mostrar
datos de contacto, contrato vigente cuando exista, obligaciones y el
historial asociado, respetando las restricciones de acceso a documentos.

## 4.2 Gestión de propiedades y contratos

**RF-06 --- Registrar propiedad.** El sistema deberá permitir registrar
una propiedad con identificador único, descripción, dirección y estado.

**RF-07 --- Crear contrato.** El sistema deberá permitir asociar un
único inquilino con una única propiedad y registrar fecha de inicio, fecha de finalización si existe, monto mensual fijo,
día de vencimiento de 1 a 31 y período de alquiler aplicable definido por
el administrador para ese contrato.

**RF-08 --- Validar solapamiento contractual.** El sistema deberá
impedir contratos incompatibles simultáneos para una misma propiedad. La
validación considerará las fechas de vigencia.

**RF-09 --- Finalizar contrato.** El sistema deberá permitir registrar
la fecha de finalización. No generará obligaciones para períodos no
cubiertos por el contrato y conservará las obligaciones ya registradas y
su historial.

**RF-10 --- Modificar condiciones contractuales.** El sistema deberá
permitir cambios autorizados en monto, día de vencimiento, período de
alquiler y vigencia, registrando fecha efectiva y auditoría. Desde la fecha
efectiva, el sistema actualizará automáticamente las obligaciones no pagadas
afectadas, incluidas las vencidas que continúen sin pagarse. Las obligaciones
pagadas no se modificarán. La actualización deberá conservar el valor
anterior, el nuevo valor y la fecha efectiva para reconstruir el cambio.

## 4.3 Obligaciones y pagos

**RF-11 --- Generar obligaciones por período.** El sistema deberá generar
una obligación por contrato y período de alquiler definido para ese contrato,
siempre que corresponda según la vigencia contractual. Usará el monto y la
regla de vencimiento aplicables. Si el día de vencimiento configurado no
existe en el mes, usará el último día calendario del mes. La definición
concreta del período y su modificación quedan sujetas a las decisiones
pendientes indicadas en el registro de decisiones.

**RF-12 --- Evitar duplicados.** El sistema deberá impedir más de una
obligación para la misma combinación de contrato y período, incluso si
el proceso de generación se ejecuta repetidamente o en paralelo.

**RF-13 --- Registrar pago completo recibido.** El administrador deberá
poder registrar el pago que completa el saldo de una obligación, indicar la
fecha real de recepción y agregar una observación opcional. La fecha real
podrá ser anterior a la fecha de registro en el sistema. Se conservarán
ambas marcas temporales; no se exigirá comprobante adjunto en esta versión.
Una obligación solo podrá marcarse pagada cuando su saldo pendiente sea cero.

**RF-14 --- Determinar estado de obligación.** El sistema deberá
distinguir los estados pendiente, vencido y pagado. La transición a
vencido se determinará usando la fecha local de Costa Rica y la fecha de
vencimiento.

**RF-15 --- Consultar historial.** El sistema deberá permitir consultar
obligaciones por inquilino, contrato, período y estado, mostrando monto
esperado, vencimiento, estado y fecha de recepción si existe.

**RF-16 --- Corregir registro de pago.** El sistema deberá permitir que
el administrador corrija un registro de pago autorizado y deberá guardar
el valor anterior, el nuevo valor, la fecha y el responsable de la
modificación.

**RF-34 --- Registrar abono de alquiler.** El administrador deberá poder
registrar uno o varios abonos manuales asociados a una obligación, indicando
importe positivo, fecha real de recepción y observación opcional. La fecha
real podrá ser anterior a la fecha de registro. El sistema conservará la fecha
real y la fecha/hora de registro. Un abono no marcará la obligación como
pagada mientras exista saldo pendiente.

**RF-35 --- Calcular saldo de alquiler.** El sistema deberá calcular y mostrar
el saldo pendiente de cada obligación como importe exigible menos la suma de
los abonos válidos registrados. El saldo no podrá ser negativo. Las
correcciones deberán quedar auditadas y no borrar el historial de movimientos.

**RF-36 --- Sustituir inquilino mediante nuevo contrato.** Cuando cambie el
inquilino asociado a una propiedad, el administrador deberá cerrar el contrato
anterior y crear un nuevo contrato para el nuevo inquilino. El sistema deberá
conservar la historia del contrato anterior y validar que las vigencias no se
solapen de forma incompatible.

## 4.4 Calendario

**RF-17 --- Mostrar calendario mensual.** El sistema deberá mostrar las
obligaciones en un calendario mensual e identificar al inquilino, la
fecha de vencimiento y el estado.

**RF-18 --- Filtrar por inquilino.** El administrador deberá poder
filtrar el calendario para mostrar solo las obligaciones de un inquilino
y quitar el filtro para recuperar la vista general.

**RF-19 --- Filtrar por estado.** El sistema deberá permitir filtrar por
pendiente, vencido y pagado.

**RF-20 --- Consultar detalle de evento.** Al seleccionar un evento, el
sistema deberá mostrar el contrato asociado, período, monto esperado,
vencimiento, estado, fecha de recepción y observación cuando exista.

## 4.5 Notificaciones

**RF-21 --- Configurar recordatorios anticipados.** El administrador
deberá poder configurar la anticipación de los recordatorios en días
antes del vencimiento. La política de aplicación de cambios deberá
evitar duplicados y respetar las notificaciones ya procesadas.

**RF-22 --- Generar alertas diarias de atraso.** El sistema deberá
detectar diariamente obligaciones vencidas que sigan pendientes y
generar una alerta por obligación y día de procesamiento. Una vez pagada
una obligación, no se generarán alertas futuras para ella.

**RF-23 --- Notificar por canales aprobados.** El sistema deberá
admitir:

-   Notificaciones persistentes dentro de la aplicación web para el
    administrador.
-   Envío de WhatsApp mediante un proveedor compatible y configurado.

El sistema no deberá declarar que un mensaje fue entregado si solo se ha
confirmado su aceptación para procesamiento.

**RF-24 --- Registrar intentos de notificación.** El sistema deberá
conservar obligación asociada, canal, destinatario, fecha programada,
fecha de intento, resultado, reintentos y los identificadores/estados
que el proveedor exponga.

**RF-25 --- Cancelar notificaciones futuras al pagar.** Cuando una
obligación pase a pagada, el sistema deberá cancelar recordatorios y
alertas futuros relacionados. Las notificaciones anteriores permanecerán
en el historial.

## 4.6 Acceso y auditoría

**RF-26 --- Autenticar administrador.** El sistema deberá requerir
autenticación antes de permitir acceso a funciones administrativas y
documentos privados.

**RF-27 --- Administrar una cuenta.** La primera versión deberá operar
con una única cuenta administradora. La recuperación y rotación de
credenciales deberán definirse en el diseño de seguridad.

**RF-28 --- Auditar operaciones críticas.** El sistema deberá registrar
cambios relevantes en inquilinos, contratos, obligaciones, pagos, abonos y
configuración de notificaciones, incluyendo actor, fecha/hora de registro,
operación y valores anteriores/nuevos necesarios para reconstruir el cambio,
sin almacenar secretos ni documentos completos en los registros.

**RF-29 --- Definir depósito de garantía.** El sistema deberá permitir
registrar en el contrato, cuando corresponda, el importe total del
depósito de garantía, la moneda contractual y las condiciones o fecha de
pago acordadas. El depósito se gestionará separado de las obligaciones
mensuales de alquiler.

**RF-30 --- Registrar abonos al depósito.** El administrador deberá
poder registrar uno o varios abonos al depósito de garantía. Cada
registro incluirá importe recibido, fecha real de recepción y
observación opcional. El sistema deberá impedir importes nulos o negativos y bloquear abonos
que superen el saldo pendiente. El flujo ordinario admite hasta tres abonos
efectivamente recibidos; una excepción administrativa puede permitir abonos
adicionales, con auditoría. Los controles concretos de esa excepción siguen
pendientes de definición.

**RF-31 --- Calcular saldo del depósito.** El sistema deberá calcular el
saldo pendiente como el importe total acordado menos la suma de los
abonos registrados, y mostrar el depósito como pendiente, parcialmente
pagado o completado.

**RF-32 --- Consultar historial del depósito.** El sistema deberá
mostrar el importe acordado, abonos, fechas, observaciones, saldo
pendiente e historial de correcciones, conservando auditoría de cada
modificación.

**RF-33 --- Configurar moneda y zona horaria.** La plataforma deberá
ofrecer CRC y `America/Costa_Rica` como valores predeterminados y
permitir configurar la moneda aplicable al contrato y la zona horaria
operativa a nivel de organización. Las fechas y procesos programados
deberán interpretarse con la zona horaria configurada correspondiente.

# 5. Reglas de negocio

  ------------------------------------------------------------------------------
  **ID**      **Regla**
  ----------- ------------------------------------------------------------------
  **RN-01**   Cada contrato corresponde a un único inquilino y una única
              propiedad.

  **RN-02**   Una propiedad no puede tener dos contratos activos incompatibles
              en el mismo período.

  **RN-03**   Cada contrato define un monto mensual fijo, día de vencimiento
              entre 1 y 31 y período de vigencia.

  **RN-04**   Se genera una sola obligación por contrato y período mensual.

  **RN-05**   El importe exigible se obtiene de las condiciones contractuales
              aplicables al período y de la regla de prorrateo aprobada.

  **RN-06**   Una obligación está pendiente si no se registró como pagada y
              todavía no ha vencido.

  **RN-07**   Una obligación está vencida cuando pasó su vencimiento y continúa
              pendiente. Se usa la zona horaria \`America/Costa_Rica\`.

  **RN-08**   Una obligación pagada no genera nuevos recordatorios ni alertas de
              atraso.

  **RN-09**   Los cambios contractuales no alteran obligaciones pagadas. Desde
              la fecha efectiva, el sistema actualizará las obligaciones no
              pagadas afectadas, incluidas las vencidas no pagadas, conservando
              auditoría del valor previo y el nuevo. Esta regla requiere casos
              de prueba específicos y aprobación formal.

  **RN-10**   Desactivar un inquilino o finalizar un contrato no elimina su
              historial.

  **RN-11**   La recepción se confirma manualmente por el administrador; la
              fecha de vencimiento o una notificación no prueban el pago.

  **RN-12**   Un fallo de notificación no cambia el estado financiero de una
              obligación.

  **RN-13**   Si el día de vencimiento no existe en el mes, se usa el último día
              calendario de ese mes.

  **RN-14**   El sistema procesa alertas de atraso una vez por día local y evita
              duplicar alertas para la misma obligación y fecha de
              procesamiento.

  **RN-15**   Solo se generan obligaciones para períodos cubiertos por la
              vigencia del contrato. Los períodos parciales se prorratean por
              días reales del mes y se redondean al colón entero más cercano,
              sujeto a validación contractual y aprobación formal.

  **RN-16**   La primera versión tiene una única cuenta administradora; no
              existen roles adicionales.

  **RN-17**   Los períodos de alquiler que no cubran un mes completo se
              calcularán mediante prorrateo diario según los días reales del
              mes, con inicio y fin cobrables inclusivos cuando así corresponda
              al contrato.

  **RN-18**   Cada obligación conservará el período, importe final, vencimiento
              y datos necesarios para reconstruir la regla de cálculo aplicada.

  **RN-19**   El depósito de garantía es independiente de las obligaciones de
              alquiler y puede completarse mediante varios abonos.

  **RN-20**   El saldo del depósito de garantía será igual al importe total
              acordado menos la suma de abonos válidos registrados.

  **RN-21**   Los abonos al depósito no habilitan pagos parciales de las
              obligaciones mensuales de alquiler en esta versión.

  **RN-22**   La moneda predeterminada será CRC y la zona horaria predeterminada
              `America/Costa_Rica`; la zona horaria se configura a nivel de
              organización y la moneda se conserva por contrato.

  **RN-23**   Una obligación puede recibir abonos manuales. Mientras exista
              saldo pendiente, no se considerará pagada y seguirá sujeta a las
              reglas de vencimiento y alertas aprobadas.

  **RN-24**   El saldo pendiente de una obligación es el importe exigible menos
              los abonos válidos registrados; no puede ser negativo.

  **RN-25**   El período de alquiler se define por contrato mediante el
              administrador. La forma de modificarlo y su impacto sobre
              obligaciones existentes permanecen pendientes de definición.

  **RN-26**   El registro admite una fecha real de recepción retroactiva. El
              sistema conserva además la fecha/hora de registro, sin exigir
              observación únicamente por haber ingresado una fecha anterior.

  **RN-27**   El depósito de garantía es uno por contrato. El flujo ordinario
              admite hasta tres abonos efectivamente recibidos; una excepción
              administrativa puede autorizar abonos adicionales, con auditoría.
              El motivo obligatorio y las condiciones de esa excepción siguen
              pendientes de definición.

  **RN-28**   El cambio de inquilino se realiza cerrando el contrato anterior
              y creando uno nuevo; no se sustituye el inquilino dentro del
              contrato histórico.
  ------------------------------------------------------------------------------

## 5.1 Ejemplo de ajuste de vencimiento

Un contrato configurado para vencer el día 31 tendrá vencimiento el 31
de enero, el 28 de febrero (29 en año bisiesto) y el 31 de marzo.

## 5.2 Estado vencido y hora de corte

Como regla propuesta para hacer el comportamiento inequívoco, una
obligación se considerará vencida desde el día siguiente a su fecha de
vencimiento, usando la fecha local de Costa Rica. El horario exacto del
proceso programado se definirá en diseño técnico; el resultado funcional
deberá ser consistente incluso si el proceso se retrasa temporalmente.

# 6. Modelo de información conceptual

## 6.1 Entidades

  --------------------------------------------------------------------------------
  **Entidad**        **Atributos conceptuales principales**
  ------------------ -------------------------------------------------------------
  **Inquilino**      id, nombre, identificación, teléfono, correo, referencia
                     privada a la fotografía de cédula, estado, fechas de
                     creación/modificación.

  **Propiedad**      id, descripción, dirección, estado.

  **Contrato**       id, inquilino_id, propiedad_id, fecha_inicio, fecha_fin
                     opcional, monto_mensual, día_vencimiento, período de
                     alquiler definido por administrador, moneda, estado y
                     fecha efectiva de condiciones.

  **Obligación de    id, contrato_id, período, fecha_vencimiento, monto_esperado,
  pago**             estado, moneda, datos del cálculo, fecha_real_recepción
                     opcional, observación opcional.

  **Depósito de      id, contrato_id, importe_total, moneda, fecha/condiciones
  garantía**         acordadas, saldo_pendiente, estado.

  **Abono de         id, deposito_id, importe, fecha_real_recepción, observación
  depósito**         opcional, auditoría.

  **Notificación**   id, obligación_id, canal, destinatario, tipo de aviso,
                     fecha_programada, fecha_intento, resultado, número de
                     intento, referencia del proveedor.

  **Auditoría**      id, entidad, registro, actor, acción, fecha, valores/cambios
                     relevantes.
  --------------------------------------------------------------------------------

## 6.2 Relaciones

-   Un inquilino puede tener varios contratos a lo largo del tiempo.
-   Cada contrato referencia exactamente un inquilino y una propiedad.
-   Una propiedad puede tener varios contratos históricos, pero no
    contratos incompatibles simultáneos.
-   Un contrato puede tener muchas obligaciones mensuales y, cuando
    corresponda, un depósito de garantía.
-   Un depósito de garantía puede tener varios abonos.
-   Una obligación puede tener varios registros de notificación.
-   Las operaciones relevantes producen registros de auditoría.

## 6.3 Restricciones de integridad

8.  Identificadores únicos para todas las entidades.
9.  Claves foráneas válidas entre contrato, inquilino y propiedad.
10. Monto mensual mayor que cero.
11. Día de vencimiento entre 1 y 31.
12. Unicidad de contrato y período en obligaciones.
13. Una obligación pagada debe tener fecha real de recepción.
14. El estado financiero no debe inferirse de una notificación.
15. Los registros históricos no se eliminan mediante las operaciones
    ordinarias.
16. Las fotografías de cédula deben almacenarse en un repositorio
    privado; la base de datos guarda una referencia protegida, no una
    URL pública.
17. La información sensible no se incluirá en logs técnicos ni en
    mensajes de error.
18. Los abonos al depósito de garantía se registran como movimientos
    separados; no se confunden con pagos de alquiler.
19. La suma de abonos válidos determina el saldo del depósito, con
    trazabilidad de correcciones.
20. Cada obligación y depósito conserva su moneda contractual; no se
    convierte automáticamente entre monedas en la primera versión.

## 6.4 Prorrateo de períodos parciales

Cuando el contrato comience o finalice a mitad de un mes, el importe del
período parcial se calculará mediante prorrateo diario según los días
reales del mes correspondiente.

**Fórmula propuesta:** importe proporcional = (alquiler mensual /
cantidad de días reales del mes) × días cobrables.

**Redondeo propuesto por el solicitante:** al colón entero más cercano
(CRC 1); debe aplicarse de manera consistente y validarse en las pruebas.

Los días cobrables se determinarán a partir de las fechas contractuales
de inicio y fin, ambas inclusivas cuando correspondan a días de
ocupación acordados. El cálculo, los días cobrables, el importe previo al redondeo y el importe
final deberán quedar registrados en la obligación. La regla requiere
validación contractual y legal aplicable antes de la aprobación final.

# 7. Requisitos no funcionales

  ---------------------------------------------------------------------------------------------
  **ID**       **Categoría**    **Requisito verificable**
  ------------ ---------------- ---------------------------------------------------------------
  **RNF-01**   Autenticación    Todas las funciones administrativas requieren una sesión
                                autenticada. Solo existirá una cuenta administradora en la
                                primera versión.

  **RNF-02**   Autorización     Solo la cuenta administradora autenticada puede consultar
                                cédulas, modificar contratos, registrar pagos o cambiar la
                                configuración.

  **RNF-03**   Privacidad       Los datos personales y documentos se protegerán en tránsito y
                                mediante controles de acceso. Los archivos no serán públicos.

  **RNF-04**   Integridad       La generación de obligaciones será idempotente y tendrá una
                                restricción de unicidad por contrato/período.

  **RNF-05**   Confiabilidad    Un fallo de WhatsApp no impedirá consultar o registrar pagos ni
                                eliminará la notificación web persistida.

  **RNF-06**   Trazabilidad     Cambios relevantes de contrato, pagos y configuración quedarán
                                auditados.

  **RNF-07**   Usabilidad       Los formularios validarán entradas y mostrarán mensajes
                                comprensibles para errores y acciones exitosas.

  **RNF-08**   Rendimiento      Objetivo inicial a validar: consultas habituales en menos de 2
                                segundos con hasta 20 usuarios concurrentes, sin contar la
                                latencia de servicios externos. Aunque el uso inicial prevé un
                                administrador, este objetivo se conserva como meta de prueba
                                futura y deberá ajustarse al despliegue real.

  **RNF-09**   Recuperación     Deberá existir una política de respaldos y recuperación;
                                frecuencia, retención y objetivo de recuperación se definirán
                                antes de producción.

  **RNF-10**   Compatibilidad   La interfaz deberá funcionar en versiones soportadas de
                                navegadores modernos de escritorio y dispositivos móviles.

  **RNF-11**   Mantenibilidad   Las responsabilidades de inquilinos, contratos, obligaciones,
                                calendario y notificaciones deberán mantenerse separadas
                                conceptualmente.

  **RNF-12**   Configuración    Fechas presentadas en formato dd/mm/aaaa; moneda CRC; fechas y
               regional         tareas programadas interpretadas en \`America/Costa_Rica\`.
  ---------------------------------------------------------------------------------------------

Los valores de rendimiento son objetivos propuestos, no resultados
medidos ni garantías de capacidad.

# 8. Criterios de aceptación

Los criterios se formulan para poder ser ejecutados como pruebas
funcionales o revisiones de aceptación.

## CA-01 --- Registro de inquilino

**Dado** un administrador autenticado, **cuando** registra los campos
obligatorios y una imagen permitida, **entonces** el sistema guarda el
inquilino con un identificador único y permite consultar su ficha. Si
faltan campos o el archivo no es válido, muestra el error y no guarda un
registro incompleto.

## CA-02 --- Creación de contrato

**Dado** un inquilino registrado y una propiedad disponible, **cuando**
se crea un contrato con vigencia, monto válido y día de vencimiento
válido, **entonces** el contrato queda registrado. El sistema rechaza
datos incoherentes o un solapamiento contractual incompatible.

## CA-03 --- Generación mensual y mes corto

**Dado** un contrato de ₡180 000 con vencimiento el día 31, **cuando**
se generan obligaciones para enero, febrero y marzo de un año no
bisiesto, **entonces** las fechas son 31 de enero, 28 de febrero y 31 de
marzo. En año bisiesto, febrero vence el 29. Ejecutar nuevamente el
proceso no crea duplicados.

## CA-04 --- Registro manual de pago

**Dado** una obligación pendiente, **cuando** el administrador registra
la fecha real de recepción y una observación opcional, **entonces** la
obligación queda pagada, la fecha y observación se conservan y se
cancelan avisos futuros. Una fecha inválida produce un error sin guardar
un estado inconsistente.

## CA-19 --- Abono parcial de alquiler y saldo pendiente

**Dado** una obligación con importe exigible de ₡180.000, **cuando** el
administrador registra un abono de ₡60.000, **entonces** el sistema conserva
el movimiento y muestra saldo pendiente de ₡120.000; la obligación no queda
pagada. La fecha real de recepción y la fecha/hora de registro se conservan
por separado.

## CA-20 --- Completar obligación con abonos

**Dado** una obligación con saldo pendiente, **cuando** los abonos válidos
acumulados alcanzan el importe exigible, **entonces** el saldo queda en cero
y la obligación puede pasar a pagada conforme al registro manual del
administrador. El sistema impide saldo negativo y conserva la auditoría.

## CA-21 --- Fecha real retroactiva

**Dado** que un pago o abono fue recibido antes del día en que se registra,
**cuando** el administrador ingresa la fecha real anterior, **entonces** el
sistema acepta la fecha si es válida, conserva la fecha/hora de registro y no
exige una observación únicamente por tratarse de una fecha retroactiva.

## CA-22 --- Modificación de condiciones con obligaciones no pagadas

**Dado** un contrato con obligaciones pagadas y no pagadas, incluidas
obligaciones vencidas, **cuando** el administrador registra un cambio con
fecha efectiva, **entonces** el sistema mantiene intactas las obligaciones
pagadas y actualiza automáticamente las obligaciones no pagadas afectadas
desde esa fecha, incluidas las vencidas que continúen impagadas. El historial
debe permitir reconstruir los valores anteriores y nuevos.

## CA-23 --- Excepción para abonos adicionales al depósito

**Dado** un depósito que ya alcanzó el máximo ordinario de tres abonos,
**cuando** el administrador autoriza una excepción, **entonces** el sistema
permite registrar abonos adicionales y deja trazabilidad de la excepción.
El motivo obligatorio y las condiciones de autorización permanecen
pendientes de definición.

## CA-05 --- Alerta diaria por atraso

**Dado** una obligación pendiente cuyo vencimiento pasó, **cuando** se
ejecuta el procesamiento diario, **entonces** la obligación queda
identificada como vencida y se genera una alerta. No se generan
duplicados para la misma obligación y día de procesamiento. Después de
marcarla pagada, no se producen nuevas alertas.

## CA-06 --- Calendario general

**Dado** obligaciones de varios inquilinos en un mes, **cuando** el
administrador abre el calendario, **entonces** puede identificar cada
vencimiento, el inquilino y el estado. Los eventos coincidentes permiten
consultar cada obligación.

## CA-07 --- Filtro por inquilino

**Dado** un calendario con obligaciones de al menos tres inquilinos,
**cuando** se selecciona uno, **entonces** solo se muestran sus
obligaciones. Al retirar el filtro se recupera la vista general y se
conserva el mes consultado.

## CA-08 --- Recordatorio configurable

**Dado** un pago pendiente y una anticipación configurada, **cuando**
llega la fecha de recordatorio calculada, **entonces** el sistema crea
la notificación web y programa el envío de WhatsApp si ese canal está
configurado. El intento y resultado quedan registrados.

## CA-09 --- Fallo de WhatsApp

**Dado** que el proveedor de WhatsApp falla o rechaza un envío,
**cuando** el sistema intenta enviar el mensaje, **entonces** registra
el resultado, aplica la política de reintentos y no cambia el estado del
pago. La notificación web persiste si la aplicación está operativa. El
sistema distingue aceptación, entrega y lectura según los estados
realmente disponibles.

## CA-24 --- Sustitución de inquilino

**Dado** que una propiedad cambia de inquilino, **cuando** el administrador
finaliza el contrato anterior y registra uno nuevo para el siguiente
inquilino, **entonces** ambos contratos conservan su historial y el sistema
rechaza solapamientos incompatibles.

## CA-10 --- Conservación del historial

**Dado** un contrato con obligaciones anteriores, **cuando** se
desactiva el inquilino o se finaliza el contrato, **entonces** el
historial permanece consultable y no se generan obligaciones para
períodos no cubiertos por la vigencia contractual.

## CA-11 --- Protección de cédula

**Dado** un visitante sin autenticación válida, **cuando** intenta
consultar una fotografía de cédula, **entonces** el acceso se deniega y
el archivo no puede recuperarse por una URL pública.

## CA-12 --- Cambio de condiciones

**Dado** un contrato con una modificación de monto efectiva desde un
período futuro, **cuando** se registra el cambio, **entonces** las
obligaciones históricas mantienen sus montos y las futuras aplican el
monto vigente para su período.

## CA-13 --- Una sola cuenta administradora

**Dado** el alcance de la primera versión, **cuando** se configura el
acceso, **entonces** solo existe una cuenta administradora habilitada
para operaciones administrativas. Las solicitudes sin autenticación
válida son rechazadas.

## CA-14 --- Finalización a mitad de mes

**Dado** un contrato con alquiler mensual de ₡180.000 en enero y un
período cobrable del 3 al 20 de enero, **cuando** el sistema calcula el
importe proporcional, **entonces** utiliza 18 de los 31 días del mes y
calcula ₡104.516 al redondear al colón entero más cercano. El importe,
período, días cobrables y regla de cálculo quedan registrados.

## CA-15 --- Abonos al depósito de garantía

**Dado** un depósito acordado de ₡300.000, **cuando** el administrador
registra un abono de ₡100.000, **entonces** el sistema conserva el
movimiento y muestra saldo pendiente de ₡200.000 y estado parcialmente
pagado.

## CA-16 --- Completar depósito mediante varios abonos

**Dado** un depósito con saldo pendiente, **cuando** se registra otro
abono válido que completa el total acordado, **entonces** el saldo queda
en cero y el depósito se muestra como completado, conservando todos los
abonos por separado.

## CA-17 --- Separación entre alquiler y depósito

**Dado** un contrato con una obligación mensual y un depósito de
garantía, **cuando** se registra un abono al depósito, **entonces** el
estado y saldo de la obligación mensual no cambian.

## CA-18 --- Configuración regional predeterminada

**Dado** una nueva configuración de la plataforma sin ajustes
regionales, **cuando** se crean contratos y se programan procesos,
**entonces** se usan CRC y `America/Costa_Rica`. Cuando se configura
otra moneda o zona horaria compatible, el sistema aplica esa
configuración sin alterar los registros históricos ni convertir
automáticamente importes.

# 9. Matriz de trazabilidad

  ------------------------------------------------------------------------
  **Necesidad / objetivo**    **Requisitos**            **Criterios**
  --------------------------- ------------------------- ------------------
  **Registrar inquilinos y    RF-01--RF-05,             CA-01, CA-11
  cédulas**                   RNF-02--RNF-03            

  **Administrar propiedades y RF-06--RF-10,             CA-02, CA-10,
  contratos**                 RN-01--RN-03              CA-12, CA-14

  **Generar obligaciones sin  RF-11--RF-12,             CA-03
  duplicados**                RN-04--RN-05, RNF-04      

  **Registrar pagos e         RF-13--RF-16,             CA-04, CA-10
  historial**                 RN-06--RN-11              

  **Consultar calendario y    RF-17--RF-20              CA-06, CA-07
  filtrar**                                             

  **Programar recordatorios y RF-21--RF-25,             CA-05, CA-08,
  alertas**                   RN-07--RN-08,             CA-09
                              RN-12--RN-14              

  **Restringir acceso y       RF-26--RF-28,             CA-11, CA-13
  auditar**                   RNF-01--RNF-03, RNF-06,   
                              RNF-13--RNF-16            

  **Gestionar depósito de     RF-29--RF-32,             CA-15--CA-17
  garantía y abonos**         RN-19--RN-21              

  **Prorratear períodos       RN-17--RN-18              CA-14
  parciales**                                           

  **Operar en varias          RF-33, RN-22, RNF-17      CA-18
  regiones**                                            
  ------------------------------------------------------------------------

# 10. Riesgos y dependencias

  -----------------------------------------------------------------------
  **Riesgo o           **Respuesta requerida**
  dependencia**        
  -------------------- --------------------------------------------------
  **Exposición de      Repositorio privado, acceso autenticado, permisos
  fotografías de       mínimos, cifrado y política de retención.
  cédula**             

  **Duplicación de     Unicidad por contrato/período y generación
  obligaciones**       idempotente.

  **Fallo de           Registro de resultados, reintentos controlados y
  WhatsApp**           notificación web como canal interno.

  **Proveedor externo  Seleccionar proveedor y verificar credenciales,
  no elegido**         costos, plantillas y políticas antes de
                       integración.

  **Ejecución diaria   Diseñar procesamiento programado independiente de
  interrumpida**       la interfaz y recuperación de ejecuciones
                       fallidas.

  **Contrato           Aplicar prorrateo diario aprobado y validar su
  comienza/termina a   correspondencia con el contrato.
  mitad de mes**       

  **Abonos del         Modelar depósito y abonos como
  depósito confundidos entidades/movimientos separados; definir política
  con alquiler**       de excesos y devoluciones.

  **Uso en múltiples   Moneda y zona horaria configurables, valores
  regiones**           predeterminados CRC y `America/Costa_Rica`; evitar
                       conversiones implícitas.

  **Cambio de monto o  Fecha efectiva, historial y valores contractuales
  vencimiento**        aplicados a cada obligación.

  **Pérdida de datos** Política de respaldo y prueba de restauración
                       antes de producción.

  **Una sola cuenta    Definir contraseñas robustas, recuperación segura,
  comprometida**       protección contra intentos repetidos y, si
                       procede, MFA.
  -----------------------------------------------------------------------

# 11. Decisiones pendientes y registro de decisiones

Las decisiones aprobadas no deben volver a tratarse como preguntas
abiertas. Solo quedan pendientes las siguientes:

  ---------------------------------------------------------------------------------
  **ID**      **Decisión            **Opciones a evaluar**        **Responsable
              pendiente**                                         sugerido**
  ----------- --------------------- ----------------------------- -----------------
  **DP-01**   Validación            Confirmar regla, días         Propietario del
              contractual/legal del cobrables y redondeo          negocio
              prorrateo diario para                               
              períodos parciales                                  

  **DP-09**   Catálogo de monedas   Definir monedas admitidas y   Propietario y
              admitidas             reglas de selección por       responsable
                                    contrato. La zona horaria     técnico
                                    queda definida a nivel de
                                    organización.                      

  **DP-02**   Hora de ejecución de  Hora local fija; política de  Propietario y
              alertas diarias       recuperación si la ejecución  responsable
                                    falla                         técnico

  **DP-03**   Cambios de            Aplicar a todas las           Propietario del
              configuración de      notificaciones futuras no     negocio
              recordatorios         procesadas o solo a nuevos    
                                    períodos                      

  **DP-04**   Proveedor de WhatsApp Proveedor, costos, estados de Propietario y
                                    entrega, credenciales y       responsable
                                    condiciones                   técnico

  **DP-05**   Política de respaldo  Período de conservación,      Propietario,
              y retención de        eliminación y recuperación    considerando
              cédulas                                             obligaciones
                                                                  aplicables

  **DP-06**   Requisitos            Carga prevista, RPO/RTO,      Propietario y
              cuantitativos de      disponibilidad y retención    responsable
              rendimiento y                                       técnico
              recuperación

  **DP-10**  Notificación al        Aclarar si registrar un abono  Propietario del
              administrador por     genera una notificación       negocio
              abono de alquiler     individual o solo actualiza
                                    el saldo visible. P2 indicó
                                    notificación automática y P8/P14
                                    indicaron no notificar cada
                                    abono individualmente.

  **DP-11**  Definición y cambio    Precisar campos del período de  Propietario del
              del período de        alquiler por contrato,         negocio
              alquiler              modificación y efecto sobre
                                    obligaciones existentes.

  **DP-12**  Excepción al máximo    Definir quién puede autorizar,  Propietario del
              de tres abonos del    si requiere motivo y qué       negocio
              depósito              evidencia se conserva.

  **DP-13**  Calendarios/acuerdos   Definir si un depósito puede    Propietario del
              de abono del depósito tener varios calendarios, cómo
                                    se modifica un acuerdo y cómo
                                    se vinculan abonos al acuerdo.

  **DP-14**  Pregunta P11 de la     La respuesta continúa pendiente; Propietario del
              ronda de aclaración   recuperar el enunciado original  negocio
                                    antes de especificar el requisito.

  **DP-15**  Corrección de fecha    Definir si la corrección de una  Propietario del
              real de pago/abono    fecha retroactiva requiere       negocio
                                    motivo y qué auditoría adicional
                                    aplica.
  ---------------------------------------------------------------------------------

# 12. Gestión de requisitos y control de cambios

18. Todo requisito deberá tener identificador único, descripción,
    fuente, prioridad, estado y método de verificación.
19. Los cambios se solicitarán con justificación y análisis de impacto
    sobre requisitos, reglas de negocio, modelo de datos, criterios de
    aceptación, seguridad y planificación.
20. El responsable designado aprobará o rechazará cada cambio antes de
    considerarlo parte de la línea base.
21. Las versiones aprobadas no se sobrescribirán sin registrar el
    cambio.
22. Los requisitos ambiguos o bloqueados se resolverán antes de
    construir funcionalidades que dependan de ellos.
23. La matriz de trazabilidad se actualizará con cada cambio aprobado.
24. Una versión se considerará aprobada solo cuando consten responsable,
    fecha y aceptación formal.

# 13. Revisión y condiciones de aprobación

Antes de aprobar esta ERS, los revisores deben confirmar:

☐ Objetivos y alcance comprensibles.

☐ Requisitos necesarios, no contradictorios y verificables.

☐ Reglas de vencimiento, período de alquiler y generación de obligaciones consistentes.

☐ Regla de prorrateo por días reales y redondeo al colón más cercano validada.

☐ Gestión de abonos de alquiler y depósito, límites, excepciones y saldos validados.

☐ Moneda y zona horaria configurables, con valores predeterminados de
Costa Rica, verificadas.

☐ Canales de notificación y límites de WhatsApp comprendidos.

☐ Protección de cédulas y datos personales aceptada.

☐ Criterios de aceptación suficientes para comprobar los requisitos.

☐ Matriz de trazabilidad revisada.

☐ Dependencias, riesgos y decisiones pendientes asignados.

☐ Aprobación formal del propietario del producto.

## Registro de aprobación

  --------------------------------------------------------------------------
  **Rol**                           **Nombre**    **Decisión**   **Fecha**
  --------------------------------- ------------- -------------- -----------
  **Propietario del producto**      Por designar  Pendiente      Pendiente

  **Responsable de requisitos**     Por designar  Pendiente      Pendiente

  **Responsable técnico**           Por designar  Pendiente      Pendiente
  --------------------------------------------------------------------------

**Estado actual:** línea base propuesta para revisión. No debe
describirse como "oficialmente aprobada" hasta completar el registro de
aprobación.

# 14. Próxima fase: arquitectura y diseño técnico

Después de aprobar los requisitos y resolver los bloqueos relevantes, se
recomienda producir artefactos separados y enlazados a esta ERS:

25. **Documento de arquitectura de software:** contexto, decisiones
    arquitectónicas, vistas de componentes, despliegue, datos, seguridad
    e integraciones.
26. **Modelo lógico y físico de datos:** entidades, relaciones, claves,
    restricciones y estrategia de migraciones.
27. **Especificación de API e interfaces:** operaciones, validaciones,
    errores y contratos de integración.
28. **Diseño del proceso de obligaciones y notificaciones:**
    idempotencia, planificación, reintentos, estados y recuperación.
29. **Plan de verificación y pruebas:** casos de prueba vinculados a los
    identificadores de requisitos.
30. **Plan de implementación por entregas:** tareas priorizadas según
    dependencias y riesgos.

La ERS define **qué** debe cumplir el sistema. El documento de
arquitectura describirá **cómo** se organizará la solución para
satisfacer esos requisitos. No deben confundirse ambos documentos.

# 15. Base metodológica y referencias

La estructura de este documento toma como referencia las siguientes
fuentes públicas. Estas referencias orientan el método de documentación;
no significan que el proyecto haya sido auditado ni certificado por esas
organizaciones.

31. **ISO/IEC/IEEE 29148:2018 --- Systems and software engineering ---
    Life cycle processes --- Requirements engineering.** Norma
    internacional sobre procesos y productos de ingeniería de requisitos
    durante el ciclo de vida. ISO indica que la edición 2018 fue
    revisada y confirmada en 2024 y continúa vigente al momento de la
    consulta.

   https://www.iso.org/standard/72089.html

32. **IEEE Standards Association --- IEEE/ISO/IEC 29148-2018.** Resume
    que la norma aborda procesos y productos de requisitos,
    características de requisitos bien redactados y aplicación iterativa
    de la ingeniería y gestión de requisitos.

   https://standards.ieee.org/ieee/29148/6937/

33. **NASA --- Systems Engineering Handbook, Appendix C: How to Write a
    Good Requirement; Appendix D: Requirements Verification Matrix;
    Appendix E: Validation Requirements Matrix.** Proporciona listas de
    comprobación para redactar, validar y verificar requisitos, y
    recomienda enlazar los requisitos identificados de manera única con
    sus métodos de verificación.

   https://www.nasa.gov/reference/system-engineering-handbook-appendix/

34. **NASA Software Engineering Handbook --- SWE-050: Software
    Requirements.** Describe la descomposición jerárquica de requisitos
    y la importancia de mantener trazabilidad hasta los niveles de
    diseño para comprobar que cada requisito deriva de necesidades
    superiores.

   https://swehb.nasa.gov/spaces/7150/pages/16449651/SWE-050%2B-%2BSoftware%2BRequirements

35. **Carnegie Mellon University, Software Engineering Institute (SEI)
    --- Views and Beyond: The SEI Approach for Architecture
    Documentation.** Recomienda organizar la documentación
    arquitectónica alrededor de vistas relevantes para los interesados y
    registrar también la información transversal y la justificación de
    las decisiones. Se utiliza aquí para orientar la siguiente fase de
    arquitectura, no para sustituir la ERS.

   https://insights.sei.cmu.edu/library/views-and-beyond-the-sei-approach-for-architecture-documentation/

36. **Clements et al. --- Documenting Software Architectures: Views and
    Beyond, 2nd edition.** Referencia del SEI para documentar
    arquitectura, estructuras, interfaces, comportamiento, decisiones y
    necesidades de distintos interesados.

   https://www.sei.cmu.edu/library/documenting-software-architectures-views-and-beyond-second-edition/

## Aplicación de estas referencias al documento

-   Requisitos con identificadores estables y lenguaje obligatorio.
-   Separación entre alcance, requisitos funcionales, calidad, reglas de
    negocio y decisiones pendientes.
-   Criterios de aceptación verificables.
-   Matriz de trazabilidad entre necesidades, requisitos y pruebas.
-   Registro de versiones, cambios y aprobación.
-   Separación explícita entre especificación de requisitos y futura
    documentación de arquitectura.

---------------------------------------------------------------------------------------------------------------------------------------

**Fin del documento --- ERS-SGA-001, versión 1.4 (borrador no aprobado).**


## Anexo A. Estado de respuestas de las rondas de aclaración

Este anexo registra respuestas del solicitante y no sustituye la aprobación
formal del propietario del negocio.

| Pregunta | Respuesta registrada | Tratamiento documental |
|---|---|---|
| P1 | Prorratear períodos parciales por días reales. | Incorporado como regla propuesta; requiere validación contractual/legal. |
| P2 | Permitir abonos de alquiler y mantener saldo pendiente; se mencionó notificación automática al administrador. | Abonos y saldo incorporados. La notificación por cada abono queda pendiente por conflicto con P8/P14. |
| P3 | Un depósito por contrato; máximo ordinario de tres abonos. | Incorporado; la excepción administrativa se refleja según P15. |
| P4 | Un inquilino por contrato. | Conserva RN-01 y el alcance actual. |
| P5 | El administrador define el período por contrato. | Incorporado; definición de campos y cambios queda pendiente. |
| P6 | Permitir fechas reales de recepción anteriores a la fecha de registro. | Incorporado; conservar ambas fechas. |
| P7 | Fecha mensual acordada; si termina antes, aplicar prorrateo. | Incorporado como regla propuesta junto con la regla de prorrateo. |
| P8 | Abonos manuales; mostrar saldo al administrador, sin notificación individual por abono. | Incorporado parcialmente; contradicción con P2 señalada en DP-10. |
| P9 | Máximo ordinario de tres abonos efectivamente recibidos al depósito. | Incorporado en RN-27. |
| P10 | Actualizar automáticamente obligaciones no pagadas desde la fecha efectiva, incluidas las vencidas que siguen impagadas. | Incorporado en RF-10/RN-09; requiere pruebas de impacto e historial. |
| P11 | Sin respuesta registrada. | Pendiente; no se inventa el enunciado ni la respuesta. |
| P12 | Cerrar el contrato anterior y crear uno nuevo al cambiar de inquilino. | Incorporado en RF-36/RN-28. |
| P13 | El administrador define el período de alquiler por contrato. | Incorporado; modificaciones del período quedan pendientes. |
| P14 | Mostrar saldo actualizado sin notificación individual por cada abono. | Incorporado provisionalmente; conflicto con P2 permanece abierto. |
| P15 | Permitir excepción administrativa para registrar abonos adicionales al depósito. | Incorporado; autorización, motivo y auditoría específica pendientes. |
| P16 | Actualizar obligaciones no pagadas desde la fecha efectiva, incluso vencidas no pagadas. | Incorporado en RF-10/RN-09. |
| P17 | Permitir fecha retroactiva sin observación obligatoria y conservar fecha de registro. | Incorporado en RF-13/RF-34/RN-26; correcciones posteriores de fecha quedan pendientes. |
| R1 | Prorrateo por días reales. | Incorporado en RN-15/RN-17 y sección 6.4. |
| R2 | Redondear al colón entero más cercano. | Incorporado en RN-15, sección 6.4 y CA-14. |
| R3 | Bloquear abonos al depósito que superen el saldo pendiente. | Decisión incorporada en RF-30; no queda como pendiente. |
| R4 | Un mismo depósito con varios acuerdos o calendarios de abono. | Un depósito por contrato; la estructura y modificación de acuerdos/calendarios queda pendiente en DP-13. |
| R5 | Devoluciones y deducciones del depósito fuera del alcance inicial. | Se conserva como exclusión de alcance; una fase futura requeriría cambio aprobado. |
| R6 | Configurar la zona horaria a nivel de organización. | Incorporado en RN-22 y DP-09; catálogo de monedas sigue pendiente. |
| R7 | Bloquear solapamientos contractuales incompatibles. | Conservado en RF-08 y RN-02. |

**Estado de la línea base:** borrador actualizado. Las reglas reflejan las
respuestas del solicitante, pero las decisiones pendientes y la aprobación
formal continúan abiertas.
