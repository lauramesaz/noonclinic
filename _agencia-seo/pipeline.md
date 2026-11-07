# Pipeline diario · Agencia SEO de noon Clinic

Conocimiento compartido: `INSTRUCCIONES.md`, `estrategia.md`, `hechos.md`, `temas.md`,
`plantilla-articulo.html`, `registro.md`. Cada agente tiene su archivo en `agentes/`.

| # | Agente | Archivo | Qué hace |
|---|---|---|---|
| 1 | Investigador-Redactor | `agentes/1-investigador-redactor.md` | Elige el tema, investiga y escribe la versión en ESPAÑOL |
| 2 | Adaptador al inglés | `agentes/2-adaptador-ingles.md` | Escribe la versión en INGLÉS (adaptada, no traducida) con su keyword. Solo público `eeuu` |
| 3 | Policía humanizador | `agentes/3-humanizador.md` | Reescribe la forma en los dos idiomas (prueba de 10 puntos, aprueba con 8), pone multas en `notas-humanizador.md`, hace control final antes de publicar y limpia 1 guía vieja por día |
| 4 | Verificador médico-legal | `agentes/4-verificador.md` | Cada dato contra `hechos.md` y las reglas de oro; puede BLOQUEAR |
| 5 | Juez SEO | `agentes/5-juez-seo.md` | Puntúa el SEO (≥ 85/100) y corrige |
| 6 | Publicador-Auditor | `agentes/6-publicador.md` | build, revisa la página generada, publica, verifica en vivo y registra |

Semanal (no diario): la revisión de los lunes (`agentes/7-analista.md`) deja la foto de Search
Console y el seguimiento de las 10 fichas. Ritmo de la semana: `INSTRUCCIONES.md` §8.
En la rutina de la nube, el Policía (3) y el Verificador (4) corren como **subagentes** separados
(herramienta Agent) y su nota queda en `registro.md`; sin esa evidencia, la pieza queda en `borrador`.

```
1 Redactor (ES) → 2 Adaptador (EN) → 3 Policía → 4 Verificador ──(bloquea)──┐
                                                    │ aprueba                     │
                                                    ▼                             │
                                              5 Juez SEO → 3 Policía (control final) → 6 Publicador      vuelve a 1
```

Reglas de la cadena:
- Los agentes 1 y 2 leen `notas-humanizador.md` (libreta de multas del Policía) antes de escribir.
- Cada día, además de lo que toque, el Policía humaniza 1 guía vieja (con su par EN si lo tiene) de
  `humanizados.md` (la primera `[pendiente]` con `actualizado` de hace 21 días o más); pasa por el
  Verificador y solo cambia `actualizado`.
- El Policía corre `python3 _agencia-seo/repetidas.py <slug>` antes de aprobar: la entrada, el intro y
  la descripción no pueden copiar 8 o más palabras seguidas de otra guía.
- El Verificador manda sobre el Juez SEO: un dato dudoso se quita aunque baje la nota SEO.
- Si el Verificador bloquea dos veces el mismo tema, se marca `en pausa` en `temas.md` con el
  motivo y se toma el siguiente.
- Cada agente deja una línea en la sección del día de `registro.md` (qué cambió, nota).
