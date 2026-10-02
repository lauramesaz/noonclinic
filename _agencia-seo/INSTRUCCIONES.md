# Agencia SEO internacional · noon Clinic

> Manual compartido por todos los agentes. La carpeta empieza por `_` y `robots.txt` la bloquea:
> no es parte de la web pública. Repositorio: `lauramesaz/noonclinic` (GitHub Pages, publica al hacer push).
> Web: https://noon.clinic

## 0. Misión

Traer a noon Clinic (Medellín) **pacientes que viven en Estados Unidos**, sobre todo colombianos y
latinos de las ciudades de `estrategia.md` (Miami, Nueva York y Nueva Jersey, Orlando y Tampa,
Houston, Atlanta, Boston). Lo logramos con páginas que Google posiciona para búsquedas como
"cirugía plástica en Medellín desde Miami", "plastic surgery in Medellin Colombia", "cuánto tiempo
quedarme en Colombia después de una lipo".

**Meta: 1 pieza nueva al día** (o 1 actualización de una vieja), siempre en **los dos idiomas**:
cada guía tiene su versión en español y su versión en inglés, enlazadas entre sí (`par`).

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

## 3. SEO internacional (cómo posicionar)

- **1 keyword principal por pieza** + 3 a 5 secundarias. Debe ir en `title`, `h1`, primer
  párrafo, un `<h2>` y la `descripcion`.
- `title` ≤ 60 caracteres (la plantilla añade " · noon Clinic"). `descripcion` 140–160 caracteres,
  con un dato concreto, distinta en cada pieza.
- **Español** = keyword en español como la escribe un latino en EE. UU. ("operarme en Colombia",
  "cirugía plástica en Medellín", "desde Miami"). **Inglés** = como la escribe un estadounidense
  ("plastic surgery in Medellin", "medical tourism Colombia", "tummy tuck Colombia"). La versión en
  inglés NO es una traducción literal: se adapta la keyword, los ejemplos y el orden.
- **Medellín** aparece natural en el primer párrafo, en un `<h2>` y en la descripción.
- **Páginas de ciudad (`tipo: "ciudad"`) = una por ciudad e idioma.** Prohibido el "copia y
  cambia el nombre": Google castiga las páginas puerta (doorway pages). Cada página de ciudad
  debe tener al menos 4 elementos propios y verdaderos de esa ciudad (vuelos, comunidad,
  barrios, diferencia horaria, temporadas de viaje, cómo es la vuelta a casa en esa ruta).
- **Enlaces internos:** cada pieza enlaza a 1–3 procedimientos (`procedimientos` en la cabecera,
  la plantilla pone los botones) + dentro del texto a 1–2 guías hermanas y a `otra-ciudad` o
  `seguridad` cuando aplique. En inglés las páginas de procedimiento están en español: se avisa.
- **FAQ:** 3 a 5 preguntas reales (las que la gente escribe en Google). La plantilla genera el
  JSON-LD `FAQPage`, `MedicalWebPage` y `BreadcrumbList` y el `hreflang`. No lo escribas a mano.
- Slugs en minúsculas con guiones, sin tildes. Español: `cirugia-plastica-en-medellin-desde-miami`.
  Inglés: `plastic-surgery-in-medellin-from-miami`.
- Direcciones limpias: los enlaces van como `seguridad.html` en la fuente; `build.py` les quita el
  `.html` solo.

## 4. Que suene a persona, no a IA

Prohibido: raya larga (—) como muletilla, "En este artículo te contamos", "Es importante
destacar", "En conclusión", "sumérgete", "descubre", listas de 3 adjetivos por costumbre,
párrafos todos del mismo largo, cierres que repiten lo dicho. En inglés: "In today's world",
"delve", "navigate the journey", "it's worth noting", "game-changer".
Sí: situaciones reales del paciente que vive afuera (pedir vacaciones, la familia en Colombia,
el vuelo de vuelta, el invierno de Boston), opiniones claras de la clínica respaldadas por las
reglas médicas, y honestidad sobre límites ("no todo se puede hacer en un viaje de una semana").

## 5. Formato de cada pieza (lo que escribe el agente)

Un archivo por idioma en `_agencia-seo/articulos/<slug>.html`. Ver `plantilla-articulo.html`.
Cabecera JSON dentro de `<!-- -->` + cuerpo HTML (solo `<p>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`,
`<strong>`, `<a>`, `<blockquote>` y el bloque `<div class="dato">`). Nada de estilos ni scripts.
Primer párrafo con `class="entrada"`. Largo: 700–1.200 palabras.

## 6. Publicar

```
cd /Users/laura/noon-clinic-web
python3 build.py                      # genera páginas, hubs, sitemap.xml y robots.txt
git add -A && git commit -m "guía: <título>"
git pull --rebase && git push
```
Luego verificar que `https://noon.clinic/<slug>` responde 200 (1–3 min) y anotar en `registro.md`.
Fase actual: **manual con visto bueno de Laura** antes del push. Cuando ella lo apruebe, la
rutina diaria publica sola con red de seguridad (se publica, se avisa y queda en el registro).

## 7. Si algo no rinde

Política: **actualizar, no borrar.** Si en 3 meses una pieza no tiene impresiones en Search
Console, se mejora (título, profundidad, enlaces) y se cambia `actualizado`.
