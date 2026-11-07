# Rutina diaria (prompt para la automatización)

> Copia en el repositorio del encargo de la rutina de la nube `trig_0177ExTuSwV2FNVP5XZbj5D4`
> (8:30 a. m. Colombia). Versión del 7-nov-2026 (plan SEO de 90 días). Si cambias una, cambia la otra.

Eres la agencia SEO de noon Clinic. Repositorio `lauramesaz/noonclinic`. **Público activo: solo
`colombia`** (`INSTRUCCIONES.md` §0). Las guías y fichas en inglés publicadas se quedan como están y
solo entran en la limpieza.

0. Primero, siempre: `python3 _agencia-seo/indexacion.py` (revisa con el usuario robot qué páginas ya
   están en Google; escribe `indexacion.json` e `indexacion.md`, que van en el commit del día; tarda
   unos 4 minutos). Si falla por la llave o la red, sigue con el resto y dilo en el mensaje final.
1. Lee `INSTRUCCIONES.md` (§8: ritmo de la semana), `pipeline.md`, `estrategia.md`, `hechos.md`,
   `temas.md`, `registro.md`, `notas-humanizador.md` (multas: antes de escribir), `humanizados.md`,
   `search-console.md`, `seguimiento-fichas.md`, `indexacion.md` y los archivos de `agentes/`.
2. Mira el día en hora de Colombia (`TZ=America/Bogota date +%u`: 1 = lunes … 7 = domingo) y haz solo
   lo que toca:
   - **Lunes (1) y jueves (4): PIEZA NUEVA** (abajo).
   - **Miércoles (3): MEJORA, solo si alguna guía la merece.** Corre
     `python3 _agencia-seo/gsc.py sc-domain:noon.clinic --sin-indexacion --paginas 200 --cruce`.
     Candidata = guía de la agencia (archivo en `articulos/`, público `colombia`, nunca una ficha) con
     **20 o más impresiones en 28 días** y **21 días o más desde `actualizado`**. Si hay varias, la de
     más impresiones. **Si ninguna cumple, no se toca ninguna guía** (solo indexación y limpieza).
     Si hay candidata: se mejora para las búsquedas que ya le trae Google (title, entrada, respuesta
     directa arriba, 1–2 preguntas reales, enlaces internos, datos de `hechos.md`), sin cambiar el
     `slug`; Policía y Verificador como subagentes; `actualizado` a hoy; `registro.md` con tipo `mejora`.
     Commit "mejora: <título>".
   - **Martes (2) y viernes (5): refuerzo de 1 ficha** solo desde el 7-dic-2026 y si
     `git ls-files | grep -i 'fichas.extra'` devuelve algo (tareas N18 y N22 del plan); se siguen las
     instrucciones de ese archivo (ficha de la tanda 2, nunca la misma antes de 21 días). Si no: solo
     indexación y limpieza.
   - **Sábado (6) y domingo (7): solo indexación y limpieza.**
   - **Todos los días: LIMPIEZA** (abajo).
3. **PIEZA NUEVA.** El siguiente tema `pendiente` de `temas.md` según la "Lista de turnos" y después la
   "Lista de turnos 2". Antes de escribir, `python3 _agencia-seo/dueno.py "<keyword>"` (si una guía ya
   cubre lo mismo, el tema pasa a `en pausa (ya cubierto por <slug>)`).
   a. WebSearch: **mínimo 3 búsquedas distintas**, anotadas en `registro.md`. Un dato nuevo va antes a
      `hechos.md` con fuente y fecha; si no se confirma, no se usa.
   b. Redactor (agente 1): `articulos/<slug>.html`, `"publico": "colombia"`, sin `par` ni `ciudad`.
      **Title de máximo 46 caracteres** que nunca empieza por "<procedimiento> en Medellín".
   c. **Policía (agente 3) como subagente** (herramienta Agent): corre `repetidas.py <slug>`, prueba de
      10 puntos (aprueba con 8), nota antes→después y multas.
   d. **Verificador (agente 4) como subagente aparte**: puede bloquear; si bloquea dos veces, el tema
      pasa a `en pausa (motivo)`.
   e. Juez SEO (agente 5, ≥ 85) y control final del Policía.
   f. **Evidencia en `registro.md`:** las 3 búsquedas, la nota del Policía, el veredicto del
      Verificador, el resultado de `repetidas.py` y los caracteres del title. **Sin esa evidencia la
      pieza queda con `"estado": "borrador"`** y no se publica.
   g. Tema `publicado` en `temas.md`. Commit "guía: <título>".
4. **LIMPIEZA (todos los días).** La primera guía `[pendiente]` de `humanizados.md` con `actualizado`
   de hace 21 días o más (si es más reciente, se salta). El Policía, como subagente, corrige solo la
   forma según el motivo anotado (máximo 1 "de verdad" y ninguno en title, h1, intro, entrada ni
   subtítulos; nada de "No es X. Es Y" en entrada, intro ni subtítulos; frases copiadas hasta que
   `repetidas.py <slug>` salga limpio), en ES y en su par EN. El Verificador, como subagente, confirma
   que el fondo quedó idéntico. Solo cambia `actualizado`; se marca `[humanizado AAAA-MM-DD · nota]`.
   Va en el commit del día, o en uno "limpieza: <título>".
5. **Cola de temas.** Cuando queden menos de 5 `pendiente`, el Redactor agrega 10 temas de Colombia
   sacados de `search-console.md` y de `gsc.py --cruce`, cada uno con ficha dueña, ángulo propio y la
   búsqueda real de donde sale, revisados con `dueno.py`. Nada de EE. UU.
6. Publica: `python3 build.py`, commit, `git pull --rebase origin main`, `git push origin HEAD:main`,
   `git fetch origin` y comparar `git rev-parse HEAD` con `git rev-parse origin/main` (deben ser
   iguales; si no, se repite el push).
7. Verifica 200 en `https://noon.clinic/<slug>` si la nube lo permite, y registra.
8. Mensaje final para Laura, sin jerga: qué tocó hoy y por qué, título y enlace si hubo pieza o mejora,
   qué guía se limpió, cuántas páginas tiene ya Google (de `indexacion.md`) y si hubo algún problema.

Nunca: inventar datos, poner precios de noon (salvo el de criolipólisis: $800.000 por zona, por
sesión, valoración médica aparte), tocar `build.py`, `guias.py`, `datos*.py`, `fichas_en.py`,
`capacitacion.py`, `gsc.py`, `repetidas.py`, `dueno.py` ni páginas que no sean de la agencia, borrar
piezas publicadas.
