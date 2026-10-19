# Agencia SEO · noon Clinic

> Manual compartido por todos los agentes. La carpeta empieza por `_` y no es parte de la web
> pública. Repositorio: `lauramesaz/noonclinic` (GitHub Pages, publica al hacer push).
> Web: https://noon.clinic

## 0. Misión

Traer pacientes a noon Clinic (Medellín) desde Google. Desde el 19-oct-2026 hay **dos públicos**
(cada pieza declara el suyo en la cabecera con `"publico"`):

1. **`"publico": "colombia"`** · pacientes que viven en Colombia (Medellín, Antioquia y el resto del
   país) y buscan en español la cirugía o el tratamiento en sí: "mentoplastia y rinoplastia",
   "cuánto dura el bótox", "criolipólisis o lipo". Es lo que Google ya le está mostrando a noon
   (Search Console, 19-oct: 66 de 129 impresiones). **Solo en español** (sin versión en inglés).
   Incluye **medicina estética**, que hasta ahora no tenía ninguna guía.
2. **`"publico": "eeuu"`** · pacientes que viven en Estados Unidos, sobre todo colombianos y latinos
   de las ciudades de `estrategia.md` (Miami, Nueva York y Nueva Jersey, Orlando y Tampa, Houston,
   Atlanta, Boston). Siempre en **los dos idiomas**: versión en español y versión en inglés,
   enlazadas entre sí (`par`). Si una pieza no dice `publico`, se entiende `eeuu`.

**Meta: 1 pieza nueva al día** (o 1 actualización de una vieja), en el orden de `temas.md`.

## 1. Marca noon (tono)

- "Quiet confidence": seguro, sobrio, cálido. Nada de exclamaciones, emojis ni "¡increíble!".
- Frases cortas. Párrafos de 2 a 4 líneas. Tuteo en español; "you" en inglés.
- Nunca precios (la web pública de noon NO muestra precios). Si el tema es costo, se habla de
  qué incluye, qué no y por qué el valor se define en la valoración.
- Nunca comparar con otras clínicas por nombre. Nunca descalificar a médicos de EE. UU.
- Especialistas reales: Dr. Fernando Ruiz (cirujano plástico) y Dra. Valeria Enciso (médica
  estética). No inventar títulos, años de experiencia ni registros. Firma: "Equipo noon Clinic".
- La cirugía se hace en quirófano, en **Q2** (sede quirúrgica), nunca en consultorio.

## 2. Reglas de oro médicas y legales (contenido de salud, YMYL)

1. **Nada inventado.** Solo cifras, rutas de vuelo, normas migratorias y datos que estén en
   `hechos.md` (verificados, con fuente). Si no está ahí, no se escribe o se dice de forma general.
2. Nunca prometer resultados ni "sin riesgo". "Todo procedimiento tiene riesgos."
3. Nunca dar días exactos para volar después de una cirugía como regla: siempre "cuando tu
   especialista lo autorice". Se pueden dar los rangos de estadía que ya usa la web
   (`otra-ciudad.html`): rostro 1–2 semanas, senos 1–2 semanas, contorno corporal y combinadas
   2–3 semanas, medicina estética mismo día o pocos días.
4. La valoración es **presencial** en Medellín. Por WhatsApp se adelanta información y se agenda;
   no se diagnostica ni se "aprueba" a nadie a distancia.
5. Viaja acompañada/acompañado si es cirugía (un adulto los primeros días).
6. El aviso médico lo pone la plantilla automáticamente; no lo quites ni lo contradigas.

## 3. SEO (cómo posicionar)

- **1 keyword principal por pieza** + 3 a 5 secundarias. Debe ir en `title`, `h1`, primer
  párrafo, un `<h2>` y la `descripcion`.
- `title` ≤ 60 caracteres (la plantilla añade " · noon Clinic"). `descripcion` 140–160 caracteres,
  con un dato concreto, distinta en cada pieza.
- **Público Colombia** = keyword como la escribe alguien en Colombia, sin "desde" ni "viviendo en
  EE. UU." ("rinoplastia y mentoplastia al mismo tiempo", "cuánto dura el ácido hialurónico en
  labios", "criolipólisis o liposucción"). Situaciones reales de aquí: pedir la incapacidad en el
  trabajo, quién te acompaña los primeros días, el sol de Medellín y las manchas, la temporada de
  fin de año. El cierre y el WhatsApp los pone la plantilla según `publico`.
- **Español (público EE. UU.)** = keyword en español como la escribe un latino en EE. UU. ("operarme en Colombia",
  "cirugía plástica en Medellín", "desde Miami"). **Inglés** = como la escribe un estadounidense
  ("plastic surgery in Medellin", "medical tourism Colombia", "tummy tuck Colombia"). La versión en
  inglés NO es una traducción literal: se adapta la keyword, los ejemplos y el orden.
- **Medellín** aparece natural en el primer párrafo, en un `<h2>` y en la descripción.
- **Cada búsqueda tiene UNA página dueña. Las guías no le roban la keyword a la página que vende.**
  "Mentoplastia en Medellín", "lipotransferencia glútea en Medellín", "bótox en Medellín" (el nombre
  del procedimiento + la ciudad, sin más) son de la página del procedimiento (`mentoplastia.html`…).
  Una guía nunca lleva como `title` o `keyword` solo "<procedimiento> en Medellín": siempre suma un
  ángulo o un calificador ("…: recuperación semana a semana", "… o …", "¿cuánto dura…?", "…desde
  EE. UU."). Antes de escribir, busca en `registro.md`, `articulos/` y `../datos_noon.py` si la
  keyword ya tiene dueña. **En inglés** (desde el 19-oct-2026) cada procedimiento tiene su página en
  `../fichas_en.py` (`rhinoplasty-medellin`, `tummy-tuck-medellin`, `botox-medellin`…): esa página es
  la dueña de "<procedure> in Medellín"; las guías en inglés llevan el ángulo de viaje ("…from the
  US", "trip guide", "how long to stay") y enlazan a esa página en el texto.
- **Enlace a la página que vende, dentro del texto:** en el primer tercio de la guía, un enlace
  natural a la página del procedimiento principal (ej. `<a href="mentoplastia.html">mentoplastia</a>`),
  además de los botones de `procedimientos`.
- **Fuentes oficiales:** cada guía con datos de salud enlaza al menos 1 fuente oficial que ya esté
  en `hechos.md` (ASPS, FDA, CDC, MinSalud, INVIMA, RETHUS, REPS, SCCP). Si la guía dice "verifica a
  tu cirujano en RETHUS" o "revisa el REPS", enlaza el buscador oficial (direcciones en `hechos.md`).
- **Páginas de ciudad (`tipo: "ciudad"`) = una por ciudad e idioma.** Prohibido el "copia y
  cambia el nombre": Google castiga las páginas puerta (doorway pages). Cada página de ciudad
  debe tener al menos 4 elementos propios y verdaderos de esa ciudad (vuelos, comunidad,
  barrios, diferencia horaria, temporadas de viaje, cómo es la vuelta a casa en esa ruta).
- **Enlaces internos:** cada pieza enlaza a 1–3 procedimientos (`procedimientos` en la cabecera,
  la plantilla pone los botones) + dentro del texto a 1–2 guías hermanas y a `otra-ciudad` o
  `seguridad` cuando aplique (`otra-ciudad` solo para quien viaja). En inglés las páginas de
  procedimiento tienen versión en inglés (los botones de `procedimientos` llevan solos a ella).
- **FAQ:** 3 a 6 preguntas reales (las que la gente escribe en Google). La plantilla genera el
  JSON-LD `FAQPage`, `MedicalWebPage` y `BreadcrumbList` y el `hreflang`. No lo escribas a mano.
- Slugs en minúsculas con guiones, sin tildes. Español: `cirugia-plastica-en-medellin-desde-miami`.
  Inglés: `plastic-surgery-in-medellin-from-miami`.
- Direcciones limpias: los enlaces van como `seguridad.html` en la fuente; `build.py` les quita el
  `.html` solo.
- **Blog:** cada guía publicada sale sola como tarjeta con foto en `/blog` (español) y `/guides`
  (inglés), en "Lecturas relacionadas" de las cirugías de su `procedimientos` y, si es de las 3 más
  nuevas, en el inicio. El tema (Procedimientos / Medicina estética / Viaje y recuperación /
  Seguridad) y la foto se eligen solos (reglas `TEMAS` en `guias.py`); opcional en la cabecera: `"categoria"` y `"foto"`
  (ruta dentro de `assets/` sin `.jpg`, ej. `"noon/foto-luz"`). El `intro` es el texto de la tarjeta:
  que se entienda solo.

## 4. Que suene a persona, no a IA

Prohibido: raya larga (—) como muletilla, "En este artículo te contamos", "Es importante
destacar", "En conclusión", "sumérgete", "descubre", listas de 3 adjetivos por costumbre,
párrafos todos del mismo largo, cierres que repiten lo dicho. En inglés: "In today's world",
"delve", "navigate the journey", "it's worth noting", "game-changer".
Sí: situaciones reales del lector (si vive afuera: pedir vacaciones, la familia en Colombia, el
vuelo de vuelta, el invierno de Boston; si vive aquí: la incapacidad en el trabajo, quién te cuida
en casa, el sol de Medellín, la cita entre semana), opiniones claras de la clínica respaldadas por las
reglas médicas, y honestidad sobre límites ("no todo se puede hacer en un viaje de una semana").

## 5. Formato de cada pieza (lo que escribe el agente)

Un archivo por idioma en `_agencia-seo/articulos/<slug>.html`. Ver `plantilla-articulo.html`.
Cabecera con `"publico": "colombia"` o `"publico": "eeuu"`. Las de Colombia van sin `par` (solo
español) y sin `ciudad`; si el procedimiento es de medicina estética, `"categoria": "estetica"`.
Cabecera JSON dentro de `<!-- -->` + cuerpo HTML (solo `<p>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`,
`<strong>`, `<a>`, `<blockquote>` y el bloque `<div class="dato">`). Nada de estilos ni scripts.
Primer párrafo con `class="entrada"`. Largo: 700–1.200 palabras.

## 6. Publicar

```
cd <carpeta del repositorio>
python3 build.py                      # genera páginas, hubs, sitemap.xml y robots.txt
git add -A && git commit -m "guía: <título>"
git pull --rebase && git push
```
Luego verificar que `https://noon.clinic/<slug>` responde 200 (1–3 min) y anotar en `registro.md`.
Fase actual: **automática** (aprobada por Laura): la rutina diaria publica sola con red de
seguridad (se publica, se avisa y queda en el registro).

## 7. Si algo no rinde

Política: **actualizar, no borrar.** Si en 3 meses una pieza no tiene impresiones en Search
Console, se mejora (título, profundidad, enlaces) y se cambia `actualizado`.
Los datos de Search Console están en `search-console.md` (los actualiza cada lunes una tarea en la
Mac de Laura, porque la nube no puede abrir Search Console). Úsalos para elegir y mejorar temas.
