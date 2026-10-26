# Actualización 2026-10-26 (d) — Cierre de la E1 (inquilinos)

**Fecha:** 2026-10-26
**Documentos afectados:** [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`AVANCE_IMPLEMENTACION.md`](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), pruebas en `src/inquilinos/` y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** plan de implementación, sección 3.1 (nueve condiciones); instrucciones del solicitante: «sí, acepto las muestras públicas y mi foto. Git pasó las pruebas» y la carpeta `img` con su foto (26-oct-2026); actualizaciones [2026-10-26 (b)](../2026-10-26b_e1-grupo-g-muestras-publicas-y-mpo/CAMBIOS.md) y [(c)](../2026-10-26c_pillow-13-pip-audit/CAMBIOS.md)
**Estado:** E1 terminada según el registro de avance; **nada de esto está aprobado**

## 1. Decisión del solicitante
Pregunta: ¿el criterio de salida (un iPhone y dos Android) se da por cumplido con muestras públicas más una foto de un documento de su teléfono? · Respuesta: «sí, acepto las muestras públicas y mi foto» · Decisión: **CA-73 se marca con esa desviación**, registrada aquí y en el registro de avance. No cubre el selector de archivos del iPhone (HEIC a JPEG): queda como riesgo conocido sin verificar.

## 2. La foto del solicitante (Motorola moto g72, Android)
| Dato | Valor |
|---|---|
| Original | JPEG 4000x3000, 2,98 MiB, orientación 1, **sin GPS**, sin perfil ICC, con las etiquetas EXIF habituales |
| Enviado por el script (Chrome 155) | JPEG 2048x1536, calidad 0,85, **0,34 MiB** (11 %), sin GPS ni EXIF, perfil sRGB |
| Servidor | acepta tanto el original como el reducido |
| Legibilidad | tras la reducción se leen el nombre, el número y la carrera de la tarjeta; un reflejo del flash tapa parte de una palabra (efecto de la foto, no de la reducción) |

La foto contiene datos personales del solicitante: **no se copió al repositorio** (`img/` sigue sin versionar) y no se anotan sus valores. Las **cinco fotos** medidas (de cuatro modelos: iPhone 14 Pro x2, Galaxy S23, Pixel 8 y moto g72) pesan de 0,34 a 1,28 MiB tras la reducción, todos bajo los 2 MB.

## 3. Alcance de CA-82
CA-82 pertenece a la **E2** (no a las ocho de la E1). La medición hecha aquí sirve de dato para la E2: en Chrome, **el archivo reducido no conserva GPS ni etiquetas EXIF** en las cinco fotos medidas. La comprobación formal de CA-82 con la medición de la E2 sigue pendiente.

## 4. Las nueve condiciones
| # | Condición | Cumple | Evidencia |
|---|---|---|---|
| 1 | Pruebas de los CA en la integración continua; ninguna Alta sin escribir | Sí | los 8 CA con pruebas; 410 pruebas en Windows y 399 en WSL; CI en verde **informada por el solicitante** |
| 2 | Integración continua en verde | Sí, por informe del solicitante | «Git pasó las pruebas» (26-oct); **no veo las corridas**; la del commit de cierre la confirma él |
| 3 | `verificar_coherencia.ps1` sin problemas | Sí | ejecutado el 26-oct |
| 4 | Privilegios de tablas nuevas con su prueba | Sí | las 5 tablas de `inquilinos` |
| 5 | Código sin cubrir revisado | Sí, **autorrevisión** | cobertura de `inquilinos`: 99 % de líneas; 5 sin ejecutar (defensas inalcanzables de `imagenes.py`); se añadieron 4 pruebas (fallo de `fsync` sin archivo parcial, duplicados sin número, acción de acceso inválida, archivo vacío en el comando). **No es una revisión independiente** |
| 6 | Desplegada en WSL con datos ficticios y criterio de salida | Sí | `desplegar.sh`, `verificar.sh` sin fallos, Pillow 13.0.0 comprobado dentro de WSL |
| 7 | Sin datos personales ni secretos en registros y auditoría | Sí | pruebas de la auditoría; Nginx sin cadena de consulta; Gunicorn sin registro de acceso |
| 8 | `CAMBIOS.md` y trazabilidad al día | Sí | actualizaciones 2026-10-24p a 2026-10-26d |
| 9 | Ningún defecto Alto conocido abierto | Sí, hasta donde sé | defecto del MPO corregido; ver riesgos |

## 5. Lo que queda abierto (no son defectos de la E1)
- **CA-29:** bloqueo real en la E2 (contrato vigente) y la E3 (saldos), con aceptación escrita del solicitante (decisión 5 de la E1).
- **CA-67 (resto):** rechazo de contratos nuevos con un inquilino que revocó el consentimiento, en la E2.
- **Texto del consentimiento:** sigue siendo un borrador sin validar por un abogado (DP-17, DP-21); el solicitante debe definir el responsable y la dirección con `configurar_organizacion` y cargar el texto.
- **iPhone con HEIC:** sin verificar el selector de archivos; el servidor rechaza HEIC.
- **Comprobación manual del navegador sin lienzo (CA-74):** no se hizo a mano; la cubre una prueba automática con un navegador real. Propuesta mía; el solicitante puede exigirla.
- **Revisor independiente** sin designar; hallazgo de la E2 sobre ACCESO_DOCUMENTO y DOCUMENTO_CONTRATO (ciclo de migraciones); ERS v1.17, DAS v0.16 y MDD v0.8 pendientes; pantallas sin estilos hasta los wireframes.
- **`E:\var`** con imágenes de prueba antiguas fuera del repositorio: el solicitante debe borrarla.

## 6. Verificación
410 pruebas en Windows (Python 3.12) y 399 en WSL (Python 3.14.4, Pillow 13.0.0); `verificar.sh` sin fallos; `verificar_coherencia.ps1` sin problemas.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
