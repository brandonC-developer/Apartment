---
name: recomendacion-buenas-practicas
description: Use cuando el usuario pida una recomendación, decisión, comparación o "qué sigue" según buenas prácticas; cuando pida investigar con documentación oficial, expertos o estudios universitarios; o cuando haya que resolver ambigüedades o decisiones pendientes (DP) del SGA una por una.
---

# Recomendación según buenas prácticas (SGA)

Resume cómo el usuario pide siempre las recomendaciones en este proyecto. Complementa `CLAUDE.md`; si hay conflicto, manda `CLAUDE.md`.

## 1. Qué espera el usuario

- Recomendaciones **basadas en buenas prácticas**, con **documentación oficial**, estándares, expertos reconocidos y **estudios universitarios**, y con **validación de cada fuente**.
- Aplicaciones o dominios parecidos como referencia (gestión de alquileres, Costa Rica).
- Una **recomendación clara**, no un catálogo de opciones. Si pesas una elección, di cuál recomiendas y por qué.
- Español.

## 2. Flujo

1. **Define la pregunta** y qué documento o ID afecta (RF, RN, RNF, CA, OL, DP, ADR).
2. **Investiga** (WebSearch/WebFetch). Prefiere: texto oficial de la ley o norma, documentación del proveedor, estándar (ISO/IEEE/NIST/OWASP), libro o autor reconocido, artículo universitario o revisado por pares. Un blog solo como apoyo, marcado como tal.
3. **Valida cada fuente** y regístrala (sección 3).
4. **Recomienda** con fundamento, costo y riesgo. Marca qué es fuente y qué es propuesta tuya.
5. **Pregunta al usuario** con `AskUserQuestion` cuando la decisión sea suya (reglas de negocio, plazos legales, alcance, costos asumidos). Una pregunta por vez cuando él lo pida ("una por una"); la opción recomendada va primera y con "(Recomendado)".
6. **Registra** la respuesta con pregunta, respuesta y decisión en el `CAMBIOS.md` de la actualización (regla 4 de `CLAUDE.md`). Distingue lo que el solicitante decidió de lo que tú propones.
7. **Verifica**: `powershell -File DOC\herramientas\verificar_coherencia.ps1` antes de dar el cambio por terminado.

## 3. Registro de fuentes

Por cada fuente:

| Campo | Contenido |
|---|---|
| Fuente y URL | Nombre y enlace |
| Tipo | Ley/norma, estándar, documentación oficial, universidad/revisión por pares, experto, tercero |
| Cómo se validó | Leída completa, leída por resumen, solo resultados de búsqueda, no se pudo abrir (403/404) |
| Qué respalda | La afirmación concreta |
| Limitaciones | Fecha, copia no oficial, versión, alcance |

Reglas: no afirmes lo que no verificaste; si una página no abrió, dilo; no cites estándares de pago como leídos si solo viste su catálogo; fecha los precios y vuélvelos a verificar si pasó tiempo.

## 4. Cuando el usuario pide explicación o costos

Si dice "explícame detalladamente" o "con costos":
- Explica con un ejemplo numérico concreto del proyecto.
- Compara opciones con costo mensual verificado y fecha de consulta.
- Acepta el criterio del usuario (por ejemplo, aprendizaje, software libre, presupuesto mínimo) como restricción real; si tu recomendación cambia, dilo y di por qué. Si él decide contra tu recomendación, registra la decisión, el riesgo asumido y las condiciones que sigues recomendando, sin bloquearlo.

## 5. Límites

- **No es asesoría legal.** Cita el artículo, distingue texto leído de interpretación y remite a la validación del abogado (DP-17).
- **No inventes** enunciados, respuestas ni datos (P11 no tiene enunciado recuperable y está cerrada, DP-14).
- **Ningún documento está aprobado.** No edites versiones reemplazadas; crea versiones nuevas con su carpeta en `actualizaciones/`.
- No hagas `git init`, commit ni push sin preguntar.

## 6. Formato de la respuesta

1. Recomendación en una o dos frases.
2. Por qué (fuentes con nivel de validación).
3. Costo y riesgo.
4. Qué decide el usuario y qué queda pendiente.

Sé breve; el detalle va en los archivos, no en el chat.
