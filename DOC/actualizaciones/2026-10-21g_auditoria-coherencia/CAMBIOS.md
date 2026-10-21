# Actualización 2026-10-21 (g) — Auditoría de enlaces, vigencia y coherencia

**Fecha:** 2026-10-21
**Documentos afectados:** correcciones puntuales en [ERS v1.9](../../fase-1-ers/ERS_SGA_001_v1.9_borrador.md) y [DAS v0.11](../../fase-2-arquitectura/DAS_SGA_001_v0.11_borrador.md); [DOC/README.md](../../README.md)
**Estado:** borrador; no aprobado

## 1. Motivo
Petición del solicitante: verificar que todos los archivos estén enlazados y actualizados y comparar los documentos entre sí, con análisis profundo, tras la ERS v1.9 y el DAS v0.11.

## 2. Método
Scripts desechables (no guardados en el proyecto) más el `verificar_coherencia.ps1`:
1. Enlaces relativos de los 63 archivos `.md` y existencia del destino.
2. Archivos de cada carpeta de fase frente a su README, y viceversa; carpetas de `actualizaciones/` frente a `DOC/README.md`.
3. Referencias a versiones dentro de los documentos vigentes.
4. IDs citados en el diseño técnico, la estrategia de pruebas y el modelo de datos frente a los definidos en la ERS v1.9 y el DAS v0.11.
5. Cobertura de la ERS: la matriz de trazabilidad para RF, RN, RNF y CA, el mapa OL → requisito, y la cobertura de CA en la estrategia de pruebas.
6. Búsqueda manual de restos de WhatsApp, comprobante, "notificación de recuperación" y "próxima versión" en los documentos vigentes.
7. Estado de Git.

## 3. Resultados
**Sin problemas:** 0 enlaces rotos; 0 IDs sin definir; la matriz cubre los 47 RF, 30 RN, 18 RNF y 61 CA; las 21 OL tienen requisito o DP; todas las carpetas de `actualizaciones/` (todas con `CAMBIOS.md`) constan en `DOC/README.md`; cada fase tiene su versión vigente indicada; el script oficial da "sin problemas".

**Corregido en esta actualización (en el sitio, porque los documentos no están reemplazados ni aprobados):**
| Dónde | Hallazgo | Corrección |
|---|---|---|
| ERS v1.9, objetivo (sección 1) | Decía "emitir comprobantes de pago" como objetivo de la v1 | Recibo de papel en la v1; comprobantes del sistema en una fase posterior |
| ERS v1.9, objetivo 9 | Igual | Igual |
| DAS v0.11, ADR-012 | "notificación de recuperación" | Avisos de seguridad por correo a dos direcciones (ADR-026) |
| DAS v0.11, sección 4 (obligaciones legales) | "comprobantes" sin matiz | Recibo físico en la v1; comprobantes en una fase posterior |

## 4. Hallazgos sin corregir (documentos desalineados con la ERS v1.9 y el DAS v0.11)
| Documento | Qué falta | Por qué no lo corregí aquí |
|---|---|---|
| Modelo de datos v0.3 | Campo opcional y único "número de recibo físico" en MOVIMIENTO; COMPROBANTE como fase posterior; `canal` y datos de correo de ORGANIZACIÓN y NOTIFICACIÓN (hoy `web` o `whatsapp` y `telefono_whatsapp_admin`); su base cita ERS v1.8 y DAS v0.7 | Requiere versión nueva (v0.4) |
| Estrategia de pruebas v0.2 | CA-58 a CA-61 sin asignar; canal de correo (CA-05, CA-08, CA-09, CA-43 y RNF-05 dicen WhatsApp); CA-37 y CA-54 como fase posterior; cita ERS v1.8 y DAS v0.9 | Requiere versión nueva (v0.3) |
| Diseño técnico v0.6 | Cita ERS v1.8 y DAS v0.10 como base; sigue diciendo "cambios pendientes en la ERS" (3.5, 3.7), HT-04 y HT-09 sin marcar como hechos en la ERS v1.9, y "la ERS v1.8 aún exige WhatsApp" | Requiere versión nueva (v0.7) |
| Resumen para el abogado v2 | Base en ERS v1.8 y DAS v0.7; describe WhatsApp como canal y comprobantes numerados; no incluye factura electrónica, foto de la cédula en la exportación, segunda dirección ni correo con enlace | Requiere versión nueva (v3) y revisión del solicitante, porque es el documento que va al abogado |
| `verificar_coherencia.ps1` | No comprueba el diseño técnico, la estrategia de pruebas, la cobertura de la matriz ni la vigencia fuera de ERS, DAS y MDD (HP-03); por eso estos desalineamientos pasan el script | Ampliar el script cambia una herramienta; se pregunta antes |

**Observaciones menores:** los README de las fases 3 y 4 resumen las versiones antiguas con "se conservan" y no las nombran una a una (las fases 1 y 2 sí); la carpeta `metodologia/` no tiene README (no lo exige `CLAUDE.md`; la describe `DOC/README.md`); el README de `legal/` cita `CAMBIOS.md` como parte de un texto explicativo, no como archivo de esa carpeta.

**Riesgo de pérdida:** 29 entradas de `git status` (nuevas o modificadas) no están confirmadas en Git: ERS v1.9, DAS v0.10 y v0.11, diseño técnico v0.1 a v0.6, estrategia de pruebas v0.1 y v0.2, siete README y las carpetas de `actualizaciones/` desde la 2026-10-20e. No se hizo commit ni push sin preguntar.

## 5. Evidencia y verificación
Salida de los scripts en la sesión; `powershell -File DOC\herramientas\verificar_coherencia.ps1` tras las correcciones: ver cierre de la sesión.

## 6. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente | Pendiente |
