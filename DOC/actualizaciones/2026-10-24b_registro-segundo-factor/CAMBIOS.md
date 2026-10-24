# Actualización 2026-10-24 (b) — Pantalla de registro del segundo factor

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/cuentas/`](../../../src/cuentas/views.py), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS v1.16, RF-27 («el segundo factor se activa en el primer ingreso»; 10 códigos mostrados una sola vez al activarlo) y CA-69; instrucción del solicitante: «sí, escribe la pantalla de registro del segundo factor» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
- **Flujo:** si la contraseña es correcta y el segundo factor no está activo, el primer paso lleva a `/entrar/registro/` (antes daba error). La pantalla muestra la clave (base32) y la dirección `otpauth://`; el administrador la agrega a su aplicación y escribe un código. Si es válido se guarda el secreto cifrado, se activa, se inicia la sesión y se muestran **una sola vez** los 10 códigos de recuperación.
- `autenticacion.activar_segundo_factor`: comprueba el código contra el secreto propuesto con la misma ventana de ±1 intervalo, **el mismo contador de intentos** y la misma espera que el inicio de sesión. Bajo bloqueo de fila; **nunca reemplaza un segundo factor ya activo**.
- `_intervalo_aceptado`: la comprobación del TOTP se extrajo de `verificar_totp` para compartirla; las pruebas anteriores siguen pasando.
- El secreto propuesto se guarda en la sesión **cifrado** (Fernet), no en claro, y se conserva si la página se recarga. La plantilla de la pantalla y la de los códigos son HTML mínimo.
- Pruebas: 8 nuevas y 1 reescrita; **64 pasan** en un PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows. Mutación manual: quitar la negativa a reemplazar un factor activo hizo fallar su prueba; se restauró. Error mío corregido en la primera corrida: el decorador de la clave de cifrado de la prueba cubría solo `setUp`.

## 2. Propuestas del asistente (sin aprobar)
- **Sin código QR:** se muestra la clave y la dirección `otpauth://`. Un QR exige una biblioteca más (`qrcode`), que no está decidida; es una mejora de comodidad, no de seguridad.
- Iniciar la sesión al activar, tras haber probado contraseña y un TOTP válido.
- Los intentos fallidos del registro suman al contador compartido (si no, el registro permitiría probar códigos sin límite).
- Los códigos de recuperación aparecen en la respuesta de esa petición; recargar la pantalla no los vuelve a mostrar (reenviar el formulario falla porque el segundo factor ya está activo). Sin cabeceras de no-caché propias todavía.
- Cambia el mensaje del primer paso: ya no menciona el segundo factor sin activar.

## 3. Qué no está hecho
- **Aviso de seguridad por correo** del registro del segundo factor (RF-27) y auditoría: no hay envío de correo ni modelo de auditoría.
- Reemplazo del segundo factor con la sesión iniciada y regeneración de códigos desde la interfaz (existe la función de emisión, no la pantalla).
- Cambio y restablecimiento de contraseña, estilos, roles de PostgreSQL, despliegue en WSL, respaldo y CI. 0 de 8 CA de la E0 cumplidos.
- No se probó en un navegador real ni con una aplicación de autenticación real; la compatibilidad de la dirección `otpauth://` con ellas es la prevista por pyotp, no verificada.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
