# Actualización 2026-10-17 (c) — ERS v1.7 y DAS v0.6

> Nota: el texto dice "pendiente de la v1.7" en secciones escritas antes de crearla; ya está incorporado, salvo H4 y H12 (DP-20, DP-26).

**Estado:** cerrada el 17-oct-2026. Las decisiones registradas aquí pasaron a la [ERS v1.7](../../fase-1-ers/ERS_SGA_001_v1.7_borrador.md) y al [DAS v0.6](../../fase-2-arquitectura/DAS_SGA_001_v0.6_borrador.md). Ambas siguen siendo borradores, sin aprobación del negocio ni validación legal. Este registro se escribió por orden cronológico; las secciones "Decisiones registradas" conservan el texto original.

**Versiones de partida:** [ERS v1.6](../../fase-1-ers/ERS_SGA_001_v1.6_borrador.md) · [DAS v0.5](../../fase-2-arquitectura/DAS_SGA_001_v0.5_borrador.md) (se conservan sin cambios)

## Decisiones registradas

### DP-04 — Proveedor de WhatsApp: diferido, con dependencia externa

**Respuesta del solicitante:** se planea crear una aplicación propia que conecte con WhatsApp de forma gratuita. Es otro proyecto, y por eso la decisión estaba diferida.

**Comparativo oficial investigado (17-oct-2026):**

| Opción | Costo mensual aproximado (100 mensajes) | Nota |
|---|---|---|
| Cloud API directo de Meta | ~$1,1 (solo tarifas de Meta) | Sin intermediario; requiere webhook público |
| Twilio | ~$1,6 ($0,005 por mensaje más Meta) | Alta guiada |
| 360dialog | €49 fijos más Meta | Solo con mucho volumen |

La tarifa de Meta para "Rest of Latin America" (Costa Rica) es de **$0,0113 a $0,013 según blogs de terceros, no oficial**: la página oficial de tarifas devolvió 404. Fuentes: [Meta, precios](https://developers.facebook.com/docs/whatsapp/pricing), [Twilio](https://www.twilio.com/en-us/whatsapp/pricing), [360dialog](https://360dialog.com/pricing), [Meta, primeros pasos](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started).

**Riesgo anotado, sin conclusión legal:** los términos de servicio de WhatsApp consultados (vigentes desde el 4-ene-2021, página de consumidores) prohíben "bulk messaging, auto-messaging, auto-dialing", el "uso no personal" no autorizado y el acceso no autorizado. No leí los términos de la WhatsApp Business Platform. Si el proyecto aparte usara medios no oficiales, esos términos podrían impedirlo o exponer la cuenta a un bloqueo. Un abogado debe revisar el proyecto aparte antes de depender de él.

**Efecto en el SGA (propuesto):**
- El SGA no depende de un proveedor concreto: define una **interfaz de canal de salida** (destinatario, contenido, clave de idempotencia) y recibe estados *aceptado*, *entregado* y *fallido*.
- DP-04 sigue abierta, ahora **ligada a ese proyecto externo**. Mientras no exista, el canal web basta para operar (RNF-05).
- Para saber si un mensaje se entregó, cualquier solución necesita un punto de recepción de estados; eso se decide con DP-08.

**Incorporado:** DP-04 actualizada en la ERS v1.7 (sección 12.1) y el DAS v0.6 (ADR-008).

### DP-07 — Respaldo y recuperación: resuelta

| Parámetro | Decisión del solicitante (17-oct-2026) |
|---|---|
| RPO (pérdida tolerable de datos) | Hasta 24 horas |
| RTO (tiempo tolerable sin sistema) | Hasta 24 horas |
| Frecuencia | Un respaldo completo al día (consecuencia del RPO) |
| Retención de respaldos | 35 días |
| Prueba de restauración | Antes de producción y cada 3 meses (base de datos, archivos, contratos, movimientos, comprobantes y fotos) |

**Origen de los valores:** todos son de diseño, a partir de las opciones que presenté; no los respalda una fuente externa. Se eligieron las opciones recomendadas por proporción con un administrador y unos 100 movimientos al mes.

**Pendiente de otras decisiones:**
- Los respaldos contienen fotos de cédula. La retención de 35 días permite que una foto eliminada a los 5 años desaparezca de todos los respaldos en ese plazo, pero la conciliación con obligaciones contables o tributarias de conservación sigue en **DP-18**.
- El cifrado de los respaldos y la copia independiente (en otro lugar) los define el hosting (**DP-08**).

**Efecto en documentos:** RNF-09 (ERS) pasa de "se definen antes de producción" a estos valores; DAS sección 11 se completa; fase 6 recibe el procedimiento de restauración.

### Modelo de datos (fase 3) — borrador iniciado

Se creó [MODELO_DATOS_SGA_001_v0.1_borrador.md](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.1_borrador.md). Al modelar surgieron cambios que deben pasar a la ERS v1.7 y al DAS v0.6:

| # | Cambio necesario en los documentos |
|---|---|
| H1 | Corregir los glosarios (ERS 1.3 y DAS): el saldo de apertura es una **obligación** de tipo apertura, no un movimiento. |
| H2 | Añadir a la ERS 7.1 la entidad que guarda el historial de condiciones del contrato (monto, vencimiento, gracia, reajuste, tope y fuente). |
| H3 | Añadir a la ERS 7.1 la entidad de configuración de la organización. |
| H4 | Decisión pendiente: numeración de comprobantes en serie global o por año (DP-20). |

### DP-08 — Exposición pública y hosting: resuelta, con una decisión contra la recomendación

| Aspecto | Decisión del solicitante (17-oct-2026) |
|---|---|
| Acceso | Desde cualquier lugar, por internet (HTTPS, contraseña larga, segundo factor) |
| Tipo de alojamiento | **Servidor virtual (VPS) administrado por el propio solicitante** |

**Historia de la decisión.** Primero recomendé la nube gestionada sin comparar costos. El solicitante eligió el VPS, luego dijo que se había equivocado, pidió una explicación con costos y argumentó que para aprendizaje es mejor. Con los costos verificados, corregí mi recomendación: la nube gestionada con base de datos administrada empieza en **$38 al mes** (Fly.io Postgres) y las opciones gratuitas no sirven (servicio que se apaga a los 15 minutos y base que caduca a los 30 días en Render), lo que choca con RE-01 y RE-02. **Decisión final del solicitante: VPS administrado por él, con datos reales de inquilinos desde el inicio.** Proveedor y región siguen sin elegir.

**Costos verificados (17-oct-2026, páginas oficiales leídas por resumen):**

| Opción | Costo mensual |
|---|---|
| VPS DigitalOcean 1 GB / 2 GB | $6 / $12, más 30 % por respaldo diario del proveedor |
| Estimación propia con 2 GB y respaldo diario | ~$15,60 |
| Fly.io, máquina de 1 GB | $6,70; Postgres gestionado desde $38 |
| Render gratuito | No viable: servicio que se apaga y base de datos que caduca a los 30 días |
| Hetzner | Precios no verificados (no cargaron) |

Fuentes: [DigitalOcean](https://www.digitalocean.com/pricing/droplets), [Fly.io](https://docs.fly.io/about/pricing), [Render](https://render.com/docs/free), [Hetzner](https://www.hetzner.com/cloud/regular-performance/).

**Riesgo asumido por el solicitante.** Las cédulas de inquilinos reales estarán en un servidor que el solicitante está aprendiendo a proteger. Mantengo como **recomendación fuerte, no como bloqueo**, estas condiciones antes de cargar datos reales: endurecimiento del servidor hecho, prueba de restauración superada y revisión legal cerrada (DP-17 a DP-19). Se registran en la fase 6 como condiciones de salida propuestas. Los respaldos del proveedor pueden no cubrir los 35 días de retención (no verificado), por lo que habrá que programar copias propias a otro lugar.

**Consecuencias que deben quedar como requisitos de operación (fase 6), propuestas por mí y sin fuente externa todavía:**
- Quien administra el VPS asume actualizaciones del sistema, firewall, renovación de HTTPS, monitoreo, y que el respaldo diario salga a **otro lugar** (copia independiente), cifrado.
- Con datos de cédulas y acceso desde internet, el endurecimiento del servidor pasa a ser un riesgo propio del proyecto. Falta investigar guías reconocidas de endurecimiento (por ejemplo, CIS Benchmarks, OWASP) y documentarlas en la fase 6; **esa investigación no está hecha**.
- Si el proyecto aparte de WhatsApp necesita un punto público para estados de entrega (DP-04), se resolverá junto con la configuración de red del VPS.
- Si el VPS está fuera de Costa Rica, aplica la revisión legal de transferencia de datos (DP-19).

**Efecto en documentos:** DP-08 sale de pendientes en la ERS y el DAS; el DAS (sección 11 y 12) añade el riesgo de operar el servidor y los controles; la fase 6 recibe la lista de tareas operativas.

### Verificación de buenas prácticas de la fase 3 y modelo de datos v0.2

**Origen:** el solicitante pidió verificar si la fase 3 cumple buenas prácticas. Se encontraron 4 fallos de fondo y 4 de proceso. Con "procede con las dos recomendaciones" el solicitante decidió los fallos 1 y 2.

| # | Hallazgo | Decisión | Dónde queda |
|---|---|---|---|
| 1 | `importe_exigible` se sobrescribía en correcciones | Los ajustes son filas nuevas e inmutables (decisión del solicitante) | [Modelo v0.2](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.2_borrador.md): `AJUSTE_OBLIGACION`, R12, R13, H9 |
| 2 | La auditoría podía retener datos personales (choque RF-28 / RF-41) | Auditar valores solo de campos no personales; de los personales, solo que cambiaron (decisión del solicitante, afinada por mí; **RF-28 pide "valores anteriores y nuevos", así que su redacción debe cambiar en la ERS v1.7**) | Modelo v0.2: AUDITORIA, R14, H10 |
| 3 | Algoritmo de contraseñas sin definir | Propuesta mía: Argon2id con mínimos OWASP | Modelo v0.2: ADMINISTRADOR, sección 1.2 |
| 4 | Decisiones sin ADR | Seis ADR propuestos, sin número hasta el DAS v0.6 | Modelo v0.2, sección 10 |

Hallazgos de proceso corregidos: cuadro de control de versiones en el modelo, tabla de fuentes (Fowler, PostgreSQL, OWASP; leídas por resumen), `verificar_coherencia.ps1` ahora comprueba también las citas del modelo, y `DOC/README.md` y `CLAUDE.md` actualizados (incluida la skill y la existencia del repositorio Git).

**Límites:** la v0.2 no fue revisada por otra persona ni probada contra una base de datos. Dinero decimal, UTC e idempotencia siguen sin fuente verificada. La retención de la auditoría y de consentimientos sigue pendiente del abogado (DP-18).

**Pendiente para la ERS v1.7 / DAS v0.6:** H1, H2, H3, H9, H10 (redacción de RF-28) y los ADR propuestos.

### Seguimiento 1 — Prueba del modelo v0.2 en PostgreSQL

**Origen:** pendiente "la v0.2 no se probó contra una base de datos". El solicitante eligió la prueba desechable en PostgreSQL local.

- Servidor aparte en el puerto 54329, creado y borrado al terminar; no se tocó el servicio PostgreSQL instalado. Evidencia: [script](evidencia/prueba_modelo_v0.2_postgres.sql) y [salida](evidencia/resultado_prueba.txt) (30 de 30 correctas tras corregir dos errores de la propia prueba, no del modelo).
- **Hallazgo H11:** una secuencia de base de datos deja huecos, y RF-37 exige comprobantes consecutivos. R7 pasa a contador en tabla con bloqueo. Revisar ADR-010 en el DAS v0.6.
- **Sigue pendiente:** revisión por otra persona (no se hizo; esto es autoverificación), concurrencia real, R8 a R11 y R14, y carga con 50 propiedades.

### Seguimiento 2 — Fuentes de dinero decimal, UTC e idempotencia

Se leyeron por resumen (17-oct-2026) Python `decimal`, PostgreSQL `numeric`, W3C *Working with Time Zones* y Stripe *Idempotent requests*; quedan en la tabla de fuentes del [modelo v0.2](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.2_borrador.md) (sección 1.2).

- Dinero decimal: respaldado.
- UTC: respaldado con salvedad (**H12**): no basta para eventos futuros en hora local.
- Idempotencia: la fuente respalda claves por petición, no la clave natural permanente de las notificaciones. Falta protección contra abonos duplicados (**H13**, propuesta).
- H12 y H13 son propuestas mías, sin decisión del solicitante. Pasan a la ERS/DAS solo si se aceptan.

### Seguimiento 3 — H13 aceptada

**Decisión del solicitante (17-oct-2026):** acepta H13. `MOVIMIENTO` incorpora `clave_solicitud` única (R15) para que un envío repetido no duplique el abono. Probada en PostgreSQL (32 de 32 comprobaciones, [salida](evidencia/resultado_prueba.txt)); no se probó concurrencia real. Debe pasar a la ERS v1.7 (requisito de idempotencia al registrar movimientos) y al DAS v0.6. H12 sigue como propuesta sin decidir.

## Resumen de la actualización (cierre)

**Documentos creados:** [ERS v1.7](../../fase-1-ers/ERS_SGA_001_v1.7_borrador.md), [DAS v0.6](../../fase-2-arquitectura/DAS_SGA_001_v0.6_borrador.md) y [modelo de datos v0.2](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.2_borrador.md). Las versiones anteriores se conservan sin cambios.

| Cambio en la ERS v1.7 | Origen |
|---|---|
| DP-07 y DP-08 resueltas; RNF-09 con RPO/RTO de 24 h y retención de 35 días; DP-04 diferida; riesgos actualizados | Respuestas del solicitante, 17-oct-2026 |
| Glosario: el saldo de apertura es obligación; nuevo término Ajuste de obligación (H1) | Modelo de datos |
| Entidades Condición del contrato, Ajuste de obligación y Organización; Obligación con importe inicial (H2, H3, H9) | Modelo de datos; decisión del solicitante sobre H9 |
| RF-10 (no sobrescribir), RF-28 (auditoría sin valores personales, H10), RF-34 (clave de solicitud, H13), RF-37 (sin huecos, H11) | Modelo de datos; prueba en PostgreSQL; decisiones del solicitante |
| Restricciones de integridad 13 a 15; CA-52 a CA-55 y matriz; DP-26 (H12) | Modelo de datos |

| Cambio en el DAS v0.6 | Origen |
|---|---|
| Sección 1.1 Restricciones (RE-01 a RE-11), sección 4.1 Árbol de calidad, anexo B Glosario | Evaluación de la metodología; respuestas del solicitante |
| Sección 11 con los valores de respaldo y condiciones del VPS; ADR-002, 007, 008, 010 y 013 actualizados | DP-07, DP-08, DP-04, H11 |
| ADR-014 a ADR-020 nuevos | Modelo de datos v0.2 |

**Verificación:** `verificar_coherencia.ps1` sin problemas (RNF 17, RF 45, RN 30, CA 55, OL 18, DP 26, ADR 20; sin enlaces rotos). No comprueba lógica ni contenido. No hubo revisión por otra persona.

**Sin resolver:** DP-01, DP-14, DP-17 a DP-21, DP-23, DP-26; H4 (numeración global o por año, con DP-20); H12; guías de endurecimiento del servidor sin investigar; términos de la plataforma empresarial de WhatsApp sin leer; reglas de IDs de nuevos prefijos (RE) fuera del script.

## Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | El solicitante (nombre por registrar) | Pendiente | Pendiente |
