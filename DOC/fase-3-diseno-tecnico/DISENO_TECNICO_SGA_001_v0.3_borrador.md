# Diseño técnico: interfaces, permisos y flujos

**Identificador:** DTE-SGA-001
**Versión:** 0.3 — reemplaza a la [v0.2](DISENO_TECNICO_SGA_001_v0.2_borrador.md), que se conserva sin cambios (la [v0.1](DISENO_TECNICO_SGA_001_v0.1_borrador.md) también)
**Estado:** Borrador para revisión; no aprobado
**Fecha:** 21 de octubre de 2026
**Base:** ERS-SGA-001 v1.8, DAS-SGA-001 v0.10 y MDD-SGA-001 v0.3 (todos borradores no aprobados)

Este documento cubre los tres productos de la fase 3 que faltaban además del modelo de datos: las interfaces (antes llamadas "contratos de API"), los permisos por operación y los flujos de negocio detallados. **No hay código ni se ha autorizado implementarlo.** Todo lo que no cita una fuente es **propuesta** del asistente y espera la decisión del solicitante (sección 7). La v0.2 incorporó las decisiones del solicitante sobre HT-05 (20-oct-2026); la v0.3 incorpora las de HT-08 (21-oct-2026). No es asesoría legal: las obligaciones de las leyes 7527 y 8968 siguen pendientes de abogado (DP-17).

## 1. ¿Está cubierta la API?

**No hay API pública en la versión 1** (ADR-022, decisión del solicitante del 20-oct-2026): la interfaz son páginas renderizadas por el servidor con Django. Por eso no se escribe una especificación de API tradicional. Lo que sí existe, o falta, son estas interfaces:

| Interfaz | Estado en la documentación | Qué hace este documento |
|---|---|---|
| Páginas web del administrador | Decidida (ADR-022); sin catálogo de pantallas | Sección 3.1 (reglas comunes) y sección 4 (operaciones) |
| Comando del proceso diario | Decidida (ADR-013, temporizador de systemd + comando de Django) | Sección 3.2 |
| Canal de salida de WhatsApp | Definida solo en concepto (ADR-008); proveedor diferido (DP-04) | Sección 3.3: contrato lógico propuesto |
| Recepción de estados de entrega del canal | **Pendiente** en ADR-008 ("punto de recepción de estados"); sería el único punto de entrada desde el exterior | Hallazgo HT-01 |
| Comprobante imprimible | Requisito RF-37; formato pendiente (DP-20) | Sección 3.4 y HT-02 |
| Exportación de datos del titular | Requisito RF-40 ("forma legible"); formato no definido | Sección 3.4 y HT-03 |
| Respaldos | Decididos (ADR-024) | Fuera de este documento |
| Avisos de seguridad de la cuenta por correo | Decididos el 20-oct-2026 (ADR-026) | Sección 3.5 |

La ERS (sección 15) todavía habla de una "especificación de API e interfaces" como artefacto futuro; ese texto es anterior al ADR-022 y se ajustará en la próxima versión de la ERS (HT-04).

## 2. Fuentes

| Fuente | Qué respalda | Cómo se validó | Limitaciones |
|---|---|---|---|
| ERS v1.8, secciones 5 y 8 | Requisitos de las operaciones y controles | Leída (secciones citadas) | RF-28 y otros se citan por el texto leído; no se revisó cada RF completo |
| DAS v0.9, sección 10 y ADR-004, 008, 012, 013, 017 y 020 | Flujos críticos y decisiones | Leída | Es borrador no aprobado |
| [Django, lista de despliegue](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) | Cookies de sesión y CSRF solo por HTTPS; HTTPS en todo el sitio con inicio de sesión | Leída por resumen | No cubre `SECURE_SSL_REDIRECT` ni HSTS |
| [OWASP, File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | Nombre aleatorio, comprobar la autorización en la descarga, no confiar en el Content-Type | Leída por resumen | Ver ADR-003 |
| [NIST SP 800-63B-4, sec. 4.6](https://pages.nist.gov/800-63-4/sp800-63b/events/); [OWASP, Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) y [Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html) | Avisos de recuperación y cambio de factores o contraseña, por canal fuera de la sesión y a más de una dirección | Leídas por resumen | NIST es una norma para sistemas federales de EE. UU. usada aquí como referencia; el cambio de contraseña no figura en su lista; ninguna fuente decide bloquear o dejar pasar la recuperación ante un fallo del envío |
| [OWASP, Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) (consultada el 21-oct-2026) | Cambio de contraseña: exigir la contraseña actual aunque la sesión esté activa. Cambio de factores (Multifactor Authentication Cheat Sheet, "Changing MFA Factors"): reautenticar con un factor ya registrado, no confiar solo en la sesión y avisar por otro canal | Leídas por resumen (WebFetch) | La Authentication Cheat Sheet no pide aviso tras cambiar la contraseña; ninguna cita fija la duración del enlace de restablecimiento: los 15 minutos son propuesta |
| [DigitalOcean, SMTP bloqueado](https://docs.digitalocean.com/support/why-is-smtp-blocked/); [Resend](https://resend.com/pricing); [django-anymail](https://anymail.dev/en/stable/) | Puertos 25, 465 y 587 bloqueados; Resend: plan gratis y dominio propio verificado; integración con Django | Leídas por resumen | Entregabilidad y términos de servicio sin verificar |

No hay estudios universitarios aquí: el contenido es derivación de requisitos ya definidos, no una afirmación técnica nueva.

## 3. Interfaces

### 3.1 Páginas web (reglas comunes, propuesta)
- Toda página, salvo el inicio de sesión, exige sesión autenticada con segundo factor (RF-26, RNF-01). Sin sesión, la respuesta es una redirección al inicio de sesión, nunca datos.
- Las cookies de sesión y de CSRF solo viajan por HTTPS (lista de despliegue de Django); el servidor redirige todo el tráfico HTTP a HTTPS (ADR-023).
- Cada formulario que crea un movimiento (abono de alquiler, abono de depósito) lleva una **clave de solicitud** generada por el formulario (UUID v4, ADR-020); un reenvío devuelve el movimiento ya registrado.
- Los errores de validación se muestran en el formulario con un mensaje comprensible y no guardan nada (RNF-07, CA-33).
- Los archivos privados no tienen URL pública: se entregan solo por una vista con comprobación de sesión y registro de acceso (ADR-003, RF-45).

### 3.2 Comando del proceso diario (propuesta)
| Aspecto | Propuesta |
|---|---|
| Invocación | Comando de gestión de Django, ejecutado por el temporizador de systemd (ADR-013) |
| Entrada | Ninguna obligatoria; opcional una fecha local para pruebas y reejecución |
| Efecto | Los seis pasos del DAS, sección 10.1; idempotente |
| Salida | Resumen de lo generado, omitido y fallido; registro de la ejecución con su resultado |
| Código de salida | 0 si terminó; distinto de 0 si algún paso falló, para que el temporizador o el monitoreo lo noten |
| Actor en auditoría | "sistema" (HT-06) |

### 3.3 Canal de salida de WhatsApp (contrato lógico, propuesta)
Basado en ADR-008, RF-23, RF-24 y RF-44. El proveedor es un proyecto aparte y sigue diferido (DP-04), por lo que este contrato no es definitivo.

| Elemento | Contenido |
|---|---|
| **Solicitud** | Destinatario (el teléfono del inquilino), plantilla aprobada, variables mínimas (por ejemplo, alias de la propiedad e importe) y clave de idempotencia. Nunca el número de documento ni imágenes (RF-44) |
| **Respuesta inmediata** | Estado *aceptado* o *fallido* e identificador del proveedor |
| **Estados posteriores** | *Entregado* o *fallido*, que pueden llegar con retraso (DAS 10.6). Cómo llegan está pendiente (HT-01) |
| **Reintentos** | Hasta cinco, con espera creciente y aleatoria; después *fallido* y la notificación web persiste (RF-24, RNF-05) |
| **Registro** | Obligación, canal, destinatario, fecha programada, fecha de intento, resultado, intentos, identificadores y estados del proveedor (RF-24) |

Mientras no exista el canal, solo opera la notificación web (RNF-05, ADR-008). Lo que el proveedor dice de sí mismo no cambia estados financieros (DAS 10.6).

### 3.4 Salidas de archivo
| Salida | Requisito | Estado |
|---|---|---|
| Comprobante de pago | RF-37: imprimible, reimprimible, con contrato, inquilino, período, importe, moneda, fecha real, medio de pago y saldo resultante; copia conservada; los anulados se marcan y no se renumeran | Formato (HTML imprimible o PDF) y contenido legal pendientes: DP-20 (HT-02) |
| Exportación de datos del titular | RF-40, CA-27: "forma legible" | Formato no definido (HT-03) |

### 3.5 Avisos de seguridad de la cuenta (HT-05, decidido el 20-oct-2026)
Detalle de la decisión y de sus fuentes en el ADR-026 del DAS v0.10.

| Aspecto | Contenido |
|---|---|
| Eventos | Uso de un código de recuperación; emisión de nuevos códigos (ambos exigidos por RF-27); registro o cambio del segundo factor; cambio o restablecimiento de la contraseña (los dos últimos amplían RF-27 y se incorporan en la próxima ERS) |
| Destinatarios | Dos direcciones de correo: la del administrador y la de una persona de confianza. WhatsApp se añadirá como segundo canal cuando exista (DP-04) |
| Contenido | Qué ocurrió, fecha y hora local (`America/Costa_Rica`) y qué hacer si no fue el administrador. **Sin códigos, contraseñas ni enlaces de acceso** |
| Envío | Servicio Resend por API HTTPS con django-anymail; requiere dominio propio verificado |
| Persistencia | El aviso se guarda en la misma transacción que el evento (propuesta del asistente, aceptada) |
| Reintentos | Inmediato y hasta cinco reintentos con espera creciente y aleatoria, mediante un temporizador de systemd de intervalo corto (propuesta, aceptada); el intervalo no está definido |
| Si falla | La recuperación **procede**. El aviso queda *fallido*, se muestra una alerta persistente en cada inicio de sesión y se registra en la auditoría |
| Datos | Solo las direcciones de correo y el texto del aviso; ningún dato de inquilinos. La dirección de la segunda persona es un dato personal de un tercero (DP-19, abogado) |

Cambios que esto exige en la ERS (próxima versión): una excepción en la sección 2.4, que excluye el correo como canal de notificación, solo para alertas de seguridad al administrador; ampliar RF-27; y el procedimiento de la sección 3.6.

### 3.6 Cambio y restablecimiento de contraseña y de segundo factor (HT-08, decidido el 21-oct-2026)
Decisiones del solicitante; los valores marcados "propuesta" son del asistente y fueron aceptados.

| Operación | Qué exige | Aviso (sección 3.5) | Fuente y estado |
|---|---|---|---|
| Cambiar la contraseña con sesión iniciada | Contraseña actual | Sí, a las dos direcciones | OWASP Authentication Cheat Sheet exige la contraseña actual; no pide aviso (el aviso lo añade el ADR-026) |
| Reemplazar el segundo factor (TOTP) con sesión iniciada | **Solo la contraseña actual** por ahora; exigir además un TOTP o un código de recuperación queda para una versión futura | Sí | **Decisión del solicitante contra la recomendación.** OWASP MFA Cheat Sheet pide reautenticar con un factor ya registrado y no confiar solo en la sesión |
| Restablecer la contraseña olvidada (sin sesión) | Enlace enviado por correo **solo a la dirección del administrador**, de un solo uso y válido 15 minutos (propuesta); el enlace solo permite fijar una contraseña nueva | Sí, a las dos direcciones, al completarse | **Decisión del solicitante contra la recomendación** (era: código de recuperación y TOTP en la web) |
| Iniciar sesión tras restablecer | Contraseña nueva y TOTP, como siempre (RF-26); el restablecimiento no inicia sesión por sí mismo | — | Propuesta |

Riesgos asumidos por el solicitante:
- Con una sesión secuestrada y la contraseña, se puede reemplazar el segundo factor; solo lo mitiga el aviso por correo, que llega después del hecho.
- El correo del administrador pasa a ser llave para restablecer la contraseña; si lo controlan terceros, solo falta superar el TOTP. El inicio de sesión depende de que funcionen Resend y el dominio (ADR-023, ADR-026).
- Un correo con enlace es de otro tipo que los avisos del ADR-026, que no llevan enlaces de acceso; el ADR-026 no cambia, pero el DAS debe describir este correo en una versión próxima.

Condiciones que se siguen recomendando: añadir el TOTP (o un código de recuperación) como requisito para el reemplazo del segundo factor; respuesta idéntica y sin revelar si la dirección existe; invalidar los enlaces anteriores y las sesiones abiertas al cambiar la contraseña; limitar la frecuencia de solicitudes. Estas tres últimas son propuestas del asistente aún no decididas ni verificadas contra la guía OWASP Forgot Password en esta sesión.

## 4. Permisos por operación

### 4.1 Modelo
- **Una sola cuenta y un solo rol** (RN-25, RE-07, RNF-02): no hay roles ni permisos distintos por usuario. La matriz no varía por persona; varía por **controles adicionales** de cada operación.
- **Toda** operación exige sesión autenticada con TOTP (RF-26, RNF-01), con cierre a las 24 horas y por inactividad de 1 hora (RF-27, CA-48).
- Las operaciones que ejecuta el proceso diario no son del administrador; se identifican como "sistema" (HT-06).

### 4.2 Catálogo de operaciones (propuesta de organización; los controles salen de los RF indicados)

| Operación | RF | Controles adicionales | Auditoría |
|---|---|---|---|
| Registrar inquilino | 01, 02, 39 | Consentimiento previo con texto informativo; formato JPEG o PNG, hasta 5 MB, tipo real del archivo; advertencia por documento duplicado (CA-25) | Sí |
| Consultar y actualizar ficha | 03, 05 | Cambios de identificación validados | Sí; sin valores de campos personales (ADR-017) |
| Desactivar o reactivar inquilino | 04 | Bloqueada con contrato vigente o saldos pendientes | Sí |
| Ver o descargar fotografía de cédula | 26, 45 | Solo por vista autorizada; no se guarda la imagen en el registro | **Cada acceso**: actor, fecha y hora, inquilino |
| Registrar propiedad | 06 | Estado derivado (disponible u ocupada); *inactiva* la marca el administrador | Sí (RF-28) |
| Crear contrato | 07, 08 | Rechazo por solapamiento con otro contrato de la propiedad; advertencia (sin bloqueo) si la vigencia pactada es menor de tres años | Sí |
| Finalizar contrato | 09 | Anula obligaciones futuras sin movimientos; prorratea el último período; ajuste manual con motivo; advertencia si faltan menos de tres meses | Sí |
| Sustituir inquilino | 36 | Cierra el contrato anterior y crea uno nuevo; el depósito no se traslada | Sí |
| Reajuste | 10 | Fecha efectiva normalizada al inicio del período siguiente; tope y fuente digitados; advierte si supera el tope; rechaza vivienda con precio en moneda extranjera; bloquea si deja el importe bajo lo abonado | Sí: valor anterior, nuevo, fecha efectiva y motivo |
| Corrección | 10 | **Motivo obligatorio**; retroactiva; no modifica obligaciones pagadas; bloquea si deja el importe bajo lo abonado | Sí |
| Registrar saldo de apertura | 43 | Solo para contratos con inicio anterior a la carga; incluye todos los períodos iniciados | Sí |
| Registrar pago o abono de alquiler | 13, 34, 37, 38 | Clave de solicitud; importe positivo; fecha real no futura; saldo no negativo; tipo de cambio manual si la moneda difiere | Sí |
| Anular movimiento | 16 | **Motivo obligatorio**; se conserva el original y se agrega una reversión | Sí |
| Anular obligación | (CA-35, RN-17) | Ver CA-35 y RN-17 para las condiciones | Sí |
| Reimprimir comprobante | 37 | Conserva el número original | Por definir (HT-02) |
| Configurar recordatorios | 21 | Hasta tres anticipaciones; reprograma sin duplicar | Sí (configuración de notificaciones) |
| Marcar notificación como leída o archivada | 23 | Nunca se borra | No exigida por la ERS |
| Definir o editar depósito | 29 | Editable solo sin abonos, o por corrección auditada nunca inferior a lo abonado; advierte si supera una mensualidad | Sí |
| Abono al depósito | 30 | Bloquea importes nulos, negativos o mayores al saldo; más de tres abonos solo con excepción de **motivo obligatorio** | Sí |
| Consultas: calendario, historial, depósito | 15, 17 a 20, 32 | Solo lectura | No exigida |
| Iniciar sesión, usar o regenerar códigos de recuperación | 26, 27 | Aviso por correo a las dos direcciones ante cada recuperación y cada emisión de códigos (sección 3.5) | Por definir |
| Registrar o cambiar el segundo factor | 27 | Aviso por correo (sección 3.5, evento ampliado respecto de RF-27); exige la contraseña actual (sección 3.6); el procedimiento aún no está en la ERS | Por definir |
| Cambiar o restablecer la contraseña | 27 | Aviso por correo (sección 3.5, evento ampliado); con sesión exige la contraseña actual, sin sesión un enlace por correo de 15 minutos (sección 3.6); aún no está en la ERS | Por definir |
| Registrar y resolver solicitud del titular; exportar datos | 40 | Fecha límite de cinco días hábiles; la supresión se atiende salvo obligación legal (DP-18) | Sí |
| Retención: avisar y eliminar o desasociar datos | 41 | Aviso al administrador antes de ejecutar; conserva movimientos financieros sin datos de identificación | Sí; la ejecuta el proceso diario |
| Registrar incidente de seguridad y avisos | 46 | Calcula el plazo de cinco días hábiles; deja constancia de cada aviso y de la revisión | Sí |
| Configurar moneda y zona horaria | 33 | La zona se configura solo a nivel de organización | Sí (RF-28) |

No todos los RF aparecen en la tabla: los que no se listan son reglas internas o cálculos derivados que ejecuta el proceso diario o el sistema (por ejemplo, RF-11, 12, 14, 22, 25, 35, 42 y 44). No se revisó cada RF restante uno por uno.

## 5. Flujos de negocio no cubiertos en el DAS, sección 10

Los flujos 10.1 (proceso diario), 10.2 (abono), 10.3 (anulación), 10.4 (reajuste), 10.5 (abono al depósito) y 10.6 (notificaciones) ya están en el DAS v0.9. Estos son los que faltaban (propuesta de detalle):

**F-01 Registrar inquilino**
1. Se muestra el texto informativo de la Ley 8968 y se registra el consentimiento (fecha, versión del texto, medio) antes de guardar datos (RF-39).
2. Se validan campos obligatorios, contacto y archivo; el tipo real del archivo se verifica y se rechazan formatos distintos de JPEG y PNG o más de 5 MB (RF-02).
3. Si existe otro inquilino activo con el mismo documento, se advierte y el administrador decide (CA-25).
4. En una transacción: se guarda el inquilino, se guarda el archivo con nombre aleatorio fuera de la raíz web (ADR-003) y se registra la auditoría.
5. Un error en cualquier paso no deja un inquilino a medias ni un archivo huérfano.

**F-02 Crear contrato**
1. Se elige inquilino y propiedad y se ingresan fechas, monto, moneda, vencimiento y gracia; si hay depósito, se define.
2. Se rechaza el contrato si comparte un día con otro de la misma propiedad; la base lo garantiza con la restricción de exclusión (RF-08, ADR-002).
3. Se advierte, sin bloquear, si la vigencia pactada es menor de tres años.
4. En una transacción: se crea el contrato, la condición inicial y la auditoría. Las obligaciones las genera el proceso diario, 30 días antes de cada período (RF-11).
5. Si el inicio es anterior a la carga en el sistema, se ofrece registrar el saldo de apertura (F-04).

**F-03 Finalizar contrato**
1. Se registra la fecha de fin (inclusive) y se advierte si faltan menos de tres meses.
2. En una transacción: se anulan las obligaciones futuras sin movimientos válidos, se prorratea el último período (RN-12) y se permite un ajuste manual con motivo, y se registra la auditoría.
3. Se conservan las obligaciones y movimientos existentes. Un depósito pendiente queda como "contrato cerrado, liquidación manual" (RF-32).

**F-04 Registrar saldo de apertura**
1. Solo para contratos con inicio anterior a la fecha de carga.
2. El administrador indica la fecha de apertura y el monto adeudado, que debe incluir todos los períodos iniciados hasta esa fecha (RF-43).
3. Se crea una obligación de tipo apertura (ADR-015) y se audita. Las obligaciones regulares comienzan en el primer período posterior; las alertas de atraso comienzan en la fecha de carga, no retroactivamente (DP-25).

**F-05 Autenticación y recuperación de acceso**
1. Contraseña de al menos 15 caracteres y TOTP (RF-27); el almacenamiento usa Argon2id (ADR-019).
2. Sesión con cierre a las 24 horas y a la hora de inactividad (CA-48).
3. Sin segundo factor, un código de recuperación válido da acceso una sola vez (CA-47) y el sistema envía el aviso por correo a las dos direcciones (sección 3.5). Si el envío falla, el acceso procede y el aviso queda pendiente con reintentos y una alerta en la web.

**F-06 Consultar o descargar la cédula**
1. Exige sesión vigente. 2. Se registra el acceso (actor, fecha y hora, inquilino) antes de entregar el archivo (RF-45). 3. El archivo se entrega por la aplicación, sin URL pública y con el nombre interno aleatorio oculto (ADR-003).

**F-07 Atender una solicitud del titular**
1. Se registra tipo (acceso, rectificación, actualización o supresión) y fecha de recepción; el sistema fija la fecha límite a cinco días hábiles (CA-27).
2. Acceso: se exporta la información del titular en forma legible (formato pendiente, HT-03). Rectificación o actualización: se aplica por el flujo de actualizar ficha, con su auditoría.
3. Supresión: se atiende salvo obligación legal de conservar el dato (DP-18); la desasociación conserva los movimientos financieros sin datos de identificación.
4. Se marca la resolución con fecha. El tratamiento de feriados en el plazo lo valida el abogado.

**F-08 Registrar un incidente de seguridad**
1. El administrador registra fecha y hora de ocurrencia y de conocimiento, naturaleza, datos comprometidos, acciones inmediatas y titulares afectados. El sistema no detecta incidentes.
2. El sistema calcula la fecha límite de cinco días hábiles (CA-56).
3. Se registra cada aviso a titulares y a la Agencia y la revisión posterior (CA-57). Desde cuándo corre el plazo y el aviso a la Agencia están pendientes de abogado (DP-17).

**F-09 Desactivar un inquilino**
1. Se rechaza si tiene un contrato vigente o saldos pendientes (CA-29).
2. Si no, se desactiva sin eliminar contratos ni historial (CA-10) y se audita. Se puede reactivar.

## 6. Hallazgos

| ID | Hallazgo | Propuesta |
|---|---|---|
| HT-01 | El único punto de entrada desde el exterior sería la recepción de estados de entrega del canal de WhatsApp (ADR-008 lo deja pendiente). Hoy el sistema solo atiende al administrador autenticado | No definir el punto de entrada hasta que exista el proveedor (DP-04). Si se hace, exigir autenticación del remitente y registrar cada recepción. Alternativa sin punto de entrada: consultar el estado al proveedor |
| HT-02 | El formato del comprobante, qué datos debe llevar y si los procedimientos pactados lo sustituyen siguen pendientes (DP-20); no está definido si la reimpresión se audita | Resolver con el abogado; mientras tanto, HTML imprimible como propuesta |
| HT-03 | RF-40 pide exportar los datos del titular "en forma legible" sin definir formato ni alcance (¿incluye la fotografía? ¿los movimientos?) | Proponer un formato al abogado (DP-21 cubre el consentimiento, no esto) |
| HT-04 | La ERS (sección 15) menciona una "especificación de API", anterior al ADR-022 | Ajustar el texto en la próxima versión de la ERS |
| HT-05 | **Resuelto el 20-oct-2026** (ver sección 3.5 y ADR-026): aviso por correo a dos direcciones, cuatro eventos, recuperación que procede ante fallo del envío. Quedan pendientes el dominio, las dos direcciones y los cambios de la ERS | Incorporado |
| HT-06 | La auditoría exige "actor" (RF-28) y no dice quién es el actor del proceso diario | Registrar "sistema" y la ejecución que lo originó |
| HT-07 | DAS 10.2 dice que se "bloquea la obligación" dentro de una transacción; la técnica exacta (bloqueo de fila de la base de datos) no se verificó en la documentación de Django | Verificar al escribir el código, junto con la prueba de concurrencia de la estrategia de pruebas |
| HT-08 | **Resuelto a nivel de diseño el 21-oct-2026** (sección 3.6): contraseña actual para cambiar la contraseña y reemplazar el TOTP; enlace por correo de 15 minutos para restablecer. La ERS sigue sin describirlo y las dos primeras decisiones van contra la recomendación | Incorporar el procedimiento en la próxima ERS; el DAS debe describir el correo con enlace |
| HT-09 | La ERS 2.4 excluye el correo como canal de notificación; el ADR-026 lo usa solo para alertas de seguridad | Registrar la excepción en la próxima ERS |

HT-nn es un identificador local de este documento, no de la lista compartida del proyecto.

## 7. Decisiones y pendientes

**Decidido el 20-oct-2026 (HT-05):** canal de correo con dos direcciones y WhatsApp después; Resend por API; cuatro eventos; la recuperación procede ante un fallo del envío. Detalle y fuentes en la [actualización 2026-10-20 (h)](../actualizaciones/2026-10-20h_ht-05-recuperacion-acceso/CAMBIOS.md).

**Decidido el 21-oct-2026 (HT-08):** contraseña actual para cambiar la contraseña y para reemplazar el segundo factor (TOTP en el futuro); restablecimiento sin sesión con enlace por correo de un solo uso y 15 minutos. Detalle en la [actualización 2026-10-21](../actualizaciones/2026-10-21_ht-08-contrasena-segundo-factor/CAMBIOS.md).

**Pendientes del solicitante:**
1. HT-01: ¿se define ahora el punto de recepción de estados de WhatsApp o se espera al proveedor?
2. HT-03: formato y alcance de la exportación del titular (con el abogado).
3. HT-02: formato del comprobante (DP-20).
4. Si la reimpresión del comprobante y las consultas de lectura deben auditarse.
5. HT-08: resuelto en la sección 3.6; queda decidir si se añade el TOTP al reemplazo del segundo factor (fecha o versión) y las tres propuestas de endurecimiento sin decidir.
6. Nombre de dominio, cuáles son las dos direcciones de correo y el intervalo del temporizador de reintentos.
## 8. Condiciones para aprobar este documento

- Aprobar la ERS v1.8, el DAS v0.10 y el modelo de datos.
- Resolver los pendientes de la sección 7.
- Revisión por otra persona distinta del autor (hoy el solicitante ocupa los tres roles, DP-23).

## Registro de aprobación

| Rol | Nombre | Resultado | Fecha |
|---|---|---|---|
| Responsable del negocio | Pendiente | Pendiente | Pendiente |
| Responsable técnico | Pendiente | Pendiente | Pendiente |
| Responsable de pruebas | Pendiente | Pendiente | Pendiente |

**Fin del documento — DTE-SGA-001, versión 0.3 (borrador no aprobado).**
