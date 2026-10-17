# Documento de Arquitectura de Software (DAS)

## Sistema de Gestión de Alquileres

**Identificador:** DAS-SGA-001\
**Versión:** 0.3\
**Estado:** Borrador actualizado para revisión; no aprobado\
**Fecha:** 14 de octubre de 2026\
**ERS de referencia:** ERS-SGA-001 v1.4 (borrador no aprobado)\
**Valores regionales por defecto:** moneda CRC; zona horaria
`America/Costa_Rica`

Este borrador incorpora el impacto arquitectónico de las respuestas de
aclaración reflejadas en ERS-SGA-001 v1.4: abonos de alquiler y saldos,
período de alquiler definido por contrato, actualización de obligaciones no
pagadas desde una fecha efectiva, fecha real retroactiva, un depósito por
contrato con máximo ordinario de tres abonos y excepción administrativa, y
cambio de inquilino mediante cierre y nuevo contrato. Las respuestas aún
requieren validación y aprobación formal del negocio. No se selecciona todavía
proveedor de nube, framework, motor de base de datos ni proveedor de WhatsApp.
Este documento no autoriza iniciar la implementación.

## Control e historial

  -----------------------------------------------------------------------
  Campo                               Valor
  ----------------------------------- -----------------------------------
  Propósito                           Describir la estructura propuesta,
                                      responsabilidades, interacciones,
                                      riesgos y decisiones
                                      arquitectónicas.

  Estado                              Borrador sujeto a validación y
                                      aprobación.

  Historial                           v0.1 --- primera propuesta; v0.2
                                      --- actualización de depósitos,
                                      prorrateo, privacidad e
                                      internacionalización; v0.3 ---
                                      impacto de abonos de alquiler,
                                      períodos contractuales, fechas
                                      retroactivas y reglas de actualización.
  -----------------------------------------------------------------------

## 1. Propósito y alcance

La arquitectura debe soportar inquilinos, propiedades, contratos,
obligaciones por período de alquiler definido por contrato, pagos completos
y abonos de alquiler registrados manualmente con cálculo de saldo, un
depósito de garantía por contrato con múltiples abonos, calendario,
notificaciones web y WhatsApp, auditoría y almacenamiento privado de
fotografías de documentos de identidad.

La primera versión no procesará dinero automáticamente, no calculará intereses o
multas, no realizará conversión monetaria automática y no gestionará
devoluciones ni deducciones del depósito de garantía. El depósito y sus
abonos son registros administrativos; no equivalen a procesamiento
bancario.

## 2. Principios y referencias metodológicas

La documentación toma como orientación SEI *Views and Beyond*, arc42, C4
Model y las guías OWASP sobre autenticación y carga de archivos. Estas
referencias guían el diseño, pero no certifican el sistema.

Principios: - Separar interfaz, casos de uso, reglas de negocio y
adaptadores de infraestructura. - Mantener la lógica de contratos, obligaciones, pagos/abonos de alquiler,
depósitos y abonos al depósito en servicios de dominio, no en la interfaz. - Preservar la historia financiera y auditar correcciones. -
Hacer idempotentes los procesos programados. - Aplicar autorización en
el backend para cada operación sensible y descarga de documentos. -
Conservar moneda original por contrato y evitar conversiones
implícitas. - Hacer explícitas las decisiones pendientes mediante
registros ADR.

## 3. Contexto del sistema

  -----------------------------------------------------------------------
  Elemento                            Responsabilidad
  ----------------------------------- -----------------------------------
  Administrador                       Gestiona inquilinos, propiedades,
                                      contratos, alquileres, depósitos,
                                      abonos, configuración y
                                      notificaciones.

  Aplicación SGA                      Coordina reglas de negocio,
                                      consultas, auditoría y acceso a
                                      documentos.

  Base de datos                       Persiste registros, relaciones,
                                      importes, estados e historial.

  Almacenamiento privado              Conserva fotografías de cédula sin
                                      acceso público directo.

  Planificador de procesos            Genera obligaciones y procesa
                                      recordatorios/alertas.

  Proveedor de WhatsApp               Envía mensajes mediante una
                                      integración aún por seleccionar.
  -----------------------------------------------------------------------

``` mermaid
flowchart LR
    Admin[Administrador] -->|Gestiona contratos, pagos y depósitos| SGA[Sistema de Gestión de Alquileres]
    SGA --> DB[(Base de datos)]
    SGA --> Files[(Almacenamiento privado)]
    SGA --> WA[Proveedor de WhatsApp]
    Scheduler[Planificador de tareas] --> SGA
```

## 4. Drivers arquitectónicos y atributos de calidad

  -----------------------------------------------------------------------
  Driver                              Implicación arquitectónica
  ----------------------------------- -----------------------------------
  Una cuenta administradora en la     Autenticación sencilla, pero con
  primera versión                     recuperación segura y opción de
                                      MFA.

  Historia financiera                 No borrar movimientos confirmados
                                      mediante operaciones ordinarias;
                                      registrar correcciones y conservar
                                      fecha real y fecha/hora de registro.

  Depósito con abonos                 Entidad de depósito separada de
                                      obligaciones de alquiler y
                                      movimientos de abono
                                      independientes.

  Prorrateo de alquiler               Guardar días reales, período,
                                      regla, moneda, redondeo e importe
                                      calculado aplicados a cada obligación.

Abonos de alquiler                    Registrar movimientos separados,
                                      recalcular saldo y no marcar pagada
                                      la obligación hasta que el saldo sea cero.

Cambios contractuales                 Mantener intactas obligaciones pagadas;
                                      actualizar las no pagadas afectadas desde
                                      la fecha efectiva, incluidas vencidas no pagadas,
                                      con historial auditable.

  Evitar duplicados                   Restricciones de unicidad e
                                      idempotencia en procesos
                                      programados.

  Plataforma configurable globalmente CRC y `America/Costa_Rica` como
                                      valores predeterminados; moneda por
                                      contrato y zona horaria regional
                                      configurable.

  Documentos de identidad privados    Almacenamiento privado y
                                      autorización en el backend para
                                      cada descarga.

  Web + WhatsApp                      Adaptador desacoplado del dominio
                                      financiero.
  -----------------------------------------------------------------------

Prioridades de calidad: seguridad y privacidad, integridad financiera,
trazabilidad, confiabilidad, mantenibilidad, recuperación y usabilidad.
RPO, RTO, retención y disponibilidad deben acordarse antes de
producción.

## 5. Estrategia de solución propuesta

Se mantiene como candidato un **monolito modular**: una aplicación
backend organizada por módulos de negocio, una base de datos relacional,
almacenamiento privado de archivos y procesos programados. Es una
propuesta proporcional al alcance actual, no una decisión tecnológica
definitiva. No se recomienda introducir microservicios sin una necesidad
comprobada.

Módulos lógicos sugeridos: 1. Inquilinos y documentos. 2. Propiedades y contratos. 3. Obligaciones,
prorrateo y saldos de alquiler. 4. Pagos/abonos de alquiler. 5. Depósitos
de garantía y abonos. 6. Calendario y consultas. 7. Notificaciones y
configuración regional. 8. Auditoría y operación.

## 6. Bloques lógicos (C4 nivel 2)

``` mermaid
flowchart TB
    UI[Interfaz web] --> API[Backend / API]
    API --> AUTH[Autenticación y sesiones]
    API --> TEN[Inquilinos y documentos]
    API --> CONTRACT[Propiedades y contratos]
    API --> RENT[Obligaciones de alquiler y prorrateo]
    API --> DEPOSIT[Depósitos y abonos]
    API --> CAL[Calendario y consultas]
    API --> NOTIF[Orquestación de notificaciones]
    API --> AUD[Auditoría]
    TEN --> DB[(Base de datos)]
    CONTRACT --> DB
    RENT --> DB
    DEPOSIT --> DB
    CAL --> DB
    NOTIF --> DB
    AUD --> DB
    TEN --> STORE[(Almacenamiento privado)]
    JOBS[Procesos programados] --> RENT
    JOBS --> NOTIF
    NOTIF --> ADAPTER[Adaptador WhatsApp]
    ADAPTER --> WA[Proveedor WhatsApp]
```

  -----------------------------------------------------------------------
  Bloque                              Responsabilidad y límites
  ----------------------------------- -----------------------------------
  Backend/API                         Valida solicitudes, autoriza
                                      operaciones y coordina casos de
                                      uso.

  Contratos                           Mantiene fechas, monto, día de
                                      vencimiento, moneda y condiciones
                                      efectivas.

  Obligaciones/prorrateo              Calcula importes por período,
                                      prorrateo y vencimientos; conserva
                                      el cálculo aplicado y recalcula
                                      obligaciones no pagadas afectadas
                                      por cambios efectivos.

Pagos/abonos de alquiler              Registra pagos completos y abonos
                                      manuales, mantiene el saldo pendiente
                                      y la fecha real junto con la marca
                                      temporal de registro.

  Depósitos/abonos                    Administra importe total, abonos,
                                      saldo y estado del depósito
                                      independientemente del alquiler.

  Persistencia                        Impone relaciones, unicidad y
                                      consistencia transaccional.

  Documentos                          Verifica autorización antes de
                                      entregar archivo y evita URL
                                      pública permanente.

  Notificaciones                      Programa avisos, registra intentos
                                      y resultados; no cambia estados
                                      financieros.

  Configuración regional              Proporciona valores predeterminados
                                      y configuraciones compatibles de
                                      moneda y zona horaria.

  Auditoría                           Registra actor, fecha, operación y
                                      cambios relevantes sin almacenar
                                      secretos ni imágenes completas.
  -----------------------------------------------------------------------

## 7. Reglas arquitectónicas de dominio

### 7.1 Prorrateo de períodos parciales

Para un período contractual que abarque solo una parte de un mes, el
cálculo propuesto es:

`importe proporcional = (alquiler mensual / días reales del mes) × días cobrables`

Los días cobrables se derivan de las fechas contractuales de inicio y
fin; se consideran inclusivos cuando correspondan a días de ocupación
pactados. El importe, moneda, período, cantidad de días, regla de
cálculo, redondeo al colón entero más cercano y resultado final deben
conservarse. La regla final y el
redondeo requieren validación de negocio y contractual antes de aprobar
el diseño.

### 7.2 Depósito de garantía y abonos

-   El depósito es una entidad financiera separada de las obligaciones
    mensuales de alquiler.
-   El contrato puede tener un depósito acordado con importe total y
    moneda.
-   Cada abono se registra como movimiento independiente con importe
    positivo, fecha real de recepción, fecha/hora de registro y observación
    opcional.
-   Se admite un máximo ordinario de tres abonos efectivamente recibidos;
    una excepción administrativa puede habilitar abonos adicionales. La
    justificación y los controles de la excepción siguen pendientes.
-   El saldo se calcula como importe total acordado menos la suma de
    abonos válidos.
-   El estado del depósito será pendiente, parcialmente pagado o
    completado.
-   Un abono al depósito no modifica el estado ni saldo de una
    obligación mensual de alquiler.
-   Se bloquean abonos que superen el saldo pendiente. El flujo ordinario
    admite hasta tres abonos efectivamente recibidos; una excepción
    administrativa puede permitir movimientos adicionales y debe quedar
    auditada. El motivo y los permisos concretos siguen pendientes.
-   Las devoluciones, deducciones, disputas y liquidación final del
    depósito quedan fuera del alcance actual.

### 7.3 Pagos y abonos de alquiler

- La obligación conserva el importe exigible y los abonos se modelan como
  movimientos separados; no se sobrescribirá un movimiento para representar
  un pago nuevo.
- El saldo pendiente se calcula como importe exigible menos la suma de
  abonos válidos. No se admite saldo negativo.
- Un abono parcial no cambia por sí solo la obligación a pagada. El estado
  pagado requiere saldo cero y confirmación manual conforme a la ERS.
- Cada movimiento conserva la fecha real de recepción y la fecha/hora en
  que fue registrado. Una fecha real retroactiva no requiere observación
  obligatoria solo por ser retroactiva.
- Las correcciones deben conservar auditoría con valores anteriores y
  nuevos. La política de corrección de fechas aún está pendiente.
- Existe una contradicción por resolver sobre si cada abono de alquiler
  genera una notificación al administrador: P2 mencionó notificación
  automática; P8/P14 indicaron mostrar saldo sin notificación individual.
  La arquitectura debe desacoplar la actualización del saldo de cualquier
  política de notificación hasta resolver DP-10.

### 7.4 Moneda y zona horaria

-   La moneda predeterminada es CRC.
-   La zona horaria predeterminada es `America/Costa_Rica` y se configura
    a nivel de organización.
-   La moneda se conserva por contrato y se muestra en sus obligaciones
    y depósito; no se mezclan importes de monedas diferentes en sumas.
-   La zona horaria operativa se configura para la región o ubicación
    pertinente y gobierna fechas límite y tareas programadas.
-   Cambiar valores predeterminados no debe alterar registros
    históricos.
-   La conversión de divisas, tipos de cambio y reportes consolidados en
    una moneda común no se incluyen en la primera versión.
-   El diseño debe decidir si la configuración regional se administra a
    nivel de organización, propiedad o contrato; la propuesta es usar
    configuración general por defecto y permitir definir la moneda del
    contrato y la zona horaria de la ubicación.

## 8. Modelo conceptual de datos

  -----------------------------------------------------------------------
  Entidad                             Datos principales
  ----------------------------------- -----------------------------------
  Inquilino                           Identificador, datos de contacto,
                                      estado y referencia privada al
                                      documento.

  Documento de identidad              Identificador interno, referencia
                                      al archivo, metadatos mínimos,
                                      fechas y auditoría de
                                      acceso/cambios.

  Propiedad                           Identificador, dirección, estado y
                                      zona horaria aplicable si
                                      corresponde.

  Contrato                            Inquilino, propiedad, vigencia,
                                      monto mensual, moneda, día de
                                      vencimiento, período de alquiler
                                      definido por administrador y
                                      condiciones efectivas.

  Obligación de alquiler              Contrato, período, vencimiento,
                                      moneda, importe exigible, saldo
                                      pendiente, estado y datos del prorrateo.

Abono de alquiler                    Obligación, importe, fecha real de
                                      recepción, fecha/hora de registro,
                                      observación y auditoría.

  Depósito de garantía                Contrato, importe acordado, moneda,
                                      condiciones/fecha acordadas y
                                      estado calculado.

  Abono de depósito                   Depósito asociado, importe, fecha
                                      real de recepción, observación y
                                      auditoría.

  Pago de alquiler                    Registro manual de pago completo de
                                      la obligación, fecha real y
                                      observación.

  Notificación                        Obligación, canal, tipo,
                                      destinatario, intentos y resultado.

  Auditoría                           Actor, entidad, acción, fecha y
                                      cambios relevantes.
  -----------------------------------------------------------------------

Invariantes propuestos: - Una obligación por contrato y período. - Un
abono pertenece a un único depósito y no se mezcla con pagos de
alquiler. - El saldo del depósito no se almacena como única fuente de
verdad: debe ser consistente con el total y sus abonos. - Los importes
históricos conservan su moneda y condiciones de cálculo. - No se permite
acceso a una fotografía sin autorización comprobada en el servidor.

## 9. Seguridad, privacidad y documentos

Controles mínimos: - HTTPS en todos los accesos autenticados. - Hash
resistente para contraseñas; nunca almacenar contraseñas en texto
plano. - Sesiones seguras, expiración y cierre de sesión efectivo;
evaluar MFA. - Archivos fuera de rutas públicas y sin enlaces públicos
permanentes. - Validar lista de formatos permitidos, tipo real del
archivo y tamaño; no confiar únicamente en el MIME del navegador. -
Generar nombres internos aleatorios y no usar número de cédula en rutas
o nombres. - Cifrado en tránsito y cifrado en reposo cuando lo permita
la infraestructura. - Auditoría proporcional al riesgo; evitar datos de
identidad completos, tokens o documentos en logs. - Definir finalidad,
retención, eliminación, respaldos y excepciones por obligaciones legales
antes de producción. - Probar la restauración de base de datos y
documentos desde respaldos protegidos.

## 10. Ejecución y escenarios críticos

### 10.1 Generación de obligaciones

1.  El proceso programado obtiene contratos y períodos aplicables.
2.  El servicio determina los días cobrables, importe prorrateado y
    vencimiento conforme a reglas aprobadas.
3.  Se verifica si ya existe una obligación para contrato/período.
4.  Se persiste de forma transaccional con clave de idempotencia o
    restricción única.
5.  Se registran resultados y errores para reprocesar sin duplicar
    obligaciones.

### 10.2 Registro de abono de alquiler

1. El administrador selecciona la obligación y registra un abono manual.
2. El backend valida que el importe sea positivo y que el saldo no resulte
   negativo.
3. El movimiento conserva la fecha real de recepción y la fecha/hora de
   registro; ambas pueden ser distintas.
4. El saldo se recalcula a partir del importe exigible y los abonos válidos.
5. Si el saldo sigue siendo positivo, la obligación no queda pagada. Si llega
   a cero, el administrador puede confirmar el pago completo.
6. La operación registra auditoría. La política de notificación individual
   por abono queda bloqueada hasta resolver DP-10.

### 10.3 Registro de abono al depósito

1.  El administrador selecciona el depósito.
2.  El backend valida importe positivo, moneda y saldo disponible según
    la política aprobada.
3.  Se registra el abono con fecha real de recepción y observación
    opcional.
4.  Se actualizan o calculan saldo y estado del depósito dentro de una
    operación consistente.
5.  Se registra auditoría y se muestra el historial.

### 10.4 Notificaciones

El proceso consulta obligaciones y configuración, registra la
notificación, genera la notificación web y solicita WhatsApp si está
configurado. Los fallos y reintentos no modifican estados financieros.
La ejecución diaria usa la zona horaria configurada.

## 11. Respaldo, recuperación y operación

La política de respaldo debe cubrir base de datos y archivos privados de
forma coordinada. Antes de producción se definirán frecuencia,
retención, cifrado, copia independiente, responsables, RPO y RTO. Se
probará restauración de contratos, obligaciones, pagos, depósitos,
abonos, relaciones y archivos. Una copia existente no se considerará
suficiente hasta verificar que puede restaurarse.

## 12. Riesgos y mitigaciones

  -----------------------------------------------------------------------
  Riesgo                              Mitigación propuesta
  ----------------------------------- -----------------------------------
  Prorrateo incorrecto                Regla explícita, cálculo trazable y
                                      casos de prueba de inicio/fin de
                                      mes.

  Abonos mezclados con alquiler       Entidades y servicios separados,
                                      validaciones y pruebas de
                                      invariantes.

  Abonos superiores al depósito       Política explícita, validación
                                      transaccional y auditoría.

  Exposición de cédulas               Repositorio privado, autorización
                                      en backend y pruebas de acceso
                                      denegado.

  Cambios regionales alteran historia Persistir moneda/condiciones
                                      aplicadas y evitar conversiones
                                      implícitas.

  Tarea programada omitida            Monitoreo, historial de ejecuciones
                                      y reproceso idempotente.

  Pérdida de información              Respaldos protegidos y restauración
                                      probada.
  -----------------------------------------------------------------------

## 13. Registros de decisiones de arquitectura (ADR)

### ADR-001 --- Estilo arquitectónico

-   **Estado:** Propuesto.
-   **Candidato:** Monolito modular.
-   **Justificación:** Proporcional al tamaño y al mantenimiento
    esperado.
-   **Pendiente:** Validar capacidades, despliegue y necesidades
    operativas.

### ADR-002 --- Persistencia relacional

-   **Estado:** Propuesto; motor pendiente.
-   **Justificación:** Relaciones, transacciones, unicidad
    contrato-período e integridad de abonos.
-   **Pendiente:** Seleccionar motor y estrategia de
    migraciones/respaldos.

### ADR-003 --- Documentos privados

-   **Estado:** Decisión de diseño adoptada como requisito; proveedor
    pendiente.
-   **Decisión:** Guardar archivos en almacenamiento privado separado de
    rutas públicas y guardar en base de datos referencias/metadatos
    mínimos.
-   **Pendiente:** Proveedor, cifrado, retención, tamaño/formato y
    proceso de descarga autorizada.

### ADR-004 --- Depósitos y abonos

-   **Estado:** Propuesto.
-   **Decisión:** Un depósito por contrato; modelar depósito y abonos
    separados de pagos de alquiler. El saldo deriva del importe acordado
    menos abonos válidos. Se admite un máximo ordinario de tres abonos y
    una excepción administrativa para abonos adicionales.
-   **Pendiente:** Justificación y permisos de la excepción, calendarios
    o acuerdos múltiples y reglas de modificación de acuerdos. Los abonos
    superiores al saldo se bloquean; las devoluciones/deducciones están
    fuera del alcance inicial.

### ADR-005 --- Configuración regional

-   **Estado:** Propuesto.
-   **Decisión:** CRC y `America/Costa_Rica` como valores
    predeterminados; conservar moneda del contrato y admitir
    configuración regional.
-   **Pendiente:** Definir niveles exactos de configuración y catálogo
    inicial de monedas/zonas admitidas.

### ADR-006 --- Abonos de alquiler y saldo

- **Estado:** Propuesto, derivado de respuestas de aclaración; requiere
  aprobación formal.
- **Decisión de dominio propuesta:** registrar los abonos como movimientos
  independientes, calcular el saldo y mantener la obligación impagada
  mientras exista saldo positivo. Conservar fecha real y marca temporal de
  registro.
- **Pendiente:** Resolver si cada abono genera una notificación individual
  al administrador (DP-10) y aprobar la política de correcciones.

### ADR-007 --- Cambios efectivos de condiciones contractuales

- **Estado:** Propuesto, derivado de respuestas de aclaración.
- **Decisión de dominio propuesta:** no modificar obligaciones pagadas;
  actualizar automáticamente las obligaciones no pagadas afectadas desde
  la fecha efectiva, incluidas las vencidas no pagadas. Registrar el antes
  y el después en auditoría.
- **Pendiente:** Definir semántica exacta del período de alquiler, cambios
  de calendario, y tratamiento de abonos ya registrados en obligaciones
  cuyo importe cambie.

### ADR-008 --- WhatsApp

-   **Estado:** Proveedor pendiente.
-   **Candidato:** Adaptador desacoplado de la lógica de negocio.
-   **Pendiente:** API, costos, plantillas, límites, webhooks y
    reintentos.

## 14. Decisiones pendientes

  -----------------------------------------------------------------------
  ID                      Decisión pendiente      Responsable sugerido
  ----------------------- ----------------------- -----------------------
  DP-01                   Validar regla de        Propietario del negocio
                          prorrateo, días         
                          cobrables y redondeo    
                          según contrato y        
                          normativa aplicable.    

  DP-02                   Política de retención y Propietario del negocio
                          eliminación de          
                          documentos de           
                          identidad.              

  DP-03                   Proveedor y presupuesto Propietario del negocio
                          de WhatsApp.            y responsable técnico

  DP-04                   RPO, RTO, frecuencia de Propietario del negocio
                          respaldos y retención.  y responsable técnico

  DP-05                   Volumen esperado y      Propietario del negocio
                          objetivos de            
                          rendimiento.            

  DP-06                   Exposición pública de   Propietario del negocio
                          la aplicación y         y responsable técnico
                          controles de operación. 

  DP-09                   Catálogo de monedas     Propietario del negocio
                          admitidas; la zona     y responsable técnico
                          horaria se configura
                          a nivel de organización.

DP-10                   Notificación por abono  Aclarar contradicción entre
                          de alquiler             notificación automática
                                                  mencionada en P2 y saldo
                                                  visible sin aviso
                                                  individual en P8/P14.

DP-11                   Configuración del        Definir campos, cambios
                          período de alquiler     de período y efecto sobre
                                                  obligaciones existentes.

DP-12                   Excepción a tres        Definir rol/permisos,
                          abonos de depósito      motivo, auditoría y límites.

DP-13                   Acuerdos/calendarios     Definir cómo se modifican
                          de abono del depósito   y cómo se vinculan abonos
                                                  a cada acuerdo.

DP-14                   Pregunta P11             Respuesta no registrada;
                                                  recuperar enunciado original.

DP-15                   Corrección de fechas     Definir si requiere motivo
                          retroactivas            y la auditoría aplicable.

DP-16                   Cambios de importe con   Definir tratamiento de
                          abonos ya registrados   abonos existentes cuando
                                                  cambia el importe exigible.
  -----------------------------------------------------------------------

## 15. Trazabilidad inicial

  ------------------------------------------------------------------------
  Requisito               Elemento arquitectónico  Evidencia futura
  ----------------------- ------------------------ -----------------------
  RF-07--RF-11,           Contratos y servicio de  Casos de prueba de
  RN-17--RN-18            obligaciones/prorrateo   vigencia, días y
                                                   cálculos.

  RF-29--RF-32,           Módulo de depósitos y    Pruebas de saldo,
  RN-19--RN-21            abonos                   abonos múltiples y
                                                   separación de alquiler.

  RF-33, RN-22, RNF-17    Configuración regional   Pruebas de valores por
                                                   defecto, configuración
                                                   y persistencia
                                                   histórica.

  RNF-13--RNF-16          Módulo de documentos,    Pruebas de
                          seguridad y operación    autorización, carga
                                                   segura, respaldo y
                                                   restauración.

  RF-21--RF-25            Orquestador de           Pruebas de
                          notificaciones y         idempotencia,
                          procesos programados     reintentos y
                                                   cancelación al pagar.
  ------------------------------------------------------------------------

## 16. Condiciones para aprobar la arquitectura

-   Validar el prorrateo y su relación con las condiciones
    contractuales.
-   Aprobar el alcance del depósito, los abonos y las reglas para
    excesos.
-   Aprobar almacenamiento privado, retención y recuperación de
    documentos.
-   Definir la configuración regional y moneda por contrato.
-   Seleccionar proveedor de WhatsApp y plataforma de despliegue.
-   Definir objetivos de respaldo y recuperación.
-   Completar trazabilidad entre la ERS aprobada, decisiones
    arquitectónicas y pruebas.

## 17. Referencias

1.  ISO --- ISO/IEC/IEEE 29148:2018:
    https://www.iso.org/standard/72089.html
2.  NASA --- Systems Engineering Handbook Appendix:
    https://www.nasa.gov/reference/system-engineering-handbook-appendix/
3.  SEI --- Documenting Software Architectures: Views and Beyond:
    https://www.sei.cmu.edu/library/documenting-software-architectures-views-and-beyond-second-edition/
4.  arc42 --- Architecture Documentation Template:
    https://arc42.org/overview/
5.  C4 Model --- Diagrams: https://c4model.com/diagrams
6.  OWASP --- File Upload Cheat Sheet:
    https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
7.  OWASP --- Authentication Cheat Sheet:
    https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
8.  OWASP --- Password Storage Cheat Sheet:
    https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

## Registro de aprobación

  Rol                       Nombre      Resultado   Fecha
  ------------------------- ----------- ----------- -----------
  Responsable del negocio   Pendiente   Pendiente   Pendiente
  Responsable técnico       Pendiente   Pendiente   Pendiente
  Responsable de pruebas    Pendiente   Pendiente   Pendiente

**Fin del documento --- DAS-SGA-001, versión 0.3 (borrador no aprobado).**


## Anexo A. Trazabilidad de las aclaraciones incorporadas

| Decisión / respuesta | Impacto arquitectónico | Estado |
|---|---|---|
| Abonos de alquiler con saldo pendiente | Entidad/movimiento Abono de alquiler; cálculo de saldo; transacción y auditoría | Incorporado como propuesta; pendiente aprobación |
| Un depósito por contrato; máximo ordinario de tres abonos | Restricción de dominio y validación; excepción administrativa auditada | Incorporado; controles de excepción pendientes |
| Período de alquiler definido por contrato | Atributos y servicio de contrato; generación de obligaciones por período | Incorporado; semántica de modificación pendiente |
| Cambios efectivos actualizan obligaciones no pagadas, incluso vencidas | Servicio de aplicación transaccional, auditoría de valores anteriores/nuevos y pruebas de regresión | Incorporado como propuesta; pendiente aprobación |
| Fecha real retroactiva y fecha/hora de registro separadas | Campos temporales separados y validación de fechas | Incorporado; política de corrección posterior pendiente |
| Cambio de inquilino mediante cierre y nuevo contrato | Flujo de cierre/alta, validación de solapamientos y conservación histórica | Incorporado |
| Prorrateo por días reales y redondeo al colón entero más cercano | Servicio de dominio de cálculo; pruebas de meses de distinta duración y límites contractuales | Incorporado; validación formal pendiente |
| Bloquear abonos al depósito superiores al saldo | Validación transaccional de saldo antes de persistir el movimiento | Incorporado |
| Zona horaria a nivel de organización | Configuración operativa centralizada; tareas programadas usan esa zona | Incorporado |
| Varios acuerdos/calendarios para un mismo depósito | Modelar acuerdos/calendarios vinculados al depósito sin crear varios depósitos por contrato | Concepto incorporado; reglas de edición y vínculo de movimientos pendientes |
| Devoluciones/deducciones del depósito fuera del alcance inicial | No diseñar flujo de devolución/liquidación en esta versión | Excluido |
| Notificación por abono | Adaptador de notificaciones desacoplado; no asumir evento hasta aclaración | Pendiente por contradicción P2 vs P8/P14 |
| P11 | No diseñar comportamiento hasta recuperar el enunciado y respuesta | Pendiente |

**Estado:** el DAS v0.3 es un borrador alineado con ERS-SGA-001 v1.4, también
no aprobada. La arquitectura sigue siendo una propuesta de monolito modular;
no se han seleccionado tecnologías ni autorizado implementación.
