# Actualización 2026-10-23 (zz) — Modelo de usuario de la E0

**Fecha:** 2026-10-23
**Documentos afectados:** ninguno editado; la decisión se incorporará en el DAS (ADR-022 o un ADR nuevo, versión nueva) y en el código de `cuentas` cuando se implemente. [DOC/README.md](../../README.md)
**Origen:** pendiente de la E0 anotado en [`src/README.md`](../../../src/README.md) y en la actualización [(zy)](../2026-10-23zy_inicio-implementacion-e0/CAMBIOS.md): el modelo de usuario debe fijarse antes de la primera migración; entidad ADMINISTRADOR del [modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md); RF-26, RF-27 y RN-25
**Estado:** decisión registrada; código sin escribir; no aprobado

## 1. Pregunta, respuesta y decisión
| Pregunta | Respuesta del solicitante (23-oct-2026) | Decisión |
|---|---|---|
| ¿Qué modelo de usuario usa el SGA? | «AbstractBaseUser con los campos del MDD» (recomendada por el asistente) | `cuentas.Administrador` basado en `AbstractBaseUser`, **sin** `PermissionsMixin`, con los atributos de ADMINISTRADOR del modelo de datos (usuario único, contraseña con Argon2id, segundo factor, contadores de intentos, `is_active`); sin nombre, correo, `is_staff`, grupos ni permisos. `AUTH_USER_MODEL = 'cuentas.Administrador'`, fijado antes de la primera migración |

## 2. Fuente
| Fuente y URL | Tipo | Cómo se validó | Qué respalda | Limitaciones |
|---|---|---|---|---|
| Django 5.2, personalización de la autenticación: https://docs.djangoproject.com/en/5.2/topics/auth/customizing/ | Documentación oficial | **Leída por resumen** (WebFetch, 23-oct-2026) | `AUTH_USER_MODEL` debe fijarse antes de la primera migración y cambiarlo después «puede ser complejo»; `AbstractBaseUser` es el núcleo mínimo y exige `USERNAME_FIELD` único, gestor propio e `is_active`; sin `PermissionsMixin` no deben usarse los métodos de permisos de `ModelBackend`, que asume campos inexistentes; el perfil `OneToOne` añade consultas | El resumen no es la página completa; no se probó nada con Django 5.2.18 |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido:** el modelo base (`AbstractBaseUser` con los campos del MDD).
- **Propuesta del asistente, sin decidir:** que no haya `PermissionsMixin` (se comprueban los accesos con la autenticación y la sesión, no con permisos de Django), un backend de autenticación propio que implemente el contador de intentos y el segundo factor, que una sola fila se imponga en la base (RN-25), y que la creación y el rescate de la cuenta sean un comando que solo se ejecuta en el servidor (RF-27).
- **Sin decidir:** la biblioteca del segundo factor y dónde se cifra su secreto.

## 4. Riesgos y límites
- Cada vista debe exigir autenticación de forma explícita; sin permisos de Django no hay un segundo seguro. Las tablas `auth_permission` y `auth_group` seguirán existiendo, vacías de uso.
- Todo lo que cuelga del usuario (auditoría, códigos de recuperación, tokens) apunta a `Administrador`; el nombre de la tabla y de los campos (`usuario`, no `username`) se confirman al escribirlo.
- El MDD dice «una sola fila en v1»; cómo se impone en PostgreSQL no está en el modelo y se propone al implementar.

## 5. Qué no se hizo
- No se escribió el modelo, el gestor, el backend ni las migraciones.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
