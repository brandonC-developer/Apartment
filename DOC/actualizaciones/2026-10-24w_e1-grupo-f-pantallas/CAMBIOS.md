# Actualización 2026-10-24 (w) — E1, grupo F: pantallas de los inquilinos

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/inquilinos/`](../../../src/inquilinos/pantallas.py), [`src/despliegue/verificar_http.py`](../../../src/despliegue/verificar_http.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS RF-01, RF-03, RF-04, RF-05, RF-39; CA-01, CA-25, CA-29, CA-67; decisión 6 de la E1 (pantallas funcionales y accesibles, sin estilos; actualización [2026-10-24 (q)](../2026-10-24q_decisiones-e1/CAMBIOS.md)); instrucción del solicitante: «sí, escribe el grupo F» (24-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Qué se escribió
| Ruta | Pantalla |
|---|---|
| `GET /inquilinos/` | Lista con búsqueda, filtro de estado (activos, desactivados, todos) y «Sin frente del documento»; 50 por página |
| `/inquilinos/nuevo/` | Registro con los datos, el texto informativo vigente (con el aviso de borrador si no lo validó un abogado), el medio, la fecha y la confirmación obligatoria del consentimiento; avisa del documento duplicado y solo guarda si se confirma |
| `GET /inquilinos/<id>/` | Ficha: datos, estado, fotografías con «Ver» y «Descargar», consentimientos (versión, medio, fechas), avisos de falta el frente y de consentimiento revocado |
| `/inquilinos/<id>/editar/` | Edita los cinco campos; solo se guarda y se audita lo que cambia |
| `/inquilinos/<id>/desactivar/` y `/reactivar/` | Confirmación (GET) y acción (POST); si hay motivos de bloqueo se muestran y no se cambia nada |
| `/inquilinos/<id>/consentimiento/revocar/` | Confirmación (GET) y revocación (POST) sin efecto retroactivo |

Todas piden sesión, usan token CSRF en cada envío, no se guardan en caché y escapan los textos. La vista solo llama a `services` y `selectors` (ADR-030). Se añadieron enlaces en el inicio y los avisos de la acción (mensajes de Django) en la plantilla base.

## 2. Propuestas del asistente (sin aprobar)
- **Fecha del consentimiento:** el formulario pide solo la fecha; se guarda a mediodía hora local (nunca después del instante actual) y vacía significa ahora. Una fecha futura se rechaza.
- **Casilla de confirmación** («se mostró este texto y la persona dio su consentimiento») además del medio; sin ella no se registra.
- **Confirmación previa** para desactivar, reactivar y revocar, y respuesta 409 cuando la acción no procede (ya desactivado, sin consentimiento vigente, motivo de bloqueo).
- Páginas de 50, como en la auditoría.
- El inquilino desasociado se puede ver pero no editar ni desactivar.

## 3. Hallazgos
1. **Una prueba mía dejaba archivos en el disco** (44 imágenes de prueba en `E:\var\lib\sga\documentos\cedulas`, fuera del repositorio) porque no cambiaba `RAIZ_DOCUMENTOS` a una carpeta temporal. En WSL falló por permisos y lo mostró. Ya usan carpeta temporal. **La carpeta `E:\var` quedó con esos archivos de prueba: bórrala tú** (mi intento de borrarla lo bloqueó la comprobación de seguridad).
2. **Mi mutación 7 (quitar actor e IP al desactivar) no la detectaba ninguna prueba.** Se añadió una que exige actor e IP en cada acción.
3. **Los mensajes de aviso se pierden si la prueba sigue la redirección antes de leerlos** (`assertRedirects` los consume); las pruebas lo tienen en cuenta.

## 4. Verificación
- **404 pruebas pasan en Windows** (Python 3.12; 14 omitidas) y **393 en WSL** con Python 3.14.4 (las 11 del navegador se omiten allí). 36 son nuevas, de las pantallas: búsqueda y filtros, escape de HTML, paginación, registro con y sin confirmación, fechas, duplicados, ficha, edición, desactivar y reactivar con y sin motivo de bloqueo (**CA-29, el mecanismo**), revocación sin cambiar datos (**CA-67 en la parte de la E1**), CSRF, métodos no admitidos, caché y auditoría de cada acción.
- **Mutaciones (7), todas detectadas** (la 7 tras añadir la prueba): no exigir la confirmación, confirmar siempre el duplicado, aceptar fecha futura, quitar la sesión de la ficha, ejecutar la acción con GET, ignorar «Sin frente» y quitar actor e IP.
- **Recorrido real por HTTPS en WSL** (`verificar.sh`, «sin fallos»): lista, búsqueda, registro con el texto, ficha creada, registro rechazado sin la confirmación, desactivar, token falso → 403 y revocar.

## 5. Qué no está hecho
Estilos y diseño (esperan los wireframes), la medición con fotos reales y la comprobación manual del navegador sin lienzo (grupo G) y la verificación en GitHub. El bloqueo real de desactivar es de la E2 y la E3. **0 de 8 CA de la E1 marcados** hasta el cierre.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
