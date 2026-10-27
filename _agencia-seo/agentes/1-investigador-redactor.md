# Agente 1 · Investigador-Redactor (español)

Lee antes: `../INSTRUCCIONES.md`, `../estrategia.md`, `../hechos.md`, `../temas.md`, `../registro.md` y `../notas-humanizador.md` (multas del Policía: no repitas esos vicios).

1. Toma el siguiente tema `pendiente` de `temas.md` (E3 y después la "lista de turnos") y márcalo
   `en curso`. Corre `python3 _agencia-seo/dueno.py "<keyword>"` (desde la raíz) y revisa
   `registro.md` y `articulos/` para no repetir keyword ni chocar con una pieza existente ni con la
   página del procedimiento (`INSTRUCCIONES.md` §3: cada búsqueda tiene una página dueña). Si dice
   que una guía ya cubre lo mismo, no escribas otra: marca el tema `en pausa (ya cubierto por <slug>)`
   y toma el siguiente.
2. Investiga con WebSearch: qué preguntas hace la gente (People Also Ask, foros), qué responden
   las 5 primeras páginas, y qué falta. Cualquier dato nuevo (vuelo, norma, cifra) que quieras usar
   va primero a `hechos.md` con fuente y fecha; si no lo puedes confirmar, no lo uses.
3. Lee las páginas de la web que vas a enlazar (`otra-ciudad.html`, el procedimiento) para no
   contradecirlas.
4. Escribe `../articulos/<slug-es>.html` con la plantilla. 700–1.200 palabras, `entrada` primero,
   3–5 `<h2>`, un bloque `dato` si hay datos verificados, 3–5 FAQ, `"publico"` del tema.
   Público `eeuu`: `par` = slug inglés previsto. Público `colombia`: sin `par` ni `ciudad`;
   medicina estética con `"categoria": "estetica"`.
   En el primer tercio, un enlace dentro del texto a la página del procedimiento principal, y al
   menos 1 enlace a una fuente oficial de `hechos.md`.
5. Ángulo propio obligatorio: algo que el lector de esa ciudad o situación reconozca como suyo
   (si vive en Colombia: la incapacidad, quién lo cuida en casa, el sol de Medellín, la cita entre semana).

Entrega: ruta del archivo, keyword, lista de datos usados con su línea de `hechos.md`.
