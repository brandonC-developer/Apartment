# Actualización 2026-10-24 (l) — Pendientes pequeños de la E0

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/cuentas/`](../../../src/cuentas/views.py) y [`src/nucleo/`](../../../src/nucleo/migrations/0004_btree_gist.py), [`src/sga/settings.py`](../../../src/sga/settings.py), [`src/despliegue/desplegar.sh`](../../../src/despliegue/desplegar.sh), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** lista de tareas de la E0 (secciones A, B, E e I); ERS RF-27 y CA-69, CA-13, RNF-02, RNF-03, RNF-14; ADR-028 y ADR-031 decisión 1; plan, condición 7 de terminado; instrucción del solicitante: «sí, cierra los pendientes pequeños de la E0» (24-oct-2026)
**Estado:** implementado y probado; no aprobado

## 1. Qué se cerró
| Tarea | Qué se hizo |
|---|---|
| Códigos de recuperación nuevos (CA-69) | Pantalla `/cuenta/codigos/`: con la sesión iniciada exige la **contraseña actual** (mismo contador de intentos y espera), **invalida los 10 anteriores**, muestra los nuevos una sola vez (sin caché), deja el evento `codigos_emitidos` y, por tanto, la alerta en la pantalla de inicio. Un enlace en la pantalla de inicio |
| Concurrencia del contador | 3 pruebas con hilos y conexiones reales: 8 fallos a la vez cuentan exactamente 5 y un solo aviso; un TOTP y un código de recuperación enviados a la vez se aceptan una sola vez |
| Todas las vistas exigen sesión (CA-13, RNF-02) | Una prueba recorre todas las rutas y falla si una vista nueva responde sin sesión y no está en la lista de las cuatro públicas del inicio de sesión |
| CSRF y enumeración (sección I) | Los cinco formularios rechazan un envío sin token, con y sin sesión; el primer paso no distingue usuario inexistente de contraseña mala |
| Sin secretos en los registros (sección I) | Se capturan todos los registros del programa durante el recorrido completo y no aparece ninguna contraseña, código, token, secreto ni lo escrito en el campo de usuario |
| `BigAutoField` (ADR-028) | Prueba que todos los modelos del proyecto lo usan |
| Documentos privados (RNF-03, RNF-14) | Ajuste `RAIZ_DOCUMENTOS` (`/var/lib/sga/documentos`, `SGA_DOCUMENTOS`), fuera del código, sin `MEDIA_ROOT` ni URL pública, no servida por Nginx |
| `btree_gist` (ADR-031 d1) | Migración `nucleo/0004` con `BtreeGistExtension` |
| Versiones en Python 3.14 | Marcada como hecha: ya se probó en WSL (actualización 2026-10-24j) |

## 2. Propuestas del asistente (sin aprobar)
- **Un intento fallido de la pantalla de códigos nuevos cuenta como `inicio_sesion_fallido`** y suma al mismo contador y a los cinco fallos; no se creó un tipo de evento nuevo.
- La pantalla de códigos nuevos queda **fuera de la zona de autenticación de Nginx** (6 por minuto): el ADR-032 d11 no la lista; la defiende el contador de la aplicación.
- **Dónde va la carpeta de documentos** y su nombre; el despliegue ya la creaba para la aplicación y el respaldo.

## 3. Verificación
- **181 pruebas pasan** (24 nuevas) en Windows con Python 3.12 y en **WSL con Python 3.14.4 y PostgreSQL 18.6, sin ninguna omitida** (en Windows se omiten 13 del respaldo por no tener `age` en el PATH); `makemigrations --check` sin cambios; `verificar.sh` sin fallos tras el despliegue (la migración de `btree_gist` la aplicó el rol dueño sin ser superusuario).
- **Mutaciones manuales, todas detectadas:** quitar el bloqueo de fila de `comprobar_contrasena`, quitar `login_required` de la pantalla de inicio, emitir códigos sin comprobar la contraseña, `csrf_exempt` en el primer paso y escribir la contraseña en un registro.
- **Limitación de las pruebas de concurrencia:** sin el bloqueo de fila fallan **con frecuencia, no siempre** (de tres corridas, falló en dos al quitar el bloqueo del TOTP y en dos al quitar el del código de recuperación). Es una carrera: con el bloqueo pasan siempre; la prueba no demuestra su ausencia en una sola corrida.
- Errores míos corregidos: dos supuestos de las pruebas sobre Windows (`/var/lib/...` no es una ruta absoluta sin unidad y Django normaliza un `MEDIA_URL` vacío a `/`) y un escape de barra invertida mal escrito en una prueba; la última línea de `desplegar.sh` sugería un comando que fallaba por las líneas de comentario del archivo de entorno.

## 4. Qué sigue pendiente de la E0
- **La primera corrida verde de la integración continua** (condiciones 1 y 2; sin ella no se marcan los 8 CA).
- **Alerta persistente por aviso de correo fallido**: depende de que existan los avisos por correo (E4).
- Condición 5 (revisión del código sin cubrir de los módulos críticos), condición 7 completa, condición 9 y el registro de avance.
- Las decisiones abiertas: decimales en colones, pantalla de la organización, `DELETE` de los códigos de recuperación y la clave Fernet fuera de línea.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
