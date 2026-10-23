# Actualización 2026-10-23 (zu) — DAS v0.15: consolidación de las decisiones BR-05, BR-06, BR-07, BR-09 y BR-10

**Fecha:** 2026-10-23
**Documentos afectados:** [DAS v0.15](../../fase-2-arquitectura/DAS_SGA_001_v0.15_borrador.md) (nuevo; reemplaza a la [v0.14](../../fase-2-arquitectura/DAS_SGA_001_v0.14_borrador.md), que no se edita). Editados en su sitio, solo para declarar la v0.15 como base: [Modelo de datos v0.7](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.7_borrador.md), [Modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md), [Plan de implementación v0.1](../../fase-5-implementacion/PLAN_IMPLEMENTACION_SGA_001_v0.1_borrador.md) y [Lista de verificación v0.1](../../fase-5-implementacion/LISTA_REVISION_CRITICA_SGA_001_v0.1_borrador.md); además los README de las fases 2 y 5 y [DOC/README.md](../../README.md)
**Origen:** las decisiones de las actualizaciones [(zo)](../2026-10-23zo_br-05-metadatos-imagenes/CAMBIOS.md), [(zp)](../2026-10-23zp_br-06-antivirus/CAMBIOS.md), [(zq)](../2026-10-23zq_br-07-registros-nginx-gunicorn/CAMBIOS.md), [(zr)](../2026-10-23zr_br-09-dispositivo-y-llave-ssh/CAMBIOS.md) y [(zs)](../2026-10-23zs_br-10-transferencia-a-proveedores/CAMBIOS.md) y la [ERS v1.16](../2026-10-23zt_alineacion-ERS-v1.16/CAMBIOS.md); el solicitante pidió consolidar el DAS v0.15 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Qué es «consolidar» aquí
**No cambia ninguna decisión ya tomada.** Las decisiones solo constaban en sus `CAMBIOS.md`; la v0.15 las integra en el DAS.

## 2. Cambios
| Parte | Cambio |
|---|---|
| Encabezado e historial | Versión 0.15; el párrafo inicial y el historial reflejan la consolidación |
| **ADR-003** | Nueva viñeta «Decisión v0.15»: decodificación completa de la imagen (CA-83), eliminación de metadatos en el servidor (CA-82) y **sin antivirus** (ClamAV pide 3 GiB; el Droplet tiene 2 GiB); el pendiente ya no menciona el antivirus |
| **Sección 10.7**, paso 3, y sección 9 | El servidor decodifica la imagen y elimina los metadatos de los originales sin reducir; DP-27 resuelta |
| **ADR-032** | De 16 a **18 decisiones**: 17 registros de Nginx y Gunicorn (formato propio sin cadena de consulta, Gunicorn sin registro de acceso, 14 días) y 18 dispositivo del administrador y llave SSH (prácticas mínimas en la fase 6; llave física como mejora futura); estado, fundamento (referencia 40) y pendientes actualizados |
| Sección 14 | DP-27 pasa a resueltas; **DP-31** nueva (transferencia de datos a proveedores, para el abogado) |
| Secciones 12 y 16 | Referencia al modelo de amenazas v0.3; la condición previa a datos reales suma la respuesta del abogado a DP-31 |
| Sección 17 y Anexo A | Referencia 40 con las fuentes; cuatro filas nuevas en el anexo |
| Bases | Los documentos de las fases 3 a 5 y el modelo de amenazas v0.3 declaran la v0.15 |

## 3. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** todo lo recogido en el ADR-003 (decisión v0.15) y en el ADR-032, decisiones 17 y 18, y consultar al abogado por la transferencia.
- **Propuesta del asistente, sin decidir:** que decodificar baste sin antivirus, la biblioteca y el método para quitar metadatos, los 14 días y los campos del registro, la lista de prácticas del dispositivo, y la redacción de DP-31.

## 4. Qué no se hizo
- **Las líneas de la v0.14 que cita el modelo de amenazas v0.3 no se actualizaron** (sección 11 del modelo: «ERS v1.15, DAS v0.14» como documentos releídos): es histórico. El modelo de amenazas todavía no recoge las decisiones BR-05, BR-06, BR-07 (Nginx y Gunicorn), BR-09 y BR-10: es una v0.4 por redactar.
- No se reescribieron los ADR uno por uno; el resto del DAS no se releyó. El script comprueba identificadores, enlaces y bases, no el contenido.
- No se verificó ninguna fuente nueva ni se leyó el texto completo de OWASP.
- El resumen para el abogado sigue en la ERS v1.8 y no incluye DP-31.

## 5. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
