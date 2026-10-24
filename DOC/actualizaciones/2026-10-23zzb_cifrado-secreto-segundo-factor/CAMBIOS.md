# Actualización 2026-10-23 (zzb) — Cifrado del secreto del segundo factor

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-032, decisión 6, o ADR nuevo; versión nueva), en `src/requirements.txt` y en el código de `cuentas`. [DOC/README.md](../../README.md)
**Origen:** el modelo de datos v0.7 define `secreto_segundo_factor` como «texto cifrado» sin decir cómo; pendiente anotado en la actualización [(zza)](../2026-10-23zza_biblioteca-segundo-factor/CAMBIOS.md)
**Estado:** decisión registrada; código sin escribir; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Cómo se cifra el secreto TOTP en la base? | «Fernet/MultiFernet con clave en /etc/sga» (recomendada por el asistente) | La aplicación cifra el secreto con **Fernet** de la biblioteca `cryptography` antes de guardarlo y lo descifra al verificar; **MultiFernet** permite rotar la clave. La clave vive en un archivo propio de `/etc/sga/` (permisos `0640`, mismo mecanismo de secretos de ADR-032, decisión 6), distinta de `SECRET_KEY` y separada de la base |

## 2. Fuentes
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| OWASP, Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html | Guía de experto reconocido | Leída por resumen (WebFetch, 23-oct-2026) | AES con clave de al menos 128 bits (idealmente 256); modos autenticados (GCM o CCM primero; CBC con autenticación separada si no); claves en un lugar distinto de los datos cifrados; rotación | **No menciona TOTP**; no habla de ChaCha20-Poly1305; el modo de Fernet (CBC + HMAC) cae en la excepción, no en la primera opción |
| Documentación de `cryptography`, Fernet: https://cryptography.io/en/latest/fernet/ | Documentación del proveedor | Leída por resumen (WebFetch, 23-oct-2026) | Fernet = AES-128-CBC con relleno PKCS7 + HMAC-SHA256, IV con CSPRNG, no permite leer ni manipular sin la clave; MultiFernet cifra con la primera clave, descifra con cualquiera y tiene `rotate()` | Es parte de la documentación, no la especificación; no compara con AES-GCM |
| PyPI, cryptography (JSON): https://pypi.org/pypi/cryptography/json | Registro del paquete | Leída en parte (JSON truncado) | Versión 50.0.2, Apache-2.0 o BSD-3-Clause, `requires_python >=3.9`, classifier de Python 3.14 | Sin la fecha de publicación; no se probó con Python 3.14 en este entorno |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido:** Fernet/MultiFernet con la clave en `/etc/sga/`.
- **Propuesta del asistente, sin decidir:** el nombre y la ruta del archivo de la clave, cómo se genera y se respalda (la pérdida de la clave imposibilita el segundo factor: el rescate por el servidor, RF-27, vuelve a registrarlo), el plazo de rotación (la de ADR-032 es de un año), el formato del campo en la base y qué hacer con el secreto durante la rotación.
- **Fernet usa AES-128**, no 256; es suficiente según OWASP («al menos 128 bits») pero no es lo ideal que cita. La prioridad dada a la simplicidad frente a AES-256-GCM es criterio del asistente.

## 4. Riesgos y límites
- **Protege contra** una fuga de la base o de un respaldo; **no contra una aplicación comprometida**, que lee la clave (ADR-032, decisión 6: el grupo de la aplicación puede leer `/etc/sga/`). Es el mismo límite ya reconocido para los demás secretos (AM-17).
- **Pérdida de la clave:** sin ella, el secreto guardado es inservible. El respaldo cifrado (`age`) no incluye `/etc/sga/` por defecto; hay que decidir si la clave se respalda y dónde (no en el mismo lugar que la base).
- **Dependencia nueva:** `cryptography` (con extensiones compiladas); en WSL con Ubuntu-26.04 debe probarse.
- El modelo de amenazas v0.4 no tiene una fila para el cifrado del secreto; AM-17 es lo más cercano.

## 5. Qué no se hizo
- No se instaló `cryptography` ni se escribió código. `src/requirements.txt` no cambia.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
