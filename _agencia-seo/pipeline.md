# Pipeline diario · Agencia SEO internacional de noon Clinic

Conocimiento compartido: `INSTRUCCIONES.md`, `estrategia.md`, `hechos.md`, `temas.md`,
`plantilla-articulo.html`, `registro.md`. Cada agente tiene su archivo en `agentes/`.

| # | Agente | Archivo | Qué hace |
|---|---|---|---|
| 1 | Investigador-Redactor | `agentes/1-investigador-redactor.md` | Elige el tema, investiga y escribe la versión en ESPAÑOL |
| 2 | Adaptador al inglés | `agentes/2-adaptador-ingles.md` | Escribe la versión en INGLÉS (adaptada, no traducida) con su keyword |
| 3 | Humanizador | `agentes/3-humanizador.md` | Quita huellas de IA en los dos idiomas; nota ≥ 8/10 o devuelve |
| 4 | Verificador médico-legal | `agentes/4-verificador.md` | Cada dato contra `hechos.md` y las reglas de oro; puede BLOQUEAR |
| 5 | Juez SEO | `agentes/5-juez-seo.md` | Puntúa el SEO (≥ 85/100) y corrige |
| 6 | Publicador-Auditor | `agentes/6-publicador.md` | build, revisa la página generada, publica, verifica en vivo y registra |

Semanal (no diario): `agentes/7-analista.md` revisa Search Console y mejora la pieza más floja.

```
1 Redactor (ES) → 2 Adaptador (EN) → 3 Humanizador → 4 Verificador ──(bloquea)──┐
                                                    │ aprueba                     │
                                                    ▼                             │
                                              5 Juez SEO → 6 Publicador      vuelve a 1
```

Reglas de la cadena:
- El Verificador manda sobre el Juez SEO: un dato dudoso se quita aunque baje la nota SEO.
- Si el Verificador bloquea dos veces el mismo tema, se marca `en pausa` en `temas.md` con el
  motivo y se toma el siguiente.
- Cada agente deja una línea en la sección del día de `registro.md` (qué cambió, nota).
