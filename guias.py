# -*- coding: utf-8 -*-
# Agencia SEO de noon Clinic: guías del blog. Dos públicos ("publico" en la cabecera): "eeuu" (español + inglés, viaje desde EE. UU.)
# y "colombia" (solo español: pacientes que viven en Colombia, cirugía y medicina estética).
# Los textos los escriben los agentes en _agencia-seo/articulos/<slug>.html (cabecera JSON + cuerpo HTML).
# build.py llama a generar() al final: crea cada página, los dos hubs, sitemap.xml y robots.txt.
import os, json, re, hashlib
from html import escape
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "_agencia-seo", "articulos")

# Ciudades objetivo (orden = prioridad). nombre_es, nombre_en, fondo
CIUDADES = {
    "miami": ("Miami y el sur de Florida", "Miami & South Florida", "seda-horizonte"),
    "nueva-york": ("Nueva York y Nueva Jersey", "New York & New Jersey", "seda-burdeos"),
    "orlando": ("Orlando y Tampa", "Orlando & Tampa", "seda-champan"),
    "houston": ("Houston", "Houston", "seda-cafe"),
    "atlanta": ("Atlanta", "Atlanta", "seda-noche"),
    "boston": ("Boston", "Boston", "seda-clara"),
}

T = {
    "es": {"hub": "pacientes-internacionales.html", "inicio": "Inicio", "hub_n": "Pacientes en EE. UU.", "por": "Equipo noon Clinic",
           "act": "Actualizado", "proc": "Procedimientos de esta guía", "rel": "Sigue leyendo", "preg": "Preguntas frecuentes",
           "aviso": "Esta guía es informativa y no reemplaza una valoración médica. La indicación, los tiempos de recuperación y la fecha de regreso los define tu especialista en persona. Todo procedimiento tiene riesgos y los resultados varían de una persona a otra.",
           "cierre": "Organicemos tu viaje", "cierre_t": "Escríbenos desde EE. UU. y armamos contigo las fechas de valoración, procedimiento y controles.",
           "boton": "Escribir por WhatsApp", "wa": "Hola, vivo en %s y quiero información para hacerme un procedimiento en noon Clinic en Medellín.",
           "wa_gen": "Hola, vivo en EE. UU. y quiero información para hacerme un procedimiento en noon Clinic en Medellín.", "ver": "Ver"},
    "en": {"hub": "international-patients.html", "inicio": "Home", "hub_n": "International patients", "por": "noon Clinic team",
           "act": "Updated", "proc": "Procedures in this guide", "rel": "Keep reading", "preg": "Frequently asked questions",
           "aviso": "This guide is for information only and does not replace a medical consultation. Your specialist decides, in person, whether a procedure is right for you, your recovery time and when you can fly home. Every procedure carries risks and results vary from person to person.",
           "cierre": "Let's plan your trip", "cierre_t": "Message us from the US and we'll set your consultation, procedure and follow-up dates with you.",
           "boton": "Message us on WhatsApp", "wa": "Hi! I live in %s and I'd like information about having a procedure at noon Clinic in Medellín.",
           "wa_gen": "Hi! I live in the US and I'd like information about having a procedure at noon Clinic in Medellín.", "ver": "Read"},
}
MESES = {"es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
         "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}


def fecha_txt(iso, lang):
    a, m, d = (int(x) for x in iso.split("-"))
    return ("%d de %s de %d" % (d, MESES["es"][m - 1], a)) if lang == "es" else ("%s %d, %d" % (MESES["en"][m - 1], d, a))


def leer():
    """Devuelve las guías publicables, más nuevas primero."""
    out = []
    if not os.path.isdir(FUENTES):
        return out
    for nombre in sorted(os.listdir(FUENTES)):
        if not nombre.endswith(".html"):
            continue
        txt = open(os.path.join(FUENTES, nombre), encoding="utf-8").read()
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->(.*)", txt, re.S)
        if not m:
            raise SystemExit("Guía sin cabecera JSON: " + nombre)
        g = json.loads(m.group(1))
        g["cuerpo"] = m.group(2).strip()
        if g.get("estado", "publicado") != "publicado":
            continue
        if g["slug"] + ".html" != nombre:
            raise SystemExit("El archivo %s debe llamarse %s.html" % (nombre, g["slug"]))
        out.append(g)
    out.sort(key=lambda g: (g.get("actualizado") or g["publicado"]), reverse=True)
    preparar(out)
    return out


# ---------------------------------------------------------------- BLOG: tema y foto de cada guía (para las tarjetas)
# Orden = prioridad: la primera regla que coincide con el slug decide el tema y la foto.
# Una guía puede fijar los suyos en la cabecera JSON con "categoria" y "foto" (ej. "noon/foto-luz").
TEMAS = [
    (r"volar|fly", "viaje", "noon/foto-luz"),
    (r"llevar|pack", "viaje", "noon/foto-detalle"),
    (r"donde-quedar|where-to-stay", "viaje", "clinica/vista-2"),
    (r"quedarse|how-long-to-stay", "viaje", "noon/foto-espera"),
    (r"acompa|companion", "viaje", "noon/foto-recepcion"),
    (r"controles|follow-up", "viaje", "noon/foto-objetos"),
    (r"elegir|choose", "seguridad", "noon/foto-consulta"),
    (r"seguro|safe", "seguridad", "clinica/recepcion"),
    (r"alerta|red-flags", "seguridad", "noon/foto-pasillo"),
    (r"viviendo-en|us-resident", "viaje", "clinica/vista"),
]
PROC_PAL = r"lipo|abdominoplastia|tummy|senos|breast|mommy|rinoplastia|rhinoplasty|blefaro|eyelid|glute|bbl|mastopexia|lift|mentoplastia"
ESTETICA_PAL = r"botox|toxina|hialuron|bioestimul|hilos|skinbooster|plasma|peeling|microagujas|limpieza-facial|melasma|manchas|laser|hifu|radiofrecuencia|criolip|sueroterapia|papada"
CATS = {"es": [("procedimientos", "Procedimientos"), ("estetica", "Medicina estética"), ("viaje", "Viaje y recuperación"), ("seguridad", "Seguridad")],
        "en": [("procedimientos", "Procedures"), ("estetica", "Aesthetic medicine"), ("viaje", "Travel & recovery"), ("seguridad", "Safety")]}
EXTRA = ["noon/foto-luz", "noon/foto-espera", "noon/foto-consulta", "noon/foto-detalle", "noon/foto-pasillo", "noon/foto-objetos", "noon/foto-recepcion"]
MESES_C = {"es": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
           "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}


def _existe(f):
    return os.path.exists(os.path.join(AQUI, "assets", f + ".jpg"))


def preparar(guias):
    """Pone a cada guía su tema (_cat) y una foto (_foto) sin repetir fotos dentro del mismo idioma.
    Se reparte de la más vieja a la más nueva, así una guía nueva nunca le cambia la foto a una vieja."""
    usadas = {"es": set(), "en": set()}
    por_slug = {g["slug"]: g for g in guias}
    for g in sorted(guias, key=lambda x: (x["publicado"], x["lang"] != "es", x["slug"])):
        regla = next((r for r in TEMAS if re.search(r[0], g["slug"])), None)
        if g.get("tipo") == "ciudad":
            cat = "ciudad"
        else:
            cat = g.get("categoria") or (regla[1] if regla else ("estetica" if re.search(ESTETICA_PAL, g["slug"]) and not re.search(PROC_PAL, g["slug"])
                                                                   else "procedimientos" if re.search(PROC_PAL + "|" + ESTETICA_PAL, g["slug"]) else "viaje"))
        g["_cat"] = cat
        par = por_slug.get(g.get("par") or "")
        if cat == "ciudad":
            g["_foto"] = "noon/" + g.get("fondo", "seda-oscura")  # las ciudades se muestran como lista, no gastan fotos
            continue
        if par and par.get("_foto") and g["lang"] == "en":
            g["_foto"] = par["_foto"]  # la versión en inglés usa la misma foto que su par en español
        else:
            opciones = ([g["foto"]] if g.get("foto") else []) + ([regla[2]] if regla else []) \
                + ["capacitacion/" + s for s in g.get("procedimientos", [])] + EXTRA
            libres = [f for f in opciones if _existe(f) and f not in usadas[g["lang"]]]
            g["_foto"] = libres[0] if libres else next((f for f in opciones if _existe(f)), "noon/" + g.get("fondo", "seda-oscura"))
        usadas[g["lang"]].add(g["_foto"])


def fecha_corta(g):
    a, m, d = (int(x) for x in (g.get("actualizado") or g["publicado"]).split("-"))
    return ("%d %s %d" % (d, MESES_C["es"][m - 1], a)) if g["lang"] == "es" else ("%s %d, %d" % (MESES_C["en"][m - 1], d, a))


def tarjeta(g, destacada=False, d=0, media=False):
    """Tarjeta del blog: foto, tema · fecha, título (con su cursiva), entrada corta y 'Leer'."""
    nombres = dict(CATS[g["lang"]])
    nombres["ciudad"] = "Por ciudad" if g["lang"] == "es" else "By city"
    meta = ("Lo más reciente · " if g["lang"] == "es" else "Latest · ") if destacada else ""
    return '''<a class="bl-card rev%s%s" href="%s.html" data-t="%s"%s><span class="bl-foto"><img src="assets/%s.jpg" alt="" loading="lazy"></span>
  <span class="bl-txt"><span class="bl-meta">%s%s · %s</span><span class="bl-tit">%s</span><span class="bl-desc">%s</span><span class="bl-ir">%s</span></span></a>''' % (
        " bl-dest" if destacada else "", " bl-media" if media else "", g["slug"], g["_cat"], ' style="--d:%dms"' % d if d else "", g["_foto"],
        meta, nombres.get(g["_cat"], ""), fecha_corta(g), g["h1"].replace("<br>", " "), g.get("intro") or g["descripcion"],
        "Leer" if g["lang"] == "es" else "Read")


def bloque_lecturas(lista, ceja, titulo, lang="es", sid=""):
    """Fila de 3 tarjetas con enlace al blog (inicio, cada cirugía y el final de cada guía)."""
    if not lista:
        return ""
    blog = BLOG[lang]
    return '''<section class="sec bl-fila"%s><div class="bl-in"><header class="bl-cab"><div><p class="ceja rev">%s</p><h2 class="rev">%s</h2></div><a class="enlace rev" href="%s">%s</a></header>
<div class="bl-grid tres">%s</div></div></section>''' % (' id="%s"' % sid if sid else "", ceja, titulo, blog["archivo"], blog["ver_todo"],
                                                         "".join(tarjeta(g, d=i * 120) for i, g in enumerate(lista[:3])))


def ultimas(guias, lang="es", n=3):
    return [g for g in guias if g["lang"] == lang and g.get("tipo") != "ciudad"][:n]


def local(g):
    return g.get("publico") == "colombia"


def de_procedimiento(guias, slug, n=3, relleno=True):
    """Lecturas para la página de un procedimiento: primero las que tratan de él; luego (si relleno) las de quien vive
    en Colombia y después las de seguridad y viaje."""
    mias = [g for g in guias if g["lang"] == "es" and g.get("tipo") != "ciudad"]
    sobre = [g for g in mias if slug in g.get("procedimientos", [])]
    raices = [p[:4] for p in slug.split("-") if len(p) > 3]  # "lipo", "aume"…: la guía la nombra en su dirección
    sobre.sort(key=lambda g: (not any(r in g["slug"] for r in raices), g.get("procedimientos", [None])[0] != slug, g["_cat"] != "procedimientos"))
    if not relleno:
        return sobre[:n]
    resto = [g for g in mias if g not in sobre]
    resto.sort(key=lambda g: (not local(g), {"seguridad": 0, "viaje": 1}.get(g["_cat"], 2)))
    return (sobre + resto)[:n]


def generar(b):
    """b = módulo build (pagina, hero, seccion, faq, cierre, tarjetas, wa, img, lineas, frase, CX_N, TR_N, HECHAS, DOMINIO)."""
    guias = leer()
    por_slug = {g["slug"]: g for g in guias}
    for g in guias:
        if g.get("par") and g["par"] not in por_slug:
            g["par"] = None  # el par aún no existe: sin hreflang roto

    def enlace_proc(slug, lang="es"):
        p = b.CX_N.get(slug) or b.TR_N.get(slug)
        if p and lang == "en" and b.FE.en_de(slug):
            return (b.FE.FICHAS_EN[slug]["nombre"], b.FE.en_de(slug))
        return (p["nombre"], slug + ".html") if p else None

    def relacionadas(g):
        mismas = [x for x in guias if x["lang"] == g["lang"] and x["slug"] != g["slug"] and x.get("tipo") != "ciudad"]
        mismas.sort(key=lambda x: (local(x) != local(g), x.get("ciudad") != g.get("ciudad") or not g.get("ciudad"),
                                   not set(x.get("procedimientos", [])) & set(g.get("procedimientos", []))))
        return mismas[:3]

    for g in guias:
        t = T[g["lang"]]
        ciudad = CIUDADES.get(g.get("ciudad") or "")
        nombre_ciudad = (ciudad[0] if g["lang"] == "es" else ciudad[1]) if ciudad else None
        msj = (t["wa"] % nombre_ciudad) if nombre_ciudad else t["wa_gen"]
        procs = [x for x in (enlace_proc(s, g["lang"]) for s in g.get("procedimientos", [])) if x]
        rel = relacionadas(g)
        cuerpo = b.hero(g.get("fondo", "seda-horizonte"), g["ceja"], g["h1"], g.get("intro", ""))
        cuerpo += '''<section class="sec marfil articulo-sec"><div class="sec-in solo articulo">
  <p class="art-meta"><a href="%s">%s</a> · %s · %s %s</p>
  %s
  %s
  <p class="art-aviso">%s</p>
</div></section>''' % (BLOG[g["lang"]]["archivo"], BLOG[g["lang"]]["nombre"], t["por"], t["act"], fecha_txt(g.get("actualizado") or g["publicado"], g["lang"]), g["cuerpo"],
                        ('<div class="art-procs"><p class="ceja">%s</p><div>%s</div></div>' % (t["proc"], "".join('<a href="%s">%s</a>' % (h, n) for n, h in procs))) if procs else "",
                        t["aviso"])
        if g.get("faq"):
            cuerpo += b.seccion(t["preg"], g.get("faq_titulo") or t["preg"], b.faq([("", p, r, []) for p, r in g["faq"]]), "marfil")
        cuerpo += bloque_lecturas(rel, BLOG[g["lang"]]["nombre"], BLOG[g["lang"]]["rel_tit"], g["lang"])
        if not local(g):  # quien vive en EE. UU.: las guías de cada ciudad, a un clic
            ciudades_g = {x["ciudad"]: x for x in guias if x["lang"] == g["lang"] and x.get("tipo") == "ciudad" and x.get("ciudad") and x["slug"] != g["slug"]}
            h = BLOG[g["lang"]]
            lista_c = "".join('<li class="rev"><a href="%s.html"><span class="ceja">%s</span><b>%s</b><span class="fl" aria-hidden="true">→</span></a></li>' % (
                ciudades_g[k]["slug"], h["desde"], v[0] if g["lang"] == "es" else v[1]) for k, v in CIUDADES.items() if k in ciudades_g)
            if lista_c:
                cuerpo += '<section class="sec bl-fila"><div class="bl-in"><header class="bl-cab"><div><p class="ceja rev">%s</p><h2 class="rev">%s</h2></div><a class="enlace rev" href="%s">%s</a></header><ul class="bl-ciudades">%s</ul></div></section>' % (
                    h["c_ceja"], h["c_tit"], h["hub"][0], h["hub"][1], lista_c)
        if local(g):
            cuerpo += b.cierre()  # quien vive en Colombia: el mismo cierre de la web (valoración presencial en Medellín)
        else:
            cuerpo += b.cierre(t["cierre"], t["cierre_t"], '<a class="boton lleno" href="%s" target="_blank" rel="noopener">%s</a>' % (b.wa(msj), t["boton"]), fondo="seda-oscura")

        url = b.DOMINIO + "/" + g["slug"]
        blog_url = b.DOMINIO + "/" + BLOG[g["lang"]]["archivo"][:-5]
        esquema = [
            {"@context": "https://schema.org", "@type": "MedicalWebPage", "headline": g["title"], "description": g["descripcion"], "url": url,
             "inLanguage": "es-CO" if g["lang"] == "es" else "en-US", "datePublished": g["publicado"], "dateModified": g.get("actualizado") or g["publicado"],
             "author": {"@type": "Organization", "name": "noon Clinic", "@id": b.DOMINIO + "/#clinica"}, "publisher": {"@id": b.DOMINIO + "/#clinica"},
             "about": [{"@type": "MedicalProcedure", "name": enlace_proc(s)[0], "url": b.DOMINIO + "/" + s} for s in g.get("procedimientos", []) if enlace_proc(s)],
             "audience": {"@type": "Patient", "geographicArea": "Colombia" if local(g) else (nombre_ciudad or "United States")}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "noon Clinic", "item": b.DOMINIO + "/"},
                {"@type": "ListItem", "position": 2, "name": BLOG[g["lang"]]["nombre"], "item": blog_url},
                {"@type": "ListItem", "position": 3, "name": g["title"], "item": url}]},
        ]
        if g.get("faq"):
            esquema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": re.sub("<[^>]+>", "", p), "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", r)}} for p, r in g["faq"]]})
        b.pagina(g["slug"] + ".html", g["title"], g["descripcion"], cuerpo, lang=g["lang"],
                 alterna=(g["par"] + ".html") if g.get("par") else None, esquema=esquema, foto=g.get("fondo"),
                 etiquetas={"seccion": "blog" if local(g) else "internacional", "tipo": g.get("tipo", "guia"), "ciudad": g.get("ciudad") or ("colombia" if local(g) else "general")})

    hubs(b, guias)
    blog(b, guias)
    sitemap(b, guias)
    return len(guias)


HUB = {
    "es": {"titulo": "Pacientes en Estados Unidos: cirugía plástica en Medellín", "desc": "Vives en Miami, Nueva York, Orlando, Houston, Atlanta o Boston y quieres operarte en Medellín. Cómo organizar tu viaje a noon Clinic, paso a paso.",
           "ceja": "Pacientes en EE. UU.", "h1": "Vives allá.<br>Te tratas <em>aquí</em>.", "sub": "Guías para organizar tu procedimiento en Medellín desde Estados Unidos: fechas, estadía, controles y regreso.",
           "frase": "Muchos de nuestros pacientes viven fuera de Colombia. El reto no es la cirugía: es <em>organizar bien el viaje</em>.",
           "c_ceja": "Desde tu ciudad", "c_tit": "Guías por ciudad", "pasos_tit": "Cómo se organiza tu viaje",
           "pasos": [("Escríbenos antes de comprar tiquetes", "Cuéntanos qué te interesa y desde qué ciudad viajas. Adelantamos tu información por WhatsApp."),
                     ("Valoración en persona al llegar", "El especialista te examina en Medellín. Si es cirugía, te ordena los exámenes previos."),
                     ("Procedimiento", "La cirugía se hace en quirófano, nunca en un consultorio."),
                     ("Recuperación y controles", "Te quedas en la ciudad los días que indique tu especialista."),
                     ("Regreso y seguimiento", "Vuelas cuando tu especialista lo autorice. Ya en casa, seguimos contigo por WhatsApp o videollamada.")],
           "g_ceja": "Guías", "g_tit": "Para leer antes de viajar", "sin_guias": "Muy pronto, nuevas guías para pacientes que viajan desde Estados Unidos.",
           "otro": ("international-patients.html", "Read in English")},
    "en": {"titulo": "International patients: plastic surgery in Medellín from the US", "desc": "Living in Miami, New York, Orlando, Houston, Atlanta or Boston and considering surgery in Medellín, Colombia? How to plan your trip to noon Clinic, step by step.",
           "ceja": "International patients", "h1": "You live there.<br>You heal <em>here</em>.", "sub": "Guides to plan your procedure in Medellín, Colombia from the United States: dates, stay, follow-ups and flying home.",
           "frase": "Many of our patients live outside Colombia. Surgery isn't the hard part: <em>planning the trip well</em> is.",
           "c_ceja": "From your city", "c_tit": "City guides", "pasos_tit": "How your trip works",
           "pasos": [("Message us before you buy tickets", "Tell us what you're interested in and where you're flying from. We get your details ready on WhatsApp."),
                     ("In-person consultation when you arrive", "Your specialist examines you in Medellín and, for surgery, orders your pre-op tests."),
                     ("Your procedure", "Surgery is always performed in an operating room, never in a doctor's office."),
                     ("Recovery and follow-ups", "You stay in the city for the days your specialist recommends."),
                     ("Flying home and follow-up", "You fly when your specialist clears you. Once you're home, we stay in touch by WhatsApp or video call.")],
           "g_ceja": "Guides", "g_tit": "Read before you travel", "sin_guias": "New guides for patients traveling from the United States are coming soon.",
           "otro": ("pacientes-internacionales.html", "Leer en español")},
}


def hubs(b, guias):
    for lang, h in HUB.items():
        t = T[lang]
        mias = [g for g in guias if g["lang"] == lang and not local(g)]  # las guías para quien vive en Colombia van solo en /blog
        ciudad_pag = {g["ciudad"]: g for g in mias if g.get("tipo") == "ciudad" and g.get("ciudad")}
        tiles = [("%s.html" % ciudad_pag[k]["slug"], h["c_ceja"], (v[0] if lang == "es" else v[1]), ciudad_pag[k]["ceja"], v[2])
                 for k, v in CIUDADES.items() if k in ciudad_pag]
        otras = [g for g in mias if g.get("tipo") != "ciudad"]
        lista = '<ul class="lineas">%s</ul>' % "".join(
            '<li class="rev"><b><a href="%s.html">%s</a></b><span>%s</span></li>' % (g["slug"], g["h1"].replace("<br>", " "), g["descripcion"]) for g in otras) if otras else '<p class="sub">%s</p>' % h["sin_guias"]
        cuerpo = (b.hero("seda-horizonte", h["ceja"], h["h1"], h["sub"], "alto")
                  + b.frase(h["ceja"], h["frase"], '<a class="enlace" href="%s" lang="%s">%s</a>' % (h["otro"][0], "en" if lang == "es" else "es", h["otro"][1]))
                  + ('<section class="sec sin-borde" id="cities"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">%s</p><h2 class="rev">%s</h2></header>%s</div></section>' % (h["c_ceja"], h["c_tit"], b.tarjetas(tiles)) if tiles else "")
                  + b.seccion(h["ceja"], h["pasos_tit"], '<ol class="tiempo num">%s</ol>' % "".join('<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in h["pasos"]), "marfil")
                  + b.seccion(h["g_ceja"], h["g_tit"], lista, sid="guides")
                  + b.cierre(t["cierre"], t["cierre_t"], '<a class="boton lleno" href="%s" target="_blank" rel="noopener">%s</a>' % (b.wa(t["wa_gen"]), t["boton"]), fondo="seda-oscura"))
        esquema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": h["titulo"], "description": h["desc"], "inLanguage": "es-CO" if lang == "es" else "en-US",
                    "hasPart": [{"@type": "WebPage", "name": g["title"], "url": b.DOMINIO + "/" + g["slug"]} for g in mias]}]
        b.pagina(t["hub"], h["titulo"], h["desc"], cuerpo, lang=lang, alterna=h["otro"][0], esquema=esquema, foto="seda-horizonte",
                 etiquetas={"seccion": "internacional", "tipo": "hub"})


BLOG = {
    "es": {"archivo": "blog.html", "nombre": "Blog", "ver_todo": "Ver todo el blog", "rel_tit": "Sigue <em>leyendo</em>.", "todo": "Todo",
           "titulo": "Blog: cirugía plástica y medicina estética en Medellín", "h1": "Para leer <em>con calma</em>.",
           "desc": "Guías de noon Clinic sobre cada procedimiento, la recuperación, la seguridad y cómo organizar tu viaje a Medellín.",
           "sub": "Guías del equipo de noon Clinic para decidir con información: cada procedimiento, la recuperación, la seguridad y cómo organizar tu viaje.",
           "c_ceja": "Por ciudad", "c_tit": "Si vives en <em>Estados Unidos</em>.", "desde": "Desde", "hub": ("pacientes-internacionales.html", "Cómo organizar tu viaje"),
           "otro": "guides.html", "filtrar": "Filtrar por tema"},
    "en": {"archivo": "guides.html", "nombre": "Guides", "ver_todo": "See all guides", "rel_tit": "Keep <em>reading</em>.", "todo": "All",
           "titulo": "Guides: plastic surgery in Medellín, Colombia from the US", "h1": "Before you <em>decide</em>.",
           "desc": "noon Clinic guides on each procedure, recovery, safety and planning your trip to Medellín, Colombia from the United States.",
           "sub": "Guides from the noon Clinic team on each procedure, recovery, safety and planning your trip to Medellín from the United States.",
           "c_ceja": "By city", "c_tit": "Flying in from <em>your city</em>.", "desde": "From", "hub": ("international-patients.html", "Plan your trip"),
           "otro": "blog.html", "filtrar": "Filter by topic"},
}


def blog(b, guias):
    """Página del blog: filtros por tema, la guía más reciente en grande, las demás en tarjetas y las guías por ciudad."""
    for lang, h in BLOG.items():
        t = T[lang]
        mias = [g for g in guias if g["lang"] == lang and g.get("tipo") != "ciudad"]
        ciudades = {g["ciudad"]: g for g in guias if g["lang"] == lang and g.get("tipo") == "ciudad" and g.get("ciudad")}
        hay = {g["_cat"] for g in mias}
        filtros = '<button type="button" class="on" data-t="" aria-pressed="true">%s</button>' % h["todo"] + "".join(
            '<button type="button" data-t="%s" aria-pressed="false">%s</button>' % (k, n) for k, n in CATS[lang] if k in hay)
        # filas siempre completas: si sobran 1 o 2 tarjetas, las primeras van de a 2 por fila (más grandes) y el resto de a 3
        medias = {0: 0, 1: 4, 2: 2}[(len(mias) - 1) % 3] if len(mias) > 4 else 0
        tarjetas = "".join(tarjeta(g, destacada=(i == 0), media=(0 < i <= medias), d=((i - 1) % (2 if i <= medias else 3)) * 120 if i else 0) for i, g in enumerate(mias))
        lista_c = "".join('<li class="rev"><a href="%s.html"><span class="ceja">%s</span><b>%s</b><span class="fl" aria-hidden="true">→</span></a></li>' % (
            ciudades[k]["slug"], h["desde"], v[0] if lang == "es" else v[1]) for k, v in CIUDADES.items() if k in ciudades)
        cuerpo = (b.hero("seda-noche", h["nombre"], h["h1"], h["sub"], "medio")
                  + '<section class="sec marfil bl-pag"><div class="bl-in"><div class="bl-filtros rev" role="group" aria-label="%s">%s</div><div class="bl-grid bl-lista">%s</div></div></section>' % (h["filtrar"], filtros, tarjetas)
                  + ('<section class="sec bl-fila"><div class="bl-in"><header class="bl-cab"><div><p class="ceja rev">%s</p><h2 class="rev">%s</h2></div><a class="enlace rev" href="%s">%s</a></header><ul class="bl-ciudades">%s</ul></div></section>' % (
                      h["c_ceja"], h["c_tit"], h["hub"][0], h["hub"][1], lista_c) if lista_c else "")
                  + (b.cierre() if lang == "es" else b.cierre(t["cierre"], t["cierre_t"], '<a class="boton lleno" href="%s" target="_blank" rel="noopener">%s</a>' % (b.wa(t["wa_gen"]), t["boton"]), fondo="seda-oscura")))
        esquema = [{"@context": "https://schema.org", "@type": "Blog", "name": h["titulo"], "description": h["desc"], "url": b.DOMINIO + "/" + h["archivo"][:-5],
                    "inLanguage": "es-CO" if lang == "es" else "en-US", "publisher": {"@id": b.DOMINIO + "/#clinica"},
                    "blogPost": [{"@type": "BlogPosting", "headline": g["title"], "url": b.DOMINIO + "/" + g["slug"], "datePublished": g["publicado"],
                                  "dateModified": g.get("actualizado") or g["publicado"], "image": b.DOMINIO + "/assets/" + g["_foto"] + ".jpg"} for g in mias]}]
        b.pagina(h["archivo"], h["titulo"], h["desc"], cuerpo, lang=lang, alterna=h["otro"], esquema=esquema, foto="seda-noche",
                 etiquetas={"seccion": "blog", "tipo": "listado"})


REGISTRO_FECHAS = os.path.join(AQUI, "_lastmod.json")  # {archivo: [huella del contenido, fecha del último cambio real]}


def _huella(archivo):
    """Solo cuenta lo que es contenido: título, descripción, datos para Google y el cuerpo de la página
    (no letras, scripts ni versiones de archivos)."""
    txt = open(os.path.join(AQUI, archivo), encoding="utf-8").read()
    partes = re.findall(r"<title>.*?</title>|<meta name=\"description\"[^>]*>|<script type=\"application/ld\+json\">.*?</script>|<main>.*</main>", txt, re.S)
    return hashlib.md5(re.sub(r"\?v=[0-9a-zA-Z]+", "", "".join(partes) or txt).encode("utf-8")).hexdigest()


def fechas_reales(b, fechas_guias, hoy):
    """Fecha honesta para el sitemap: la guía usa su 'actualizado'; el resto, el día en que su contenido cambió de verdad
    (se compara la huella con la del build anterior, guardada en _lastmod.json, que va en el repositorio)."""
    try:
        reg = json.load(open(REGISTRO_FECHAS, encoding="utf-8"))
    except (OSError, ValueError):
        reg = {}
    out = {}
    for a in sorted(set(b.HECHAS)):
        h = _huella(a)
        if a in fechas_guias:
            out[a] = fechas_guias[a]
        else:
            out[a] = reg[a][1] if a in reg and reg[a][0] == h else hoy
        reg[a] = [h, out[a]]
    with open(REGISTRO_FECHAS, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=0, sort_keys=True)
    return out


def sitemap(b, guias):
    hoy = date.today().isoformat()
    fechas = fechas_reales(b, {g["slug"] + ".html": g.get("actualizado") or g["publicado"] for g in guias}, hoy)
    pares = {g["slug"] + ".html": g["par"] + ".html" for g in guias if g.get("par")}
    pares.update({"pacientes-internacionales.html": "international-patients.html", "international-patients.html": "pacientes-internacionales.html",
                  "blog.html": "guides.html", "guides.html": "blog.html"})
    idioma = {g["slug"] + ".html": g["lang"] for g in guias}
    idioma["international-patients.html"] = idioma["guides.html"] = "en"
    for es, en in getattr(b, "PARES_EN", {}).items():  # fichas y hubs en inglés ↔ español
        pares[es], pares[en] = en, es
        idioma[en] = "en"
    urls = []
    for a in sorted(set(b.HECHAS)):
        loc = b.DOMINIO + "/" + ("" if a == "index.html" else a[:-5])
        x = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n" % (loc, fechas[a])
        if a in pares:
            otro = pares[a]
            es_a, en_a = (a, otro) if idioma.get(a, "es") == "es" else (otro, a)
            for hl, f in (("es", es_a), ("en", en_a), ("x-default", es_a)):
                x += '    <xhtml:link rel="alternate" hreflang="%s" href="%s/%s"/>\n' % (hl, b.DOMINIO, f[:-5])
        urls.append(x + "  </url>\n")
    with open(os.path.join(AQUI, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s</urlset>\n' % "".join(urls))
    reglas = "Allow: /\nDisallow: /capacitacion-comercial\nDisallow: /cotizador\nDisallow: /_agencia-seo/\n"
    ia = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
          "Google-Extended", "Applebot-Extended", "Bingbot", "meta-externalagent"]
    with open(os.path.join(AQUI, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\n" + reglas + "\n# Buscadores y asistentes con IA: bienvenidos (mismas reglas)\n"
                + "".join("User-agent: %s\n" % x for x in ia) + reglas + "\nSitemap: %s/sitemap.xml\n" % b.DOMINIO)
    llms(b, guias)


def llms(b, guias):
    """llms.txt: resumen de noon para asistentes con IA (ChatGPT, Claude, Perplexity…), con el contacto único de la clínica."""
    d = b.DOMINIO
    wa = "https://wa.me/" + b.WHATSAPP
    def fila(slug):
        en = b.FE.en_de(slug)
        return "- [%s](%s/%s)" % (b.NOMBRE_EN[slug], d, en[:-5] if en else slug)
    txt = ["# noon Clinic", "",
           "> Plastic surgery and aesthetic medicine clinic in Medellín, Colombia. Contact for patients (WhatsApp and phone): %s (%s). Website: %s" % (b.TEL_VISIBLE, wa, d), "",
           "## Key facts", ""] + ["- %s: %s" % (k, re.sub("<[^>]+>", "", v)) for k, v in b.DATOS_EN] + [
           "- Patients: people who live in Colombia and international patients.", "",
           "## About", "", "- [About noon Clinic (English)](%s/about-noon-clinic)" % d, "- [International patients](%s/international-patients)" % d,
           "- [Specialists (Spanish)](%s/especialistas)" % d, "- [Safety (Spanish)](%s/seguridad)" % d, "",
           "## Plastic surgery", ""] + [fila(c["slug"]) for c in b.CIRUGIAS_NOON] + [
           "", "## Aesthetic medicine", ""] + [fila(t["slug"]) for t in b.TRATAMIENTOS] + [
           "- [Cryolipolysis (fat freezing)](%s/criolipolisis)" % d, "",
           "## Guides in English", ""] + ["- [%s](%s/%s)" % (g["title"], d, g["slug"]) for g in guias if g["lang"] == "en"] + [
           "", "## Guías en español", ""] + ["- [%s](%s/%s)" % (g["title"], d, g["slug"]) for g in guias if g["lang"] == "es"] + [
           "", "## Contact", "", "- WhatsApp / phone: %s" % b.TEL_VISIBLE, "- WhatsApp link: %s" % wa, ""]
    with open(os.path.join(AQUI, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(txt))
