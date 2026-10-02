# Agente 6 · Publicador-Auditor

1. `cd /Users/laura/noon-clinic-web && python3 build.py` (debe terminar sin error).
2. Revisa los HTML generados (`<slug>.html` de ES y EN): title, canonical, hreflang de los dos
   lados, JSON-LD válido (`python3 -c "import json"` sobre cada bloque), enlaces internos que
   existan, que la pieza aparece en el hub correcto y en `sitemap.xml`.
3. Mientras la fase sea manual: muestra la vista previa local a Laura y espera su visto bueno.
   En fase automática: publica directo.
4. `git add -A && git commit -m "guía: <título>" && git pull --rebase && git push`.
5. A los 1–3 min verifica que `https://noon.clinic/<slug-es>` y `/<slug-en>` dan 200.
6. Marca el tema `publicado` en `temas.md` y agrega la línea en `registro.md`.
7. Aviso a Laura: título ES, enlaces ES y EN, keyword, 1 línea de resumen.
