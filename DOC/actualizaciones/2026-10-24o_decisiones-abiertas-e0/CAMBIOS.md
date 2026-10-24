# Actualización 2026-10-24 (o) — Decisiones abiertas de la E0

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/nucleo/`](../../../src/nucleo/formato.py), [`src/cuentas/`](../../../src/cuentas/autenticacion.py) y [`src/sga/`](../../../src/sga/settings.py); [`AVANCE_IMPLEMENTACION.md`](../../fase-5-implementacion/AVANCE_IMPLEMENTACION.md), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). **No se editan la ERS v1.16, el DAS v0.15 ni el modelo de datos v0.7**: lo que cambia en ellos queda en la sección 5.
**Origen:** instrucción del solicitante: «primero las 4 decisiones abiertas» (24-oct-2026), contestadas una por una; durante ellas el asistente halló un quinto asunto, que se contestó igual
**Estado:** decisiones registradas e implementadas; no aprobado

## 1. Trazabilidad: pregunta, respuesta y decisión
| # | Pregunta | Recomendación del asistente | Respuesta del solicitante | Decisión |
|---|---|---|---|---|
| 1 | ¿Cuántos decimales se muestran por defecto en los colones? (RNF-12 muestra `₡180.000,50`; los CA, `₡180.000` y `₡92.903`) | Sin decimales si es entero y con dos si tiene céntimos; dólares siempre con dos | «Sin decimales si es entero, con 2 si tiene céntimos (Recomendado)» | `formato.moneda` lo hace así; nunca oculta un céntimo guardado |
| 2 | ¿Cómo y cuándo se edita la configuración de la organización? | Comando de servidor; pantallas web solo donde un RF las pida | «Comando de servidor; pantallas solo donde un RF las pida (Recomendado)» | Comando `configurar_organizacion` (con auditoría); la pantalla de recordatorios es RF-21 en la E4; no hay pantalla general |
| 3 | **Hallazgo del asistente:** ¿cómo se guardan los códigos de recuperación (SHA-256 sin sal, unos 49 bits)? | Argon2id con sal; códigos cortos | «Argon2id con sal; códigos cortos (Recomendado)» | Hash Argon2id con sal por código; migración que borra los códigos de prueba existentes |
| 4 | ¿Se mantiene el `DELETE` del rol de la aplicación sobre los códigos de recuperación? | Mantenerlo solo en esa tabla | «Mantener el DELETE solo en esa tabla (Recomendado)» | Se mantiene; excepción escrita al ADR-027 |
| 5 | ¿Se guarda una copia fuera de línea de la clave Fernet? | No; si se pierde, rescate | «No guardar copia; si se pierde, rescate (Recomendado)» | Sin copia; el secreto ilegible deja de ser un error 500 |

## 2. Fuentes y su validación
| Fuente | Qué respalda | Cómo se validó | Límites |
|---|---|---|---|
| [NIST SP 800-63B-3, §5.1.2.2](https://pages.nist.gov/800-63-3/sp800-63b.html) y [SP 800-63B-4, §3.1.2](https://pages.nist.gov/800-63-4/sp800-63b.html) | Un secreto de búsqueda de menos de 112 bits se guarda con sal (32 bits o más) y un esquema de hash de contraseñas, con limitación de intentos; uso único | Leídas con un resumen automático de la página; la 63B-4 solo hasta donde cabía (la sección 4.2 sobre recuperación no llegó) | La 63B-3 está reemplazada por la 63B-4 (1-ago-2025); coinciden en este punto. La estimación de «horas con una GPU» para romper SHA-256 de 49 bits es del asistente, sin medir |
| [Documentación de `cryptography` (Fernet)](https://cryptography.io/en/latest/fernet/) | La clave debe mantenerse secreta; si se pierde no se descifra; rotación con `MultiFernet` | Leída con un resumen automático | No dice nada sobre guardar la clave aparte de los datos; esa regla es práctica general, sin fuente |
| [Delfino.cr](https://delfino.cr/2026/01/monedas-de-5-10-y-25-del-diseno-anterior-dejaran-de-funcionar-como-medio-de-pago) y [Observador.cr](https://observador.cr/monedas-viejas-de-25-10-y-5-no-podran-utilizarse-a-partir-de-hoy-conozca-cuales-tarifas-se-ajustan/) | Las monedas de ₡5, ₡10 y ₡25 del diseño anterior dejaron de ser medio de pago el 1-jul-2026 | Solo resultados de búsqueda, sin abrir | Prensa; no respalda por sí sola ocultar o mostrar céntimos. No se encontró una norma del BCCR sobre redondeo ni la regla de decimales de los comprobantes electrónicos de Hacienda |
| ERS (RNF-12, CA-03, CA-14, RF-21, RF-33, DP-02), ADR-027, ADR-031 y mi despliegue en WSL | Las decisiones 1, 2 y 4 | Leídos/comprobados por el asistente | Criterio de diseño del asistente, sin estudio externo |

## 3. Qué se implementó
| Decisión | Cambio |
|---|---|
| 1 | `formato.moneda` sin `decimales` muestra los colones sin decimales si son enteros (tras redondear a céntimos) y con dos si tienen céntimos; el dólar, siempre con dos. El filtro de plantilla `|moneda` usa lo mismo |
| 2 | `python manage.py configurar_organizacion [--nombre-responsable ...] [--direccion-responsable ...] [--zona-horaria ...] [--hora-proceso-diario HH:MM]`: sin opciones muestra la configuración; con ellas la cambia con `organizacion.actualizar` (actor `servidor`; del nombre y la dirección solo consta que cambiaron). Rechaza una zona o una hora inválidas sin cambiar nada. **Cambiar la hora aquí no mueve el temporizador de systemd** (el proceso diario llega en la E2) |
| 3 | `hash_codigo` pasa a Argon2id con sal propia (parámetros mínimos de OWASP: 19 MiB, 2 iteraciones, 1 hilo; baratos solo al correr las pruebas); la columna ya no es única ni se busca por hash; verificar comprueba los hasta 10 códigos sin usar sin cortar en el primero; migración `cuentas/0004` que **borra los códigos existentes** (eran de prueba; hay que emitir nuevos con la pantalla `/cuenta/codigos/`) |
| 4 | Sin cambio de código: se confirma el `DELETE` solo sobre `cuentas_codigorecuperacion`; el comentario de `sga/privilegios.py` dice ahora que es una excepción decidida |
| 5 | Un secreto del autenticador que no se puede descifrar ya no da un error 500: cuenta como fallo, deja el evento `segundo_factor_ilegible` (que sale en la alerta de la pantalla de inicio) y se puede entrar con un código de recuperación |

## 4. Verificación
- **211 pruebas pasan** (15 nuevas) en Windows con Python 3.12 y **en WSL con Python 3.14.4, sin ninguna omitida**; `makemigrations --check` sin cambios; el despliegue aplicó la migración 0004 con el rol dueño; `verificar.sh` y `verificar_respaldo.sh` sin fallos, y el recorrido real por HTTPS **emite 10 códigos con los parámetros de producción** dentro del tiempo de Gunicorn.
- **Mutaciones manuales, todas detectadas:** volver a SHA-256 sin sal, no capturar el secreto ilegible, no registrar su evento y mostrar siempre colones sin decimales.
- Errores míos corregidos en el camino: ninguno de código; una prueba existente buscaba el código por su hash y pasó a usar `codigo_disponible`.

## 5. Cambios pendientes en los documentos (no se hicieron aquí)
- **ERS v1.17:** RNF-12 y los CA con importes en colones deben decir la misma regla de decimales; RF-27/CA-69 pueden mencionar que los códigos se guardan con hash con sal; el comando `configurar_organizacion` y el hecho de que la organización no tiene pantalla de edición (salvo RF-21).
- **DAS v0.16:** ADR-027 (excepción de `DELETE` sobre los códigos de recuperación, decidida), una decisión sobre el almacenamiento de los códigos (Argon2id con sal, NIST SP 800-63B) y sobre la clave Fernet (sin copia, rescate); ADR-005 si se recoge la regla de decimales.
- **Modelo de datos v0.8:** `CODIGO_RECUPERACION.hash_codigo` es un hash Argon2id con sal, no único.
- **Modelo de amenazas:** la amenaza de filtración de la base y de los códigos de recuperación gana esta mitigación; sin cambio de nivel propuesto.

## 6. Consecuencia para el cierre de la E0
La condición 9 de terminado se marcó «sin defecto Alta conocido». El asistente clasifica el almacenamiento sin sal como **Media** (límite de intentos, uso único, respaldos cifrados, base solo por socket y sin datos reales todavía), pero lo habría encontrado la revisión por otra persona. Queda anotado en el registro de avance sin cambiar el estado de la E0; el solicitante puede reclasificarlo.

## 7. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
