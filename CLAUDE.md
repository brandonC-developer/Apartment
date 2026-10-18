# Sistema de Gestión de Alquileres (SGA) — documentación

Proyecto en fase de **documentación**. No hay código ni se ha autorizado implementarlo. Idioma de trabajo y de los documentos: español.

## Estructura de `DOC/`

- `fase-1-ers/` a `fase-6-despliegue-operacion/`: un documento por fase, con todas sus versiones en la misma carpeta. Cada carpeta tiene un `README.md` que indica la versión vigente.
- `actualizaciones/AAAA-MM-DD_<docs y versiones>/`: un `CAMBIOS.md` por actualización (motivo, cambios, decisiones, evidencia, aprobación) y la evidencia de investigación. Plantilla: `DOC/metodologia/plantilla_CAMBIOS.md`.
- `legal/`: resumen para el abogado y dictámenes.
- `metodologia/`: evaluación de la metodología de seis fases.
- `herramientas/verificar_coherencia.ps1`: comprobación de identificadores y enlaces.
- `.claude/skills/recomendacion-buenas-practicas/`: skill con el modo de trabajo para recomendaciones (fuentes validadas, preguntas una por una).
- `DOC/README.md`: índice y convenciones.

## Reglas

1. **Ningún documento está aprobado.** No lo describas como aprobado ni como "oficial". La aprobación requiere responsable, fecha y aceptación formal en el registro del propio documento.
2. **No edites una versión que ya fue reemplazada o aprobada.** Crea una versión nueva (`ERS_SGA_001_v1.6_...`) y no copies documentos entre carpetas: cada versión vive en un solo lugar.
3. **Toda actualización lleva su carpeta** en `actualizaciones/` con un `CAMBIOS.md`, y actualiza los README de la fase y `DOC/README.md`.
4. **Trazabilidad desde el origen:** cada cambio de requisito indica la pregunta, la respuesta y la decisión que lo originó.
5. **Las respuestas del solicitante no son aprobación del negocio.** Distingue lo que el solicitante decidió de lo que tú propones, y márcalo (por ejemplo, "regla propuesta").
6. **Identificadores únicos y compartidos** entre ERS y DAS: RF, RN, RNF, CA, OL (obligación legal), DP (decisión pendiente), ADR, y RE (restricción, solo en el DAS). No reutilices ni cambies el significado de un ID.
7. **Nada de asesoría legal.** Las obligaciones de las leyes 7527 y 8968 están pendientes de validación por un abogado (DP-17). Cita el artículo y distingue texto leído de interpretación.
8. **Investigación:** cita la fuente con URL, indica cómo se validó (leída completa, por resumen, solo resultados de búsqueda) y sus limitaciones. No afirmes lo que no verificaste. Si una fuente no se pudo abrir, dilo.
9. **No inventes** enunciados, respuestas ni datos. La pregunta P11 no tiene enunciado recuperable y fue cerrada por el solicitante (DP-14); si reaparece, se reabre con un ID nuevo.
10. **Decisiones que no son tuyas:** pregunta al usuario antes de decidir reglas de negocio, plazos legales o alcance. Propón con recomendación y fundamento.

## Antes de dar por terminado un cambio

```
powershell -File DOC\herramientas\verificar_coherencia.ps1
```

Comprueba que cada RF, RN, RNF, CA, OL, DP y ADR citado en la ERS, el DAS o el modelo de datos esté definido en la última versión de la ERS o del DAS, y que los enlaces relativos entre `.md` existan. No comprueba el contenido ni la lógica; tras cambios de reglas, relee los documentos y recalcula a mano los ejemplos numéricos.

## Convenciones de contenido

- Redacción de requisitos: "El sistema deberá…", con identificador y criterio verificable.
- Los valores son de diseño salvo que tengan fuente; marca lo propuesto con "propuesta" o con un DP.
- El proyecto ya tiene un repositorio Git creado por el solicitante. No ejecutes `git init`, commit ni push, ni cambies la estructura, sin preguntar.
- Archivos en UTF-8. Scripts en PowerShell (el entorno es Windows y no hay Python instalado).
