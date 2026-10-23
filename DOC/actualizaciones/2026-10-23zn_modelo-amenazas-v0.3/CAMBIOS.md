# Actualización 2026-10-23 (zn) — Modelo de amenazas v0.3

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de amenazas v0.3](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.3_borrador.md) (nuevo; reemplaza a la [v0.2](../../fase-3-diseno-tecnico/MODELO_AMENAZAS_SGA_001_v0.2_borrador.md), que no se edita), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md)
**Origen:** la v0.2 seguía listando BR-11 y BR-12 como abiertas y no recogía las decisiones de PostgreSQL, Gunicorn, Nginx, salida, respaldo, TLS, CAA y reinicio ni los requisitos de la ERS v1.15 (señalado en las actualizaciones (zk) y (zm)); el solicitante pidió redactar la v0.3 (23-oct-2026)
**Estado:** borrador; no aprobado

## 1. Cambios
| Parte | Cambio |
|---|---|
| Encabezado, historial, supuesto 5 | Versión 0.3; las decisiones BR-11 y BR-12 entran en el supuesto de "nada aplicado" |
| AM-03 | Segundo factor en las dos direcciones de avisos (BR-12, RNF-19, CA-80); ya no remite a una brecha |
| AM-06 | PostgreSQL solo por socket, `peer`, `CONNECT` revocado; salida de los firewalls denegada (frena la exfiltración, no impide salir por el 443) |
| AM-12, AM-13 | Cifrados TLS y CAA; `Host` y `X-Forwarded-*` sustituidos, `server_tokens off`, socket de Gunicorn `0660` |
| AM-16 | `Automatic-Reboot-WithUsers` en `false` |
| AM-21, AM-23 | Los controles pasan a ser requisitos: RNF-20/CA-81 y RNF-19/CA-80 |
| AM-25 | Respaldo a las 05:00 y aviso a las 26 horas (RF-53, CA-79); límite: no detecta un servidor caído |
| AM-26 | Registro de PostgreSQL decidido; Nginx y Gunicorn, rotación y retención siguen abiertos |
| AM-27 | El CAA queda atado a la cuenta ACME |
| AM-28 | CSP decidida (BR-11); sin probar con la interfaz |
| Sección 8 | BR-11 y BR-12 **decididas**; BR-07 **parcial**; nota con los requisitos nacidos de las decisiones |
| Fuentes y mantenimiento | Fuentes de las decisiones nuevas; la lista de revisiones apunta a las brechas que siguen abiertas |

**Sin amenazas nuevas y sin cambios de nivel:** siguen 28 amenazas, 1 alto, 20 medios y 7 bajos. Que ningún nivel cambie es juicio del asistente: en una escala de tres niveles los controles nuevos no mueven ninguna casilla.

## 2. Lo que decidió el solicitante y lo que propone el asistente
- **Decidido (23-oct-2026):** BR-11, BR-12, las decisiones 12 a 16 del ADR-032 y los requisitos RF-53, RNF-19 y RNF-20 (actualizaciones (ze), (zg) a (zj), (zl)).
- **Propuesta del asistente, sin decidir:** que los niveles no cambien; BR-05, BR-06, BR-09 y BR-10 y la parte de BR-07 sobre Nginx y Gunicorn siguen siendo propuestas abiertas.

## 3. Qué no se hizo
- **No se releyeron enteras** la ERS v1.15 ni las actualizaciones (zg), (zh) e (zi): se tomaron del ADR-032 (detalle en la sección 11 del modelo).
- No se añadió una amenaza para la salida a internet ni para la CSP rota; no se evaluó si hacen falta.
- No se verificó ningún control: no hay servidor. Sigue sin revisión de otra persona (DP-23).
- El DAS v0.14 todavía cita el modelo de amenazas v0.2 en su historial; no se editó.

## 4. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
