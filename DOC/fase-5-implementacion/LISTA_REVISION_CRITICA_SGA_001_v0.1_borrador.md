# Lista de verificación de la revisión por otra persona

**Sistema de Gestión de Alquileres**

**Identificador:** LRC-SGA-001
**Versión:** 0.1
**Estado:** Borrador para revisión; no aprobado
**Fecha:** 21 de octubre de 2026
**Base:** ERS-SGA-001 v1.16, DAS-SGA-001 v0.15, MDD-SGA-001 v0.7 y PIM-SGA-001 v0.1 (todos borradores no aprobados)
**Ajuste del 22-oct-2026 (actualización 2026-10-22g, sin versión nueva):** alineada con la ERS v1.10; se precisa RV-14.
**Ajuste del 22-oct-2026 (actualización 2026-10-22k, sin versión nueva):** alineada también con la ERS v1.11; las fotografías del contrato (RF-52) entran por analogía en las verificaciones de documentos privados (área 3); no se añadieron puntos.
**Ajuste del 23-oct-2026 (actualización 2026-10-23f, sin versión nueva):** alineada con la ERS v1.12; RV-14 usa 5 MiB; no se añadieron puntos (sin zona temporal no hay verificaciones de ella).

Esta lista sirve a la persona que revise las partes críticas del SGA antes de cargar datos reales (plan de implementación, sección 3.3, DP-23). **No hay persona designada ni código escrito**: la parte A se puede usar ya sobre los documentos y las partes B y C se usarán sobre el código y el servidor. Los puntos a verificar son **propuesta del asistente**, derivados de las decisiones del proyecto y de las fuentes de la sección 2; el solicitante no los revisó uno por uno. No es asesoría legal ni una auditoría de seguridad.

## 1. Cómo se usa
1. La persona revisora completa la sección 3 (sus datos y su independencia) antes de empezar.
2. Para cada punto marca un resultado: **Cumple**, **No cumple**, **No aplica** o **No pude verificar**, y anota la evidencia que miró (documento y sección, archivo y línea, comando o prueba).
3. Cada incumplimiento o duda va a la tabla de hallazgos (sección 6) con su gravedad (Alta, Media o Baja).
4. El solicitante responde cada hallazgo (corregido, aceptado con riesgo escrito o rechazado con motivo) y la persona revisora confirma el cierre.
5. La condición de la sección 4 del plan (revisión de lo crítico antes de datos reales) se da por cumplida solo cuando no queda ningún hallazgo Alta abierto y la sección 7 está firmada.

Momentos: **A** diseño (documentos, ya); **B** código (al terminar cada entrega que toca el punto); **C** servidor y despliegue (etapa B del plan).

## 2. Fuentes
| Fuente | Qué respalda | Cómo se validó | Limitaciones |
|---|---|---|---|
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | Base para probar los controles técnicos de seguridad de una aplicación web; versión estable 5.0.0 | Página del proyecto leída por resumen, 21-oct-2026 | No se leyeron sus capítulos, requisitos ni niveles de verificación; **no se cita ningún número de requisito de ASVS**. El nivel que usaría la persona revisora no está decidido |
| [OWASP, Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html) | `DEBUG`, `SECRET_KEY`, `check --deploy`, redirección a HTTPS, HSTS, cookies seguras, CSRF, XSS, clickjacking, validadores de contraseña, limitación de intentos | Leída por resumen, 21-oct-2026 | No cubre la subida de archivos. Su recomendación de una política de seguridad de contenido (CSP) usa el middleware de Django 6.0 o posterior, que **no existe en la 5.2 LTS elegida** |
| OWASP Cheat Sheets de autenticación, autenticación multifactor, restablecimiento de contraseña, subida de archivos y registros | Puntos de las áreas 1, 3 y 4 | Leídas por resumen en sesiones anteriores (ver DAS, referencias 5, 26 y 27; diseño técnico, sección 2) | Resúmenes, no lecturas completas |
| NIST SP 800-218 (SSDF), prácticas PW.2.1 y PW.7.1 | Una persona calificada que no participó en el diseño y/o procesos automatizados revisan el diseño; revisión de código por una persona y/o análisis con herramientas | Solo páginas de terceros que reproducen el texto; el PDF no se pudo leer | Marco para organizaciones, usado como referencia |
| Documentación de Django (lista de verificación de despliegue, migraciones, sesiones, bases de datos) y de PostgreSQL (privilegios, roles, `peer`) | Áreas 5, 6 y 7 | Leídas por resumen en sesiones anteriores (DAS, referencias 17 a 35) | Resúmenes |

No hay estudios universitarios en este documento: es una lista de verificación derivada de decisiones del proyecto.

## 3. Datos de la revisión (los completa la persona revisora)
| Dato | Valor |
|---|---|
| Nombre de quien revisa | Pendiente |
| Relación con el proyecto y declaración de que no diseñó ni escribió lo que revisa | Pendiente |
| Calificación o experiencia relevante | Pendiente |
| Fecha de inicio y de fin | Pendiente |
| Versiones de los documentos y del código revisados | Pendiente |
| Nivel de verificación que aplicará (por ejemplo, un nivel de ASVS) | Pendiente; sin decidir |

## 4. Áreas y puntos a verificar
Resultado: Cumple / No cumple / No aplica / No pude verificar. Los identificadores `RV-nn` son locales de este documento.

### Área 1. Cuenta, autenticación y restablecimiento
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-01 | Toda página, salvo el inicio de sesión, exige sesión autenticada **con segundo factor** | RF-26, RNF-01, CA-13 | B | |
| RV-02 | La contraseña tiene al menos 15 caracteres sin reglas de composición, y se guarda con Argon2id con los parámetros mínimos de OWASP | RF-27, ADR-019 | B | |
| RV-03 | Cierre de sesión a las 24 horas y a 1 hora de inactividad; la cookie de sesión es segura | RF-27, CA-48 | B, C | |
| RV-04 | Los códigos de recuperación se guardan con hash, se usan una sola vez y su uso genera el aviso | RF-27, CA-47 | B | |
| RV-05 | El enlace de restablecimiento se guarda con hash, vale 15 minutos, es de un solo uso, solo se envía a la dirección del administrador y **no inicia sesión** | RF-27, CA-59 | B | |
| RV-06 | La solicitud de restablecimiento responde igual y en un tiempo parecido exista o no la cuenta; se rechaza la cuarta solicitud de una hora; al fijar la contraseña se invalidan los demás enlaces y las sesiones abiertas | RF-27, CA-59 | B | |
| RV-07 | Cambiar la contraseña o reemplazar el segundo factor exige la contraseña actual (decisión contra la recomendación: confirmar que el riesgo aceptado consta) | RF-27, diseño técnico 3.6 | A, B | |
| RV-08 | Los avisos de seguridad van a las dos direcciones, no llevan códigos, contraseñas ni enlaces de acceso; si el envío falla, la operación procede, el aviso se reintenta y queda una alerta persistente | RF-27, CA-60, ADR-026 | A, B | |

| RV-48 | Hay un límite de intentos fallidos por cuenta, compartido por contraseña, TOTP y códigos de recuperación: espera creciente (1 minuto tras 5 fallos, duplicándose hasta 1 hora), sin bloqueo permanente, con el restablecimiento de contraseña disponible y un aviso al llegar a 5 | RF-27, CA-68 | B | |
| RV-49 | Se entregan 10 códigos de recuperación guardados con hash; un TOTP aceptado no se reutiliza; emitir códigos nuevos exige la contraseña actual e invalida los anteriores | RF-27, CA-69 | B | |
| RV-50 | La cuenta se crea y se rescata solo con comandos de gestión en el servidor; no existe ninguna pantalla pública de alta ni de rescate | RF-27, CA-70, RN-25 | B, C | |
| RV-51 | Cambiar una dirección de correo exige la contraseña actual y la confirmación en la dirección nueva, y avisa a las dos anteriores (decisión contra la recomendación de exigir además el TOTP: confirmar que el riesgo consta) | RF-27, CA-64 | A, B | |

| RV-52 | La auditoría registra inicios de sesión correctos y fallidos y los eventos de seguridad con la dirección IP de origen, sin contraseñas, códigos ni tokens; la pantalla de consulta es de solo lectura | RF-28, CA-71 | B | |
| RV-53 | Si el proceso diario no corre o falla, hay un aviso registrado, una alerta web persistente y un correo, sin repetir el correo en cada comprobación | RF-49, CA-72 | B, C | |

### Área 2. Autorización y acceso a datos
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-09 | Cada vista comprueba la autorización en el servidor; los identificadores internos son enteros adivinables, así que ninguna vista confía en que el identificador sea impredecible | ADR-028, RNF-02 | B | |
| RV-10 | El sitio de administración de Django no está expuesto ni se usa sobre las tablas de R12 | ADR-027 | B, C | |
| RV-11 | Existe una prueba de acceso denegado sin sesión y sin segundo factor para las vistas de datos personales | RNF-02, CA-11 | B | |

### Área 3. Documentos privados (cédulas)
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-12 | Los archivos están fuera de la raíz web, con nombre aleatorio y sin el número de documento en la ruta; ninguna URL pública los sirve | ADR-003, R11, CA-11 | B, C | |
| RV-13 | La descarga pasa por una vista que comprueba la autorización y registra el acceso (actor, fecha, inquilino) sin guardar la imagen | RF-45, CA-26 | B | |
| RV-14 | Solo se aceptan JPEG y PNG, se verifica el tipo real, el límite es 5 MiB (5 242 880 bytes) y Nginx limita el tamaño de la subida (6m en la ruta de subida de un archivo, 1m en el resto); la reducción en el navegador (RF-50) no cuenta como control | ADR-003, RF-02, RF-50 | B, C | |
| RV-15 | La retención elimina el archivo del almacenamiento, marca la fila y avisa antes de ejecutar | RF-41, CA-28 | B | |

### Área 4. Datos personales y registros
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-16 | La auditoría registra que cambió un campo personal, nunca su valor | RF-28, R14, CA-53 | B | |
| RV-17 | Ningún registro técnico, de auditoría ni de errores contiene datos personales, contraseñas, códigos, tokens ni identificadores de sesión | RF-28, PIM 3.1 (condición 7) | B, C | |
| RV-18 | No se guardan datos personales en la integración continua, en el repositorio ni en la carpeta de respaldos sin cifrar | ADR-024, ADR-025 | B, C | |
| RV-19 | El consentimiento se registra antes de guardar los datos personales de un inquilino | RF-39 | B | |
| RV-20 | La exportación del titular incluye todo su registro y no datos de terceros, y queda registrada en la auditoría | RF-40, RF-45, CA-27 | B | |
| RV-21 | Los correos de notificación no contienen número de documento ni imágenes y limitan los datos del inquilino | RF-44, CA-43 | B | |

### Área 5. Base de datos y roles
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-22 | La aplicación no se conecta como dueña de las tablas; hay tres roles (dueño, aplicación, respaldos) con autenticación `peer` y sin contraseñas de base de datos | ADR-027 | B, C | |
| RV-23 | El rol de la aplicación solo tiene `SELECT` e `INSERT` en movimientos, ajustes, auditoría y accesos a documentos; `DELETE` solo donde se justificó (`django_session`) | ADR-027, R12 | B | |
| RV-24 | Existe una prueba de que PostgreSQL rechaza un `UPDATE` y un `DELETE` sobre un movimiento con el rol de la aplicación | ADR-027, R12 | B | |
| RV-25 | El archivo de privilegios cubre cada tabla y secuencia y una prueba exige una entrada por tabla | ADR-031 | B | |
| RV-26 | La restricción de exclusión impide que dos contratos de una propiedad compartan un día, ignora los anulados y admite contratos abiertos | RN-02, R2, CA-02, ADR-031 | B | |
| RV-27 | Las migraciones se aplican desde cero con el rol dueño y la extensión `btree_gist` se crea en una migración | ADR-031 | B, C | |

### Área 6. Integridad financiera
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-28 | Los importes usan decimales exactos (14 dígitos y 2 decimales), nunca flotantes; el redondeo está en un solo lugar | ADR-031, RN-22 | B | |
| RV-29 | Registrar un abono bloquea la fila con `select_for_update()` dentro de una transacción, sin `nowait`, y varias filas se bloquean siempre en el mismo orden | DAS 10.2, HT-07 | B | |
| RV-30 | Dos abonos simultáneos sobre una obligación nunca dejan un saldo negativo (prueba con `TransactionTestCase` y PostgreSQL) | RN-18, CA-52 | B | |
| RV-31 | Un envío repetido con la misma clave de solicitud no crea otro movimiento | ADR-020, CA-52 | B | |
| RV-32 | Un movimiento no se edita ni se borra: se anula con una reversión y un motivo, y el número de recibo físico es único | RN-22, RF-47, CA-61 | B | |
| RV-33 | Un abono sobre un período futuro más allá del inmediato siguiente se rechaza | RN-15, CA-58 | B | |

### Área 7. Configuración de Django y del servidor
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-34 | `DEBUG` es falso, `SECRET_KEY` no está en el repositorio, `ALLOWED_HOSTS` no está vacío y `check --deploy` no reporta advertencias sin justificar | ADR-025, Django Security Cheat Sheet | B, C | |
| RV-35 | Redirección a HTTPS, HSTS, cookies de sesión y CSRF solo por HTTPS, `X_FRAME_OPTIONS` y `SECURE_CONTENT_TYPE_NOSNIFF` activos | Django Security Cheat Sheet | C | |
| RV-36 | Política de seguridad de contenido: la 5.2 LTS no trae el middleware (es de Django 6.0 o posterior); verificar si se añadió por otra vía o se aceptó la falta | Django Security Cheat Sheet, ADR-022 | A, C | |
| RV-37 | Gunicorn escucha detrás de Nginx; el firewall de DigitalOcean y el del servidor permiten solo lo necesario; el acceso SSH usa claves | ADR-023 | C | |
| RV-38 | El certificado se renueva solo y se probó con `certbot renew --dry-run` | ADR-023 | C | |
| RV-39 | Las dependencias tienen versión fija y se actualizan; no hay secretos en el repositorio ni en la integración continua en texto claro | ADR-025 | B, C | |
| RV-40 | Se aplicó una guía de endurecimiento reconocida (las guías CIS y OWASP aún no se investigaron) | RE-09, DAS 9 | C | |

### Área 8. Respaldos y recuperación
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-41 | El respaldo diario es cifrado, cubre la base, los roles (sin contraseñas) y los documentos, y se sube a Spaces con credenciales distintas de las de pruebas | ADR-024 | C | |
| RV-42 | Las claves de cifrado de los respaldos tienen custodia definida y no están junto a los respaldos | ADR-024 | A, C | |
| RV-43 | Se restauró un respaldo completo en un servidor temporal y se midió frente al RTO de 24 horas; la restauración incluye contratos, movimientos y fotografías | RNF-09 | C | |
| RV-44 | La retención de 35 días de los respaldos se concilia con la desasociación de datos personales | ADR-024, DP-18, RE-11 | A | |

### Área 9. Trazabilidad y pruebas
| Punto | Qué verificar | Referencia | Momento | Resultado y evidencia |
|---|---|---|---|---|
| RV-45 | Cada CA de prioridad Alta de la entrega tiene una prueba escrita que pasa | EPP sección 5, PIM 3.1 | B | |
| RV-46 | El registro de avance refleja el estado real y ninguna entrega con una prueba Alta pendiente figura como terminada | PIM 3.2 | B | |
| RV-47 | `verificar_coherencia.ps1` no reporta problemas y el `CAMBIOS.md` de la entrega existe | CLAUDE.md | B | |

## 5. Qué esta lista no cubre
- Pruebas de penetración por un tercero (fuera del alcance de la estrategia de pruebas).
- Requisitos legales: el solicitante declaró que un abogado los verificó, sin dictamen aportado (ver `../actualizaciones/2026-10-21i_registro-validacion-legal/CAMBIOS.md`).
- Los números de requisito de ASVS y su nivel: no se leyeron.
- Rendimiento y disponibilidad (RNF-08): se miden con la prueba de carga.

## 6. Hallazgos
| ID | Punto | Gravedad | Descripción | Respuesta del solicitante | Estado |
|---|---|---|---|---|---|
| (sin hallazgos todavía) | | | | | |

## 7. Cierre de la revisión
| Dato | Valor |
|---|---|
| Hallazgos Alta abiertos | Pendiente |
| Conclusión de la persona revisora | Pendiente |
| Nombre, fecha y firma de la persona revisora | Pendiente |
| Aceptación del solicitante | Pendiente |

**Fin del documento — LRC-SGA-001, versión 0.1 (borrador no aprobado).**