# Actualización 2026-10-23 (zza) — Biblioteca del segundo factor (TOTP)

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-022 o ADR nuevo, versión nueva), en `src/requirements.txt` y en el código de `cuentas` cuando se implemente. [DOC/README.md](../../README.md)
**Origen:** pendiente de la E0 anotado en la actualización [(zz)](../2026-10-23zz_modelo-de-usuario/CAMBIOS.md); RF-26, RF-27, CA-68 y CA-69; entidad ADMINISTRADOR del [modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md)
**Estado:** decisión registrada; código sin escribir; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Qué biblioteca implementa el segundo factor TOTP? | «pyotp + campos propios del MDD» (recomendada por el asistente) | **pyotp** solo para generar y verificar el código (RFC 4226 y 6238); el secreto, el último intervalo usado (CA-69), los fallos consecutivos y la espera creciente (CA-68) viven en `cuentas.Administrador` según el modelo de datos. Sin django-otp ni django-two-factor-auth |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| PyPI, pyotp (JSON): https://pypi.org/pypi/pyotp/json | Registro del paquete | Leída (WebFetch, 23-oct-2026) | Versión 2.10.0 (14-jun-2026), MIT, sin dependencias de ejecución, `requires_python >=3.8`, classifiers hasta 3.13, implementa HOTP y TOTP | **No lista Python 3.14**, que es el del plan; no se probó en 3.14. No se leyó su código ni su historial de seguridad |
| PyPI, django-otp (JSON): https://pypi.org/pypi/django-otp/json | Registro del paquete | Leída en parte (el JSON se truncó) | Versión 1.7.5, Unlicense, `django>=4.2`; no se obtuvo la fecha de publicación | Incompleta |
| PyPI, django-two-factor-auth (JSON): https://pypi.org/pypi/django-two-factor-auth/json | Registro del paquete | Leída (WebFetch, 23-oct-2026) | Versión 1.18.1 (27-sep-2025), MIT, Python hasta 3.13, Django hasta 5.2, dependencias `django-otp`, `qrcode`, `django-phonenumber-field`, `django-formtools`; extras de SMS y llamadas | La descripción y los classifiers difieren en Django 5.2 |
| Documentación de django-otp (modelo TOTP): https://django-otp-official.readthedocs.io/en/stable/_modules/django_otp/plugins/otp_totp/models.html | Documentación del proveedor | **Solo resultados de búsqueda** | La clave es un `CharField` hexadecimal que no consta cifrado; `last_t` evita la repetición; la espera es exponencial (c·2^(n-1)) | No se abrió la página; que no cifre es lo que **no** aparece, no una afirmación leída |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido:** pyotp con campos propios del modelo de datos.
- **Propuesta del asistente, sin decidir:** cómo se cifra el secreto en la base (el MDD solo dice «texto cifrado»: biblioteca, clave y dónde se guarda), el número de dígitos y la tolerancia de ventana, el formato del código QR y la pantalla de alta del factor, y la implementación de la espera de CA-68.
- Que escribir la lógica de repetición y de espera propia sea preferible a django-otp se apoya en que su espera no coincide con CA-68; no se probó adaptarla.

## 4. Riesgos y límites
- **Python 3.14:** pyotp no lo lista; hay que probarlo en WSL antes de darlo por bueno (es Python puro, pero eso no basta como evidencia).
- **Código propio de seguridad:** la verificación, la repetición y la espera se escriben aquí y exigen pruebas (CA-68, CA-69); un error puede dejar entrar o dejar fuera a la única cuenta.
- **Cifrado del secreto** sin decidir: es la siguiente decisión, porque determina una dependencia más (`cryptography`) y dónde vive la clave.

## 5. Qué no se hizo
- No se instaló pyotp ni se escribió código. `src/requirements.txt` no cambia.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
