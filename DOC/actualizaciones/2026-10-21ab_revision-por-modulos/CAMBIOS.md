# Actualización 2026-10-21 (ab) — Revisión guiada de la documentación por módulos

**Fecha:** 2026-10-21 (se amplía a medida que avanza la revisión)
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md) y los que cada módulo indique; [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Motivo y método
El solicitante pidió repasar toda la documentación uno por uno, lo más importante por módulo, para rectificar. Se recorren los diez módulos de la sección 5 del DAS. Para cada uno se presenta una ficha (qué hace, reglas, datos, decisiones, pruebas, entrega y quién decidió qué) y los puntos que el asistente detecta como dudosos; el solicitante corrige o decide. Cada decisión se registra aquí y se aplica a los documentos.

## 2. Módulo 1 — Inquilinos, documentos y consentimientos
| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | Campos obligatorios y finalidad de teléfono y correo | Obligatorios: nombre completo, tipo y número de documento, frente de la fotografía y consentimiento; teléfono y correo opcionales, para contacto manual del administrador | Igual |
| 2 | Fotografía "de la cédula" | Fotografía del documento de identidad de cualquier tipo; "frente" = cara con la fotografía y los datos principales | Igual |

**Cambios:** ERS v1.9 (RF-01, sección 4, CA-01, glosario); modelo de datos v0.4 (`INQUILINO`: nombre obligatorio, teléfono y correo opcionales).
**Fuente:** el principio de pertinencia de la Ley 8968 ya recogido en la RN-24 (lectura propia del proyecto); no hay fuente nueva. Validación legal: declarada por el solicitante, sin dictamen.
**Límites:** la redacción de "frente" para el pasaporte es del asistente; el nombre "cédula" se conserva en el modelo y las pruebas como término histórico.

## 3. Módulo 2 — Propiedades y contratos
| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | Anular un contrato (el estado *anulado* existía sin operación) | Solo si no tiene movimientos válidos, con motivo obligatorio; anula sus obligaciones y su depósito sin abonos | Igual |
| 2 | Alias de la propiedad (RF-44 hablaba de un alias no definido) | Alias obligatorio y único (nombre corto) | Igual |
| 3 | Regla de propiedad inactiva | Se bloquea con contrato vigente, futuro o por decidir; se puede reactivar; una inactiva no admite contratos nuevos | Igual |

**Cambios:** ERS v1.9: RF-06 (alias y regla de inactiva), **RF-48 nuevo** (anular contrato), **CA-62 y CA-63 nuevos**, matriz, datos; modelo de datos v0.4: `PROPIEDAD.alias`, `CONTRATO.anulado_en` y `motivo_anulacion`, restricciones R20 y R21; diseño técnico v0.7 (catálogo de operaciones); DAS v0.11 (entidades); estrategia de pruebas v0.3 (CA-62 y CA-63; 63 CA); plan de implementación (E2: RF-48, CA-62 y CA-63) y registro de avance (E2: 19 CA).
**Consecuencia:** los totales pasan a 48 RF y 63 CA. El script de coherencia lo comprueba (matriz, pruebas y plan).
**Fuente:** coherencia con RN-17 (solo se anula una obligación sin movimientos), RN-10 y RN-22; sin fuente externa.
**Límites:** el alias y las reglas son criterio del solicitante y del asistente; la validación legal sigue declarada por el solicitante, sin dictamen.

## 4. Módulo 3 — Obligaciones, períodos, vencimientos y prorrateo
**Verificación del asistente:** los ejemplos numéricos de CA-03, CA-14, CA-30, CA-36 y CA-50 se recalcularon a mano y son correctos (por ejemplo, 180.000 × 16/31 = 92.903,2, que da ₡92.903).

| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | CA-49 decía "en o después" de la fecha de apertura, frente a "después" de RF-43 y DP-25 | Corregir a "después" | Igual |
| 2 | Contrato *por decidir* sin recordatorio | Notificación web persistente hasta cerrar o renovar y una línea en el resumen diario por correo | Igual |

**Cambios:** ERS v1.9 (CA-49, RF-42, RF-23, CA-32); DAS v0.11 (10.1); modelo de datos v0.4 (`NOTIFICACION.tipo` con `contrato_por_decidir`). No hay IDs nuevos.
**Límites:** la forma de la línea en el resumen y de la notificación web es criterio del asistente; el resumen se envía ahora si hay obligaciones vencidas o contratos por decidir.

## 5. Módulo 4 — Movimientos, saldos y recibos
**Verificación del asistente:** CA-19 (180.000 − 60.000 = 120.000) y CA-38 (₡150.000 ÷ ₡500 = $300) son correctos; el nuevo ejemplo de CA-38 se calculó con aritmética decimal (100.000 ÷ 512,35 = 195,179…, que da $195,18).

| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | Cálculo y redondeo del equivalente de un pago en otra moneda (RF-38 no lo definía) | El sistema lo calcula con el tipo de cambio digitado y lo redondea a dos decimales, mitad hacia arriba | Igual |
| 2 | Pago mayor que el saldo o que cubre varias obligaciones | Se mantiene el rechazo del exceso; un abono por cada obligación | Igual |

**Cambios:** ERS v1.9 (RF-38, RF-34, CA-38); DAS v0.11 (7.2); modelo de datos v0.4 (`MOVIMIENTO.tipo_cambio`); estrategia de pruebas v0.3 (casos límite). No hay IDs nuevos.
**Límites:** la unidad del tipo de cambio (colones por dólar) se infirió del ejemplo de CA-38 y se explicitó; el solicitante la aceptó al elegir la opción recomendada.

## 6. Módulo 5 — Depósitos de garantía
**Verificación del asistente:** CA-15 (300.000 − 100.000 = 200.000) y CA-45 (400.000 supera 180.000) son correctos.

| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | Moneda del depósito (podía diferir de la del contrato, sin regla para compararla con una mensualidad) | El depósito usa siempre la moneda del contrato | Igual |
| 2 | A quién aplica la advertencia de depósito mayor a una mensualidad | Solo a contratos de vivienda, según S-02 | Igual |

**Cambios:** ERS v1.9 (RF-29, RF-30, RN-26, datos, CA-45); DAS v0.11 (entidad Depósito); modelo de datos v0.4 (`DEPOSITO` sin campo de moneda). No hay IDs nuevos.
**Límites:** que la advertencia solo aplique a vivienda es una lectura del proyecto de OL-11 y del art. 92 (lectura propia); el solicitante declaró que el abogado la verificó, sin dictamen aportado.

## 7. Módulo 6 — Calendario y consultas
| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | La obligación de apertura (sin período) no tenía fecha de vencimiento definida | La digita el administrador al registrar la apertura; por defecto, la fecha de apertura más los días de gracia; su fecha límite es la misma | Igual |
| 2 | El calendario solo mostraba obligaciones | También muestra, como eventos informativos sin alertas, el fin de cada contrato y la fecha límite acordada del depósito | Propuesto en la ficha; adoptado por el solicitante |
| 3 | No había filtro por propiedad | Se agrega, por alias | Propuesto en la ficha; adoptado por el solicitante |

**Cambios:** ERS v1.9 (RF-43, RN-06, RF-17, RF-18, CA-06, CA-07, CA-49); modelo de datos v0.4 (`OBLIGACION.fecha_vencimiento` y `fecha_limite` en `apertura`); estrategia de pruebas v0.3 (fila del calendario). No hay IDs nuevos (RF-18 cambia de título, no de ID).
**Límites:** los puntos 2 y 3 se adoptaron tal como los redactó el asistente en la ficha, sin variantes; el rendimiento del calendario sigue siendo un objetivo por medir (RNF-08).

## 8. Módulo 7 — Notificaciones y configuración regional
| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | Formato de números (la ERS usa ₡180.000 y Django con `es` usa espacio no separable de miles) | Punto de miles y coma decimal con el símbolo delante (₡180.000,50) y porcentajes con coma, con formato propio | Igual |
| 2 | Muchos correos de recordatorio | Un único resumen diario con tres secciones (recordatorios, vencidas, por decidir); las notificaciones web siguen siendo individuales | Propuesto en la ficha; adoptado |
| 3 | Cambio de una dirección de correo (sin requisito) | Contraseña actual y confirmación en la dirección nueva; aviso a las dos anteriores. **Sin código TOTP** | Contraseña actual **y código TOTP**, confirmación y aviso (OWASP) |

**Riesgo asumido en el punto 3:** una sesión robada junto con la contraseña puede cambiar la dirección si controla también la nueva. Es la misma decisión de fondo que HT-08.
**Cambios:** ERS v1.9 (RF-27, RF-21, RF-23, RNF-12, CA-05, CA-08, **CA-64 nuevo**, matriz); DAS v0.11 (ADR-026: cinco eventos; 10.6; 7.6); modelo de datos v0.4 (`evento_seguridad` con `cambio_correo`); diseño técnico v0.7 (§3.5); estrategia de pruebas v0.3 (CA-64; 64 CA; formato de números); plan (E4: CA-64) y registro de avance (E4: 11 CA). Totales: 48 RF y 64 CA.
**Fuentes:** DAS (comprobación por resumen del archivo `es/formats.py` de Django 5.2: coma decimal y espacio no separable de miles; no encontré `es_CR` en esa rama) y OWASP Authentication Cheat Sheet (cambio de correo con multifactor o contraseña actual y aviso a la dirección actual; leída por resumen en una sesión anterior).
**Límites:** no se verificó la norma costarricense de formato de números; el formato propio requiere implementación en Django (fase 5).

## 9. Módulo 8 — Privacidad
**Verificación del asistente:** CA-56 (viernes 6 de noviembre de 2026 más cinco días hábiles, sin sábado ni domingo, es el viernes 13 de noviembre de 2026) es correcto.

| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | No había operación para ejecutar una supresión a petición | "Desasociar a petición" con los mismos bloqueos que desactivar a un inquilino; si se niega, resolución escrita con motivo | Igual |
| 2 | Inquilinos sin contrato o con todos anulados no tenían plazo de retención | Plazo corto configurable (propuesta de 1 año) desde el registro o la última anulación, el posterior | Igual |
| 3 | El texto de cada versión del consentimiento no se guardaba y la revocación no tenía efecto definido | Guardar cada versión; al revocar: aviso en la ficha, sin contratos nuevos y solicitud de supresión de oficio | Igual |

**Cambios:** ERS v1.9 (RF-39, RF-40, RF-41; **CA-65, CA-66 y CA-67 nuevos**; matriz; configuración de la organización); modelo de datos v0.4 (`TEXTO_CONSENTIMIENTO` nuevo, `CONSENTIMIENTO.texto_id`, `SOLICITUD_TITULAR.origen`, `ORGANIZACION.retencion_sin_contrato_meses`); DAS v0.11 (7.7); diseño técnico v0.7 (catálogo); estrategia de pruebas v0.3 (67 CA); plan (CA-65 y 66 en E5; CA-67 en E2, hallazgo HI-04) y registro de avance (E2: 20; E5: 8). Totales: 48 RF y 67 CA.
**Fuentes:** Ley 8968 (arts. 5, 6 y 7) y Reglamento 37554-JP (arts. 22 y 26), leídos en las copias del Archivo Nacional en sesiones anteriores; lectura del proyecto, no asesoría legal.
**Límites:** el plazo de un año y la apertura de oficio de una solicitud de supresión al revocar son propuestas del asistente, aceptadas por el solicitante; el abogado las validó según el solicitante, sin dictamen aportado. Un contrato vigente impide desasociar: la solicitud se resuelve como denegada con motivo, lo que debe ser coherente con el art. 26 del Reglamento.

## 10. Módulo 9 — Autenticación y sesiones
**Riesgo acumulado registrado (no se cambió):** con una sesión abierta robada y la contraseña, alguien puede cambiar la contraseña, reemplazar el segundo factor y cambiar el correo sin necesitar el TOTP; los avisos llegan después. Es la suma de tres decisiones del solicitante contra la recomendación (HT-08 y cambio de correo).

| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | No había límite de intentos fallidos | Espera creciente por cuenta, sin bloqueo permanente: tras 5 fallos seguidos, 1 minuto, duplicándose hasta 1 hora; aviso al llegar a 5 | Igual |
| 2 | Faltaban reglas del segundo factor y de los códigos | 10 códigos de un solo uso; un TOTP aceptado no se reutiliza; tolerancia de un intervalo de 30 s; emitir códigos nuevos exige la contraseña actual e invalida los anteriores | Igual |
| 3 | No se definía la creación de la cuenta ni el rescate | Comandos de gestión en el servidor para crear la cuenta y para el rescate (desactiva el segundo factor y obliga a registrarlo de nuevo); sin pantallas públicas | Igual |

**Cambios:** ERS v1.9 (RF-27, RN-25, **CA-68, CA-69 y CA-70 nuevos**, matriz); DAS v0.11 (ADR-026: siete eventos; sección 9); modelo de datos v0.4 (`ADMINISTRADOR.fallos_consecutivos`, `espera_hasta`, `ultimo_intervalo_totp`; `evento_seguridad` con `intentos_fallidos` y `rescate_servidor`); diseño técnico v0.7 (§3.5); estrategia de pruebas v0.3 (70 CA); plan (E0: CA-68, 69 y 70; hallazgo HI-05) y registro de avance (E0: 7 CA); lista de verificación (RV-48 a RV-51; 51 puntos). Totales: 48 RF y 70 CA.
**Fuentes (por resumen, 21-oct-2026):** OWASP, Authentication Cheat Sheet (el bloqueo por cuenta es la protección más común contra la fuerza bruta, con riesgo de denegación de servicio; contador asociado a la cuenta y no a la IP; permitir el restablecimiento aun bloqueado) y Multifactor Authentication Cheat Sheet (las contraseñas de un solo uso son de un solo uso; 30 s por intervalo según RFC 6238; número de códigos de recuperación no especificado).
**Límites:** todas las cifras (5 fallos, 1 minuto a 1 hora, 10 códigos, tolerancia de un intervalo) son propuesta del asistente: ninguna fuente leída las fija. El rescate por el servidor solo vale si el solicitante conserva el acceso al servidor.

## 11. Módulo 10 — Auditoría y operación
| # | Punto | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | Los eventos de autenticación no estaban en la auditoría | Se auditan los inicios de sesión correctos y fallidos, los cierres de sesión y los siete eventos de seguridad, con la dirección IP de origen y sin contraseñas, códigos ni tokens | Igual |
| 2 | No había consulta de la auditoría ni plazo de conservación | Pantalla de solo lectura con filtros (fecha, tipo de evento, entidad, actor); sin borrado automático en la v1; el plazo se define con DP-18 | Igual |
| 3 | Nadie se enteraba si el proceso diario fallaba | Alerta web persistente y correo si una hora después de la hora programada no hay una ejecución correcta del día o la última falló (el reintentador lo comprueba) | Igual |

**Cambios:** ERS v1.9 (RF-28; **RF-49 nuevo**; **CA-71 y CA-72 nuevos**; matriz); modelo de datos v0.4 (`AUDITORIA.ip_origen`, `NOTIFICACION.tipo` con `proceso_diario_fallido`); DAS v0.11 (entidad Auditoría; ADR-013); diseño técnico v0.7 (catálogo); estrategia de pruebas v0.3 (72 CA); plan (E0: CA-71; E4: RF-49 y CA-72; hallazgo HI-06) y registro de avance (E0: 8; E4: 12); lista de verificación (RV-52 y RV-53; 53 puntos).
**Fuente:** OWASP, Logging Cheat Sheet (por resumen, 21-oct-2026): registrar la identidad y la dirección de origen y las funciones de mayor riesgo; no guardar contraseñas, tokens ni identificadores de sesión.
**Límites:** la hora de la comprobación (una hora después) es propuesta del asistente; no se cubre un servidor caído (monitoreo externo, fase 6); la dirección IP es un dato del propio acceso del administrador; el plazo de conservación de la auditoría sigue abierto en DP-18.

## 12. Cierre de la revisión por módulos
**Totales después de los diez módulos:** 49 requisitos funcionales (RF-48 y RF-49 nuevos) y 72 criterios de aceptación (CA-62 a CA-72 nuevos), sin cambios en RN, RNF, OL, DP ni ADR existentes salvo textos. El script de coherencia comprueba que todos están en la matriz, en la estrategia de pruebas y exactamente una vez en una entrega del plan.
**Decisiones contra la recomendación del asistente en esta revisión:** ninguna nueva; en el módulo 7 el cambio de correo sin código TOTP se registró como riesgo asumido, junto con las de HT-08.
**Pendientes que siguen abiertos:** validación legal con dictamen (declarada por el solicitante, sin documento); persona revisora y nivel de verificación; formato del origen y consentimiento de los inquilinos actuales para la carga inicial; versiones exactas (micro) y forma de instalar Django; dominio y precios al contratar; monitoreo externo, endurecimiento del servidor y verificación de Resend (fase 6).
**Propuestas del asistente que el solicitante aceptó con la opción recomendada y no revisó una por una:** todas las cifras numéricas (límites de intentos, plazos de un año y de 15 minutos, 10 códigos, hora de la comprobación del proceso) y la forma de los datos nuevos.
