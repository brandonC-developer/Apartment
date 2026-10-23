# Actualización 2026-10-23 (zs) — BR-10: datos que viajan a Resend y DigitalOcean (preguntas para el abogado)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado. La decisión se incorporará en la ERS (v1.16: nueva **DP-31**, propuesta aquí), los resúmenes para el abogado (versión nueva), el modelo de amenazas (versión nueva: BR-10, AM-11, AM-20) y el DAS (ADR-021). [DOC/README.md](../../README.md)
**Origen:** brecha BR-10 y amenazas AM-11 y AM-20 del [modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md); DP-19 de la [ERS v1.15](../../fase-1-ers/ERS_SGA_001_v1.15_borrador.md), que trata la aplicabilidad de la Ley 8968 pero **no menciona la transferencia a proveedores**
**Estado:** decisión registrada; documentos sin cambiar; **no es asesoría legal**; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Cómo se trata la salida de datos a Resend y DigitalOcean sin que el asistente dé asesoría legal? | "Preguntas escritas al abogado (nueva DP)" (recomendada por el asistente) | Registrar una decisión pendiente nueva, **DP-31 (propuesta; se crea en la ERS v1.16)**, responsable: abogado, con las tres preguntas de la sección 3, y añadirla al resumen para el abogado. No se cambia ningún requisito (por ejemplo, el texto de consentimiento de RF-39) antes del dictamen. Bloquea cargar datos reales |

## 2. Qué se leyó de la ley y qué no
| Fuente y URL | Tipo | Cómo se validó | Qué dice (texto leído) | Limitaciones |
|---|---|---|---|---|
| Ley 8968, copia de la Municipalidad de Goicoechea (2021): https://transparencia.munigoicoechea.go.cr/wp-content/uploads/2021/07/No-8968-PROTECCION-DE-LA-PERSONA-FRENTE-AL-TRATAMIENTO-DE-SUS-DATOS-PERSONALES.pdf | Ley (copia no oficial) | **Leída en parte**: PDF convertido con `pdftotext`; leídos los artículos 14 y 31; el resto no | **Art. 14:** los responsables de las bases de datos, públicas o privadas, "solo podrán transferir datos contenidos en ellas cuando el titular del derecho haya autorizado expresa y válidamente tal transferencia y se haga sin vulnerar los principios y derechos reconocidos en esta ley". **Art. 31 f):** es falta gravísima "transferir, a las bases de datos de terceros países, información de carácter personal de los costarricenses o de los extranjeros radicados en el país, sin el consentimiento de sus titulares" | Copia municipal, no el texto oficial vigente; no se comprobó si hay reformas posteriores. Una búsqueda indicó un proyecto de reforma integral (n.º 22.388) cuyo estado **no se verificó** |
| Reglamento 37554-JP y definiciones del art. 2 (responsable, encargado) | Reglamento y ley | **No leídos en esta actualización** | Nada | No se sabe si la ley distingue a un proveedor que trata datos por cuenta del responsable; no se afirma |

Lo que **no** se afirma: que enviar un correo mínimo a Resend o guardar un respaldo cifrado en DigitalOcean sea o no una «transferencia» del art. 14, ni que el art. 31 f) aplique. Eso es interpretación y le toca al abogado.

## 3. Preguntas propuestas para el abogado (DP-31, propuesta)
1. ¿El envío de correos con datos mínimos a Resend (RF-44) y el alojamiento en DigitalOcean (servidor y respaldos cifrados en Nueva York, EE. UU.) constituyen una «transferencia» del art. 14, o es un servicio prestado por cuenta del responsable de la base?
2. Si lo son, ¿el consentimiento de RF-39 debe mencionar a esos proveedores y el país de destino? ¿Qué texto?
3. ¿Aplica el art. 31 f) (transferencia a bases de terceros países sin consentimiento, falta gravísima) a este caso, y cómo cambia si los respaldos están cifrados con una clave que el proveedor no tiene (ADR-032)?

**Hecho relevante, no obvio:** no solo salen correos y respaldos. El **servidor completo** (base de datos y fotografías de cédulas) está en un Droplet de DigitalOcean en la región NYC3 (ADR-023), de modo que los datos originales también residen fuera de Costa Rica. Debe ir en la consulta.

## 4. Lo que propone el asistente y el solicitante no decidió
- Las tres preguntas y su redacción; el número DP-31 (no existe aún en la ERS; hoy hay 30 DP).
- Que no se cambie RF-39 antes del dictamen.
- Que se incluya en el resumen para el abogado: ese resumen está desactualizado (ERS v1.8) y debe rehacerse antes de enviarlo.

## 5. Qué no se hizo
- No se creó DP-31 en la ERS ni se actualizó el resumen para el abogado ni el modelo de amenazas.
- No se leyó el reglamento ni el resto de la ley; no se buscó jurisprudencia ni criterios de la Prodhab.
- No se evaluó cambiar de región o de proveedor.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
