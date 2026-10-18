# Actualización 2026-10-17 (d) — ERS v1.8 y DAS v0.7

**Estado:** cerrada el 17-oct-2026. Las decisiones pasaron a la [ERS v1.8](../../fase-1-ers/ERS_SGA_001_v1.8_borrador.md), el [DAS v0.7](../../fase-2-arquitectura/DAS_SGA_001_v0.7_borrador.md) y el [modelo de datos v0.3](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.3_borrador.md). Siguen siendo borradores, sin aprobación ni validación legal.

**Origen:** el solicitante pidió resolver, una por una y según buenas prácticas, las decisiones pendientes que dejó la actualización [2026-10-17c](../2026-10-17c_ERS-v1.7_DAS-v0.6/CAMBIOS.md).

## Decisiones registradas

### DP-26 (H12) — Hora local de las notificaciones: resuelta

**Pregunta:** ¿se guarda la hora programada como un instante UTC calculado de antemano, o como fecha y hora locales con la zona?
**Respuesta del solicitante (17-oct-2026):** hora local más zona, y calcular el instante al ejecutar (la opción recomendada).
**Fundamento:** [W3C, Working with Time Zones](https://www.w3.org/TR/timezone/), leída por resumen el 17-oct-2026: UTC es lo recomendable "when in doubt", pero un evento futuro en hora local depende de reglas de zona que pueden cambiar. Costa Rica no usa horario de verano, por lo que el riesgo actual es bajo; la limitación es que no se verificaron las reglas vigentes de la zona.
**Efecto en documentos:** modelo v0.3 (`NOTIFICACION` guarda fecha local, hora local y zona), ADR-013, RNF-12 y DP-26 resuelta en la ERS v1.8 y el DAS v0.7.

### H4 — Numeración de comprobantes: serie global (provisional)

**Pregunta:** ¿una serie continua o una por año?
**Respuesta del solicitante (17-oct-2026):** serie global continua (la opción recomendada).
**Fundamento y límites:** la Ley 7527, art. 58 (copia leída), exige acreditar el pago pero no fija formato de numeración. No se leyeron normas tributarias de comprobantes; si el comprobante debiera cumplir reglas de facturación, el formato puede cambiar. **La decisión es provisional hasta que el abogado o contador responda DP-20.**
**Efecto en documentos:** ADR-018 pasa de "propuesto" a "decisión del solicitante, provisional (DP-20)"; no cambia el modelo (R7 ya asume serie global).

### DP-23 — Responsables del documento: resuelta

**Pregunta:** ¿quién ocupa los roles de propietario del producto, responsable de requisitos y responsable técnico, y con qué nombre se registran?
**Respuesta del solicitante (17-oct-2026):** una sola persona ocupa los tres roles; se registra con el identificador **brandonC-developer** (usuario de Git del proyecto, no necesariamente su nombre legal).
**Consecuencias registradas:**
- La aprobación no tiene revisión independiente: quien redacta, revisa y aprueba es la misma persona. ISO/IEC/IEEE 29148 (leída solo por catálogo) recomienda revisión por partes interesadas; este límite debe quedar visible en el registro de aprobación.
- El **asesor legal** sigue sin designar; es una persona distinta y es necesaria para DP-17 a DP-21.
- Esta respuesta no equivale a la aprobación del documento.
**Efecto en documentos:** control del documento y registro de aprobación de la ERS y el DAS; DP-23 pasa a resuelta, con el asesor legal pendiente de designar.

### DP-14 — Pregunta P11: cerrada como no recuperable

**Pregunta:** ¿se recuperó el enunciado y la respuesta de P11?
**Respuesta del solicitante (17-oct-2026):** no se recuperó; se retira.
**Tratamiento:** P11 se cierra como "sin enunciado recuperable". No se inventa su contenido. Si reaparece, se reabre como pregunta nueva con ID nuevo (no se reutiliza DP-14). Ningún requisito dependía de ella.
**Efecto en documentos:** DP-14 pasa a resuelta en la ERS y el DAS; el Anexo A de la ERS cambia la fila P11 a "Cerrada: sin enunciado recuperable"; CLAUDE.md regla 9 debe actualizarse (ya no está pendiente).

### Bloque legal (DP-01, DP-17 a DP-21) — verificación de fuentes oficiales

**Pedido del solicitante (17-oct-2026):** antes de enviar nada al abogado, verificar las leyes en fuente oficial. **Esto no resuelve ninguna de las decisiones: siguen abiertas y requieren un abogado.** Solo mejora el texto que se le entregará.

| Fuente | Resultado | Nivel de validación |
|---|---|---|
| SCIJ / SINALEVI, Ley 7527 y Ley 8968 (`sinalevi.go.cr`) | **No se pudo leer.** La página es un visor dinámico que no entrega el articulado; el sitio antiguo (`pgrweb.go.cr`) redirige a él. | No leída |
| [Archivo Nacional, texto de la Ley 8968](https://www.archivonacional.go.cr/web/normativa/ley8968.docx) | Leída completa (documento .docx descargado y extraído). Coincide con la copia de SUTEL en los artículos 2, 5, 6 y 7 (cinco días hábiles; diez años). Organismo estatal, pero es una copia, no el SCIJ. | Leída completa; copia de organismo estatal |
| [Archivo Nacional, Reglamento 37554-JP](https://www.archivonacional.go.cr/web/normativa/reglamento37554.docx) | **Leído por primera vez.** Incluye reformas del decreto 40008 de 2016. Hay que confirmar con el SCIJ que no existan reformas posteriores. | Leído parcialmente (arts. 3, 32, 34 a 39, 44) |
| Ley 7527 | Solo la copia de unpcr.com ya leída; Justia y un bufete la publican, sin cotejar. | Sin cambio |
| [delfino.cr, expediente 25465](https://delfino.cr/asamblea/proyecto/25465) | Proyecto para **derogar el último párrafo del art. 67** (reajuste), presentado el 25-mar-2026, en la Comisión de Asuntos Jurídicos. Medio periodístico, no la Asamblea; el texto del párrafo no aparece. | Leído por resumen; sin confirmar en fuente oficial |

**Hallazgos que cambian el trabajo:**

1. **Reglamento, art. 38 y 39 (leídos):** ante una vulnerabilidad de seguridad el responsable debe informar a los titulares afectados dentro de **cinco días hábiles** y a la Agencia (Prodhab), con la naturaleza del incidente, los datos comprometidos, las acciones inmediatas y dónde obtener más información. **La ERS v1.7 no tiene este requisito.** Pesa más porque el servidor lo administra el solicitante (DP-08).
2. **Reglamento, art. 32 y 36 (leídos):** protocolos mínimos de actuación y documentación de seguridad (descripción de datos, inventario de infraestructura, análisis de riesgos, riesgo residual, plan de trabajo); art. 37: revisión anual si hay datos sensibles. **La ERS no los recoge.**
3. **Reglamento, art. 44 (leído):** hay que inscribir las bases de datos ante la Agencia, pero "no serán sujetas de inscripción… las bases de datos personales, internas o domésticas". Si la base del SGA es "interna" (art. 2 de la ley: fines exclusivamente internos, personales o domésticos y no comercializada) es **una pregunta para el abogado (DP-19)**, no una conclusión mía.
4. **Expediente 25465:** si prospera, cambiaría el reajuste de vivienda (RF-10, OL-06, OL-07). No afecta hoy; conviene vigilarlo.
5. El expediente **25288** que citaba el resumen para el abogado es **otro** proyecto (retención de depósitos). No se reconfirmó su contenido.

**Límites:** son mis lecturas de copias, no asesoría legal; no se leyó normativa tributaria ni contable; no se confirmó la vigencia en el SCIJ.

## Resumen de la actualización (cierre)

| Decisión | Resultado | Dónde queda |
|---|---|---|
| DP-26 / H12 | Resuelta: hora local más zona | ERS RNF-12; DAS ADR-013; modelo v0.3 |
| H4 | Serie global, **provisional** hasta DP-20 | DAS ADR-018; ERS DP-20 |
| DP-23 | Resuelta: una persona, tres roles, brandonC-developer; asesor legal sin designar | ERS control del documento y registro de aprobación |
| DP-14 | Cerrada: P11 sin enunciado recuperable | ERS 12.2 y Anexo A |
| Bloque legal | **No resuelto** (requiere abogado). Se verificaron fuentes y se leyó parte del Reglamento 37554-JP | ERS OL-19 a OL-21, RF-46, RNF-18, CA-56, CA-57; DAS ADR-021; [resumen para el abogado v2](../../legal/RESUMEN_PARA_ABOGADO_SGA_v2.md) |

**Pendientes que siguen abiertos:** DP-01, DP-17 a DP-21 (abogado), designación del asesor legal, DP-18 (contador), confirmar la vigencia de las leyes en el SCIJ (la página oficial no entrega el texto), expediente 25465 sobre el art. 67 (vigilar), leer el resto del reglamento, guías de endurecimiento del servidor, términos de la plataforma empresarial de WhatsApp, revisión por otra persona. La skill y CLAUDE.md deben actualizarse (regla 9: P11 ya no está pendiente).

**Verificación:** `verificar_coherencia.ps1` sin problemas (RNF 18, RF 46, RN 30, CA 57, OL 21, DP 26, ADR 21; sin enlaces rotos). No comprueba lógica ni contenido.

## Aprobación

| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Propietario del producto | brandonC-developer | Pendiente | Pendiente |
