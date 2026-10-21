# Actualización 2026-10-21 (c) — Diseño técnico v0.5 (HT-03)

**Fecha:** 2026-10-21
**Documentos afectados:** [Diseño técnico v0.5](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.5_borrador.md); README de la [fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Versión anterior:** [Diseño técnico v0.4](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.4_borrador.md) (se conserva sin cambios)
**Estado:** borrador; no aprobado

## 1. Motivo
Hallazgo HT-03: RF-40 pide exportar los datos del titular "en forma legible" sin definir alcance ni formato.

## 2. Cambios
| ID | Tipo | Descripción | Origen |
|---|---|---|---|
| DTE 3.4.1 | añadido | Alcance, contenido, formato, entrega y frecuencia de la exportación | P1 y P2 |
| DTE 1, 3.4, 5 (F-0x), 6 (HT-03), 7 | modificado | Estado de la exportación y de HT-03 | — |
| DTE 2 | modificado | Fila nueva: Ley 8968 art. 7 y Reglamento 37554-JP arts. 21 y 22 | — |

## 3. Impacto
- **ERS (próxima versión):** RF-40 y CA-27 deben decir qué incluye la exportación y que es un informe web imprimible.
- **DAS:** sin cambios; el informe web no añade dependencias ni paquetes del servidor.
- **Legal:** alcance, exclusiones (datos de terceros, codeudores o fiadores) y la foto de la cédula, para el abogado (DP-17). Falta anotarlo en el resumen para el abogado.
- **Pruebas:** CA-27 debería verificar el contenido del informe; hoy solo verifica la fecha límite y que se pueda exportar.
- **HT-02 (comprobante):** puede reutilizar el mismo mecanismo (informe web imprimible); no está decidido.

## 4. Decisiones
| # | Pregunta | Respuesta del solicitante | Recomendación del asistente |
|---|---|---|---|
| P1 | ¿Qué incluye la exportación? (primero pidió que le explicara la recomendación 1, con un ejemplo) | Todo su registro, incluida la foto de la cédula | Igual |
| P2 | ¿En qué formato? | Primero: PDF generado por el sistema. **Rectificó después (misma sesión):** informe web imprimible, la recomendación | Informe web imprimible, sin dependencias nuevas |

**Rectificación:** el solicitante pidió cambiar P2 por la recomendación. Se corrigió la v0.5 en su sitio, pues no estaba reemplazada ni aprobada; el registro de la primera elección queda aquí. Por eso ya no hay riesgo de biblioteca ni de paquetes del servidor. Queda el límite del informe web: el PDF lo produce el navegador del administrador y el sistema no controla su aspecto.

**Propuestas del asistente, no decididas:** entrega fuera del correo y de WhatsApp; auditar cada exportación; informar al administrador del intervalo de seis meses.

**Pendientes:** validación del abogado; resumen para el abogado; ERS v1.9.

## 5. Evidencia y fuentes
- Ley 8968, art. 7, y Reglamento 37554-JP, arts. 21 y 22, de las copias .docx del Archivo Nacional. Validación: leídos completos en esos artículos, extrayendo el texto del .docx descargado. Limitaciones: copias no oficiales, no comparadas con la Gaceta, sin reformas posteriores comprobadas.
- No se encontró texto de portabilidad ni de formato obligatorio en esos artículos; no se revisó el resto de la ley y del reglamento.
- Los resultados de búsqueda sobre el Reglamento fueron en su mayoría peruanos y se descartaron.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`. No revisa el diseño técnico.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
