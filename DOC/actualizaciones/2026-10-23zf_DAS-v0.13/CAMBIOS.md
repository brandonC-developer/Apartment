# Actualización 2026-10-23 (zf) — DAS v0.13: consolidación de las decisiones de seguridad

**Fecha:** 2026-10-23
**Documentos afectados:** [DAS v0.13](../../fase-2-arquitectura/DAS_SGA_001_v0.13_borrador.md) (nuevo; reemplaza a la [v0.12](../../fase-2-arquitectura/DAS_SGA_001_v0.12_borrador.md), que no se edita). Editados en su sitio, solo para declarar la v0.13 como base: [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md), [Modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además los README de las fases 2, 5 y 6 y [DOC/README.md](../../README.md)
**Origen:** las decisiones de las actualizaciones [(y)](../2026-10-23y_br-01-cuentas-proveedores/CAMBIOS.md), [(z)](../2026-10-23z_br-02-autenticacion-correo/CAMBIOS.md), [(za)](../2026-10-23za_br-03-respaldos-clave-spaces/CAMBIOS.md), [(zb)](../2026-10-23zb_br-04-dependencias-python/CAMBIOS.md), [(zc)](../2026-10-23zc_br-08-limite-solicitudes-nginx/CAMBIOS.md) y [(ze)](../2026-10-23ze_br-12-correo-del-administrador/CAMBIOS.md); el solicitante pidió consolidar el DAS v0.13 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Qué es "consolidar" aquí
**No cambia ninguna decisión ya tomada.** Las seis decisiones de seguridad de la v0.12 (ADR-032) estaban en el DAS; las cinco brechas del modelo de amenazas que se decidieron después (BR-01, BR-02, BR-03, BR-04, BR-08) y BR-12 solo constaban en sus `CAMBIOS.md`. La v0.13 las integra en el DAS y cierra los pendientes que dependían de ellas.

## 2. Cambios
| Parte | Cambio |
|---|---|
| Encabezado e historial | Versión 0.13; el párrafo inicial y el historial reflejan la consolidación |
| **ADR-032** | Ampliado de 6 a **11 decisiones**: se añaden cuentas de proveedores y de correo (7), autenticación del correo del dominio (8), respaldos (9), dependencias de Python (10) y límite de solicitudes con AM-04 aceptado (11); el título pasa a "Endurecimiento del servidor y de las cuentas que lo rodean"; se actualizan el fundamento, lo propuesto, lo no verificado y lo pendiente |
| ADR-022 | Cierra el pendiente "forma de instalar Django": `pip` en un entorno virtual con versiones fijadas (queda pendiente solo la versión micro y el estilo de las interfaces internas) |
| ADR-024 | Cierra el pendiente "herramienta y custodia de las claves": `age` a clave pública, clave privada en dos copias fuera de línea, llave de Spaces limitada, versionado y copia mensual; queda pendiente la hora del respaldo y la ausencia del solicitante |
| ADR-025 | Añade `pip-audit` y las alertas de Dependabot |
| ADR-026 | Añade el correo del dominio: subdominio de envío, DMARC y puertos del SMTP del servidor |
| Secciones 9, 11, 12 y 16 | Endurecimiento ampliado; copias de respaldo cifradas; cuatro riesgos nuevos (cuentas de proveedores, dependencias, correo falsificado y AM-04 aceptado); condición adicional antes de cargar datos reales (revisar el modelo de amenazas con otra persona y probar la restauración con la clave de custodia) |
| Sección 17 | Referencia 38 con las fuentes de las decisiones nuevas |
| Anexo A | Cinco filas nuevas; la fila de endurecimiento pasa a "primeras seis medidas" |
| Bases | Los documentos de las fases 3 a 5 y el modelo de amenazas v0.2 declaran la v0.13 |

## 3. Qué no se hizo
- **No se reescribieron los ADR uno por uno:** conservan sus viñetas históricas de decisión, fundamento y "no verificado". Sigue habiendo texto histórico dentro de ellos.
- Sigue pendiente lo que no se decidió: Gunicorn por socket Unix, Nginx (`server_tokens`), PostgreSQL (red, acceso, registro y contraseñas), cifrados TLS, CAA, política de contenido, regla de salida de los firewalls, hora del respaldo, `Automatic-Reboot-WithUsers` y BR-05, 06, 07, 09, 10 y 11.
- **No se editó la ERS:** el segundo factor de las cuentas de proveedores y de correo, y el correo autenticado, son decisiones del DAS y no requisitos de la ERS. Convertirlos en requisito (y qué CA los comprueba) sigue sin decidir.
- No se actualizó el modelo de amenazas con el cierre de BR-12 (v0.3).
- El script comprueba identificadores, enlaces y bases, no el contenido.

## 4. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** todo lo recogido en el ADR-032, decisiones 1 a 11, y el riesgo aceptado AM-04.
- **Propuesta del asistente, sin decidir:** lo enumerado como "propuesta" en el propio ADR-032.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
