# Actualización 2026-10-21 (m) — ADR-027: roles de la base de datos y R12

**Fecha:** 2026-10-21
**Documentos afectados (editados en su sitio, porque ninguno está reemplazado ni aprobado):** [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md) (ADR-027 nuevo, sección 9, anexo A, referencia 28), [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md) (R12), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md) y [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Motivo
El solicitante preguntó si estaba planeada la gestión de la base de datos frente a las páginas y la API. Se respondió que el modelo es lógico y que faltan seis puntos de diseño físico (esquema y migraciones, aplicación de R12, usuarios y permisos, conexión, formato de identificadores y módulos como aplicaciones de Django). Se empezó por el punto 2.

## 2. Decisión
| # | Pregunta | Decisión del solicitante | Recomendación |
|---|---|---|---|
| 1 | ¿Cómo se aplica R12 (sin `UPDATE` ni `DELETE` por la aplicación sobre el historial)? | Dos roles de base de datos (dueño solo para migraciones; aplicación con solo `SELECT` e `INSERT` en esas tablas) más guardas en Django | Igual |

**Fuentes (leídas por resumen el 21-oct-2026):** PostgreSQL, privilegios (los privilegios son por tabla y por columna; el dueño siempre puede modificar o destruir el objeto); Django, bases de datos (rol de conexión distinto con `assume_role`; no lista los permisos que PostgreSQL exige a Django).

## 3. Cambios
- DAS v0.11: **ADR-027** nuevo; sección 9 (control); anexo A (fila); referencia 28.
- Modelo de datos v0.4: R12 remite al ADR-027.
- Estrategia de pruebas v0.3: la integración incluye la prueba de que el rol de la aplicación es rechazado.

## 4. Propuestas del asistente, no decididas
Los nombres de los roles; los privilegios por columna para las excepciones de R12; ningún `DELETE`; un tercer rol de solo lectura para los respaldos; el paso que concede privilegios tras cada migración.

## 5. Límites
El rol dueño sigue pudiendo modificar todo. No se verificó qué privilegios exige Django a un rol de aplicación en PostgreSQL ni las secuencias de identificadores (dependen de H7, abierto). Un disparador no se adoptó.

## 6. Quedan por revisar (puntos 1, 3, 4, 5 y 6)
Esquema físico y migraciones; usuarios y permisos (el tercer rol es propuesta); conexión; formato de los identificadores (H7); módulos como aplicaciones de Django.

## 7. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1`.