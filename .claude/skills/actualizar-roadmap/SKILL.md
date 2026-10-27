---
name: actualizar-roadmap
description: Use después de cada commit (y su push) del SGA, o cuando el usuario pida actualizar el roadmap o la hoja de ruta interactiva; vuelve a publicar el artefacto con el avance real (entregas, grupos de la E2, pruebas, pendientes y último commit).
---

# Actualizar el roadmap interactivo del SGA

El solicitante pidió el 27-oct-2026 que **tras cada commit se actualice el roadmap**. Es una página privada en claude.ai, fuera del repositorio (decisión del solicitante: «Artefacto privado, fuera del repositorio»), así que actualizarla **no es un commit ni cambia la estructura del proyecto**.

- **URL del artefacto:** https://claude.ai/artifact/GuBNtYxitGsiqBjrT8pGEH (se actualiza en el mismo enlace; no crees otro).
- **Cuándo:** cuando el usuario autorizó el commit y este ya se hizo, antes de dar el trabajo por cerrado. Este skill nunca hace `git commit` ni `git push`; esos pasos siguen necesitando la autorización expresa del usuario (CLAUDE.md).

## Pasos

1. **Reúne los datos reales**, sin inventar ninguno:
   - `git log --oneline -1` para el hash del último commit y la fecha de hoy;
   - `DOC/fase-5-implementacion/AVANCE_IMPLEMENTACION.md` (estado de cada entrega, CA aprobados sobre asignados, condiciones cumplidas, fechas);
   - `DOC/fase-5-implementacion/TAREAS_IMPLEMENTACION_SGA.md` (grupos de la entrega en curso marcados `[x]`, tareas pendientes);
   - la última actualización en `DOC/actualizaciones/` (conteo de pruebas en Windows y en WSL).
2. **Lee el artefacto publicado** con `Artifact` `action: "read"` y la URL de arriba. No dependas de un archivo local de una sesión anterior: la copia en la carpeta temporal puede no existir. Si el resultado nombra un archivo guardado con la página completa, trabaja sobre ese.
3. **Cambia solo los datos**, que están en el `<script>`:
   - `ENTREGAS`: `est` (`done`, `doing`, `todo`), `ca` (`[aprobados, asignados]`), `cond`, `ini`, `fin`, `nota`;
   - `GRUPOS`: el tercer valor de cada grupo (1 hecho, 0 pendiente) de la entrega en curso;
   - `PRUEBAS`: un par `[grupo, pruebas en Windows]` por cada cierre de grupo, y el `mx` del gráfico si el máximo lo supera;
   - el sello de la cabecera («Datos al …», hash del commit) y los tres horizontes de la vista Ruta (Ahora, Siguiente, Después);
   - la vista «Pendientes y fuentes», si cambió lo que le toca al usuario o lo abierto en los documentos;
   - la vista Pantallas solo cuando una pantalla del grupo G se escribe de verdad: marca en su nota que ya existe y qué difiere del boceto.
4. **Publica** con `Artifact` y la `url` del artefacto, usando `edits` (old_str/new_str copiados exactos de lo leído) o el archivo completo. No pases `icon` (se conserva). Si ya hay un archivo local de esta sesión con el mismo contenido, publica ese mismo `file_path`.
5. **Comprueba una vez** que el resultado confirme la publicación y dile al usuario en una línea qué cambió (por ejemplo, «Roadmap actualizado: E2 grupo F hecho, 731 pruebas, commit abc1234»).

## Reglas

- Las cifras salen de los documentos; lo que sea propuesta del asistente (horizontes, mockups) sigue marcado como propuesta, y **ningún documento se describe como aprobado**.
- Si una cifra no se puede verificar, déjala como estaba y dilo; no la estimes.
- No pongas en la página datos personales ni los valores de la foto de `img/`; el roadmap no los usa.
- El artefacto es privado: si el usuario quiere que otras personas lo vean, se comparte desde su menú *Share*; tú no puedes cambiarlo.
- Si el artefacto ya no se puede leer o fue eliminado, avisa al usuario antes de crear uno nuevo: sería otro enlace.
