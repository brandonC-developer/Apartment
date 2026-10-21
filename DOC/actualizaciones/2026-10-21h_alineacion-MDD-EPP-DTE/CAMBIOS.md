# Actualización 2026-10-21 (h) — Modelo de datos v0.4, estrategia de pruebas v0.3 y diseño técnico v0.7

**Fecha:** 2026-10-21
**Documentos afectados:** [Modelo de datos v0.4](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.4_borrador.md), [Diseño técnico v0.7](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.7_borrador.md), [Estrategia de pruebas v0.3](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.3_borrador.md); README de las fases 3 y 4 y [DOC/README.md](../../README.md)
**Versiones anteriores:** [MDD v0.3](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.3_borrador.md), [DTE v0.6](../../fase-3-diseno-tecnico/DISENO_TECNICO_SGA_001_v0.6_borrador.md) y [EPP v0.2](../../fase-4-pruebas/ESTRATEGIA_PRUEBAS_SGA_001_v0.2_borrador.md) (se conservan sin cambios)
**Estado:** borrador; no aprobado

## 1. Motivo
La auditoría de la [actualización 2026-10-21 (g)](../2026-10-21g_auditoria-coherencia/CAMBIOS.md) encontró estos tres documentos desalineados con la ERS v1.9 y el DAS v0.11. Esta actualización los alinea. **No contiene decisiones nuevas del solicitante.**

## 2. Cambios
**Modelo de datos v0.4** (base ERS v1.9 y DAS v0.11):
| ID | Descripción | Origen |
|---|---|---|
| `MOVIMIENTO.numero_recibo_fisico`, R16 | Campo opcional, único si no es nulo | RF-47, CA-61 |
| `COMPROBANTE` | Marcado como fase posterior; transacciones y retención ajustadas | RF-37 (fase posterior) |
| `ORGANIZACION` | `correo_admin` y `correo_aviso_persona_confianza`; teléfono y aceptación de WhatsApp pasan a opcionales y futuros | RF-27, RF-44, DP-19 |
| `NOTIFICACION` | Canal `correo`; tipo `aviso_seguridad` con `evento_seguridad` y `destinatario_tipo`; `proximo_intento_en` | RF-23, RF-24, RF-27, ADR-026, ADR-013 |
| `TOKEN_RESTABLECIMIENTO`, R17 | Entidad nueva: hash, vencimiento a 15 minutos, un solo uso | RF-27, CA-59 |
| Transacciones, trazabilidad, H14 | Restablecer contraseña y evento de seguridad; filas de trazabilidad; hallazgo H14 | — |

**Estrategia de pruebas v0.3:** referencias a ERS v1.9 y DAS v0.11; 61 CA asignados (CA-58 a CA-61 nuevos); pruebas del canal de correo (CA-05, CA-08, CA-09, CA-43, RNF-05); CA-37 y CA-54 como fase posterior; HP-01 resuelto en la ERS; HP-03 actualizado.

**Diseño técnico v0.7:** base ERS v1.9, DAS v0.11 y MDD v0.4; los "cambios pendientes en la ERS" pasan a "hechos en la ERS v1.9"; HT-01, HT-02, HT-04, HT-08 y HT-09 apuntan a donde quedaron incorporados.

## 3. Impacto
- El script de coherencia no revisa estos tres documentos; se verificó con scripts desechables (ver sección 6).
- **Propuestas mías, no decididas por el solicitante:** la forma de las entidades nuevas (`TOKEN_RESTABLECIMIENTO`, `evento_seguridad`, `destinatario_tipo`, `proximo_intento_en`) y que el aviso guarde el tipo de destinatario y no la dirección (H14); el reparto de prioridades y niveles de CA-58 a CA-61 en la estrategia de pruebas.
- **Legal:** sin cambios. La dirección de la persona de confianza sigue pendiente (DP-19).

## 4. Decisiones
Ninguna nueva. Se trasladan las ya registradas en las actualizaciones 2026-10-20h y 2026-10-21 a 2026-10-21f.

**Afirmación del solicitante sin registro:** el solicitante indicó, en la conversación, que "ya está verificado por el abogado todo". No consta dictamen, nombre del profesional, fecha ni alcance en `DOC/legal/` ni en ningún documento, y `CLAUDE.md` (reglas 1 y 7) exige ese registro para dar por validada una obligación legal. Por eso los DP-17, DP-18, DP-19, DP-20 y DP-21 y los CA marcados (L) siguen abiertos en los documentos. Se cerrarán cuando se aporte el dictamen.

## 5. Evidencia y fuentes
Las de las actualizaciones citadas; sin fuentes nuevas.

## 6. Verificación
`powershell -File DOC\herramientas\verificar_coherencia.ps1` y scripts desechables: enlaces relativos, README frente a archivos, referencias de versión, IDs citados frente a los definidos, cobertura de la matriz y de los CA en la estrategia. Resultado: ver el cierre de la sesión.

## 7. Aprobación
| Rol | Nombre | Decisión | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente | Pendiente |
