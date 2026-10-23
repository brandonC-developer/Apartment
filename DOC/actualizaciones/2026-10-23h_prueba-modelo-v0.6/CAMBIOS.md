# Actualización 2026-10-23 (h) — Prueba del modelo de datos v0.6 en PostgreSQL

**Fecha:** 2026-10-23
**Documentos afectados:** [Modelo de datos v0.6](../../fase-3-diseno-tecnico/MODELO_DATOS_SGA_001_v0.6_borrador.md) (sección 12.2 nueva y correcciones de la 12.1), [README de la fase 3](../../fase-3-diseno-tecnico/README.md) y [DOC/README.md](../../README.md); nota de corrección en la [actualización 2026-10-22 (m)](../2026-10-22m_prueba-modelo-v0.5/CAMBIOS.md). La v0.6 se edita en su sitio porque es un borrador del mismo día, no reemplazado ni aprobado.
**Origen:** pendiente de la [actualización 2026-10-23 (g)](../2026-10-23g_modelo-datos-v0.6/CAMBIOS.md) ("sin probar en PostgreSQL")
**Estado:** autoverificación del asistente; no es revisión por otra persona

## 1. Qué se hizo
- Servidor PostgreSQL 18.4 desechable en el puerto 54329, con directorio de datos temporal; se arrancó, se probó y se borró. **No se tocó el servicio de PostgreSQL instalado**; al terminar el puerto quedó libre y no quedaron directorios temporales.
- Evidencia en [`evidencia/`](evidencia/): [`prueba_modelo_v0.6_postgres.sql`](evidencia/prueba_modelo_v0.6_postgres.sql), [`ejecutar_prueba_v0.6.ps1`](evidencia/ejecutar_prueba_v0.6.ps1) (arranca el servidor, corre el SQL, hace la concurrencia con dos sesiones reales y el patrón del archivo huérfano, y lo borra todo) y [`resultado_prueba_v0.6.txt`](evidencia/resultado_prueba_v0.6.txt).

## 2. Resultado
**37 de 37 comprobaciones de una sola sesión y 6 de 6 pruebas de concurrencia y de archivo huérfano correctas** (la última ejecución).

| Probado | Resultado |
|---|---|
| R26 (contrato sin fotografías, con solo el reverso; con el frente; tras reemplazar el frente) | Cumple; el rechazo no deja contrato |
| R27 (5 242 880 bytes se acepta; 5 242 881, cero bytes y PDF se rechazan, en cédula y en fotografía del contrato) | Cumple |
| Reemplazo rechazado | Se deshace todo; el frente anterior sigue activo |
| Consentimiento vigente antes de agregar una fotografía | Rechaza sin consentimiento |
| R25, R22, R23, R12, R11, R2 y la derivación de RF-51 | Cumplen, como en la v0.5 |
| Concurrencia H18 sin y con bloqueo del contrato | Sin bloqueo: error de R22. Con bloqueo: la segunda espera y se registra (órdenes 1,2,3,4) |
| Concurrencia R25 (dos reemplazos del mismo frente) | La segunda espera y falla con error de R25; queda un solo frente activo |
| Concurrencia R26 (contrato durante un reemplazo del frente) | Se crea sin esperar; nunca hay un instante visible sin frente |
| Archivo huérfano (patrón de borrar el archivo si falla la transacción) | Con fallo: archivo borrado y sin fila; con confirmación: archivo y fila |

## 3. Errores de la propia prueba (no del modelo)
- **Primera ejecución: 1 falla de 6.** La prueba de R26 exigía que crear el contrato no esperara y midió 2,1 s. Con una medición aparte con `lock_timeout` y sin él, el contrato se creaba en 0,1 s: **el defecto era del cronómetro del script**, que paraba el reloj de la segunda sesión después de esperar a la primera. Se corrigió (la segunda sesión se cierra primero) y se repitió la prueba completa.
- **Consecuencia para la prueba anterior:** el script de la v0.5 tenía el mismo defecto, de modo que la cifra "2,1 s" de espera de R24 y la condición `Segundos >= 2` **no demostraban la espera**. Lo que sí demuestra el bloqueo es el resultado (la segunda sesión solo falla con "no válido" después de que la primera confirma). Está anotado en el modelo v0.6 (12.1) y en la actualización (m). La v0.5 no se editó.
- Un diagnóstico aparte se hizo con archivos en el directorio temporal del trabajo y se borró.

## 4. Hallazgo
Dos reemplazos simultáneos del mismo frente no se corrompen, pero la segunda sesión recibe un error de R25 y el usuario tendría que reintentar. Caso raro con una sola cuenta administradora; **no se propone cambiar nada**, solo queda anotado.

## 5. Límites de la prueba
- **No probado:** que el borrado del archivo ocurra con Django y el disco real (aquí es PowerShell con un archivo simulado: el patrón, no la implementación); el tipo real del archivo (lo verifica la aplicación); tipos físicos con `sqlmigrate`; carga con 50 propiedades; un fallo del proceso entre escribir el archivo y borrarlo (quedaría huérfano; un barrido periódico sería la alternativa).
- R26 se aplica aquí con una función SQL; en la aplicación real la aplica el servicio (propuesta). Los `CHECK` de R11 y R27 son propuestas del asistente.
- Las entidades de apoyo (`inquilino`, `consentimiento`, `propiedad`, `contrato`) son versiones mínimas, no el modelo completo.
- Es autoverificación del asistente, no revisión por otra persona (DP-23).

## 6. Aprobación
| Rol | Nombre | Aprobación | Fecha |
|---|---|---|---|
| Solicitante (todos los roles, DP-23) | Pendiente | Pendiente; las respuestas no son aprobación del documento | Pendiente |
