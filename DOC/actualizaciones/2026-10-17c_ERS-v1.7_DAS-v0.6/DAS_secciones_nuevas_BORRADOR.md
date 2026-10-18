# Secciones nuevas para el DAS v0.6 (borrador)

> **Estado: incorporado en el DAS v0.6** (secciones 1.1, 4.1 y anexo B), con correcciones. Este archivo se conserva como evidencia; la versión vigente está en el DAS.

**Origen:** la evaluación de la metodología encontró que el DAS v0.5 no tiene sección de restricciones, árbol de requisitos de calidad ni glosario, frente a la plantilla arc42 (fuente: [arc42](https://docs.arc42.org/home/)). Estas secciones **no están aún en el DAS**; se incorporarán al crear la v0.6.

## A. Restricciones

### A.1 Técnicas

| ID | Restricción | Origen |
|---|---|---|
| RE-01 | Se usan herramientas de software libre o sin costo de licencia. | Solicitante, 17-oct-2026 |
| RE-02 | El costo mensual de operación debe ser mínimo; no hay tope numérico definido. | Solicitante, 17-oct-2026 |
| RE-03 | El sistema se aloja en un servidor virtual (VPS) administrado por el solicitante, accesible por internet con HTTPS. | DP-08 |
| RE-04 | No se fija lenguaje, framework ni motor de base de datos; el solicitante no indicó preferencia. | Solicitante, 17-oct-2026 |
| RE-05 | El canal de WhatsApp no depende de un proveedor comercial concreto; se integra mediante una interfaz con un proyecto aparte, aún inexistente. | DP-04 |
| RE-06 | La interfaz funciona en las dos últimas versiones mayores de Chrome, Edge, Firefox y Safari, en escritorio y móvil. | ERS RNF-10 |

### A.2 De recursos y organización

| ID | Restricción | Origen |
|---|---|---|
| RE-07 | Hay una única cuenta administradora y un único usuario humano. | ERS RN-25 |
| RE-08 | Volumen de diseño: hasta 50 propiedades. | ERS RNF-08 |
| RE-09 | La administración del servidor (actualizaciones, firewall, HTTPS, respaldos) recae en el propio solicitante. | DP-08 |

### A.3 Legales y de cumplimiento

| ID | Restricción | Origen |
|---|---|---|
| RE-10 | Las reglas de la Ley 7527 (gracia, reajuste, plazo, garantía, moneda, recibo) y de la Ley 8968 (consentimiento, derechos del titular, retención, seguridad) son obligatorias, sujetas a validación por un abogado. | ERS sección 3; DP-17 |
| RE-11 | Los respaldos deben respetar la eliminación de datos personales por retención (35 días de respaldos). | DP-07; DP-18 |

**Efecto sobre la arquitectura.** RE-01, RE-02 y RE-09 empujan hacia pocas piezas y software con comunidad amplia. El monolito modular (ADR-001) encaja con ellas, pero no se justifica por ellas: lo justifica el volumen. RE-09 es un riesgo operativo: el solicitante, y no una plataforma, asume la seguridad del servidor.

## B. Árbol de requisitos de calidad

Escenarios medibles por atributo. Los valores provienen de la ERS v1.6 y de las decisiones DP-07 y DP-08.

| Atributo | Escenario | Medida | Referencia |
|---|---|---|---|
| **Seguridad** | Una persona sin sesión válida pide una foto de cédula | Se deniega; ninguna URL pública sirve el archivo | RF-26, RNF-14, CA-11 |
| | El administrador inicia sesión | Exige contraseña de 15 caracteres o más y segundo factor; sesión de 24 h máximo y 1 h de inactividad | RF-27, CA-48 |
| | Se pierde el segundo factor | Acceso solo con código de recuperación de un solo uso, con aviso al administrador | CA-47 |
| **Integridad financiera** | Se ejecuta dos veces el proceso de generación | No se crean obligaciones duplicadas | RNF-04, CA-03 |
| | Se anula un movimiento | El original se conserva; el saldo y el estado se recalculan | RF-16, CA-34 |
| | Se registran tres movimientos seguidos | Los comprobantes son consecutivos y no se renumeran al anular | RF-37, CA-37 |
| **Disponibilidad y recuperación** | Falla el servidor | Se recupera en 24 h máximo (RTO) con pérdida de datos de 24 h máximo (RPO) | DP-07, RNF-09 |
| | Prueba de restauración | Antes de producir y cada 3 meses | DP-07 |
| **Rendimiento** | El administrador abre el calendario con 50 propiedades | Responde en menos de 2 s en el percentil 95 | RNF-08 |
| **Cumplimiento y privacidad** | Un inquilino pide acceso a sus datos | Se resuelve en 5 días hábiles y sin costo | RF-40, CA-27 |
| | Un contrato terminó hace más de 5 años | Se elimina la foto y se desasocian los datos | RF-41, CA-28 |
| **Confiabilidad de notificaciones** | Falla un envío de WhatsApp | Hasta 5 intentos con espera creciente; el estado financiero no cambia | RF-24, CA-09 |
| | El proceso diario no corrió dos días | Solo se emite la alerta del día actual | CA-42 |
| **Usabilidad y compatibilidad** | Uso desde el celular | Funciona en las dos últimas versiones mayores de los cuatro navegadores | RNF-10 |
| **Mantenibilidad** | Se cambia una regla de reajuste | El cambio queda confinado al módulo de obligaciones | RNF-11 |

## C. Glosario

| Término | Significado |
|---|---|
| Abono | Movimiento parcial de dinero recibido, asociado a una obligación o a un depósito. |
| Anulación | Reversión de un movimiento con motivo; el original se conserva. |
| Anulada | Estado de una obligación cancelada con motivo. |
| Comprobante | Documento numerado de forma consecutiva que respalda un movimiento. |
| Contrato | Acuerdo entre un inquilino y una propiedad con vigencia, monto, moneda y día de vencimiento. |
| Corrección | Cambio retroactivo de monto, vencimiento o período, con motivo. |
| Depósito de garantía | Importe pagado en garantía del contrato; se gestiona aparte del alquiler. |
| Fecha límite de pago | Vencimiento más los días de gracia. |
| Fecha real de recepción | Fecha en que se recibió el dinero; distinta de la fecha/hora de registro. |
| Gracia | Días posteriores al vencimiento en que el pago aún es tolerado (7 por defecto). |
| Importe exigible | Importe que el inquilino debe pagar por una obligación. |
| Movimiento | Registro inmutable de un abono, un saldo de apertura o una anulación. |
| Obligación | Importe exigible de un contrato para un período de alquiler. |
| Pagada | Estado de una obligación con saldo cero. |
| Pendiente | Estado de una obligación con saldo mayor que cero y fecha límite no superada. No confundir con el saldo pendiente. |
| Período de alquiler | Mes que va de un día X al día anterior al mismo día X del mes siguiente. |
| Por decidir | Estado de un contrato cuya fecha de fin venció sin cierre ni renovación. |
| Reajuste | Cambio prospectivo del precio, con tope legal, a partir del período siguiente a la notificación. |
| RPO | Pérdida máxima tolerable de datos (24 h). |
| RTO | Tiempo máximo tolerable sin el sistema (24 h). |
| Saldo de apertura | Deuda previa cargada al registrar un contrato antiguo en el sistema. |
| Saldo pendiente | Importe exigible menos movimientos válidos. |
| Titular de datos | Persona física cuyos datos personales se tratan (el inquilino). |
| Vencida | Estado de una obligación con saldo mayor que cero y fecha límite superada. |
| Vencimiento | Fecha pactada de pago de una obligación. |

## D. Efecto en el DAS v0.6

- Nueva sección de **Restricciones** (A), tras la sección 1.
- Nueva sección **Requisitos de calidad** (B), tras la sección 4.
- Nuevo **Glosario** (C), como anexo.
- El árbol de calidad remite a requisitos que ya existen; no introduce requisitos nuevos.
