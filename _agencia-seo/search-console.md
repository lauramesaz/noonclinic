# Search Console de noon.clinic (foto para la agencia)

Esta foto la saca cada lunes a las 9:30 a. m. la rutina de la nube "revisión SEO de los lunes"
(`trig_01FQqiZS6GTMc8C7tMK83kNj`) con el usuario robot de Search Console (solo lectura), corriendo
`python3 _agencia-seo/gsc.py sc-domain:noon.clinic --paises --marca --cruce --seguimiento`. Ya no
depende del Mac. Lo más nuevo arriba. Úsala para elegir temas (la cola de `temas.md` sale de aquí),
para la mejora de los miércoles y para no escribir sobre búsquedas que ya tienen página dueña.
El seguimiento semanal de las 10 fichas va aparte, en `seguimiento-fichas.md`.

## Plan orgánico 13-nov-2026 (hecho a mano en la sesión con Laura)

**NO TOCAR ANTES DEL 4-DIC-2026** los títulos, los h1 (título grande), las preguntas ni los enlaces de esta sección. Google
necesita unas 3 semanas para volver a leer y mover las páginas; si se cambian antes, no se sabe qué funcionó. La revisión
de los lunes solo mira (foto y seguimiento); el lunes 7-dic se compara con la foto del 9-nov.

**Diagnóstico:** muchas páginas y ninguna gana (0 búsquedas sin la marca en primera página). Menos volumen, más fuerza:
una dueña por búsqueda, las 10 fichas en seguimiento reforzadas y freno a las páginas nuevas parecidas (`temas.md`).

### Dueña de cada búsqueda (las 10 que competían en la foto del 9-nov)

| Búsqueda | Dueña | Qué se hizo para que las otras no le compitan |
|---|---|---|
| mentoplastia y rinoplastia | /rinoplastia-y-mentoplastia | Pregunta nueva con la búsqueda exacta; /mentoplastia y /especialistas la enlazan con el texto "Mentoplastia y rinoplastia en la misma cirugía". El título de Google no se tocó (el del 27-oct está funcionando). |
| mentoplastia en medellín | /mentoplastia | El h1 de /rinoplastia-y-mentoplastia ya no dice "…mentoplastia en Medellín" (ahora "…juntas en Medellín"); /especialistas enlaza "Mentoplastia en Medellín". |
| liposucción medellín · liposuccion en medellin | /liposuccion | Título y h1 con "Liposucción en Medellín"; la guía para EE. UU., /lipo-360 y /especialistas la enlazan con ese texto; la ficha en inglés ya no dice "Lipo 360" en el título; la guía /lipotransferencia-glutea-en-medellin se fusionó (abajo). |
| lipotransferencia precio colombia medellín | /lipotransferencia-glutea | La guía que le competía se fusionó en la ficha y redirige a ella. |
| mastopexia precio colombia · mastopexia bogota | /mastopexia | Las fichas con y sin implantes enlazan a /mastopexia con "Mastopexia en Medellín: precio y viaje". |
| mastopexia sin implantes precio colombia | /mastopexia-sin-implantes | Sin cambio de título; pregunta nueva de incapacidad y bloque "en Medellín, paso a paso". |
| gynecomastia surgery colombia | /gynecomastia-surgery-medellin (inglés) | Par español/inglés revisado: hreflang correcto en los dos sentidos. Sin cambios. |
| rhinoplasty medellin | /rhinoplasty-medellin (inglés) | La otra página es el índice de cirugías en inglés (normal). hreflang correcto. Sin cambios. |

Revisión técnica del mismo día: los 186 pares y páginas del sitemap tienen canónica propia, ninguna tiene noindex, todos
los hreflang son recíprocos y ninguna página queda a más de 2 clics del inicio (las 10 fichas en seguimiento, a 1 clic).

### Títulos y h1 cambiados (antes → después)

| Página | Qué | Antes | Después |
|---|---|---|---|
| /liposuccion | título de Google | Lipo en Medellín: liposucción y lipoescultura | Liposucción en Medellín: lipo y lipoescultura |
| /liposuccion | h1 | Liposucción y lipoescultura en Medellín | Liposucción en Medellín |
| /liposuction-medellin | título de Google (inglés) | Liposuction and Lipo 360 in Medellín, Colombia | Liposuction in Medellín, Colombia |
| /rinoplastia-y-mentoplastia | h1 | Rinoplastia y mentoplastia en Medellín | Rinoplastia y mentoplastia juntas en Medellín |
| /nutricion | h1 | Nutrición en Medellín | Nutrición personalizada en Medellín |

Títulos de Google cambiados: 2 (tope del plan: 10). Los demás se dejaron como estaban a propósito.

### Fusión y redirección

- `/lipotransferencia-glutea-en-medellin` (guía en español para quien viaja de EE. UU.) → **redirige a
  `/lipotransferencia-glutea`** y salió del sitemap. Tres de sus cinco apartados repetían la ficha y su dirección era la
  búsqueda de la ficha. Lo que la ficha no tenía pasó a sus preguntas (poca grasa para transferir, duración y anestesia,
  venir de otra ciudad o de otro país). Su versión en inglés `/bbl-in-medellin-colombia` sigue publicada, ya sin par.
  El archivo queda en `articulos/` con `"estado": "fusionado"` (no se publica).

### Refuerzo de las 10 fichas en seguimiento (solo con datos ya publicados o de `hechos.md`; sin precios)

Lo que tienen los que salen arriba en Google y a noon le faltaba: preguntas de duración y anestesia, cicatriz, incapacidad
y precio, y un bloque de "cómo es en Medellín" con el nombre del cirujano y la sede.

| Ficha | Preguntas nuevas | Otros |
|---|---|---|
| /mentoplastia | duración y anestesia · cicatriz (ASPS) · cuándo se ve el resultado | bloque "Tu mentoplastia en Medellín, paso a paso" |
| /lipotransferencia-glutea | poca grasa para transferir · duración y anestesia · si vives en otra ciudad o país | recibe la guía fusionada |
| /rinoplastia-y-mentoplastia | "¿La mentoplastia y la rinoplastia se pueden hacer al mismo tiempo?" · recuperación | bloque paso a paso · h1 |
| /mastopexia-sin-implantes | días de incapacidad | bloque paso a paso · enlace a /mastopexia |
| /braquioplastia | días de incapacidad · duración y anestesia | — |
| /nutricion | cómo es un plan de alimentación personalizado | h1 |
| /otoplastia | duración y anestesia · cuánto tiempo la banda | bloque paso a paso |
| /liposuccion | qué zonas · duración y anestesia | bloque paso a paso · título y h1 |
| /abdominoplastia | cicatriz · días de incapacidad · abdominoplastia o lipoabdominoplastia · precio (enlaza la guía de precio) | bloque paso a paso |
| /mamoplastia-de-aumento | duración y anestesia · primeras semanas (enlaza la guía) · precio (enlaza la guía de precio) | bloque paso a paso |

El bloque "en Medellín, paso a paso" ahora nombra la sede (Torre Médica El Tesoro 2, El Poblado) en todas las fichas que lo tienen.

### Enlaces internos

- `/especialistas` (de las pocas páginas en primera página, por la marca) no enlazaba ninguna ficha: ahora tiene la lista
  "Lo que más nos consultan" con las 10 fichas en seguimiento y el texto de cada búsqueda.
- Las guías enlazan a /liposuccion con el texto "Liposucción en Medellín" (campo `ancla` de la ficha).
- `/about-noon-clinic` (ya en Google) enlaza 5 guías en inglés que Google todavía no tiene.
- Las fichas de abdominoplastia y aumento de senos enlazan sus guías de precio y de recuperación (dos de ellas sin indexar).

### Páginas sin indexar (25 en la revisión del 13-nov)

Ninguna tiene noindex ni canónica equivocada; todas están en el sitemap, a 2 clics o menos del inicio y con 8 o más enlaces
internos. 23 son páginas en inglés: Google las conoce y todavía no las lee, que es lo normal en un dominio nuevo sin enlaces
desde otras webs. No se arregla con más páginas: se arregla con enlaces de afuera (ficha de Google, directorios médicos,
prensa) y con que las fichas en español empiecen a traer visitas.

### Qué mirar el lunes 7-dic-2026

1. "Búsquedas que compiten": de 10 deberían bajar (meta: 5 o menos).
2. "liposucción medellín": que la página que salga sea /liposuccion.
3. "mentoplastia y rinoplastia": que siga pasando a /rinoplastia-y-mentoplastia, y "mentoplastia en medellín" a /mentoplastia.
4. Seguimiento de las 10 fichas: posición frente a la fila del 11-oct a 7-nov.

## Foto del 23-nov-2026 (últimos 28 días: 25-oct al 21-nov)

**Total:** 15 clics · 654 impresiones · CTR 2,3 % · posición media 46,6.
De los 15 clics, 5 son de la búsqueda "noon clinic" (13 impr.), 8 llegan sin búsqueda visible y 2 por búsquedas sin la marca.

**Sin la marca (búsquedas que no dicen "noon"):** 2 clics · 472 impresiones en 167 búsquedas distintas ·
posición media 52,2. Por país: Colombia 1/216 · España 1/71 · Estados Unidos 0/110 · México 0/34 · Chile 0/8.
**Búsquedas sin la marca en primera página** (posición media 10 o mejor, 3 o más impresiones): **6** ("melasma facial" 8,7,
"liposuccion medellin" 6,6, "acido hialuronico labios precio colombia" 7,8, "causas del melasma" 10,0, "melasma dermico" 5,7,
"que es melasma en la cara" 6,7).

**Países (clics / impresiones, todo):** Colombia 14/317 · España 1/80 · EE. UU. 0/134 · México 0/38 · Brasil 0/12 ·
Chile 0/8 · Venezuela 0/6 · Argentina 0/5 · Pakistán 0/5 · Reino Unido 0/4.

**Búsquedas sin la marca (top 10, impresiones · posición):** melasma 52 · 30 (1 clic) · mentoplastia y rinoplastia 30 · 76 ·
melasma que es 14 · 21 · mastopexia bogota 12 · 71 · melasma facial 12 · 9 · bioestimulador 11 · 66 ·
otoplasty columbia sc 9 · 75 · liposuccion en medellin 8 · 59 · bioestimuladores 8 · 57 · mentoplastia medellin 4 · 76 (1 clic).

**Páginas (top 10, clics / impresiones):** / 9/37 · /especialistas 5/22 · /melasma-por-que-aparece-y-como-se-trata 1/127 ·
/mentoplastia 1/11 · /rinoplastia-y-mentoplastia 0/33 · /lipo-en-medellin-para-pacientes-de-estados-unidos 0/27 ·
/bioestimuladores-de-colageno-que-son-y-para-quien 0/26 · /how-to-choose-a-plastic-surgeon-in-medellin 0/26 ·
/labios-con-acido-hialuronico 0/20 · /ear-surgery-medellin 0/19.

**Búsquedas que compiten** (2 o más páginas de noon, 3 o más impresiones): **19** (antes 14). Las principales:
- "mentoplastia y rinoplastia" (32): /rinoplastia-y-mentoplastia 26 (la principal) · /mentoplastia 6.
- "liposuccion en medellin" (16) y "liposucción medellín" (15): guía para EE. UU. · /liposuccion · /lipotransferencia-glutea-en-medellin · /liposuction-medellin.
- "mastopexia bogota" (14): /mastopexia · /mastopexia-con-implantes.
- "rhinoplasty medellin" (8), "plastic surgery in colombia medellin" (5), "plastic surgery in medellin" (4): /rhinoplasty-medellin o /plastic-surgery-medellin · /how-to-choose-a-plastic-surgeon-in-medellin · otras.
- "mentoplastia medellin" (6) y "mentoplastia en medellín" (6): /mentoplastia · /rinoplastia-y-mentoplastia · /cirugia-plastica.
- "aumento de senos medellin" (7): guía para EE. UU. · /mommy-makeover; "acido hialuronico medellin" (4); "bioestimuladores medellin" (3);
  "lipotransferencia" (3 búsquedas): /lipotransferencia-glutea · /lipotransferencia-glutea-en-medellin; gynecomastia/gyno surgery colombia (2); "liposuction columbia" (3); mastopexia precio colombia (3).
Ojo: las fusiones y los cambios de dueña del 13/16-nov (liposucción, lipotransferencia, mentoplastia) todavía no se notan: Google tarda semanas.

**Cambió de página entre quincenas** (25 al 7-nov → 8 al 21-nov): "plastic surgery in colombia medellin" y "plastic surgery in medellin" pasaron
a /how-to-choose-a-plastic-surgeon-in-medellin (1 impr. cada una); "rhinoplasty medellin" pasó en parte a esa misma guía (2 de 5);
"cuanto cuesta una lipotransferencia en medellin" y "lipotransferencia precio colombia medellín" cambiaron entre /lipotransferencia-glutea y la guía para EE. UU. (1 impr. cada una; pocos datos).

**Cerca de la primera página** (sin contar las que salen solo por "noon clinic"): /how-to-choose-a-plastic-surgeon-in-medellin (18,7; "top 5 plastic surgeons in medellin colombia" pos. 11),
/bichectomia (11,1; "bichectomia medellin"), /aumento-de-senos-en-medellin-desde-estados-unidos (15,8), /lipo-360-medellin (10,3; "liposuction columbia" 14),
/lipoabdominoplastia-con-transferencia-glutea (11,7). /cuantos-dias-quedarse... sale por "si": no cuenta. /especialistas, /tu-proceso, /otra-ciudad y /medicina-estetica solo por la marca: no cuentan.

**Seguimiento de las 10 fichas** (posición · impresiones): mentoplastia 80 · 11 · lipotransferencia-glutea 72 · 14 ·
rinoplastia-y-mentoplastia 81 · 33 · mastopexia-sin-implantes 86 · 16 · braquioplastia 84 · 4 · nutricion 49 · 17 ·
otoplastia 66 · 7 · liposuccion 75 · 10 · abdominoplastia 82 · 1 · mamoplastia-de-aumento 84 · 3.
La que más subió: nutricion (62 → 49). En el puesto 40 o mejor: 0 de 10 (meta al 7-feb-2027: 4).

**Indexación:** 189 páginas en el sitemap, **166 en Google**, 23 todavía no (9 "Google no reconoce esta URL",
14 "Descubierta: actualmente sin indexar"). Faltan sobre todo fichas en inglés para EE. UU. (facelift, hifu, prp, thigh-lift,
thread-lift, chemical-peel, skin-boosters, breast-lift, guides, why-noon-clinic, nutrition…) y 2 en español
(/cirugia-plastica-en-medellin-desde-atlanta, /rinomodelacion-con-acido-hialuronico-o-rinoplastia).

**Lectura:** parecido a la semana pasada: 15 clics (antes 14), 654 impresiones (antes 452) y 2 clics sin la marca (antes 1). El aumento de apariciones
viene de Colombia (317, antes 228) y también de EE. UU. (134, antes 91); los clics siguen casi todos de Colombia. Primera página sin la marca: 6 búsquedas (antes 1),
sobre todo de melasma. Indexadas 166 (antes 164). Ninguna ficha de las 10 está aún en el puesto 40 o mejor.
(Sección "Salen pero casi nadie abre": /how-to-choose-a-plastic-surgeon-in-medellin, puesto 19 con 26 impr. y 0 clics.)

## Foto del 16-nov-2026 (últimos 28 días: 18-oct al 14-nov)

**Total:** 14 clics · 452 impresiones · CTR 3,1 % · posición media 59,0.
De los 14 clics, 6 son de la búsqueda "noon clinic" (12 impr.), 7 llegan sin búsqueda visible y 1 por una búsqueda sin la marca.

**Sin la marca (búsquedas que no dicen "noon"):** 1 clic · 305 impresiones en 126 búsquedas distintas ·
posición media 67,5. Por país: Colombia 1/141 · Estados Unidos 0/77 · España 0/48 · México 0/14 · Chile 0/3.
**Búsquedas sin la marca en primera página** (posición media 10 o mejor, 3 o más impresiones): **1** ("melasma facial", pos. 5).

**Países (clics / impresiones, todo):** Colombia 14/228 · EE. UU. 0/91 · España 0/53 · México 0/16 · Brasil 0/11 ·
Venezuela 0/6 · Pakistán 0/5 · Argentina 0/3 · Bangladés 0/3 · Chile 0/3.

**Búsquedas sin la marca (top 10, impresiones · posición):** mentoplastia y rinoplastia 35 · 75 · melasma 25 · 38 ·
bioestimulador 9 · 66 · otoplasty columbia sc 9 · 75 · redondo beach nonsurgical rhinoplasty 7 · 75 ·
brachioplasty nora 6 · 54 · hilos tensores barranquilla 6 · 70 · liposucción medellín 6 · 79 ·
lipotransferencia medellín 6 · 77 · mentoplastia medellin 4 · 76 (1 clic).

**Páginas (top 10, clics / impresiones):** / 10/32 · /especialistas 4/23 · /mentoplastia 1/25 ·
/melasma-por-que-aparece-y-como-se-trata 0/48 · /rinoplastia-y-mentoplastia 0/24 ·
/bioestimuladores-de-colageno-que-son-y-para-quien 0/20 · /plastic-surgery-medellin 0/19 ·
/ear-surgery-medellin 0/18 · /lipotransferencia-glutea 0/17 · /mastopexia-sin-implantes 0/17.

**Búsquedas que compiten** (2 o más páginas de noon, 3 o más impresiones): **14** (antes 10).
- "mentoplastia y rinoplastia" (37): /mentoplastia 20 · /rinoplastia-y-mentoplastia 17 (la principal).
- "liposucción medellín" (13) y "liposuccion en medellin" (13): guía para EE. UU. · /liposuccion · /lipotransferencia-glutea-en-medellin · /liposuction-medellin.
- "mentoplastia medellin" (6) y "mentoplastia en medellín" (6): /mentoplastia · /rinoplastia-y-mentoplastia · /cirugia-plastica.
- "rhinoplasty medellin" (6): /rhinoplasty-medellin 4 · /plastic-surgery-medellin 1 · /rhinoplasty-in-medellin-colombia 1.
- "gynecomastia surgery colombia" (5) y "gyno surgery colombia" (3): /gynecomastia-surgery-medellin · /ginecomastia.
- "mastopexia bogota" (5), "mastopexia precio colombia" (3), "mastopexia sin implantes precio colombia" (3): /mastopexia · /mastopexia-con-implantes · /mastopexia-sin-implantes.
- "lipotransferencia precio colombia medellín" (4), "cuanto cuesta una lipotransferencia en medellin" (3), "lipotrasferencia medellin" (3): /lipotransferencia-glutea · /lipotransferencia-glutea-en-medellin.

**Cambió de página entre quincenas** (18 al 31-oct → 1 al 14-nov): "mentoplastia y rinoplastia" pasó de /mentoplastia
a /rinoplastia-y-mentoplastia (14 de 14); "gynecomastia surgery colombia" y "gyno surgery colombia" pasaron a /ginecomastia;
"rhinoplasty medellin" pasó a /rhinoplasty-medellin (4 de 5); "mastopexia sin implantes precio colombia" a /mastopexia;
"cuanto cuesta una lipotransferencia en medellin" a /lipotransferencia-glutea.

**Cerca de la primera página:** solo /cuantos-dias-quedarse-en-colombia-despues-de-una-cirugia-plastica (4,3; la búsqueda "si", poco útil)
y dos páginas por búsquedas que Google no muestra (/plastic-surgery-in-colombia-as-a-us-resident 7,0 y /por-que-noon 10,3).
/especialistas (8,3), /medicina-estetica, /tu-proceso y /otra-ciudad solo salen por "noon clinic": no cuentan.

**Seguimiento de las 10 fichas** (posición · impresiones): mentoplastia 77 · 25 · lipotransferencia-glutea 80 · 17 ·
rinoplastia-y-mentoplastia 82 · 24 · mastopexia-sin-implantes 86 · 17 · braquioplastia 76 · 8 · nutricion 62 · 14 ·
otoplastia 66 · 7 · liposuccion 81 · 8 · abdominoplastia 82 · 1 · mamoplastia-de-aumento 83 · 2.
La que más subió: otoplastia (70 → 66). En el puesto 40 o mejor: 0 de 10 (meta al 7-feb-2027: 4).

**Indexación:** 187 páginas en el sitemap, **164 en Google**, 23 todavía no (15 "Google no reconoce esta URL",
8 "Descubierta: actualmente sin indexar"). Faltan sobre todo fichas en inglés para EE. UU. (facelift, hifu, prp,
thigh-lift, chemical-peel, skin-boosters, breast-lift, guides, why-noon-clinic…) y 2 en español
(/cirugia-plastica-en-medellin-desde-atlanta, /skinboosters-o-bioestimuladores-cual-necesita-tu-piel).

**Lectura:** sube un poco: 14 clics (antes 8), 452 impresiones (antes 377) y el primer clic por una búsqueda sin la marca
("mentoplastia medellin"). El aumento viene de Colombia (228 impresiones, antes 180); EE. UU. 91 (antes 80). Indexadas 164 (antes 160).
Ojo: las búsquedas que compiten subieron a 14. Plan orgánico vigente: no tocar títulos/h1 antes del 4-dic.
(Sección "Salen pero casi nadie abre": ninguna.)

## Foto del 9-nov-2026 (últimos 28 días: 11-oct al 7-nov)

**Total:** 8 clics · 377 impresiones · CTR 2,1 % · posición media 64,9.
De los 8 clics, 4 son de la búsqueda "noon clinic" y 4 llegan sin búsqueda visible (Google no muestra la consulta).

**Sin la marca (búsquedas que no dicen "noon"):** 0 clics · 241 impresiones en 99 búsquedas distintas ·
posición media 76,5. Por país: Colombia 0/107 · Estados Unidos 0/68 · España 0/52 · Hungría 0/2 · Puerto Rico 0/2.
**Búsquedas sin la marca en primera página** (posición media 10 o mejor, 3 o más impresiones): **0**.

**Países (clics / impresiones, todo):** Colombia 7/180 · España 1/67 · Estados Unidos 0/80 · Brasil 0/12 ·
Pakistán 0/4 · Venezuela 0/4 · Argentina 0/3 · Rusia 0/3 · Bangladés 0/2 · Canadá 0/2.

**Búsquedas sin la marca (top 10, impresiones · posición):** mentoplastia y rinoplastia 46 · 75 ·
lipotransferencia medellín 9 · 80 · otoplasty columbia sc 9 · 75 · melasma 7 · 53 · redondo beach nonsurgical
rhinoplasty 7 · 75 · brachioplasty nora 6 · 54 · hilos tensores barranquilla 6 · 70 · gynecomastia surgery
colombia 5 · 79 · bioestimulador 4 · 67 · braquioplastia en medellin 4 · 74.

**Páginas (top 10, clics / impresiones):** / 5/31 · /especialistas 4/22 · /mentoplastia 0/41 ·
/lipotransferencia-glutea 0/20 · /plastic-surgery-medellin 0/19 · /ear-surgery-medellin 0/18 ·
/mastopexia-sin-implantes 0/17 · /rinoplastia-y-mentoplastia 0/17 · /nutricion 0/14 · /ginecomastia 0/10.

**Búsquedas que compiten** (2 o más páginas de noon, 3 o más impresiones): **10** (igual que el 7-nov).
- "mentoplastia y rinoplastia" (48): /mentoplastia 37 · /rinoplastia-y-mentoplastia 11 (la principal).
- "liposucción medellín" (8) y "liposuccion en medellin" (7): guía para EE. UU. · /liposuccion · /lipotransferencia-glutea-en-medellin · /liposuction-medellin.
- "mentoplastia en medellín" (6): /rinoplastia-y-mentoplastia 4 · /cirugia-plastica 2.
- "gynecomastia surgery colombia" (5): /gynecomastia-surgery-medellin 3 · /ginecomastia 2.
- "mastopexia bogota" (4): /mastopexia 2 · /mastopexia-con-implantes 2.
- "lipotransferencia precio colombia medellín" (3): /lipotransferencia-glutea 2 · /lipotransferencia-glutea-en-medellin 1.
- "mastopexia precio colombia" (3): /mastopexia-con-implantes 2 · /mastopexia-sin-implantes 1.
- "mastopexia sin implantes precio colombia" (3): /mastopexia-sin-implantes 2 · /mastopexia 1.
- "rhinoplasty medellin" (3): /rhinoplasty-medellin 2 · /plastic-surgery-medellin 1.

**Cambió de página entre quincenas** (11 al 24-oct → 25-oct al 7-nov): "mentoplastia y rinoplastia" sigue
pasando de /mentoplastia a /rinoplastia-y-mentoplastia (11 de 17); "gynecomastia surgery colombia" pasó a la ficha
en inglés; "mastopexia sin implantes precio colombia" pasó a /mastopexia (1 de 2).

**Cerca de la primera página:** ninguna por búsquedas que no sean la marca. /especialistas (9,4),
/medicina-estetica (11) y /tu-proceso (11,5) solo salen por "noon clinic": no cuentan.
/plastic-surgery-in-colombia-as-a-us-resident (5,7) con 3 impr. por búsquedas que Google no muestra.

**Seguimiento de las 10 fichas** (posición · impresiones): mentoplastia 77 · 41 · lipotransferencia-glutea
81 · 20 · rinoplastia-y-mentoplastia 83 · 17 · mastopexia-sin-implantes 86 · 17 · braquioplastia 76 · 8 ·
nutricion 62 · 14 · otoplastia 70 · 8 · liposuccion 84 · 4 · abdominoplastia 82 · 1 ·
mamoplastia-de-aumento 83 · 2. La que más subió: rinoplastia-y-mentoplastia (84 → 83).
En el puesto 40 o mejor: 0 de 10 (meta al 7-feb-2027: 4).

**Indexación:** 186 páginas en el sitemap, **160 en Google**, 26 todavía no (15 "Google no reconoce esta URL",
11 "Descubierta: actualmente sin indexar"). Faltan sobre todo fichas en inglés para EE. UU. (breast-lift, facelift,
hifu, prp, thigh-lift, guides, international-patients, why-noon-clinic…) y 2 en español
(/cirugia-plastica-en-medellin-desde-atlanta, /recuperacion-del-aumento-de-senos-que-esperar-las-primeras-semanas).

**Lectura:** casi igual a la línea base: 8 clics (antes 7), 377 impresiones (antes 363), y siguen sin llegar clics por
búsquedas sin la marca. Colombia 180 impresiones y EE. UU. 80 (sube de 73): el grueso viene de Colombia, con EE. UU.
creciendo despacio. Indexadas 160 (antes 151, método comparable con el 2-nov).

## Línea base del plan de 90 días (leída el 7-nov-2026 con el robot; datos del 9-oct al 5-nov)

**Total:** 7 clics · 363 impresiones · CTR 1,9 % · posición media 64,5.
De los 7 clics, 4 son de la búsqueda "noon clinic" y 3 llegan sin búsqueda visible (Google no muestra
la consulta).

**Sin la marca (búsquedas que no dicen "noon"):** 0 clics · 231 impresiones en 92 búsquedas distintas ·
posición media 76,7. Por país: Colombia 0/106 · Estados Unidos 0/61 · España 0/51.
**Búsquedas sin la marca en primera página** (posición media 10 o mejor, 3 o más impresiones): **0**.

**Países (clics / impresiones, todo):** Colombia 6/178 · Estados Unidos 0/73 · España 1/66 · Brasil 0/12 ·
Venezuela 0/4 · Argentina 0/3 · Rusia 0/3 · Canadá 0/2 · Hungría 0/2 · México 0/2.

**Búsquedas sin la marca (top 10, impresiones · posición):** mentoplastia y rinoplastia 46 · 74 ·
lipotransferencia medellín 9 · 80 · otoplasty columbia sc 9 · 75 · redondo beach nonsurgical rhinoplasty
7 · 75 · brachioplasty nora 6 · 54 · hilos tensores barranquilla 6 · 70 · gynecomastia surgery colombia
5 · 79 · braquioplastia en medellin 4 · 74 · liposucción medellín 4 · 83 · melasma 4 · 52.

**Búsquedas que compiten** (2 o más páginas de noon para la misma búsqueda, 3 o más impresiones): **10**.
- "mentoplastia y rinoplastia" (48): /mentoplastia 39 · /rinoplastia-y-mentoplastia 9.
- "liposucción medellín" (8) y "liposuccion en medellin" (7): reparten entre la guía para EE. UU.
  /lipo-en-medellin-para-pacientes-de-estados-unidos, /liposuccion, /lipotransferencia-glutea-en-medellin
  y /liposuction-medellin.
- "mentoplastia en medellín" (6): /rinoplastia-y-mentoplastia 4 · /cirugia-plastica 2.
- "gynecomastia surgery colombia" (5): /gynecomastia-surgery-medellin 3 · /ginecomastia 2.
- "mastopexia bogota" (4): /mastopexia 2 · /mastopexia-con-implantes 2.
- "lipotransferencia precio colombia medellín" (3): /lipotransferencia-glutea 2 · la guía para EE. UU. 1.
- "mastopexia precio colombia" (3): /mastopexia-con-implantes 2 · /mastopexia-sin-implantes 1.
- "mastopexia sin implantes precio colombia" (3): /mastopexia-sin-implantes 2 · /mastopexia 1.
- "rhinoplasty medellin" (3): /rhinoplasty-medellin 2 · /plastic-surgery-medellin 1.
- (La marca "noon clinic" sale en 6 páginas: es normal y no cuenta.)

**Cambió de página entre quincenas** (9 al 22-oct → 23-oct al 5-nov): "mentoplastia y rinoplastia" pasó
de /mentoplastia (33) a /rinoplastia-y-mentoplastia (9 de 15): el arreglo de títulos del 27-oct está
funcionando, no hay que tocarlo. "gynecomastia surgery colombia" pasó de /ginecomastia a la ficha en inglés.

**Cerca de la primera página:** ninguna por búsquedas que no sean la marca. /especialistas (9,8),
/medicina-estetica (11) y /tu-proceso (11,5) solo salen por "noon clinic": no cuentan como avance.

**Seguimiento de las 10 fichas** (posición · impresiones): mentoplastia 76 · 43 · lipotransferencia-glutea
82 · 24 · rinoplastia-y-mentoplastia 84 · 15 · mastopexia-sin-implantes 86 · 17 · braquioplastia 76 · 8 ·
nutricion 62 · 14 · otoplastia 70 · 8 · liposuccion 84 · 4 · abdominoplastia 82 · 1 ·
mamoplastia-de-aumento 83 · 2. En el puesto 40 o mejor: 0 de 10 (meta al 7-feb-2027: 4).

**Lectura:** lo que trae Google es de Colombia y casi todo pregunta por una cirugía concreta o por su
precio, lejos de la primera página (puestos 60 a 98). Por eso la cola nueva de `temas.md` (sección J) sale
de estas búsquedas, y la agencia deja de reescribir guías con 4 a 9 impresiones.

## Foto del 2-nov-2026 (últimos 28 días: 4-oct al 31-oct)

**Total:** 6 clics · 315 impresiones · CTR 1,9 % · posición media 63,3.

**Países (clics / impresiones):** Colombia 5/148 · España 1/70 · Estados Unidos 0/64 · Brasil 0/10 · México 0/3 ·
Argentina 0/2 · Hungría 0/2 · Pakistán 0/2 · Puerto Rico 0/2 · Venezuela 0/2.

**Consultas principales (clics / impresiones):**
| Consulta | Clics | Impr. |
|---|---|---|
| noon clinic | 4 | 11 |
| mentoplastia y rinoplastia | 0 | 51 |
| lipotransferencia medellín | 0 | 10 |
| lipoabdominoplastia con transferencia glutea | 0 | 8 |
| transferencia de grasa a gluteos | 0 | 8 |
| lipotransferencia glutea | 0 | 7 |
| redondo beach nonsurgical rhinoplasty | 0 | 7 |
| brachioplasty nora | 0 | 6 |
| hilos tensores barranquilla | 0 | 6 |
| braquioplastia en medellin | 0 | 4 |

**Páginas principales (clics / impresiones):**
| Página | Clics | Impr. |
|---|---|---|
| / | 3 | 28 |
| /especialistas | 3 | 26 |
| /valoracion | 1 | 3 |
| /mentoplastia | 0 | 53 |
| /lipotransferencia-glutea | 0 | 40 |
| /plastic-surgery-medellin | 0 | 19 |
| /ear-surgery-medellin | 0 | 11 |
| /ginecomastia | 0 | 11 |
| /nutricion | 0 | 11 |
| /medicina-estetica | 0 | 9 |

**Indexación (inspección página por página del sitemap):** 183 páginas, **151 en Google**, 32 todavía no
(17 "Google no reconoce esta URL", 15 "Descubierta: actualmente sin indexar"). Casi todas las que faltan son
las fichas nuevas en inglés para EE. UU. (rhinoplasty-medellin, facelift-medellin, hifu-medellin,
lipo-360-medellin, thigh-lift-medellin, guides, international-patients, why-noon-clinic…) y 3 en español
(/rinomodelacion, /es-seguro-operarse-en-colombia, /operarme-en-diciembre-en-colombia).
(Nota: esta cifra viene de otro método que la foto anterior, que usaba el informe de páginas; no son comparables.)

**Lectura:** subida: de 4 a 6 clics y de 186 a 315 impresiones. Colombia sube de 86 a 148 impresiones y
EE. UU. salta de 16 a 64 (posición ~73): ya empieza a verse el contenido en inglés, aunque aún sin clics.
Búsquedas nuevas de EE. UU.: "redondo beach nonsurgical rhinoplasty", "brachioplasty nora", "gynecomastia surgery
colombia", "plastic surgery in colombia medellin", "otoplasty columbia sc" (las fichas en inglés van saliendo, lejos
de la primera página). Nuevas de Colombia: "lipotransferencia medellín" (10, pasó a ser la 3.ª), "mentoplastia en medellín",
"hilos tensores barranquilla" (6, sube). Sin páginas en posición ≤20 con muchas impresiones y pocos clics, salvo
/medicina-estetica (posición 9,6, 9 impr.). Las fichas de cirugía siguen en posiciones 60–90.

## Foto del 26-oct-2026 (datos del 30-sep al 24-oct)

**Total:** 4 clics · 186 impresiones · CTR 2,2 % · posición media 59,2.

**Países (clics / impresiones):** Colombia 3/86 · España 1/72 · Estados Unidos 0/16 · México 0/3 ·
Brasil 0/3 · Costa Rica 0/1 · Venezuela 0/1 · Perú 0/1 · Arabia Saudí 0/1 · Bután 0/1 · Argentina 0/1.

**Consultas principales (clics / impresiones), 32 en total:**
| Consulta | Clics | Impr. |
|---|---|---|
| noon clinic | 2 | 9 |
| mentoplastia y rinoplastia | 0 | 51 |
| lipoabdominoplastia con transferencia glutea | 0 | 9 |
| transferencia de grasa a gluteos | 0 | 8 |
| lipotransferencia medellín | 0 | 7 |
| lipotransferencia glutea | 0 | 6 |
| nutricion personalizada medellin | 0 | 3 |
| hilos tensores barranquilla | 0 | 3 |
| lipotransferencia gluteos | 0 | 3 |
| braquioplastia en medellin | 0 | 2 |

**Páginas principales (clics / impresiones), 30 en total:**
| Página | Clics | Impr. |
|---|---|---|
| / | 3 | 26 |
| /valoracion | 1 | 4 |
| /mentoplastia | 0 | 54 |
| /lipotransferencia-glutea | 0 | 36 |
| /especialistas | 0 | 17 |
| /medicina-estetica | 0 | 13 |
| /ginecomastia | 0 | 11 |
| /nutricion | 0 | 9 |
| /plastic-surgery-in-colombia-from-houston | 0 | 7 |
| /cirugia-plastica | 0 | 5 |

**Indexación (informe de esta semana):** 74 indexadas · 111 sin indexar:
- 85 "Descubierta: actualmente sin indexar" (Google las conoce pero aún no las lee; sube por las
  fichas nuevas ES/EN del 20 y 21-oct).
- 15 "Rastreada: actualmente sin indexar" (Google las leyó y por ahora no las incluye).
- 6 "Duplicada sin canónica" (/valoracion?cx=…, ya resuelto en la web; se limpia solo).
- 3 "Página con redirección" y 2 "Alternativa con canónica adecuada" (lo esperado).

**Lectura:** subida pequeña frente a la foto anterior (de 3 a 4 clics, de 129 a 186 impresiones),
sobre todo desde Colombia (55 → 86). Consultas nuevas, todas de Colombia y en español, de la
parte de estética y nutrición: "nutricion personalizada medellin" (5 impr. sumando con tilde,
posición ~60), "braquioplastia en medellin" (3), "hilos tensores barranquilla" (3) y "ginecomastia
precio". EE. UU. sigue bajo (16 impr., posición ~80), con búsquedas de precio de rinoplastia en
inglés ("rhinoplasty colombia cost", "how much is a nose job in colombia"). Las páginas generales
(/, /especialistas, /medicina-estetica, /cirugia-plastica) ya salen en primera página (posición
5–11); las fichas de cirugía siguen lejos (60–90). Temas que valen: nutrición personalizada en
Medellín y braquioplastia en Medellín (precio y recuperación).

## Foto del 19-oct-2026 (datos del 30-sep al 17-oct)

**Total:** 3 clics · 129 impresiones · CTR 2,3 % · posición media 57,7.

**Países (clics / impresiones):** Colombia 2/55 · España 1/55 · Estados Unidos 0/13 · Brasil 0/3 ·
Perú 0/1 · México 0/1 · Arabia Saudí 0/1.

**Consultas principales (clics / impresiones), 24 en total:**
| Consulta | Clics | Impr. |
|---|---|---|
| noon clinic | 1 | 7 |
| mentoplastia y rinoplastia | 0 | 37 |
| lipoabdominoplastia con transferencia glutea | 0 | 9 |
| transferencia de grasa a gluteos | 0 | 8 |
| lipotransferencia glutea | 0 | 5 |
| lipotransferencia medellín | 0 | 4 |
| lipotransferencia gluteos | 0 | 3 |
| colombian plastic surgery prices | 0 | 2 |
| rhinoplasty colombia cost | 0 | 2 |
| noon medical clinic | 0 | 1 |

**Páginas principales (clics / impresiones), 26 en total:**
| Página | Clics | Impr. |
|---|---|---|
| / | 2 | 22 |
| /valoracion | 1 | 4 |
| /mentoplastia | 0 | 40 |
| /lipotransferencia-glutea | 0 | 30 |
| /especialistas | 0 | 13 |
| /medicina-estetica | 0 | 11 |
| /plastic-surgery-in-colombia-from-houston | 0 | 7 |
| /ginecomastia | 0 | 6 |
| /cirugia-plastica | 0 | 5 |
| /otoplastia | 0 | 4 |

**Indexación (informe del 11-oct):** 67 indexadas · 25 sin indexar:
- 17 "Descubierta: actualmente sin indexar" (Google las conoce pero aún no las lee; casi todas guías:
  /cirugia-plastica-en-medellin-desde-atlanta, /como-elegir-cirujano-plastico-en-medellin,
  /controles-despues-de-operarme-en-colombia-al-volver-a-estados-unidos, /es-seguro-operarse-en-colombia,
  /follow-up-care-at-home-after-surgery-in-colombia, /how-to-choose-a-plastic-surgeon-in-medellin,
  /international-patients, /is-it-safe-to-get-plastic-surgery-in-colombia,
  /plastic-surgery-in-colombia-from-boston, /plastic-surgery-in-medellin-from-miami…).
- 6 "Duplicada sin canónica": /valoracion?cx=… (ya resuelto en la web desde el 2-oct; se limpia solo).
- 2 "Página con redirección" (páginas viejas que redirigen: es lo esperado).

**Lectura:** lo que Google ya muestra son búsquedas en español sobre la cirugía en sí (Colombia y
España), no de viaje desde EE. UU. Por eso se sumó el público Colombia (`estrategia.md`).
