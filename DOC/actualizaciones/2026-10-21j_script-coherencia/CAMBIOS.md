# Actualización 2026-10-21 (j) — Ampliación de `verificar_coherencia.ps1`

**Fecha:** 2026-10-21
**Documentos afectados:** [`herramientas/verificar_coherencia.ps1`](../../herramientas/verificar_coherencia.ps1), [CLAUDE.md](../../../CLAUDE.md), [DOC/README.md](../../README.md) y la estrategia de pruebas v0.3 (HP-03)
**Estado:** herramienta; no es un documento aprobado

## 1. Motivo
La auditoría de la [actualización 2026-10-21 (g)](../2026-10-21g_auditoria-coherencia/CAMBIOS.md) mostró que el diseño técnico, la estrategia de pruebas y el modelo de datos habían quedado desalineados con la ERS v1.9 sin que el script avisara. El solicitante pidió ampliarlo.

## 2. Cambios
| Comprobación | Antes | Ahora |
|---|---|---|
| Identificadores citados y definidos | ERS, DAS y modelo de datos | También el diseño técnico y la estrategia de pruebas (más RE) |
| Vigencia en README | ERS, DAS y modelo de datos | También diseño técnico y estrategia de pruebas; las versiones anteriores solo se marcan como vigentes si son de la misma familia |
| Base declarada | No existía | La base que citan el DAS, el modelo de datos, el diseño técnico y la estrategia de pruebas (ERS, DAS, modelo de datos) debe ser la última versión |
| Cobertura de la matriz | No existía | Cada RF, RN, RNF y CA definido aparece en la sección 10 de la ERS (rangos incluidos) |
| Cobertura de pruebas | No existía | Cada CA definido está asignado en la tabla de cobertura de la estrategia de pruebas |
| README de fase | No existía | Cada `.md` de las fases 1 a 4 consta por nombre en el README de su carpeta |

## 3. Verificación
- Sobre los documentos reales: "sin problemas" (47 RF, 30 RN, 18 RNF, 61 CA).
- Prueba negativa en una copia temporal con seis fallos introducidos a propósito (un CA citado y no definido, una base desactualizada en el diseño técnico, otra en la estrategia de pruebas, un CA fuera de la matriz, un CA sin asignar en las pruebas y un archivo sin listar en un README): el script detectó los seis. Una séptima alteración no se aplicó por un error de texto de la prueba y no cuenta.
- La copia temporal se borró.

## 4. Límites
- Sigue sin revisar el contenido ni la lógica: no detecta, por ejemplo, un texto que dice "WhatsApp" donde la ERS dice "correo".
- La base se detecta en las 14 primeras líneas de cada documento, en las líneas con "Base:" o "de referencia:".
- No revisa los resúmenes para el abogado ni las carpetas `actualizaciones/` (salvo que tengan `CAMBIOS.md`).
- Los identificadores locales HT-nn y HP-nn no se comprueban.

## 5. Incidente durante esta actualización (corregido)
Al aplicar ediciones a `CLAUDE.md`, `DOC/README.md` y la estrategia de pruebas v0.3, una función auxiliar del asistente interpretó mal un único par de texto a reemplazar y sustituyó letras sueltas en los tres archivos (en `CLAUDE.md` y `DOC/README.md`, todas las `C` y `c` por `o`; en la estrategia de pruebas, todos los `|` por espacios). El script ampliado lo delató (decía "61 CA sin asignar"). Reparación:
- `CLAUDE.md`: restaurado desde Git (la copia de trabajo solo difería por el daño) y reaplicada la única edición prevista.
- `DOC/README.md`: reconstruido a partir de su contenido previo y comprobado aplicando el mismo daño al texto reconstruido: solo difería la línea de `herramientas/`, que es el cambio previsto.
- Estrategia de pruebas v0.3: regenerada desde la v0.2 con las mismas ediciones.
- Búsqueda de restos del daño en los 67 `.md`: ninguno. El commit `01c1350` del solicitante es anterior al daño y no lo contiene.
