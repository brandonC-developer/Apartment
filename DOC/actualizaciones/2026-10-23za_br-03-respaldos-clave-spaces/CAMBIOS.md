# Actualización 2026-10-23 (za) — BR-03: cifrado de los respaldos, custodia de la clave y llaves de Spaces

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-024), el modelo de amenazas (versión nueva) y el procedimiento de la fase 6. [DOC/README.md](../../README.md)
**Origen:** brecha BR-03 y amenazas AM-24 y AM-25 del [modelo de amenazas v0.1](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.1_borrador.md); pendiente del ADR-024 ("herramienta y custodia de las claves de cifrado"). Sigue a la [BR-02](../2026-10-23z_br-02-autenticacion-correo/CAMBIOS.md)
**Estado:** decisiones registradas; documentos sin cambiar; no aprobado

## 1. Preguntas, respuestas y decisiones
| # | Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|---|
| 1 | ¿Con qué herramienta se cifran los respaldos? | "age con clave pública, un archivo por día" (recomendada por el asistente) | `age` con cifrado a clave pública. El servidor tiene solo la clave pública; la privada nunca está en él. Cada día se genera un archivo independiente (`pg_dump`, `pg_dumpall --globals-only` y los documentos), cifrado y subido como un objeto. No se usa restic |
| 2 | ¿Dónde se guarda la clave privada? | "Dos copias fuera de línea y prueba trimestral" (recomendada) | El par de claves se genera fuera del servidor. La clave privada se guarda en dos lugares independientes y fuera de línea (impresa en un lugar seguro y en un medio cifrado aparte), ninguno es el servidor ni el dispositivo de uso diario. Cada restauración trimestral (RNF-09) se hace con esa copia. Si se sospecha exposición, se rota el par y se registra qué respaldos quedan con la clave vieja |
| 3 | ¿Cómo se protegen los respaldos de un borrado con la llave del servidor? | "Llave limitada + versionado + copia mensual con llave de solo lectura" (recomendada) | Llave del servidor limitada a un solo bucket (Read/Write/Delete), guardada en el archivo de secretos (ADR-032); versionado del bucket activado; descarga mensual de los respaldos cifrados al equipo del solicitante con otra llave de solo lectura, guardada fuera del servidor; se mantiene el respaldo semanal del Droplet de ADR-024 |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| age: https://github.com/FiloSottile/age | Herramienta de código abierto | Leída por resumen (WebFetch, 23-oct-2026) | Cifra con clave pública (solo hace falta la privada para descifrar), sin opciones de configuración, funciona en flujos (`tar ... \| age ...`); versión citada v1.3.2; las identidades pueden protegerse con contraseña, aunque no es necesario en la mayoría de los casos | **Sin auditoría mencionada** en la página; herramienta joven; no se leyó la especificación |
| restic, referencia: https://restic.readthedocs.io/en/stable/100_references.html | Documentación oficial | Leída por resumen (23-oct-2026) | AES-256 con Poly1305; repositorio de paquetes, índices y snapshots con deduplicación; borrar archivos fuera de restic puede hacer desaparecer snapshots; los paquetes se eliminan con `forget` y `prune` | Se usa para descartar restic por incompatibilidad con el ciclo de vida de Spaces; esa incompatibilidad es inferencia del asistente |
| DigitalOcean, llaves de Spaces: https://docs.digitalocean.com/products/spaces/how-to/manage-access/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Acceso completo o limitado a buckets con solo dos niveles, Read o Read/Write/Delete; sin "escribir sin borrar"; llaves solo desde el panel; el secreto se muestra una vez | — |
| DigitalOcean, versionado de Spaces: https://docs.digitalocean.com/products/spaces/how-to/enable-versioning/ | Documentación del proveedor | Leída por resumen (23-oct-2026) | Soporta versionado (desactivado por defecto); al borrar crea un marcador y conserva el original; una versión puede borrarse permanentemente con la llave de API | No dice qué permisos exige borrar versiones ni si se puede impedir; **no aparece bloqueo de objetos (WORM)** |
| OWASP, Secrets Management Cheat Sheet | Guía de experto reconocido | Leída por resumen (23-oct-2026, actualización (t)) | No guardar las claves junto a los secretos que cifran; los respaldos se cifran y guardan con permisos reducidos | — |
| DAS v0.12, ADR-024 | Documento del proyecto | Releído | Respaldo diario cifrado a Spaces con regla de ciclo de vida de 35 días y respaldo semanal del Droplet | — |

## 3. Lo que propone el asistente y el solicitante no decidió
- **Dos copias fuera de línea, en papel y en un medio cifrado**, y una descarga mensual: criterio del asistente, sin fuente. Un gestor de contraseñas y GnuPG **no se investigaron**.
- Que restic sea incompatible con la regla de 35 días: inferencia del asistente a partir de la advertencia de su documentación.
- Qué día del mes se descarga la copia y dónde se guarda en el equipo.
- Con una sola persona (DP-23), nadie más sabe dónde están las copias de la clave: **riesgo anotado, no resuelto**.

## 4. Qué no se hizo
- No se generó ninguna clave, no se creó ningún bucket ni llave; es etapa B.
- No se verificó cómo interactúa el versionado con la regla de ciclo de vida de 35 días (si las versiones antiguas también se borran).
- No se calculó el costo de almacenamiento de un archivo completo por día ni del versionado dentro de los 250 GiB del plan.
- No se probó `age` ni su formato con archivos grandes; no se leyó su especificación ni se buscó una auditoría.
- No se resolvió la pérdida de acceso a las copias de la clave si el solicitante no está.
- La llave del servidor puede borrar los respaldos aun con versionado: la medida limita el daño con la copia mensual y el respaldo semanal del Droplet, no lo elimina. Con RPO de 24 h, el último respaldo fuera del alcance de esa llave puede tener hasta un mes de antigüedad.

## 5. Qué falta hacer
1. DAS: completar el ADR-024 con la herramienta, la custodia y las llaves (versión nueva o ajuste consolidado).
2. Modelo de amenazas v0.2: BR-03 cerrada; AM-24 y AM-25 con su nueva respuesta y riesgo residual.
3. Fase 6: procedimiento de generación de claves, descarga mensual, rotación y restauración con la copia fuera de línea.
4. Plan de implementación y estrategia de pruebas: la restauración trimestral debe usar la copia de custodia.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
