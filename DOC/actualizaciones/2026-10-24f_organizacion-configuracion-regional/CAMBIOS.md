# Actualización 2026-10-24 (f) — Organización y configuración regional

**Fecha:** 2026-10-24
**Documentos afectados:** código en [`src/nucleo/`](../../../src/nucleo/models.py), [`TAREAS_IMPLEMENTACION_SGA.md`](../../fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md), [`src/README.md`](../../../src/README.md) y [DOC/README.md](../../README.md). Ningún documento de las fases cambia.
**Origen:** ERS v1.16, RF-33, RNF-12, RNF-17 y CA-18; modelo de datos v0.7 (entidad ORGANIZACION); ADR-005; instrucción del solicitante: «sí, escribe la organización y la configuración regional» (24-oct-2026)
**Estado:** implementado y probado en un PostgreSQL desechable; no aprobado

## 1. Qué se escribió
| Archivo | Contenido | Requisito |
|---|---|---|
| `nucleo/models.py` | `Organizacion`: una sola fila (restricción `id = 1`), zona horaria validada contra IANA (`America/Costa_Rica` por defecto), hora del proceso diario 07:00, nombre y dirección del responsable | RF-33, DP-02, MDD |
| `nucleo/migrations/0002` y `0003` | Tabla y fila inicial con los valores predeterminados | RF-33 |
| `nucleo/organizacion.py` | `actual()` y `actualizar()`, que audita el cambio (campos personales solo por nombre) | RF-28, CA-18 |
| `nucleo/middleware.py` | Activa la zona de la organización en cada petición; si el valor guardado es ilegible usa la predeterminada | RF-33, RNF-12 |
| `nucleo/regional.py` | Monedas CRC y USD, moneda y zona predeterminadas, símbolos | RF-33 |
| `nucleo/formato.py` y `templatetags/formato.py` | Formato propio: fechas dd/mm/aaaa, `180.000,50`, `₡180.000,50`, `3,2 %`; lectura estricta de números y fechas; `Decimal`, nunca `float` | RNF-12, RNF-17 |
| Plantillas | La auditoría y la pantalla de inicio usan el formato propio y la zona de la organización | RNF-12 |

## 2. Propuestas del asistente (sin aprobar)
- **Alcance de la organización en la E0:** solo los atributos que esta entrega usa (zona, hora del proceso, identidad del responsable). Los demás atributos del MDD (dos correos, anticipaciones de recordatorio, retención, días de gracia, WhatsApp) se añaden con la entrega que los necesita, en migraciones propias.
- **Sin pantalla de edición de la organización:** el plan no asigna ninguna a la E0. Hoy se cambia solo con el servicio `actualizar`. Hay que decidir en qué entrega va (ver abajo).
- Símbolo `$` para USD; signo negativo antes del símbolo (`-₡20.000,00`); redondeo de presentación medio hacia arriba; porcentaje con un espacio normal (`3,2 %`, literal de la ERS); horas en formato de 24 h.
- **Lectura estricta:** el punto agrupa de a tres cifras y la coma separa los decimales; `1.5` y `1.234,5.6` se rechazan porque `1.234` sería ambiguo.
- La zona se consulta a la base en cada petición (una fila); no se guarda en caché.

## 3. Puntos por decidir
1. **Decimales en colones:** la ERS muestra `₡180.000,50` en RNF-12 pero `₡180.000` y `₡92.903` en varios CA. La función admite ambos; falta decidir cuál se muestra por defecto (el servicio redondea los importes de colones a unidad entera, ADR-031).
2. **Pantalla para editar la organización** (responsable, zona, hora): sin entrega asignada. Propuesta: E4, donde se configuran las dos direcciones de correo.
3. **Hora del proceso diario (07:00) y zona:** el cambio de la hora afecta al temporizador de systemd (E2/F); el vínculo no existe todavía.

## 4. Verificación
- **121 pruebas pasan** (21 nuevas) en PostgreSQL 18 desechable (ya borrado), Python 3.12 en Windows.
- Se prueba: números, moneda, porcentajes y fechas con casos límite (redondeo de .005 y .995, negativos, separador sin espacio de no separación), `float` rechazado, lectura estricta, ida y vuelta, filtros de plantilla, fila única, fila inicial de la migración, zona inválida, auditoría del cambio sin valores personales, que **cambiar la zona no modifica el instante guardado** (CA-18), y que la pantalla de auditoría usa la zona de la organización y la restablece al terminar.
- **Mutaciones manuales:** un separador de miles distinto, no activar la zona, redondeo medio-par y aceptar `1.5` hicieron fallar sus pruebas; se restauró el código. Una primera mutación del redondeo no valió (error de nombre) y se repitió bien.

## 5. Qué no está hecho
- CA-18 en su parte de contratos en USD (E2). La zona horaria del temporizador del proceso diario (E2/F).
- El resto de la E0: roles de PostgreSQL, WSL, respaldo, CI. 0 de 8 CA de la E0 cumplidos.

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
