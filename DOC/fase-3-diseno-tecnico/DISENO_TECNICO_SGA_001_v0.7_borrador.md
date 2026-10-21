# Diseño técnico: interfaces, permisos y flujos

**Identificador:** DTE-SGA-001
**Versión:** 0.7 — reemplaza a la [v0.6](DISENO_TECNICO_SGA_001_v0.6_borrador.md), que se conserva sin cambios (las [v0.5](DISENO_TECNICO_SGA_001_v0.5_borrador.md), [v0.4](DISENO_TECNICO_SGA_001_v0.4_borrador.md), [v0.3](DISENO_TECNICO_SGA_001_v0.3_borrador.md), [v0.2](DISENO_TECNICO_SGA_001_v0.2_borrador.md) y [v0.1](DISENO_TECNICO_SGA_001_v0.1_borrador.md) también)
**Estado:** Borrador para revisión; no aprobado
**Fecha:** 21 de octubre de 2026
**Base:** ERS-SGA-001 v1.9, DAS-SGA-001 v0.11 y MDD-SGA-001 v0.4 (todos borradores no aprobados)

Este documento cubre los tres productos de la fase 3 que faltaban además del modelo de datos: las interfaces (antes llamadas "contratos de API"), los permisos por operación y los flujos de negocio detallados. **No hay código ni se ha autorizado implementarlo.** Todo lo que no cita una fuente es **propuesta** del asistente y espera la decisión del solicitante (sección 7). La v0.2 incorporó las decisiones del solicitante sobre HT-05 (20-oct-2026); la v0.3 incorporó las de HT-08 (21-oct-2026); la v0.7 alinea el documento con la ERS v1.9, el DAS v0.11 y el modelo de datos v0.4, que ya recogen las decisiones de HT-01, HT-02, HT-03, HT-05 y HT-08 (sin decisiones nuevas); la v0.6 incorporó las de HT-02 (21-oct-2026: comprobantes físicos fuera del sistema por ahora); la v0.5 incorporó las de HT-03 (21-oct-2026: alcance y formato de la exportación del titular); la v0.4 incorporó las de HT-01 (21-oct-2026), que cambian el alcance de las notificaciones (sección 3.7), y corrige un error de la sección 3.3 (el destinatario de WhatsApp es el administrador, RF-44, no el inquilino). No es asesoría legal: las obligaciones de las leyes 7527 y 8968 siguen pendientes de abogado (DP-17).

## 1. ¿Está cubierta la API?

**No hay API pública en la versión 1** (ADR-022, decisión del solicitante del 20-oct-2026): la interfaz son páginas renderizadas por el servidor con Django. Por eso no se escribe una especificación de API tradicional. Lo que sí existe, o falta, son estas interfaces:

| Interfaz | Estado en la documentación | Qué hace este documento |
|---|---|---|
| Páginas web del administrador | Decidida (ADR-022); sin catálogo de pantallas | Sección 3.1 (reglas comunes) y sección 4 (operaciones) |
| Comando del proceso diario | Decidida (ADR-013, temporizador de systemd + comando de Django) | Sección 3.2 |
| Notificaciones al administrador por correo | **Decididas el 21-oct-2026** para la v1 (cambio de alcance ya recogido en la ERS v1.9) | Sección 3.7 |
| Canal de salida de WhatsApp | Futuro: queda fuera de la v1 por decisión del solicitante; proveedor diferido (DP-04) | Sección 3.3: contrato lógico conservado para cuando exista |
| Recepción de estados de entrega del canal | **Fuera de la v1**: no hay punto de entrada desde el exterior (HT-01 resuelto el 21-oct-2026) | Hallazgo HT-01 |
| Comprobante de pago | Requisito RF-37; el solicitante lo divide el 21-oct-2026: ahora recibo de papel fuera del sistema y el SGA anota su número; el comprobante generado por el sistema, después | Sección 3.4.2 y HT-02 |
| Exportación de datos del titular | Requisito RF-40 ("forma legible"); alcance y formato decididos el 21-oct-2026 (informe web imprimible) | Sección 3.4 y HT-03 |
| Respaldos | Decididos (ADR-024) | Fuera de este documento |
| Avisos de seguridad de la cuenta por correo | Decididos el 20-oct-2026 (ADR-026) | Sección 3.5 |

La ERS (sección 15) todavía habla de una "especificación de API e interfaces" como artefacto futuro; ese texto era anterior al ADR-022 y la ERS v1.9 ya lo ajustó (HT-04, resuelto).

## 2. Fuentes

| Fuente | Qué respalda | Cómo se validó | Limitaciones |
|---|---|---|---|
| ERS v1.9 (v1.8 en las versiones anteriores de este documento), secciones 5 y 8 | Requisitos de las operaciones y controles | Leída (secciones citadas) | RF-28 y otros se citan por el texto leído; no se revisó cada RF completo |
| DAS v0.11 (v0.9 en las versiones anteriores), sección 10 y ADR-004, 008, 012, 013, 017 y 020 | Flujos críticos y decisiones | Leída | Es borrador no aprobado |
| [Django, lista de despliegue](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) | Cookies de sesión y CSRF solo por HTTPS; HTTPS en todo el sitio con inicio de sesión | Leída por resumen | No cubre `SECURE_SSL_REDIRECT` ni HSTS |
| [OWASP, File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | Nombre aleatorio, comprobar la autorización en la descarga, no confiar en el Content-Type | Leída por resumen | Ver ADR-003 |
| [NIST SP 800-63B-4, sec. 4.6](https://pages.nist.gov/800-63-4/sp800-63b/events/); [OWASP, Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) y [Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html) | Avisos de recuperación y cambio de factores o contraseña, por canal fuera de la sesión y a más de una dirección | Leídas por resumen | NIST es una norma para sistemas federales de EE. UU. usada aquí como referencia; el cambio de contraseña no figura en su lista; ninguna fuente decide bloquear o dejar pasar la recuperación ante un fallo del envío |
| [OWASP, Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) (consultada el 21-oct-2026) | Cambio de contraseña: exigir la contraseña actual aunque la sesión esté activa. Cambio de factores (Multifactor Authentication Cheat Sheet, "Changing MFA Factors"): reautenticar con un factor ya registrado, no confiar solo en la sesión y avisar por otro canal | Leídas por resumen (WebFetch) | La Authentication Cheat Sheet no pide aviso tras cambiar la contraseña; ninguna cita fija la duración del enlace de restablecimiento: los 15 minutos son propuesta |
| [Ley 8968, art. 7](https://www.archivonacional.go.cr/web/normativa/ley8968.docx) y [Reglamento 37554-JP, arts. 21 y 22](https://www.archivonacional.go.cr/web/normativa/reglamento37554.docx) (consultados el 21-oct-2026) | Contenido, forma y plazo de la respuesta al derecho de acceso | Leídos completos en los artículos citados, extrayendo el texto de las copias .docx del Archivo Nacional | Copias no oficiales, no comparadas con la Gaceta; no incluyen reformas posteriores; interpretación del asistente, no asesoría legal |
| Notas de prensa: [El Financiero](https://www.elfinancierocr.com/tecnologia/arrendadores-de-casas-apartamentos-o-locales/QW73VHVGG5BETDEK2FT34HFH4E/story/) y [La Nación](https://www.nacion.com/economia/finanzas/arrendatarios-deberan-dar-factura-electronica-a/234EFYUVABDKPPDCKA5YQPLFBQ/story/) (consultadas el 21-oct-2026) | Solo señalan que se cita la obligación de factura electrónica para arrendadores (resolución DGT-R-012-2018); no se citan como respaldo | Solo resultados de búsqueda; las páginas no se abrieron | Prensa de 2018 a 2024, tercero no oficial; puede estar desactualizado; no es asesoría legal |
| [Meta, webhooks de WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks) (consultada el 21-oct-2026) | Los estados de los mensajes enviados llegan por webhook a un endpoint propio; reintentos hasta 7 días con posibles duplicados | Leída por resumen (WebFetch) | No dice cómo se verifica el remitente ni si el estado puede consultarse sin webhook; solo aplica si WhatsApp vuelve |
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

### 3.3 Canal de salida de WhatsApp (contrato lógico, propuesta; futuro, fuera de la v1)
Basado en ADR-008, RF-23, RF-24 y RF-44. El proveedor es un proyecto aparte y sigue diferido (DP-04), por lo que este contrato no es definitivo. Por decisión del solicitante del 21-oct-2026, WhatsApp no forma parte de la v1 (sección 3.7); este contrato se conserva para cuando exista.

| Elemento | Contenido |
|---|---|
| **Solicitud** | Destinatario (el teléfono del administrador, RF-44), plantilla aprobada, variables mínimas (por ejemplo, alias de la propiedad e importe) y clave de idempotencia. Nunca el número de documento ni imágenes (RF-44) |
| **Respuesta inmediata** | Estado *aceptado* o *fallido* e identificador del proveedor |
| **Estados posteriores** | *Entregado* o *fallido*, que pueden llegar con retraso (DAS 10.6). Cómo llegan está pendiente (HT-01) |
| **Reintentos** | Hasta cinco, con espera creciente y aleatoria; después *fallido* y la notificación web persiste (RF-24, RNF-05) |
| **Registro** | Obligación, canal, destinatario, fecha programada, fecha de intento, resultado, intentos, identificadores y estados del proveedor (RF-24) |

Mientras no exista el canal, solo opera la notificación web (RNF-05, ADR-008). Lo que el proveedor dice de sí mismo no cambia estados financieros (DAS 10.6).

### 3.4 Salidas de archivo
| Salida | Requisito | Estado |
|---|---|---|
| Comprobante de pago | RF-37: imprimible, reimprimible, con contrato, inquilino, período, importe, moneda, fecha real, medio de pago y saldo resultante; copia conservada; los anulados se marcan y no se renumeran | **Dividido el 21-oct-2026:** ahora, recibo de papel fuera del sistema; luego, comprobante generado por el sistema. Contenido legal y formato pendientes: DP-20 (ver 3.4.2) |
| Exportación de datos del titular | RF-40, CA-27: "forma legible" | **Informe web imprimible** con todo el registro del titular (decisión del solicitante, 21-oct-2026; ver 3.4.1) |

#### 3.4.2 Comprobante de pago: recibos físicos primero (HT-02, decidido el 21-oct-2026)
Decisión del solicitante: primero se trabaja con **recibos de papel hechos fuera del sistema** (opción B) y poco a poco se integra el comprobante generado por el sistema (opción A). Es un cambio de alcance respecto de RF-37, que la ERS v1.8 exigía completo; la ERS v1.9 lo marca como fase posterior y añade RF-47.

| Aspecto | Contenido | Origen |
|---|---|---|
| Fase actual (B) | Cada movimiento puede llevar el campo opcional **número de recibo físico** (texto, único si se llena). El administrador conserva la copia en papel | Decisión del solicitante; el campo es propuesta mía, aceptada |
| Fase posterior (A) | El sistema genera, numera (consecutivo y sin huecos), imprime y reimprime el comprobante, como pide RF-37; los anulados se marcan | RF-37 conservado para esa fase |
| Qué sale de la v1 | RF-37 (generación y numeración por el sistema), CA-37, la parte de comprobante de CA-04 y CA-34, y la numeración consecutiva de la sección 6 de la ERS, hasta la fase A | Propuesta; la ERS v1.9 debe reescribirlo |
| Regla de prioridad | La estrategia de pruebas dice que nada de prioridad Alta se difiere sin aceptación escrita, y CA-37 es Alta. Esta decisión difiere un requisito Alta; la aceptación del solicitante consta en la actualización 2026-10-21d, pero no es aprobación del negocio | Estrategia de pruebas v0.2, sección 11 |
| Riesgos asumidos | Numeración a mano y posibles errores; el papel no se marca como anulado cuando se anula el movimiento; sin copia electrónica del recibo; el art. 56 exige que el arrendador conserve copia, y aquí es física | Propuesta |
| Pendiente tributario | Si Hacienda exige factura electrónica por el alquiler (la ERS la excluye) no se investigó en fuente oficial; solo notas de prensa citan la resolución DGT-R-012-2018. Es pregunta para el contador o abogado, sumada a DP-20 | Solo resultados de búsqueda, 21-oct-2026 |
| Reimpresión | No aplica en la fase B; su auditoría se decide en la fase A | — |

#### 3.4.1 Exportación de los datos del titular (HT-03, decidido el 21-oct-2026)
Fundamento: Ley 8968, art. 7.1 y Reglamento 37554-JP, arts. 21 y 22, leídos por extracción de las copias .docx del Archivo Nacional (no se comparó con la Gaceta). Lo que sigue es interpretación del asistente, no asesoría legal; la valida el abogado (DP-17).

| Aspecto | Contenido | Origen |
|---|---|---|
| Alcance | Todo el registro del titular, **incluida la fotografía de la cédula**: identificación, contratos, obligaciones y movimientos, comprobantes, notificaciones que lo mencionan, consentimiento, finalidad y uso | Decisión del solicitante, a favor de la recomendación |
| Exclusiones | Datos de terceros (art. 7.1.c) y secretos del sistema (contraseñas, códigos). Qué cuenta como dato de tercero con codeudores o fiadores queda pendiente del abogado | Texto de la ley; el resto, propuesta |
| Contenido | Informe "completo, claro y exento de codificaciones", con explicación de los términos técnicos y de la finalidad y el uso (art. 7.1.b); estados con su nombre y no con códigos internos | Texto de la ley |
| Formato | **Informe web imprimible**, con la foto de la cédula incrustada; el administrador lo imprime o lo guarda como PDF desde el navegador | Decisión del solicitante, a favor de la recomendación (rectificó su primera elección, PDF generado por el sistema, el 21-oct-2026) |
| Consecuencias | Sin dependencias nuevas ni paquetes del servidor. El PDF depende del navegador del administrador y su aspecto no se controla desde el sistema. Si luego se quiere un PDF generado por el sistema, requiere un ADR con biblioteca y prueba. El comprobante (HT-02) podría usar el mismo mecanismo; no está decidido | Propuesta |
| Entrega | El archivo contiene datos sensibles: no se envía por correo ni por WhatsApp; entrega en mano o por un medio seguro (propuesta). Cada exportación se audita (RF-45): decisión del solicitante del 21-oct-2026, siguiendo la recomendación | Entrega: propuesta; auditoría: decidido |
| Plazo y costo | Gratuita, cinco días hábiles desde la recepción (art. 7; RF-40) | Texto de la ley |
| Frecuencia | El Reglamento fija un intervalo mínimo de seis meses entre consultas, salvo motivo fundamentado; el sistema no lo hace cumplir hoy (propuesta: solo informar al administrador de la consulta anterior) | Texto del art. 21; la solución, propuesta |

### 3.5 Avisos de seguridad de la cuenta (HT-05, decidido el 20-oct-2026)
Detalle de la decisión y de sus fuentes en el ADR-026 del DAS v0.11.

| Aspecto | Contenido |
|---|---|
| Eventos | Uso de un código de recuperación; emisión de nuevos códigos (ambos exigidos por RF-27); registro o cambio del segundo factor; cambio o restablecimiento de la contraseña (los dos últimos ampliaron RF-27; incorporados en la ERS v1.9) |
| Destinatarios | Dos direcciones de correo del propio solicitante, en proveedores distintos (decisión del 21-oct-2026); no constan en los documentos, solo en la configuración. WhatsApp se añadirá como segundo canal cuando exista (DP-04) |
| Contenido | Qué ocurrió, fecha y hora local (`America/Costa_Rica`) y qué hacer si no fue el administrador. **Sin códigos, contraseñas ni enlaces de acceso** |
| Envío | Servicio Resend por API HTTPS con django-anymail; requiere dominio propio verificado |
| Persistencia | El aviso se guarda en la misma transacción que el evento (propuesta del asistente, aceptada) |
| Reintentos | Inmediato y hasta cinco reintentos con espera creciente y aleatoria, mediante un temporizador de systemd que corre cada 1 minuto (decisión del solicitante del 21-oct-2026; la espera entre intentos la fija cada envío) |
| Si falla | La recuperación **procede**. El aviso queda *fallido*, se muestra una alerta persistente en cada inicio de sesión y se registra en la auditoría |
| Datos | Solo las direcciones de correo y el texto del aviso; ningún dato de inquilinos. Las dos direcciones son del solicitante: no hay dato de un tercero |

Cambios que esto exigía en la ERS: hechos en la ERS v1.9 (sección 2.4, RF-27, CA-47, CA-59 y CA-60).

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

Condición que se sigue recomendando: añadir el TOTP (o un código de recuperación) como requisito para el reemplazo del segundo factor (futuro).

Protecciones del enlace adoptadas por el solicitante el 21-oct-2026, siguiendo la recomendación (OWASP, Forgot Password Cheat Sheet, leída por resumen ese día): respuesta y tiempo idénticos exista o no la cuenta; al fijar la contraseña nueva se invalidan los demás enlaces y se cierran las sesiones abiertas (cierre automático: propuesta del asistente); y un máximo de 3 solicitudes por hora para la cuenta (número propuesto por el asistente; la fuente no lo fija).

### 3.7 Notificaciones al administrador por correo en la v1 (HT-01, decidido el 21-oct-2026)
Decisión del solicitante (cambio de alcance): en la v1, los recordatorios y alertas de las obligaciones (RF-21, RF-22) se entregan al administrador por **notificación web persistente y correo**. WhatsApp queda para una versión futura.

| Aspecto | Contenido |
|---|---|
| Destinatario | La dirección de correo del administrador (propuesta: la misma de los avisos de seguridad; no la segunda dirección) |
| Envío | El mismo servicio que los avisos de seguridad: Resend por API HTTPS con django-anymail y dominio propio verificado (ADR-026). No hay proveedor nuevo |
| Contenido | Propuesta: aplicar a los correos los mismos límites de RF-44: sin número de documento ni imágenes, solo alias de la propiedad e importe |
| Reintentos y registro | Propuesta: los de RF-24 (hasta cinco intentos con espera creciente y aleatoria; después *fallido* y la notificación web persiste) |
| Estados de entrega | La API de envío solo informa de aceptación. No se recibe ningún estado posterior: **no hay punto de entrada desde el exterior** y HT-01 desaparece de la v1. El sistema no declarará entregado un correo solo aceptado (RF-23) |
| Capacidad | El plan gratuito de Resend declara 100 correos al día y 3.000 al mes (consultado el 20-oct-2026, por resumen); suficiente para un resumen diario más recordatorios, sin cálculo hecho para el volumen real |

Cambios que esto exigía en la ERS y el DAS (hechos en la ERS v1.9 y el DAS v0.11): ERS, sección 2.4 (retirar la exclusión del correo para estas notificaciones), RF-23, RF-24, RF-44, CA-09 y la matriz; DAS, ADR-008 (canal) y ADR-026 y ADR-013 (el temporizador de reintentos también cubriría estas notificaciones). La excepción limitada a alertas de seguridad (HT-09) pasa a ser más amplia. Los límites legales de RF-44 (OL-17) se redactaron para WhatsApp; su aplicación al correo es una propuesta que debe validar el abogado (DP-17).

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
| Reimprimir comprobante | 37 | Solo en la fase A (3.4.2); conserva el número original | Por definir en la fase A |
| Configurar recordatorios | 21 | Hasta tres anticipaciones; reprograma sin duplicar | Sí (configuración de notificaciones) |
| Marcar notificación como leída o archivada | 23 | Nunca se borra | No exigida por la ERS |
| Definir o editar depósito | 29 | Editable solo sin abonos, o por corrección auditada nunca inferior a lo abonado; advierte si supera una mensualidad | Sí |
| Abono al depósito | 30 | Bloquea importes nulos, negativos o mayores al saldo; más de tres abonos solo con excepción de **motivo obligatorio** | Sí |
| Consultas: calendario, historial, depósito | 15, 17 a 20, 32 | Solo lectura | No exigida |
| Iniciar sesión, usar o regenerar códigos de recuperación | 26, 27 | Aviso por correo a las dos direcciones ante cada recuperación y cada emisión de códigos (sección 3.5) | Por definir |
| Registrar o cambiar el segundo factor | 27 | Aviso por correo (sección 3.5, evento ampliado respecto de RF-27); exige la contraseña actual (sección 3.6); el procedimiento está en la ERS v1.9 (RF-27, CA-59) | Por definir |
| Cambiar o restablecer la contraseña | 27 | Aviso por correo (sección 3.5, evento ampliado); con sesión exige la contraseña actual, sin sesión un enlace por correo de 15 minutos (sección 3.6); en la ERS v1.9 (RF-27, CA-59) | Por definir |
| Registrar y resolver solicitud del titular; exportar datos | 40 | Fecha límite de cinco días hábiles; la supresión se atiende salvo obligación legal (DP-18) | Sí; la exportación se audita también (RF-45) |
| Retención: avisar y eliminar o desasociar datos | 41 | Aviso al administrador antes de ejecutar; conserva movimientos financieros sin datos de identificación | Sí; la ejecuta el proceso diario |
| Registrar incidente de seguridad y avisos | 46 | Calcula el plazo de cinco días hábiles; deja constancia de cada aviso y de la revisión | Sí |
| Configurar moneda y zona horaria | 33 | La zona se configura solo a nivel de organización | Sí (RF-28) |

No todos los RF aparecen en la tabla: los que no se listan son reglas internas o cálculos derivados que ejecuta el proceso diario o el sistema (por ejemplo, RF-11, 12, 14, 22, 25, 35, 42 y 44). No se revisó cada RF restante uno por uno.

## 5. Flujos de negocio no cubiertos en el DAS, sección 10

Los flujos 10.1 (proceso diario), 10.2 (abono), 10.3 (anulación), 10.4 (reajuste), 10.5 (abono al depósito) y 10.6 (notificaciones) ya están en el DAS (hoy v0.11; la v0.9 era la vigente al escribir la v0.1 de este documento). Estos son los que faltaban (propuesta de detalle):

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
2. Acceso: se exporta el registro completo del titular en un informe web imprimible (sección 3.4.1, HT-03). Rectificación o actualización: se aplica por el flujo de actualizar ficha, con su auditoría.
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
| HT-01 | **Resuelto el 21-oct-2026** (sección 3.7): en la v1 las notificaciones salen por correo y notificación web; WhatsApp es futuro, por lo que no hay punto de recepción de estados. Si WhatsApp vuelve, se decide entonces con el proveedor (DP-04): Meta entrega los estados por webhook, con reintentos de hasta 7 días y duplicados posibles (leído por resumen); consultar el estado sin webhook no se confirmó en Meta | Incorporado como cambio de alcance en la ERS v1.9 y el DAS v0.11 |
| HT-02 | **Resuelto a nivel de diseño el 21-oct-2026** (sección 3.4.2): comprobantes de papel fuera del sistema primero, con un campo opcional de número de recibo físico; el comprobante generado por el sistema, después. Siguen pendientes con el abogado o contador (DP-20): contenido legal, si el recibo de papel basta y si Hacienda exige factura electrónica | Cambio de alcance que difiere un requisito Alta (RF-37, CA-37); reescrito en la ERS v1.9 (RF-37, RF-47, CA-61) y el modelo de datos v0.4 |
| HT-03 | **Resuelto a nivel de diseño el 21-oct-2026** (sección 3.4.1): todo el registro del titular, incluida la fotografía de la cédula, en un informe web imprimible (el solicitante rectificó su primera elección, PDF generado por el sistema, y adoptó la recomendación) | El abogado valida alcance y exclusiones (DP-17); ERS: RF-40 y CA-27 |
| HT-04 | La ERS (sección 15) menciona una "especificación de API", anterior al ADR-022 | **Resuelto en la ERS v1.9 (21-oct-2026):** sección 15 ajustada |
| HT-05 | **Resuelto el 20-oct-2026** (ver sección 3.5 y ADR-026): aviso por correo a dos direcciones, cuatro eventos, recuperación que procede ante fallo del envío. Quedan pendientes el dominio y las dos direcciones. Los cambios de la ERS se hicieron en la v1.9 | Incorporado |
| HT-06 | **Resuelto el 21-oct-2026:** la auditoría registra actor = sistema, tipo de actor = proceso y el `ejecucion_id` cuando lo hace el proceso diario. El solicitante preguntó por dos cuentas o un sistema aparte tipo CMS; no se adoptaron (ver actualización 2026-10-21l) | Incorporado en la ERS v1.9 (RF-28), el DAS v0.11 y el modelo de datos v0.4 (R19) |
| HT-07 | **Resuelto el 21-oct-2026:** la técnica es `select_for_update()` de Django dentro de `transaction.atomic()` (`SELECT ... FOR UPDATE` en PostgreSQL), verificada en la documentación de Django (leída por resumen, primera mitad) y de PostgreSQL (bloqueos de fila). Sin `nowait`: la segunda operación espera. Bloquear varias filas siempre en el mismo orden. Sin efecto en SQLite | Incorporado en el DAS v0.11 (10.2); la prueba de concurrencia usa `TransactionTestCase` y PostgreSQL (estrategia de pruebas) |
| HT-08 | **Resuelto a nivel de diseño el 21-oct-2026** (sección 3.6): contraseña actual para cambiar la contraseña y reemplazar el TOTP; enlace por correo de 15 minutos para restablecer. Las dos primeras decisiones van contra la recomendación | Incorporado en la ERS v1.9 (RF-27, CA-59), el DAS v0.11 (ADR-026) y el modelo de datos v0.4 (`TOKEN_RESTABLECIMIENTO`) |
| HT-09 | La ERS 2.4 excluye el correo como canal de notificación; el ADR-026 lo usa solo para alertas de seguridad | **Resuelto en la ERS v1.9 (21-oct-2026):** sección 2.4 y RF-23 |

HT-nn es un identificador local de este documento, no de la lista compartida del proyecto.

## 7. Decisiones y pendientes

**Decidido el 20-oct-2026 (HT-05):** canal de correo con dos direcciones y WhatsApp después; Resend por API; cuatro eventos; la recuperación procede ante un fallo del envío. Detalle y fuentes en la [actualización 2026-10-20 (h)](../actualizaciones/2026-10-20h_ht-05-recuperacion-acceso/CAMBIOS.md).

**Decidido el 21-oct-2026 (HT-08):** contraseña actual para cambiar la contraseña y para reemplazar el segundo factor (TOTP en el futuro); restablecimiento sin sesión con enlace por correo de un solo uso y 15 minutos. Detalle en la [actualización 2026-10-21](../actualizaciones/2026-10-21_ht-08-contrasena-segundo-factor/CAMBIOS.md).

**Decidido el 21-oct-2026 (HT-02):** primero recibos de papel hechos fuera del sistema, con un campo opcional de número de recibo físico; el comprobante generado por el sistema se integra después. Detalle en la [actualización 2026-10-21d](../actualizaciones/2026-10-21d_ht-02-comprobante-fisico/CAMBIOS.md).

**Decidido el 21-oct-2026 (HT-03):** la exportación incluye todo el registro del titular, con la fotografía de la cédula, y se entrega como informe web imprimible (rectificó su primera elección, PDF generado por el sistema). Detalle en la [actualización 2026-10-21c](../actualizaciones/2026-10-21c_ht-03-exportacion-titular/CAMBIOS.md).

**Decidido el 21-oct-2026 (HT-01):** en la v1 los recordatorios y alertas al administrador salen por notificación web y correo; WhatsApp queda para el futuro y no se define punto de recepción de estados. Detalle en la [actualización 2026-10-21b](../actualizaciones/2026-10-21b_ht-01-canal-correo/CAMBIOS.md).

**Pendientes del solicitante:**
1. HT-01: resuelto (sección 3.7). Queda confirmar, para la ERS v1.9, la dirección de destino, los límites de contenido del correo y su validación legal.
2. HT-03: resuelto (sección 3.4.1). Quedan la validación del abogado y la entrega y auditoría de la exportación.
3. HT-02: resuelto (sección 3.4.2). Queda DP-20 con el abogado o contador y la fecha o versión de la fase A.
4. Auditoría de lecturas: decidido el 21-oct-2026 (fotos de cédula y exportación del titular; no las lecturas ordinarias). La reimpresión del comprobante se decide en la fase A.
5. HT-08: resuelto en la sección 3.6; queda decidir si se añade el TOTP al reemplazo del segundo factor (fecha o versión) y las tres propuestas de endurecimiento sin decidir.
6. Decidido el 21-oct-2026: dominio `.com` en Cloudflare Registrar (nombre y precio por confirmar al comprarlo); dos direcciones del solicitante en proveedores distintos; reintentador cada 1 minuto; protecciones del enlace de restablecimiento. Detalle en la actualización 2026-10-21k.
## 8. Condiciones para aprobar este documento

- Aprobar la ERS v1.9, el DAS v0.11 y el modelo de datos v0.4.
- Resolver los pendientes de la sección 7.
- Revisión por otra persona distinta del autor (hoy el solicitante ocupa los tres roles, DP-23).

## Registro de aprobación

| Rol | Nombre | Resultado | Fecha |
|---|---|---|---|
| Responsable del negocio | Pendiente | Pendiente | Pendiente |
| Responsable técnico | Pendiente | Pendiente | Pendiente |
| Responsable de pruebas | Pendiente | Pendiente | Pendiente |

**Fin del documento — DTE-SGA-001, versión 0.6 (borrador no aprobado).**
