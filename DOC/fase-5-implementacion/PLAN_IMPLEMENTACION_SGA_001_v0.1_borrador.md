# Plan de implementación

**Sistema de Gestión de Alquileres**

**Identificador:** PIM-SGA-001
**Versión:** 0.1
**Estado:** Borrador para revisión; no aprobado
**Fecha:** 21 de octubre de 2026
**Base:** ERS-SGA-001 v1.9, DAS-SGA-001 v0.11, MDD-SGA-001 v0.4, DTE-SGA-001 v0.7 y EPP-SGA-001 v0.3 (todos borradores no aprobados)

Este documento propone en qué orden se construiría el SGA y cuándo se daría por terminada cada entrega. **No hay código ni se ha autorizado implementarlo**: la ERS y la arquitectura siguen sin aprobar. Lo que no cita una fuente es **propuesta** del asistente y espera la decisión del solicitante (sección 8). No es asesoría legal; el solicitante declaró que el abogado verificó el contenido legal, sin dictamen aportado (ver `../actualizaciones/2026-10-21i_registro-validacion-legal/CAMBIOS.md`).

## 1. Principio de orden (decisión del solicitante, 21-oct-2026)
**Esqueleto andante primero y después rebanadas verticales, ordenadas por riesgo y por dependencia entre aplicaciones.** Cada entrega es completa de punta a punta (modelo, servicio, pantalla y pruebas) y se despliega. Fue la opción recomendada por el asistente.

## 2. Fuentes
| Fuente | Qué respalda | Cómo se validó | Limitaciones |
|---|---|---|---|
| [Fowler, MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html) | Empezar con un monolito y descubrir los límites antes de dividir | Leída por resumen, 21-oct-2026 | El autor presenta su postura como tentativa |
| Cockburn, esqueleto andante (*walking skeleton*) | Una implementación mínima que recorre de punta a punta una función pequeña, desplegable y probada | Solo resultados de búsqueda (fuentes secundarias que citan a Cockburn); la página original no apareció y la del Agile Alliance dio 404 | No se leyó el original |
| DAS v0.11 (ADR-001, 013, 022 a 031) y EPP v0.3 | Aplicaciones, dependencias, pruebas y prioridades | Leídos (son documentos del proyecto) | Borradores no aprobados |

No hay estudios universitarios en este documento: el orden y los criterios de salida son derivación de los requisitos y del DAS, más criterio del asistente.

## 3. Entregas
Dependencias entre aplicaciones (ADR-030): `nucleo` → `cuentas`, `inquilinos` → `alquileres` → `notificaciones`; `privacidad` depende de `inquilinos`. Las entregas siguen ese orden.

| Entrega | Aplicaciones | Contenido | Requisitos funcionales | RNF | CA | Criterio de salida (propuesta) |
|---|---|---|---|---|---|---|
| E0 Esqueleto | nucleo, cuentas | Proyecto Django, integración continua con PostgreSQL 18, roles y archivo de privilegios (ADR-027, 031), despliegue en el entorno local (etapa A, WSL 2 con Ubuntu-26.04) con HTTPS autofirmado, inicio de sesión con contraseña y segundo factor, códigos de recuperación, sesión, auditoría base, organización y configuración regional, respaldo cifrado y su restauración | RF-26, 27, 28, 33 | RNF-01, 02, 06, 09, 12, 14, 17 | CA-13, 18, 48, 53 | Despliegue repetible con un comando en el entorno local; inicio de sesión con segundo factor; una restauración completa probada desde el respaldo local; pruebas de las restricciones de R12. La restauración desde Spaces y el HTTPS real se prueban en la etapa B |
| E1 Inquilinos | inquilinos | Inquilino, cédulas privadas, consentimiento, accesos a documentos y su auditoría | RF-01, 02, 03, 04, 05, 39, 45 | RNF-03, 15 | CA-01, 11, 25, 26, 29 | Cédula servida solo por la vista con autorización y registrada; acceso denegado sin sesión |
| E2 Contratos y obligaciones | alquileres, nucleo | Propiedades, contratos y condiciones, solape (R2), finalizar y sustituir inquilino, reajuste y corrección, obligaciones por período, estados, saldo de apertura y proceso diario | RF-06, 07, 08, 09, 10, 11, 12, 14, 36, 42, 43 | RNF-04, 16 | CA-02, 03, 10, 12, 14, 22, 24, 30, 31, 32, 36, 39, 40, 49, 50, 51, 55 | Proceso diario idempotente (dos ejecuciones sin duplicados); casos de fin de mes, bisiesto, prorrateo y gracia pasan |
| E3 Movimientos y depósitos | alquileres | Abonos y pagos completos, moneda distinta, anulación, saldo derivado, historial, depósito de garantía, número de recibo físico, rechazo de períodos futuros (RN-15) | RF-13, 15, 16, 29, 30, 31, 32, 34, 35, 38, 47 | — | CA-04, 15, 16, 17, 19, 20, 21, 23, 33, 34, 35, 38, 45, 46, 52, 58, 61 | Saldo nunca negativo ni con dos abonos simultáneos (bloqueo de fila, HT-07); envío repetido no duplica; historial inmutable |
| E4 Notificaciones y cuenta | notificaciones, cuentas | Notificación web y por correo, recordatorios, resumen diario de atraso, reintentos cada minuto, avisos de seguridad, cambio y restablecimiento de contraseña | RF-21, 22, 23, 24, 25, 44 | RNF-05 | CA-05, 08, 09, 41, 42, 43, 44, 47, 59, 60 | Correo simulado que falla no bloquea nada; avisos a dos direcciones; enlace de un solo uso y 15 minutos con sus protecciones |
| E5 Calendario y privacidad | alquileres, privacidad | Calendario mensual y filtros, solicitudes del titular y su exportación, retención y desasociación, incidentes de seguridad y su constancia, preparación de la carga inicial por digitación con conciliación (sección 5) | RF-17, 18, 19, 20, 40, 41, 46 | RNF-13 | CA-06, 07, 27, 28, 56, 57 | Exportación con todo el registro y su auditoría; retención con aviso previo; plazo de cinco días hábiles |
| E6 Etapa B y salida | todas | Contratar los servicios (dominio, Droplet de pruebas, Spaces, Resend), endurecimiento del servidor real, HTTPS con Certbot, restauración desde Spaces, entregabilidad del correo, prueba de carga, restauración mensual y trimestral, documento de seguridad, ensayo de salida y paso a producción | — | RNF-07, 08, 10, 11, 18 | — | Percentil 95 menor de 2 s con 50 propiedades en el Droplet de pruebas; restauración desde Spaces medida frente al RTO; correo entregado en una cuenta real; revisión de código sin cubrir de los módulos críticos |
| Posterior | alquileres | Comprobante numerado generado por el sistema (fase posterior por decisión del 21-oct-2026) | RF-37 | — | CA-37, 54 | Fuera de la v1 |

### 3.1 Definición de terminado (decisión del solicitante, 21-oct-2026)
Una entrega se da por terminada cuando cumple **todas** estas condiciones comunes **y** su criterio de salida propio de la tabla anterior. Si falta alguna, la entrega no se da por terminada. La lista es propuesta del asistente y el solicitante la aceptó (opción recomendada); apoya el concepto de "definición de terminado" de la Scrum Guide (leída por resumen el 21-oct-2026; es una guía de Scrum y aquí se usa solo como referencia de concepto).

| # | Condición común | Origen |
|---|---|---|
| 1 | Las pruebas de los CA asignados a la entrega pasan en la integración continua con PostgreSQL 18. Ninguna prueba de prioridad Alta queda sin escribir; una Media solo con aceptación escrita del solicitante; una Baja puede diferirse | EPP v0.3, sección 11 (decisión 7) |
| 2 | La integración continua está en verde: pruebas, `check --deploy` y migraciones aplicadas desde cero | ADR-025 |
| 3 | `verificar_coherencia.ps1` no reporta problemas | CLAUDE.md |
| 4 | Cada tabla o secuencia nueva consta en el archivo de privilegios y su prueba pasa | ADR-027, ADR-031 |
| 5 | Se revisó el código sin cubrir de los módulos críticos (períodos, prorrateo, reajuste, movimientos y plazos legales); sin umbral numérico de cobertura | EPP v0.3, sección 9 |
| 6 | La entrega está desplegada en el entorno de la etapa A (WSL 2 con Ubuntu-26.04) con datos ficticios, y cumple su criterio de salida propio | Este documento |
| 7 | Ningún dato personal ni secreto aparece en los registros ni en la auditoría | ERS RF-28, RNF-06; modelo de datos R14 |
| 8 | Hay un `CAMBIOS.md` de la entrega y la trazabilidad (RF, CA, ADR) está al día | CLAUDE.md |
| 9 | No queda abierto ningún defecto conocido de prioridad Alta | Este documento (propuesta) |
### 3.2 Seguimiento del avance (decisión del solicitante, 21-oct-2026)
Opción recomendada por el asistente. Reglas completas en [`AVANCE_IMPLEMENTACION.md`](AVANCE_IMPLEMENTACION.md):
- **Una entrega a la vez** (límite de trabajo en curso de 1): no se empieza la siguiente hasta que la actual cumpla la definición de terminado.
- **Registro de avance:** el archivo `AVANCE_IMPLEMENTACION.md`, solo de adiciones, con una fila por entrega (estado, fechas, condiciones de terminado cumplidas, CA aprobados sobre asignados, desviaciones y enlace a su `CAMBIOS.md`).
- **Si falta una prueba de prioridad Alta, la entrega queda *bloqueada*, no *terminada*.** Las únicas salidas son completarla o un cambio de alcance escrito (nueva versión del plan y `CAMBIOS.md` con la decisión del solicitante). Una Alta no se difiere por decisión de la entrega.
- **Media y Baja:** una Media solo se difiere con aceptación escrita del solicitante; una Baja puede diferirse; toda diferida se anota.

Fuentes (por resumen, 21-oct-2026): Kanban Guide (kanbanguides.org: límite de trabajo en curso y políticas explícitas) y Scrum Guide (lo que no cumple la definición de terminado no se entrega). Son guías de metodologías ágiles, usadas como referencia de concepto; ninguna habla de equipos de una sola persona. El archivo de avance y sus estados son propuesta del asistente.
## 4. Condiciones antes de cargar datos reales
Tomadas de la ERS (DP-08, RNF-09, RNF-14, RNF-18) y del DAS (sección 11); son del asistente en cuanto a su agrupación:
- Servidor endurecido (las guías de endurecimiento aún no se investigaron, RE-09).
- Una prueba de restauración superada.
- Revisión legal cerrada: el solicitante declaró que el abogado la verificó, sin dictamen aportado (DP-17 a DP-21 siguen abiertos en los documentos).
- Dominio comprado y servicio de correo verificado (entregabilidad, términos y registros DNS).
- Aprobación formal de la ERS y del DAS.

## 5. Carga inicial de datos (decisión del solicitante, 21-oct-2026)
**Decisión:** los inquilinos, los contratos y los saldos de apertura se cargan **digitándolos por las pantallas del sistema**, sin script de importación, y se concilian después contra los registros actuales del solicitante. Fue la opción recomendada por el asistente. La función del saldo de apertura (RF-43, CA-49) existe desde la E2; la carga real ocurre después de la E5 y de cumplir las condiciones de la sección 4.

**Procedimiento propuesto (del asistente; solo la decisión anterior es del solicitante):**
1. **Origen:** el solicitante prepara sus registros actuales fuera del sistema y del repositorio, porque contienen datos personales.
2. **Ensayo:** al menos dos ensayos con datos ficticios en el entorno de pruebas, incluida una reversión.
3. **Carga real:** cada inquilino se guarda con su consentimiento registrado (fecha, versión del texto y medio) y su cédula subida, como exige RF-39; no se cargan datos reales antes de las condiciones de la sección 4.
4. **Conciliación:** el número de inquilinos, propiedades y contratos, y el saldo de apertura de cada contrato y su total, contra el origen; una diferencia, por pequeña que sea, se investiga. Con hasta 50 propiedades se revisan todos los registros y no una muestra.
5. **Reversión:** un respaldo completo inmediatamente antes de la carga; si la conciliación falla, se restaura (los movimientos son inmutables, RN-22, y el rol de la aplicación no puede borrar el historial, ADR-027).
6. **Constancia:** un registro de la carga en el repositorio (fecha, quién, resultado de la conciliación y diferencias) sin ningún dato personal.

**Fuentes (solo resultados de búsqueda, nivel bajo):** blogs y consultoras (KPMG, Redwerk y glosarios de migración de datos): ensayos previos, conciliación de conteos, totales y saldos, tolerancia mínima de diferencias y punto de reversión probado. Ninguna compara digitar con importar en un conjunto pequeño: esa elección es criterio del asistente, apoyada en el volumen de la ERS (DP-06).

**Pendiente:** el formato y la ubicación de los registros de origen; si todos los inquilinos actuales pueden dar o tienen ya el consentimiento (RF-39, DP-21); quién concilia (hoy la misma persona que digita, DP-23); cuándo se hace la carga real.
## 5.1 Etapas, entornos, región y tamaño (decisiones del solicitante, 21-oct-2026)
**Planteamiento del solicitante:** primero se despliega todo **en local y gratis**, se prueba, y solo después se contratan los servicios (DigitalOcean, dominio, Resend). Se registra como dos etapas:

- **Etapa A, local y gratis (US$0):** se construyen, despliegan y prueban las entregas E0 a E5 en la máquina del solicitante.
- **Etapa B, servicios de pago:** cuando la etapa A esté probada se contrata lo que necesita internet y se hace la E6 y el paso a producción.

**Entorno de la etapa A (decisión del solicitante, opción recomendada): sin contenedores, WSL 2 con `Ubuntu-26.04`**, la misma versión que el Droplet (ADR-023), con Nginx, Gunicorn, PostgreSQL 18 con los roles y la autenticación `peer` (ADR-027), temporizadores de systemd y respaldos cifrados a una carpeta local. Se descartó Docker: el criterio de buenas prácticas es la **paridad entre desarrollo y producción** (The Twelve-Factor App, factor X, leída por resumen el 21-oct-2026, que advierte contra servicios distintos en local y en producción), y producción es sin contenedores (ADR-023), con temporizadores de systemd y `peer` que un contenedor no reproduce igual. Docker Desktop, ya instalado en la máquina del solicitante, no se usa. La documentación de Docker (por resumen) presenta los contenedores como una vía de consistencia entre entornos cuando producción también los usa; aquí no es el caso.

**Qué sustituye a cada servicio en la etapa A (propuesta del asistente):**

| En producción (etapa B) | En la etapa A |
|---|---|
| Droplet con Ubuntu 26.04, Nginx, Gunicorn, systemd | WSL 2 con `Ubuntu-26.04` y los mismos servicios |
| PostgreSQL 18, roles y `peer` | Igual, dentro de WSL, por el socket Unix local |
| Respaldos cifrados a Spaces | Respaldos cifrados a una carpeta local |
| Resend con dominio propio | Un buzón local de pruebas; sin dominio |
| HTTPS con Certbot y un dominio | HTTPS local con certificado autofirmado |

**Qué no se prueba en la etapa A y queda para la B:** la renovación real del certificado, la restauración desde Spaces, la entregabilidad del correo, el rendimiento en el hardware del Droplet y el endurecimiento del servidor real.

**Verificado en la máquina del solicitante (21-oct-2026, solo lectura):** Windows 11 compilación 26200, WSL 2 versión 2.6.2.0, `Ubuntu-26.04` disponible en `wsl --list --online`, 15,7 GB de memoria, 18,6 GB libres en C: y solo la distribución `docker-desktop` instalada. La distribución puede moverse a otra unidad si falta espacio. Según la documentación de Microsoft (por resumen), systemd viene activado por defecto en la versión actual de Ubuntu instalada con `wsl --install`, y los servicios de systemd no mantienen viva la instancia de WSL (hay que dejarla abierta durante las pruebas); no se verificó que `Ubuntu-26.04` lo traiga activo, ni los paquetes de PostgreSQL 18 en esa versión.

| Entorno | Uso | Tamaño y costo |
|---|---|---|
| Local del desarrollador | Unitarias, integración y vistas, con datos sintéticos | US$0 |
| Etapa A: WSL 2 con Ubuntu-26.04 | Despliegue de cada entrega E0 a E5, con datos ficticios | US$0 |
| Integración continua (GitHub Actions) | Pruebas, `check --deploy` y migraciones contra PostgreSQL 18 | Según el plan de GitHub (ADR-025) |
| Etapa B: Droplet de pruebas temporal (DigitalOcean, NYC3) | Restauración desde Spaces, HTTPS real, temporizador, prueba de carga; se crea y se destruye | 2 GiB y 1 vCPU, facturación por segundo (la página de precios lo indica desde el 1-ene-2026) |
| Etapa B: producción (DigitalOcean, NYC3) | Datos reales, solo tras las condiciones de la sección 4 | 2 GiB y 1 vCPU, US$12 al mes; respaldo semanal 20 % (US$2,40); Spaces US$5; unos **US$19,40 al mes**, más el dominio |

**Región y tamaño de la etapa B (decisiones del solicitante, opciones recomendadas):** NYC3 y 2 GiB y 1 vCPU. Fuentes: disponibilidad regional y precios de Droplets de DigitalOcean, por resumen el 21-oct-2026 (la de precios no indica moneda ni fecha; asumo dólares). Los precios se reconfirman al contratar; no se contrata nada antes de terminar la etapa A. Detalle y límites en el ADR-023 del DAS.

**Condición de revisión:** si la prueba de carga (RNF-08, menos de 2 s en el percentil 95 con 50 propiedades) no cumple en la etapa B, se pasa al plan de 2 vCPU y 2 GiB (US$18). No se midió nada todavía.
## 5.2 Versiones (decisión del solicitante, 21-oct-2026)
**Django 5.2 LTS con el Python 3.14 del sistema** (el de Ubuntu 26.04), en la etapa A y en la B. Opción recomendada por el asistente. Se fijan las versiones exactas (micro) al crear el entorno y se vuelve a evaluar el salto a la 6.2 LTS después de abril de 2027, antes de que termine el soporte de la 5.2 (abril de 2028). PostgreSQL 18 es la versión de Ubuntu 26.04 (ADR-002). Fuentes y límites en el ADR-022 del DAS: Django (descargas y FAQ de instalación), la guía de versiones de Python y las notas de Ubuntu 26.04, todas leídas por resumen el 21-oct-2026.
## 6. Hallazgos
| ID | Hallazgo | Propuesta |
|---|---|---|
| HI-01 | El orden por dependencia pone `notificaciones` después de `alquileres`, pero `cuentas` envía avisos de seguridad por `notificaciones` (ADR-030): la E0 queda sin avisos por correo | En la E0, el aviso de seguridad se registra y se muestra solo como alerta en la web; el envío por correo llega en la E4 |
| HI-02 | CA-47 (recuperación con aviso) y CA-18 (configuración regional) mezclan dos entregas | CA-47 se verifica en la E4 (con el aviso) y su parte de códigos de recuperación en la E0; CA-18 en la E0 |
| HI-03 | Un solo desarrollador, que además decide el negocio: no hay revisión por otra persona (DP-23) | Registrar en cada entrega qué se revisó y cómo; no es un reemplazo de la revisión independiente |

HI-nn es un identificador local de este documento, no de la lista compartida del proyecto.

## 7. Qué no cubre este borrador
- Estimaciones de tiempo o de esfuerzo: no se hicieron.
- Casos de prueba detallados (se escriben con cada entrega, EPP).
- La integración con WhatsApp: fuera de la v1 (DP-04).
- El plan de operación de la fase 6 (monitoreo, procedimiento ante un aviso inesperado).

## 8. Decisiones y pendientes
**Decidido el 21-oct-2026:** el principio de orden (sección 1), la definición de terminado (sección 3.1), la carga inicial por digitación con conciliación (sección 5) y las dos etapas (local y gratis primero, servicios de pago después), el entorno sin contenedores en WSL 2 con Ubuntu-26.04, la región y el tamaño de la etapa B (sección 5.1) las versiones de Python y Django (sección 5.2) y el seguimiento del avance (sección 3.2).

**Pendientes del solicitante, uno por uno:**
1. ~~Definición de "terminado"~~ Resuelta (sección 3.1). Los criterios de salida propios de cada entrega siguen siendo propuesta del asistente.
2. ~~Plan de carga inicial de datos~~ Resuelto en lo esencial (sección 5); quedan el formato del origen, el consentimiento de los inquilinos actuales, quién concilia y cuándo.
3. ~~Entornos, tamaño del Droplet y región~~ Resuelto (sección 5.1).
4. ~~Versiones de Python y Django~~ Resuelto (sección 5.2); quedan las versiones exactas (micro) al crear el entorno y la forma de instalar Django.
5. ~~Cómo se registra el avance y qué hacer si una entrega Alta no se completa~~ Resuelto (sección 3.2 y `AVANCE_IMPLEMENTACION.md`).
6. Revisión por otra persona (DP-23).

## 9. Condiciones para aprobar este documento
- Aprobar la ERS v1.9 y el DAS v0.11.
- Resolver los pendientes de la sección 8.
- Revisión por otra persona distinta del autor (hoy el solicitante ocupa los tres roles, DP-23).

## Registro de aprobación

| Rol | Nombre | Resultado | Fecha |
|---|---|---|---|
| Responsable del negocio | Pendiente | Pendiente | Pendiente |
| Responsable técnico | Pendiente | Pendiente | Pendiente |
| Responsable de pruebas | Pendiente | Pendiente | Pendiente |

**Fin del documento — PIM-SGA-001, versión 0.1 (borrador no aprobado).**