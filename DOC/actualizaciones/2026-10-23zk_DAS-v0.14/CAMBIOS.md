# Actualización 2026-10-23 (zk) — DAS v0.14: consolidación de las decisiones de PostgreSQL, Gunicorn, Nginx, salida, respaldo, TLS, CAA, CSP y reinicio

**Fecha:** 2026-10-23
**Documentos afectados:** [DAS v0.14](../../fase-2-arquitectura/DAS_SGA_001_v0.14_borrador.md) (nuevo; reemplaza a la [v0.13](../../fase-2-arquitectura/DAS_SGA_001_v0.13_borrador.md), que no se edita). Editados en su sitio, solo para declarar la v0.14 como base: [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md), [Modelo de amenazas v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además los README de las fases 2, 5 y 6 y [DOC/README.md](../../README.md)
**Origen:** las decisiones de las actualizaciones [(zg)](../2026-10-23zg_endurecimiento-07-postgresql/CAMBIOS.md), [(zh)](../2026-10-23zh_endurecimiento-08-gunicorn-nginx/CAMBIOS.md), [(zi)](../2026-10-23zi_salida-firewall-y-hora-respaldo/CAMBIOS.md) y [(zj)](../2026-10-23zj_tls-caa-csp-reinicio/CAMBIOS.md); el solicitante pidió consolidar el DAS v0.14 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Qué es "consolidar" aquí
**No cambia ninguna decisión ya tomada.** Las decisiones de PostgreSQL, Gunicorn, Nginx, la salida de los firewalls, el respaldo, TLS, CAA, CSP y el reinicio solo constaban en sus `CAMBIOS.md`. La v0.14 las integra en el DAS y cierra los pendientes que dependían de ellas.

## 2. Cambios
| Parte | Cambio |
|---|---|
| Encabezado e historial | Versión 0.14; el párrafo inicial y el historial reflejan la consolidación |
| **ADR-032** | De 11 a **16 decisiones**: 12 PostgreSQL, 13 Gunicorn y Nginx, 14 salida de los firewalls, 15 hora y aviso del respaldo, 16 cifrados TLS, CAA y CSP; las decisiones 2, 3, 5 y 9 remiten a ellas (la 2 ya no dice "salida sin decidir"; la 3 añade `Automatic-Reboot-WithUsers` en `false`); se actualizan el fundamento (referencia 39), lo propuesto, lo no verificado y lo pendiente |
| ADR-013 | Nueva viñeta "Vigilancia del respaldo": el temporizador de intervalo corto comprueba la marca del último respaldo correcto (26 horas) |
| ADR-024 | Cierra el pendiente "hora del respaldo" (05:00 hora de Costa Rica) |
| ADR-029 | Cierra el pendiente "número de procesos de Gunicorn" (3 workers `sync`) |
| Secciones 9, 11, 12 y 16 | Endurecimiento: solo quedan pendientes la revisión con otra persona y la auditoría con Lynis; la tabla de respaldo suma la hora y el aviso; tres riesgos nuevos (respaldo que falla en silencio, datos personales en los registros de PostgreSQL y una CSP que rompa la interfaz); condición ajustada antes de cargar datos reales |
| Sección 17 | Referencia 39 con las fuentes de las decisiones nuevas |
| Anexo A | Cinco filas nuevas; la de endurecimiento anota que son las primeras seis medidas |
| Bases | Los documentos de las fases 3 a 5 y el modelo de amenazas v0.2 declaran la v0.14 |

## 3. Qué no se hizo
- **No se reescribieron los ADR uno por uno:** conservan sus viñetas históricas.
- **La ERS no se tocó:** los tres requisitos nuevos (segundo factor de las cuentas de proveedores y de correo, correo autenticado y aviso de fallo del respaldo) siguen sin redactar. El DAS ya los menciona como pendientes.
- El **modelo de amenazas** todavía lista BR-11 y BR-12 como abiertas, no recoge el aviso de fallo del respaldo ni los controles nuevos de AM-12, AM-23, AM-25 y AM-28: es una v0.3 por redactar.
- No se releyeron las secciones 7.1 a 7.6 ni la 15, que no cambiaron.
- El script comprueba identificadores, enlaces y bases, no el contenido.

## 4. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** todo lo recogido en el ADR-032, decisiones 1 a 16.
- **Propuesta del asistente, sin decidir:** lo enumerado como "propuesta" en el propio ADR-032, incluidos los valores numéricos de Gunicorn y de los tiempos del proxy, el umbral de 1 000 ms, las 05:00 y las 26 horas del respaldo y la política CSP concreta.

## 5. Qué sigue pendiente
Revisión crítica con otra persona y auditoría con Lynis; OCSP stapling; las brechas BR-05, 06, 07, 09 y 10; los tres requisitos nuevos de la ERS; la rotación y retención de los registros; y todo lo marcado "no verificado" en el ADR-032.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
