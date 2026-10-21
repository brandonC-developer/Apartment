# Modelo lógico de datos

**Sistema de Gestión de Alquileres**

**Identificador:** MDD-SGA-001
**Versión:** 0.4 — Borrador para revisión (reemplaza a [v0.3](MODELO_DATOS_SGA_001_v0.3_borrador.md), que se conserva sin cambios; la [v0.2](MODELO_DATOS_SGA_001_v0.2_borrador.md) y la [v0.1](MODELO_DATOS_SGA_001_v0.1_borrador.md) también)
**Fecha:** 21 de octubre de 2026
**Estado:** Borrador; no aprobado
**Base:** [ERS-SGA-001 v1.9](../fase-1-ers/ERS_SGA_001_v1.9_borrador.md) y [DAS-SGA-001 v0.11](../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md). La v0.4 alinea el modelo con las decisiones del 20 y 21-oct-2026 (correo en lugar de WhatsApp, avisos de seguridad, restablecimiento de contraseña, recibo físico y comprobante como fase posterior). Los hallazgos H1, H2, H3, H9, H10, H11, H12 y H13 están incorporados en ellos; H4 es decisión provisional (DP-20).

Este documento es un **modelo lógico**: entidades, atributos, claves, restricciones y valores derivados. **No fija motor de base de datos, tipos físicos ni nombres de tabla definitivos** (ADR-002 sigue abierto). Los tipos son lógicos. Lo que no proviene de la ERS o del DAS se marca como *propuesta*.

## 1. Convenciones

| Tipo lógico | Significado |
|---|---|
| `id` | Identificador único e inmutable: entero de 64 bits autoincremental (`BigAutoField` de Django; ADR-028, decisión del 21-oct-2026). Los UUID se mantienen en `clave_solicitud` y en los nombres de archivo de las cédulas. |
| `fecha` | Fecha de calendario sin hora (vencimientos, períodos, fecha real de recepción). |
| `instante` | Marca de tiempo almacenada en UTC (registro, auditoría). Se presenta en la zona de la organización. |
| `dinero` | Decimal exacto (nunca flotante), con la moneda en una columna aparte. Escala: 2 decimales almacenados; el redondeo a la unidad entera aplica solo al prorrateo de CRC (ERS RN-12). |
| `moneda` | Código de 3 letras: `CRC` o `USD` (ERS RN-23). |
| `texto`, `entero`, `lógico` | Como indican. |

Regla general: **los movimientos y los ajustes de importe no se editan ni se borran** (ERS 7.3, punto 6). Los saldos, el importe exigible vigente y los estados **no se almacenan**; se derivan (sección 5).

### 1.1 Control del documento

| Versión | Fecha | Cambio | Origen | Aprobación |
|---|---|---|---|---|
| 0.1 | 17-oct-2026 | Primer borrador | "empieza el modelo de datos" | Ninguna |
| 0.2 | 17-oct-2026 | Ajustes de importe como filas nuevas (`AJUSTE_OBLIGACION`); auditoría sin valores personales; algoritmo de contraseña; fuentes; ADR propuestos; prueba en PostgreSQL (sección 12), hallazgo H11; fuentes de dinero, UTC e idempotencia; H12 y H13 (H13 aceptada, con `clave_solicitud` y R15) | Verificación de buenas prácticas de la fase 3; decisión del solicitante "procede con las dos recomendaciones" | Ninguna |
| 0.3 | 17-oct-2026 | Hora de notificación como fecha local, hora local y zona (DP-26); entidad `INCIDENTE_SEGURIDAD` (RF-46); H4 y H12 resueltas | DP-26 y H4 respondidas por el solicitante; ERS v1.8 | Ninguna |
| 0.4 | 21-oct-2026 | `MOVIMIENTO.numero_recibo_fisico` (RF-47, R16); `COMPROBANTE` como fase posterior; `ORGANIZACION` con correos (la segunda, del solicitante); `NOTIFICACION` con canal correo, avisos de seguridad y reintentos; entidad `TOKEN_RESTABLECIMIENTO`; H14; transacciones y trazabilidad ajustadas | ERS v1.9 y DAS v0.11 (decisiones del solicitante del 20 y 21-oct-2026) | Ninguna |

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Responsable técnico | Por designar (DP-23) | Pendiente | Pendiente |

### 1.2 Fuentes de las prácticas de diseño

| Práctica | Fuente | Cómo se validó | Limitaciones |
|---|---|---|---|
| Entradas inmutables y saldos calculados, no editados | [Fowler, *Accounting Transaction*](https://martinfowler.com/eaaDev/AccountingTransaction.html) | Leída por resumen | Borrador de mediados de los 2000. No trata reversiones ni correcciones: esa parte del modelo es criterio propio. |
| Evitar solapamiento de rangos con restricción de exclusión | [PostgreSQL, tipos de rango](https://www.postgresql.org/docs/current/rangetypes.html) | Leída por resumen | Solo vale si se elige PostgreSQL (ADR-002 abierto). |
| Hash de contraseñas: Argon2id, mínimo 19 MiB de memoria, 2 iteraciones, paralelismo 1 | [OWASP, Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | Leída por resumen | Los parámetros son un mínimo; se afinan en el servidor real (menos de ~1 s por hash). |
| Dinero exacto: decimal y no flotante | [Python, módulo `decimal`](https://docs.python.org/3/library/decimal.html) y [PostgreSQL, tipos numéricos](https://www.postgresql.org/docs/current/datatype-numeric.html) | Ambas leídas por resumen | Respaldan `numeric`/decimal y el redondeo a mitad hacia arriba (`ROUND_HALF_UP`). Python: `round()` sin decimales redondea al par; usar `quantize` con el modo explícito. PostgreSQL: `numeric` es lento frente a enteros o flotantes, irrelevante a este volumen. |
| Instantes en UTC, con salvedad | [W3C, Working with Time Zones](https://www.w3.org/TR/timezone/) | Leída por resumen | Recomienda UTC "when in doubt", pero **no basta para eventos futuros en hora local** (cambios de reglas de zona); ver H12. Las fechas sin hora (vencimientos) se guardan sin zona, como indica la guía. |
| Idempotencia de operaciones reintentables | [Stripe, Idempotent requests](https://docs.stripe.com/api/idempotent_requests) | Leída por resumen | Clave única generada por el cliente (UUID v4), de hasta 255 caracteres; se compara con los parámetros originales y se descarta tras 24 h. Es el patrón para **peticiones**; nuestra `clave_unica` de notificaciones es una clave natural permanente, patrón distinto que esta fuente no respalda. Ver H13. |

## 2. Diagrama entidad-relación

```mermaid
erDiagram
    ORGANIZACION ||--|| ADMINISTRADOR : "una cuenta"
    ADMINISTRADOR ||--o{ CODIGO_RECUPERACION : tiene
    ADMINISTRADOR ||--o{ TOKEN_RESTABLECIMIENTO : solicita
    INQUILINO ||--o{ CONSENTIMIENTO : otorga
    INQUILINO ||--o{ DOCUMENTO_IDENTIDAD : tiene
    DOCUMENTO_IDENTIDAD ||--o{ ACCESO_DOCUMENTO : "se consulta"
    INQUILINO ||--o{ SOLICITUD_TITULAR : presenta
    INQUILINO ||--o{ CONTRATO : "firma"
    PROPIEDAD ||--o{ CONTRATO : "se alquila en"
    CONTRATO ||--|{ CONDICION_CONTRATO : "historial de condiciones"
    CONTRATO ||--o{ OBLIGACION : genera
    CONTRATO ||--o| DEPOSITO : "puede tener"
    OBLIGACION ||--o{ AJUSTE_OBLIGACION : "se ajusta con"
    CONDICION_CONTRATO ||--o{ AJUSTE_OBLIGACION : origina
    OBLIGACION ||--o{ MOVIMIENTO : recibe
    DEPOSITO ||--o{ MOVIMIENTO : recibe
    MOVIMIENTO ||--o| COMPROBANTE : "respalda (fase posterior)"
    MOVIMIENTO ||--o| MOVIMIENTO : "es anulado por"
    OBLIGACION ||--o{ NOTIFICACION : origina
    CONTRATO ||--o{ NOTIFICACION : origina
    EJECUCION_PROCESO ||--o{ NOTIFICACION : emite
    ORGANIZACION ||--o{ NOTIFICACION : "avisos de seguridad"
    ORGANIZACION ||--o{ AUDITORIA : registra
```

## 3. Entidades y atributos

### 3.1 Configuración y acceso

**ORGANIZACION** (una sola fila en v1) — *ERS RF-33, RF-21, RF-41, OL-13*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| nombre_responsable | texto | Identidad del responsable de la base de datos (art. 5 de la Ley 8968, inciso h). Se completa con DP-23. |
| direccion_responsable | texto | Idem. |
| zona_horaria | texto | Identificador IANA; `America/Costa_Rica` por defecto (RF-33). |
| hora_proceso_diario | hora local | 07:00 por defecto (DP-02). |
| correo_admin | texto | Destinatario de las notificaciones, los avisos de seguridad y el enlace de restablecimiento (RF-23, RF-27, RF-44). Dato personal del administrador. |
| correo_aviso_secundario | texto, nulo | Segunda dirección de los avisos de seguridad (RF-27): del propio solicitante, en otro proveedor (decisión del 21-oct-2026); no es dato de un tercero. Nunca recibe el enlace de restablecimiento. |
| telefono_whatsapp_admin | texto, nulo | **Futuro, fuera de la v1** (DP-04): destinatario de avisos por WhatsApp (RF-44). |
| aceptacion_whatsapp_admin | instante, nulo | **Futuro:** fecha de aceptación de recibir mensajes de WhatsApp. |
| anticipaciones_recordatorio | lista de enteros (máx. 3) | Días antes del vencimiento; por defecto `[3]` (RF-21). |
| retencion_fotos_anios | entero | 5 por defecto; no mayor que 10 (RF-41). |
| dias_gracia_defecto | entero | 7 (RN-06). |

**ADMINISTRADOR** (una sola fila en v1) — *RF-26, RF-27, RN-25*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| usuario | texto | Único. |
| hash_contrasena | texto | Nunca la contraseña. Propuesta: Argon2id con al menos los parámetros mínimos de OWASP (sección 1.2), con sal única por contraseña. |
| secreto_segundo_factor | texto cifrado | TOTP. |
| segundo_factor_activo | lógico | Obligatorio para operar (RNF-01). |
| creado_en, actualizado_en | instante | |

**CODIGO_RECUPERACION** — *RF-27*: `id`, `administrador_id`, `hash_codigo`, `usado_en` (instante, nulo si disponible), `creado_en`. Un código se usa una sola vez; no se guarda en claro.

**TOKEN_RESTABLECIMIENTO** — *RF-27, CA-59* (propuesta de estructura): `id`, `administrador_id`, `hash_token` (nunca el token en claro), `creado_en` (instante), `expira_en` (instante; `creado_en` más 15 minutos, valor propuesto), `usado_en` (instante, nulo si no usado). Un token se usa una sola vez y no sirve vencido (R17). El enlace se envía solo a `correo_admin`. Los `creado_en` de las últimas 24 horas sirven para limitar a 3 solicitudes por hora (R18).

### 3.2 Inquilinos y datos personales

**INQUILINO** — *RF-01 a RF-05, RN-10, RN-24*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| nombre_completo | texto | Se anula al desasociar (ver sección 6). |
| tipo_documento | texto | `cedula`, `dimex`, `pasaporte` u `otro`. |
| numero_documento | texto | Se anula al desasociar. Único junto con `tipo_documento` entre inquilinos activos; duplicado → advertencia (RF-01), no bloqueo. |
| telefono, correo | texto | Se anulan al desasociar. |
| activo | lógico | No se puede poner en falso con contrato vigente o saldos (RF-04). |
| desasociado_en | instante | No nulo si ya se eliminaron los datos personales (RF-41). |
| creado_en, actualizado_en | instante | |

**CONSENTIMIENTO** — *RF-39, OL-13*: `id`, `inquilino_id`, `version_texto`, `medio` (`fisico` o `electronico`), `otorgado_en`, `revocado_en` (nulo si vigente).

**DOCUMENTO_IDENTIDAD** — *RF-01, RF-02, ADR-003*: `id`, `inquilino_id`, `cara` (`frente` o `reverso`), `referencia_archivo` (referencia protegida al almacenamiento privado, nunca una URL pública), `tipo_real_archivo`, `tamano_bytes`, `creado_en`, `eliminado_en`. El frente es obligatorio; el reverso, opcional.

**ACCESO_DOCUMENTO** — *RF-45*: `id`, `documento_id`, `actor` (administrador), `accion` (`consulta` o `descarga`), `ocurrido_en`. No guarda la imagen.

**SOLICITUD_TITULAR** — *RF-40, OL-15*: `id`, `inquilino_id`, `tipo` (`acceso`, `rectificacion`, `actualizacion`, `supresion`), `recibida_el` (fecha), `fecha_limite` (cinco días hábiles), `resuelta_el` (nulo si abierta), `resolucion` (texto).

### 3.3 Propiedades y contratos

**PROPIEDAD** — *RF-06*: `id`, `descripcion`, `direccion`, `inactiva` (lógico), `creado_en`. El estado *disponible* u *ocupada* se deriva del contrato vigente (sección 5).

**CONTRATO** — *RF-07 a RF-10, RF-36, RF-42*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| inquilino_id | id | |
| propiedad_id | id | |
| destino | texto | `vivienda` u `otro` (OL-06, OL-08). |
| fecha_inicio | fecha | Fecha de entrega del bien; ancla el período (RN-03). |
| fecha_fin | fecha, nulo | Inclusive (RN-02). |
| moneda | moneda | |
| anulado | lógico | Contrato dado de baja (RN-30). |
| creado_en | instante | |

El monto, el día de vencimiento y los días de gracia **no viven en el contrato**: están en `CONDICION_CONTRATO`, para conservar el historial.

**CONDICION_CONTRATO** — *RF-10, RN-14, DP-22* (propuesta de estructura; la ERS pide conservar valor anterior, nuevo, fecha efectiva y motivo)

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| contrato_id | id | |
| monto_mensual | dinero | Mayor que cero. |
| dia_vencimiento | entero | De 1 a 31; por defecto, el día de `fecha_inicio` (DP-24). |
| dias_gracia | entero | |
| vigente_desde | fecha | Fecha efectiva. En un reajuste, inicio de período (RF-10). |
| tipo | texto | `inicial`, `reajuste` o `correccion`. |
| fecha_notificacion | fecha, nulo | Solo en reajustes. |
| porcentaje | decimal, nulo | Solo en reajustes. |
| tope_digitado | decimal, nulo | Solo en reajustes de vivienda (DP-22). |
| fuente_tope | texto, nulo | Certificación del INEC o publicación del MIVAH. |
| motivo | texto, nulo | Obligatorio en correcciones. |
| registrada_en | instante | |

La condición aplicable a un período es la de mayor `vigente_desde` que no supere el inicio del período. Las correcciones retroactivas **no sustituyen** filas: la nueva fila queda registrada y cada obligación afectada recibe una fila de `AJUSTE_OBLIGACION` que apunta a esa condición.

**DEPOSITO** — *RF-29 a RF-32*: `id`, `contrato_id` (único: un depósito por contrato), `importe_total`, `moneda`, `fecha_limite_acordada` (nulo), `notas`, `creado_en`. Si se corrige `importe_total`, se registra en auditoría y nunca puede quedar por debajo de lo abonado.

### 3.4 Obligaciones y movimientos

**OBLIGACION** — *RF-11 a RF-15, RF-43, RN-04, RN-05, RN-12, RN-13*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| contrato_id | id | |
| tipo | texto | `regular` o `apertura` (CA-49, ERS 7.1). |
| periodo_inicio | fecha, nulo | Nulo solo en `apertura`. |
| periodo_fin | fecha, nulo | Idem. |
| fecha_vencimiento | fecha | Regla RN-05. |
| fecha_limite | fecha | `fecha_vencimiento` + días de gracia (RN-06). |
| importe_inicial | dinero | Importe con el que se creó la obligación. **No se modifica nunca**; los cambios posteriores son filas de `AJUSTE_OBLIGACION`. |
| moneda | moneda | La del contrato. |
| condicion_id | id, nulo | Condición aplicada al crearla (nulo en `apertura`). |
| datos_calculo | texto estructurado | Días cobrables, importe previo al redondeo, importe final y regla aplicada; se guarda cuando hubo prorrateo al crearla (RN-12, RN-13). |
| anulada_en | instante, nulo | Se completa una sola vez (excepción registrada, igual que el estado del comprobante). |
| motivo_anulacion | texto, nulo | Obligatorio si hay `anulada_en` (RN-17). |
| creado_en | instante | |

**AJUSTE_OBLIGACION** — *RF-09, RF-10, RN-14* (propuesta de estructura; resuelve el hallazgo H9)

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| obligacion_id | id | |
| tipo | texto | `reajuste`, `correccion`, `prorrateo_fin` (RF-09, RN-12) o `ajuste_manual` (RF-09). |
| importe_delta | dinero | Con signo; distinto de cero. Suma al importe de la obligación. |
| condicion_id | id, nulo | Condición que lo originó (reajuste o corrección). |
| motivo | texto | Obligatorio en `correccion` y `ajuste_manual`. |
| registrado_en | instante | |

Cada fila conserva el importe anterior y el nuevo implícitos: anterior = importe vigente antes de ella; nuevo = anterior + `importe_delta`. Una equivocación se corrige con otra fila, nunca editando.

**MOVIMIENTO** — *RF-13, RF-16, RF-30, RF-34, RF-38, RN-22*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| tipo | texto | `abono` o `reversion`. |
| obligacion_id | id, nulo | Exactamente uno de `obligacion_id` y `deposito_id` (restricción). |
| deposito_id | id, nulo | |
| importe_aplicado | dinero | Siempre positivo; en la moneda de la obligación o del depósito. |
| moneda_recibida | moneda | |
| importe_recibido | dinero | En `moneda_recibida`. Igual a `importe_aplicado` si la moneda coincide. |
| tipo_cambio | decimal, nulo | Ingresado a mano; obligatorio si las monedas difieren (RF-38). |
| fecha_real | fecha | No futura ni anterior al inicio del contrato (RN-29). |
| registrado_en | instante | Siempre se conserva (RN-29). |
| medio_pago | texto | `efectivo`, `transferencia`, `cheque` u `otro`. |
| observacion | texto, nulo | |
| numero_recibo_fisico | texto, nulo | Número del recibo de papel entregado fuera del sistema (RF-47). Único cuando no es nulo (R16). Se conserva aunque el movimiento se anule. |
| anula_a | id, nulo | Solo en `reversion`: el movimiento original (RF-16). |
| motivo | texto, nulo | Obligatorio en `reversion`. |
| excepcion_motivo | texto, nulo | Solo en abonos de depósito sobre el tercero (RF-30). |
| clave_solicitud | uuid | Generada por el formulario (UUID v4) antes de enviar; única (R15). Evita duplicar el movimiento si el envío se repite (H13). |

Un movimiento `abono` es **válido** si ninguna `reversion` apunta a él (RN-22). Una `reversion` nunca se anula.

**COMPROBANTE** (**fase posterior**; no existe en la v1, decisión del solicitante del 21-oct-2026) — *RF-37, ADR-010*: `id`, `numero` (único, consecutivo, sin reutilizar), `movimiento_id` (único), `estado` (`vigente` o `anulado`), `emitido_en`. El contenido impreso se reconstruye a partir del movimiento y su contexto.

### 3.5 Notificaciones, procesos y auditoría

**NOTIFICACION** — *RF-21 a RF-25, RF-27, RF-42, RF-44*

| Atributo | Tipo | Notas |
|---|---|---|
| id | id | |
| obligacion_id, contrato_id | id, nulo | Una u otra, según el tipo; ninguna en los avisos de seguridad. |
| tipo | texto | `recordatorio`, `alerta_atraso`, `vencimiento_contrato`, `aviso_seguridad`. |
| evento_seguridad | texto, nulo | Solo en `aviso_seguridad`: `uso_codigo_recuperacion`, `nuevos_codigos`, `cambio_segundo_factor`, `cambio_contrasena` o `restablecimiento_contrasena` (RF-27; ADR-026). |
| canal | texto | `web` o `correo`; `whatsapp` queda para el futuro (DP-04). |
| destinatario_tipo | texto | `administrador` o `secundaria` (solo avisos de seguridad). Se guarda el tipo y no la dirección, para no copiar datos personales a cada fila (propuesta). |
| clave_unica | texto | Obligación + tipo + anticipación + fecha (idempotencia, RF-21). Única. |
| fecha_programada | fecha | Fecha local según la zona de la organización (DP-26). |
| hora_programada | hora local | Hora local; el instante exacto se calcula al ejecutar con la zona de `ORGANIZACION` (DP-26). |
| estado_web | texto, nulo | `nueva`, `leida`, `archivada` (solo canal web). |
| intentos | entero | Hasta 5 (RF-24). |
| proximo_intento_en | instante, nulo | Cuándo el reintentador de intervalo corto debe volver a intentar (ADR-013, ADR-026); nulo si no hay reintento pendiente. Propuesta. |
| resultado | texto | `pendiente`, `aceptado`, `entregado`, `fallido`, `cancelado`. |
| referencia_proveedor | texto, nulo | |
| ejecucion_id | id, nulo | Ejecución que la emitió. |

**INCIDENTE_SEGURIDAD** — *RF-46, OL-19* (propuesta de estructura): `id`, `ocurrio_en` (instante), `conocido_en` (instante), `naturaleza` (texto), `datos_comprometidos` (texto, sin copiar los datos), `acciones_inmediatas` (texto), `fecha_limite_aviso` (fecha, cinco días hábiles), `estado` (`abierto` o `atendido`). Los avisos van en `AVISO_INCIDENTE`: `id`, `incidente_id`, `destinatario` (`titular` o `agencia`), `inquilino_id` (nulo si es la Agencia), `emitido_en`, `contenido_minimo` (texto). No se guardan datos personales del inquilino en el texto del incidente (R14).

**EJECUCION_PROCESO** — *RNF-16, DAS 10.1* (propuesta): `id`, `fecha_local`, `iniciada_en`, `terminada_en`, `resultado`, `detalle`. Sirve para saber qué días corrió el proceso y emitir solo la alerta del día actual (RF-22).

**AUDITORIA** — *RF-28, RNF-06*: `id`, `entidad`, `registro_id`, `actor` (el usuario o `sistema`), `tipo_actor` (`administrador` o `proceso`), `ejecucion_id` (nulo, salvo si lo hizo el proceso diario), `accion`, `ocurrido_en`, `campos_modificados` (lista de nombres de campo), `valor_anterior` y `valor_nuevo` (solo para campos **no personales**: estados, importes, fechas, motivos). Para campos personales (`nombre_completo`, `numero_documento`, `telefono`, `correo`, imagen de cédula) se registra únicamente **que cambiaron**, nunca su valor. No guarda secretos ni documentos completos. Así la auditoría no retiene datos personales que la desasociación debe eliminar (sección 6).

## 4. Claves y restricciones

| # | Restricción | Origen |
|---|---|---|
| R1 | `OBLIGACION`: único (`contrato_id`, `periodo_inicio`) para `regular`; a lo sumo una `apertura` por contrato. | RF-12, RN-04, RNF-04 |
| R2 | `CONTRATO`: dos contratos de una misma propiedad no comparten ningún día (`fecha_inicio` a `fecha_fin` inclusive; sin fin = abierto). **Se impone con una restricción de exclusión de PostgreSQL con `btree_gist` (ADR-031); no cuentan los contratos anulados (decisión del solicitante, 21-oct-2026).** | RF-08, RN-02 |
| R3 | `CONDICION_CONTRATO`: `monto_mensual` > 0; `dia_vencimiento` entre 1 y 31; `dias_gracia` ≥ 0; `vigente_desde` no puede preceder a `fecha_inicio`. | ERS 7.3 |
| R4 | `MOVIMIENTO`: exactamente uno de `obligacion_id` y `deposito_id`; `importe_aplicado` > 0; `tipo_cambio` obligatorio si `moneda_recibida` ≠ moneda destino; `anula_a` y `motivo` obligatorios si `tipo` = `reversion`. | RF-16, RF-38 |
| R5 | `MOVIMIENTO`: una `reversion` apunta a un único `abono` que no tenga ya otra reversión. | RN-22 |
| R6 | El saldo derivado nunca es negativo: se valida al insertar el movimiento, con la fila de la obligación o depósito bloqueada para evitar dos abonos simultáneos. | RN-18, RF-35 |
| R7 | `COMPROBANTE` (fase posterior): `numero` único y **sin huecos**; se toma de un contador en tabla, con bloqueo de fila, dentro de la misma transacción que el movimiento. **No usar una secuencia de base de datos**: deja huecos al revertir (H11). | RF-37 |
| R8 | `DEPOSITO`: uno por contrato; a lo sumo tres abonos válidos, salvo confirmación con motivo en `excepcion_motivo`. | RN-27 |
| R9 | `NOTIFICACION`: `clave_unica` única. | RF-21, RNF-16 |
| R10 | `INQUILINO`: único (`tipo_documento`, `numero_documento`) solo entre activos, como **advertencia**, no como restricción dura. | RF-01 |
| R11 | `DOCUMENTO_IDENTIDAD`: nunca una URL pública; el nombre del archivo almacenado es aleatorio. | RNF-14 |
| R12 | Las filas de `MOVIMIENTO`, `AJUSTE_OBLIGACION`, `COMPROBANTE`, `AUDITORIA` y `ACCESO_DOCUMENTO` no admiten `UPDATE` ni `DELETE` por la aplicación (salvo el estado del comprobante). **Se aplica con el rol de base de datos de la aplicación, que solo tiene `SELECT` e `INSERT` en esas tablas, más guardas en Django (ADR-027, decisión del 21-oct-2026).** `OBLIGACION.importe_inicial` tampoco se actualiza; `anulada_en` se completa una sola vez. | ERS 7.3, DAS 2, ADR-027 |
| R13 | `AJUSTE_OBLIGACION`: `importe_delta` ≠ 0; `motivo` obligatorio en `correccion` y `ajuste_manual`; el importe vigente resultante nunca queda por debajo de la suma de movimientos válidos, con la obligación bloqueada al insertar. | RF-10, RN-14 |
| R14 | `AUDITORIA` no almacena valores de campos personales ni secretos (ver su definición). | RF-28, RF-41, RNF-06 |
| R19 | `AUDITORIA`: si `tipo_actor` = `proceso`, `actor` = `sistema` y `ejecucion_id` es obligatorio; si es `administrador`, `ejecucion_id` es nulo. No existe una cuenta `sistema` en `ADMINISTRADOR` (RF-27). | RF-28, HT-06 |
| R15 | `MOVIMIENTO`: `clave_solicitud` única. Un reintento con la misma clave no crea otro movimiento; la aplicación devuelve el ya registrado. | H13 |
| R16 | `MOVIMIENTO`: `numero_recibo_fisico` único cuando no es nulo (índice único parcial o equivalente). | RF-47, CA-61 |
| R17 | `TOKEN_RESTABLECIMIENTO`: se acepta solo si `usado_en` es nulo y la hora actual es anterior a `expira_en`; al usarlo se completa `usado_en` en la misma transacción que fija la contraseña nueva, se invalidan los demás tokens pendientes y las sesiones abiertas, y se avisa a las dos direcciones. | RF-27, CA-59 |
| R18 | `TOKEN_RESTABLECIMIENTO`: a lo sumo 3 solicitudes (filas creadas) por hora para la cuenta; la solicitud siguiente se rechaza con la misma respuesta externa que una aceptada (sin revelar el estado). El límite numérico es propuesta del asistente. | RF-27, CA-59 |

## 5. Valores derivados (no se almacenan)

| Valor | Cálculo | Referencia |
|---|---|---|
| Movimientos válidos de una obligación | Abonos sin reversión que apunte a ellos | RN-22 |
| **Importe exigible vigente** | `importe_inicial` + suma de `importe_delta` de sus ajustes | RF-10, RF-35 |
| **Saldo de obligación** | importe exigible vigente − suma de `importe_aplicado` de movimientos válidos | RF-35, RN-18 |
| **Estado de obligación** | `anulada` si `anulada_en` no es nulo; si no, `pagada` si saldo = 0; si no, `vencida` si hoy (zona de la organización) > `fecha_limite`; si no, `pendiente` | RF-14, RN-07 |
| **Fecha de pago completo** | `fecha_real` del movimiento válido que dejó el saldo en cero | Q-6 |
| Saldo y estado de depósito | `importe_total` − abonos válidos; `pendiente` (sin abonos), `parcialmente pagado` o `completado` | RF-31 |
| Estado de contrato | `anulado`; `futuro` si hoy < `fecha_inicio`; `finalizado` si `fecha_fin` < hoy; `por decidir` si hubo fin vencido sin cierre ni renovación; si no, `vigente` | RN-30, RF-42 |
| Estado de propiedad | `inactiva` si está marcada; `ocupada` si tiene un contrato vigente; si no, `disponible` | RF-06 |
| Período y vencimiento | Calculados por el servicio de obligaciones con las reglas RN-03 y RN-05 | RN-03, RN-05 |

## 6. Retención y desasociación (Ley 8968)

Cuando vence el plazo de retención del último contrato del inquilino (RF-41):

| Entidad | Acción |
|---|---|
| `DOCUMENTO_IDENTIDAD` | Se elimina el archivo del almacenamiento privado; la fila conserva `eliminado_en`. |
| `INQUILINO` | `nombre_completo`, `numero_documento`, `telefono` y `correo` se anulan; `desasociado_en` se completa. La fila y su `id` permanecen. |
| `CONSENTIMIENTO`, `SOLICITUD_TITULAR` | Se evalúa con asesoría legal (pueden requerirse como evidencia de cumplimiento). **Pendiente** (DP-18). |
| `CONTRATO`, `OBLIGACION`, `MOVIMIENTO`, `COMPROBANTE` (fase posterior) | Se conservan sin datos de identificación; el comprobante impreso se regenera sin nombre. El `numero_recibo_fisico` se conserva con el movimiento. **Pendiente** de confirmar con DP-18 y DP-20. |
| `ORGANIZACION.correo_aviso_secundario` | Dirección del propio solicitante; se conserva mientras esté configurada. |
| `AUDITORIA` | No contiene valores personales (R14), por lo que no requiere depuración. Las filas anteriores a una regla de este tipo no existen: se aplica desde el inicio. |
| Respaldos | 35 días de retención; la foto eliminada desaparece de ellos en ese plazo (DP-07). |

## 7. Transacciones críticas

| Operación | Debe ocurrir en una sola transacción |
|---|---|
| Registrar abono | Bloquear la obligación o depósito → validar saldo y fecha → insertar `MOVIMIENTO` (con `numero_recibo_fisico` si se anotó, R16) → insertar `AUDITORIA`. En la fase posterior del comprobante, también asignar `COMPROBANTE` antes de la auditoría |
| Anular movimiento | Insertar la `reversion` → insertar `AUDITORIA`; en la fase posterior, marcar el comprobante como `anulado` |
| Restablecer contraseña | Validar `TOKEN_RESTABLECIMIENTO` (R17) → fijar la contraseña nueva → completar `usado_en` → insertar `NOTIFICACION` de seguridad para las dos direcciones → `AUDITORIA` |
| Evento de seguridad de la cuenta | Aplicar el evento (por ejemplo, usar un código de recuperación) → insertar la `NOTIFICACION` de seguridad en la misma transacción (ADR-026) → `AUDITORIA`; el envío ocurre después y no bloquea el evento |
| Reajuste o corrección | Insertar `CONDICION_CONTRATO` → insertar un `AJUSTE_OBLIGACION` por obligación afectada → validar que ninguna quede bajo lo abonado (si alguna lo hace, se revierte todo) → `AUDITORIA` |
| Generar obligación | Comprobar R1 → insertar `OBLIGACION` (idempotente) |
| Finalizar contrato | Actualizar `fecha_fin` → `AJUSTE_OBLIGACION` de tipo `prorrateo_fin` en el último período → anular las posteriores sin movimientos → `AUDITORIA` |

## 8. Trazabilidad

| Entidad | Requisitos |
|---|---|
| ORGANIZACION, ADMINISTRADOR, CODIGO_RECUPERACION, TOKEN_RESTABLECIMIENTO | RF-26, RF-27, RF-33, RN-25 |
| INQUILINO, DOCUMENTO_IDENTIDAD, ACCESO_DOCUMENTO | RF-01 a RF-05, RF-45 |
| CONSENTIMIENTO, SOLICITUD_TITULAR | RF-39, RF-40, RF-41 |
| PROPIEDAD, CONTRATO, CONDICION_CONTRATO | RF-06 a RF-10, RF-36, RF-42 |
| OBLIGACION, AJUSTE_OBLIGACION | RF-09 a RF-15, RF-43 |
| MOVIMIENTO, COMPROBANTE (fase posterior) | RF-13, RF-16, RF-34, RF-35, RF-37, RF-38, RF-47 |
| DEPOSITO | RF-29 a RF-32 |
| NOTIFICACION, EJECUCION_PROCESO | RF-21 a RF-25, RF-27, RF-42, RF-44 |
| INCIDENTE_SEGURIDAD, AVISO_INCIDENTE | RF-46 |
| AUDITORIA | RF-28 |

## 9. Problemas y decisiones que surgieron al modelar

| # | Hallazgo | Propuesta |
|---|---|---|
| H1 | **Contradicción de glosario.** El glosario de la ERS (sección 1.3) y el del borrador del DAS definen el saldo de apertura como un tipo de *movimiento*, pero la ERS 7.1 y el criterio CA-49 lo tratan como una *obligación* de tipo apertura. | Tratarlo como obligación `apertura` (como CA-49), y corregir ambos glosarios. **Incorporado en la ERS v1.7 y el DAS v0.6.** |
| H2 | La ERS no tiene entidad para el **historial de condiciones** (monto, vencimiento, gracia, reajuste), aunque RF-10 lo exige. | Entidad `CONDICION_CONTRATO` (sección 3.3). Añadirla a la sección 7.1 de la ERS. **Incorporado en la ERS v1.7.** |
| H3 | La ERS no menciona la **organización** como entidad, pero guarda configuración (zona, hora, anticipaciones, teléfono, retención). | Entidad `ORGANIZACION` de una sola fila. Añadirla a la ERS. **Incorporado en la ERS v1.7.** |
| H4 | **Numeración de comprobantes:** ¿una serie global o una por año? La ERS solo pide "consecutiva" (RF-37). | Serie global. **Decisión provisional del solicitante (17-oct-2026)**, sujeta a DP-20; un abogado o contador puede exigir otra cosa. |
| H5 | El `importe_aplicado` de un pago en otra moneda requiere una **regla de redondeo** del equivalente. | Redondear a 2 decimales (USD) o a la unidad entera (CRC) con empate hacia arriba, igual que RN-12. **Propuesta**; confirmar. Probado en PostgreSQL (sección 12); sigue pendiente de confirmar por el solicitante. |
| H6 | La restricción de **no solapamiento de contratos** (R2) depende del motor elegido. | Decidir con ADR-002; PostgreSQL lo impone con una restricción de exclusión (sección 1.2). Mientras tanto se valida en la aplicación. |
| H7 | **Identificadores:** ¿UUID o secuencia? Los comprobantes ya necesitan secuencia propia. | **Resuelta el 21-oct-2026 (ADR-028):** entero de 64 bits autoincremental para todas las entidades; UUID solo en `clave_solicitud` y nombres de archivo. El número de comprobante (fase posterior) sigue con su contador en tabla, no con la secuencia del identificador (R7, H11). |
| H8 | Qué ocurre con `CONSENTIMIENTO` y `SOLICITUD_TITULAR` al desasociar (¿evidencia legal?). | DP-18; pendiente de abogado. **Abierta** (DP-18). |
| H9 | **Importe modificable (v0.1).** Las correcciones sobrescribían `importe_exigible` y el valor anterior solo quedaba en la auditoría. Decisión del solicitante: registrar los ajustes como filas nuevas. | Entidad `AJUSTE_OBLIGACION`; importe vigente derivado. **Incorporado en la ERS v1.7 (7.1 y RF-10) y el DAS v0.6 (ADR-016).** |
| H10 | **RF-28 vs Ley 8968.** RF-28 exige guardar "valores anteriores y nuevos"; si incluyen nombre, documento o teléfono, la auditoría retendría datos que RF-41 manda desasociar. | Auditar valores solo de campos no personales y, para los personales, solo que cambiaron (R14). **Requiere ajustar la redacción de RF-28 en la ERS v1.7** (incorporado); validar con abogado (DP-18). |
| H11 | **Huecos en la numeración.** La prueba mostró que una secuencia de PostgreSQL entrega números que se pierden si la transacción falla (el comprobante real era el 2 y la secuencia ya iba en 4); la documentación lo confirma. RF-37 exige consecutivos. | Contador en tabla con bloqueo de fila (R7). Revisar el texto de ADR-010 en el DAS v0.6. |
| H12 | **UTC y eventos futuros.** `NOTIFICACION.programada_para` es un instante UTC calculado de antemano a partir de la hora local 07:00; si cambiaran las reglas de la zona, quedaría desfasado (W3C). Costa Rica no tiene horario de verano, pero la regla puede cambiar. | **Resuelta (DP-26, 17-oct-2026):** guardar fecha y hora locales; el instante se calcula al ejecutar. |
| H13 | **Registro duplicado de abonos.** El modelo no protegía contra el mismo abono enviado dos veces (doble clic o reintento de red): R6 solo evita el sobrepago. | **Aceptada por el solicitante (17-oct-2026).** `clave_solicitud` única en `MOVIMIENTO` (R15), según el patrón de Stripe. Probada en PostgreSQL. |
| H14 | **Avisos de seguridad y restablecimiento de contraseña sin entidad (v0.4).** El modelo no tenía dónde guardar el aviso de un evento de la cuenta (sin obligación asociada), la segunda dirección ni el enlace de restablecimiento. | Propuesta del asistente derivada de ERS v1.9 y ADR-026: tipo `aviso_seguridad` con `evento_seguridad` y `destinatario_tipo` en `NOTIFICACION`; `proximo_intento_en` para el reintentador; entidad `TOKEN_RESTABLECIMIENTO` con hash, vencimiento y un solo uso (R17); `correo_admin` y `correo_aviso_secundario` en `ORGANIZACION`. **No decidida por el solicitante.** |

## 10. Decisiones de diseño que requieren ADR (propuestas)

Incorporadas al DAS v0.6 con los números indicados.

| Propuesta | Decisión | Alternativa descartada |
|---|---|---|
| ADR-014 | Historial de condiciones como entidad `CONDICION_CONTRATO` | Guardar monto, vencimiento y gracia en el contrato |
| ADR-015 | Saldo de apertura como obligación de tipo `apertura` (H1) | Tratarlo como movimiento |
| ADR-016 | Ajustes de importe como filas inmutables (H9) | Sobrescribir el importe y auditar |
| ADR-017 | Auditoría sin valores personales (H10) | Auditar todos los valores |
| ADR-018 | Comprobantes en serie global (H4, con DP-20) | Serie por año |
| ADR-019 | Hash de contraseñas con Argon2id | bcrypt, scrypt o PBKDF2 |
| ADR-020 | Clave de solicitud única en cada movimiento (H13) | Sin protección contra envíos repetidos |

## 11. Qué no cubre este borrador

- Índices concretos adicionales, particiones, orden de las migraciones y nombres de tablas. Los tipos físicos principales y la restricción de solape de contratos constan en la sección 13 y en el ADR-031 del DAS.
- Contratos de API (siguiente producto de la fase 3), permisos por operación y flujos detallados.
- Datos de prueba.
- Revisión por otra persona. La prueba en PostgreSQL (sección 12) es autoverificación mía, no revisión de pares.

## 12. Prueba en PostgreSQL (autoverificación, 17-oct-2026)

Se montó una base desechable en un servidor PostgreSQL 18.4 aparte (puerto 54329, sin tocar el servicio instalado) y se probó el modelo con un script de **32 comprobaciones: 32 correctas**. El script y su salida están en la carpeta de evidencia de la actualización [2026-10-17c](../actualizaciones/2026-10-17c_ERS-v1.7_DAS-v0.6/CAMBIOS.md). Esto **no fija ADR-002**: solo muestra que las restricciones son expresables y se cumplen.

| Probado | Resultado |
|---|---|
| R1 (período duplicado, segunda apertura), R15 (envío repetido), R2 (solape de un día, contrato abierto, contiguo válido), R3 (monto cero, día 32), R4, R5, R6 (sobrepago), R7 (consecutivos, un comprobante por movimiento), R12 (UPDATE y DELETE bloqueados), R13 | Cumplen |
| Derivaciones: saldo, estado vencida, saldo tras anulación, importe vigente tras corrección | Correctas |
| Prorrateo RN-12 (300 000 × 11 / 31 = 106 452) y empates de redondeo H5 (1,005 → 1,01; 0,5 → 1) | Correctos en PostgreSQL |
| H11: huecos de la secuencia | Confirmado; el contador en tabla no los tiene |

**No probado:** R3 `vigente_desde` ≥ `fecha_inicio` (requiere otra tabla), R8 (tope de abonos de depósito), R9 a R11, R14, concurrencia real (dos abonos simultáneos), carga con 50 propiedades y el tiempo de respuesta de RNF-08.
**Fuente:** [PostgreSQL, funciones de secuencia](https://www.postgresql.org/docs/current/functions-sequence.html), leída por resumen: las secuencias "cannot be used to obtain gapless sequences".

## 13. Tipos físicos decididos (21-oct-2026, ADR-031)

| Dato | Tipo físico en PostgreSQL (por confirmar con `sqlmigrate`) | Notas |
|---|---|---|
| Identificadores | `bigint` autoincremental (`BigAutoField`) | ADR-028 |
| Importes (`importe_inicial`, `importe_delta`, `importe_aplicado`, `importe_recibido`, depósito) | `numeric(14,2)` | Tamaño propuesto por el asistente; colones redondeados a unidad entera por el servicio |
| `tipo_cambio` | `numeric(12,4)` | Propuesta; ingresado a mano (RF-38) |
| Moneda | texto de 3 letras con `CHECK` (`CRC` o `USD`) | RF-33 |
| Fechas de calendario (vencimiento, período, fecha real, inicio y fin de contrato) | `date` | Sin hora ni zona |
| Instantes (`registrado_en`, `ocurrido_en`, `creado_en`, `expira_en`) | `timestamp with time zone`, guardado en UTC (`USE_TZ = True`) | W3C; ver sección 1.2 |
| Solape de contratos (R2) | Restricción de exclusión con `btree_gist` sobre propiedad y rango de fechas `[inicio, fin]`, sin límite superior si el contrato es abierto | Los contratos anulados no cuentan (decisión del solicitante, 21-oct-2026; ADR-031) |