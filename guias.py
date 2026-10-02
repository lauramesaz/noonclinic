# -*- coding: utf-8 -*-
# Agencia SEO internacional de noon Clinic: guías y páginas por ciudad (español e inglés) para pacientes en EE. UU.
# Los textos los escriben los agentes en _agencia-seo/articulos/<slug>.html (cabecera JSON + cuerpo HTML).
# build.py llama a generar() al final: crea cada página, los dos hubs, sitemap.xml y robots.txt.
import os, json, re
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
           "act": "Updated", "proc": "Procedures in this guide (pages in Spanish)", "rel": "Keep reading", "preg": "Frequently asked questions",
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
    return out


def generar(b):
    """b = módulo build (pagina, hero, seccion, faq, cierre, tarjetas, wa, img, lineas, frase, CX_N, TR_N, HECHAS, DOMINIO)."""
    guias = leer()
    por_slug = {g["slug"]: g for g in guias}
    for g in guias:
        if g.get("par") and g["par"] not in por_slug:
            g["par"] = None  # el par aún no existe: sin hreflang roto

    def enlace_proc(slug):
        p = b.CX_N.get(slug) or b.TR_N.get(slug)
        return (p["nombre"], slug + ".html") if p else None

    def relacionadas(g):
        mismas = [x for x in guias if x["lang"] == g["lang"] and x["slug"] != g["slug"]]
        mismas.sort(key=lambda x: (x.get("ciudad") != g.get("ciudad") or not g.get("ciudad"),
                                   not set(x.get("procedimientos", [])) & set(g.get("procedimientos", []))))
        return mismas[:3]

    for g in guias:
        t = T[g["lang"]]
        ciudad = CIUDADES.get(g.get("ciudad") or "")
        nombre_ciudad = (ciudad[0] if g["lang"] == "es" else ciudad[1]) if ciudad else None
        msj = (t["wa"] % nombre_ciudad) if nombre_ciudad else t["wa_gen"]
        procs = [x for x in (enlace_proc(s) for s in g.get("procedimientos", [])) if x]
        rel = relacionadas(g)
        cuerpo = b.hero(g.get("fondo", "seda-horizonte"), g["ceja"], g["h1"], g.get("intro", ""))
        cuerpo += '''<section class="sec marfil articulo-sec"><div class="sec-in solo articulo">
  <p class="art-meta"><a href="%s">%s</a> · %s · %s %s</p>
  %s
  %s
  <p class="art-aviso">%s</p>
</div></section>''' % (t["hub"], t["hub_n"], t["por"], t["act"], fecha_txt(g.get("actualizado") or g["publicado"], g["lang"]), g["cuerpo"],
                        ('<div class="art-procs"><p class="ceja">%s</p><div>%s</div></div>' % (t["proc"], "".join('<a href="%s">%s</a>' % (h, n) for n, h in procs))) if procs else "",
                        t["aviso"])
        if g.get("faq"):
            cuerpo += b.seccion(t["preg"], g.get("faq_titulo") or t["preg"], b.faq([("", p, r, []) for p, r in g["faq"]]), "marfil")
        if rel:
            cuerpo += b.seccion(t["rel"], "noon Clinic", '<ul class="lineas">%s</ul>' % "".join(
                '<li class="rev"><b><a href="%s.html">%s</a></b><span>%s</span></li>' % (x["slug"], x["h1"].replace("<br>", " "), x["descripcion"]) for x in rel))
        cuerpo += b.cierre(t["cierre"], t["cierre_t"], '<a class="boton lleno" href="%s" target="_blank" rel="noopener">%s</a>' % (b.wa(msj), t["boton"]), fondo="seda-oscura")

        url = b.DOMINIO + "/" + g["slug"]
        hub_url = b.DOMINIO + "/" + t["hub"][:-5]
        esquema = [
            {"@context": "https://schema.org", "@type": "MedicalWebPage", "headline": g["title"], "description": g["descripcion"], "url": url,
             "inLanguage": "es-CO" if g["lang"] == "es" else "en-US", "datePublished": g["publicado"], "dateModified": g.get("actualizado") or g["publicado"],
             "author": {"@type": "Organization", "name": "noon Clinic", "@id": b.DOMINIO + "/#clinica"}, "publisher": {"@id": b.DOMINIO + "/#clinica"},
             "about": [enlace_proc(s)[0] for s in g.get("procedimientos", []) if enlace_proc(s)], "audience": {"@type": "Patient", "geographicArea": nombre_ciudad or "United States"}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "noon Clinic", "item": b.DOMINIO + "/"},
                {"@type": "ListItem", "position": 2, "name": t["hub_n"], "item": hub_url},
                {"@type": "ListItem", "position": 3, "name": g["title"], "item": url}]},
        ]
        if g.get("faq"):
            esquema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": re.sub("<[^>]+>", "", p), "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", r)}} for p, r in g["faq"]]})
        b.pagina(g["slug"] + ".html", g["title"], g["descripcion"], cuerpo, lang=g["lang"],
                 alterna=(g["par"] + ".html") if g.get("par") else None, esquema=esquema, foto=g.get("fondo"))

    hubs(b, guias)
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
        mias = [g for g in guias if g["lang"] == lang]
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
        b.pagina(t["hub"], h["titulo"], h["desc"], cuerpo, lang=lang, alterna=h["otro"][0], esquema=esquema, foto="seda-horizonte")


def sitemap(b, guias):
    hoy = date.today().isoformat()
    fechas = {g["slug"] + ".html": g.get("actualizado") or g["publicado"] for g in guias}
    pares = {g["slug"] + ".html": g["par"] + ".html" for g in guias if g.get("par")}
    pares.update({"pacientes-internacionales.html": "international-patients.html", "international-patients.html": "pacientes-internacionales.html"})
    idioma = {g["slug"] + ".html": g["lang"] for g in guias}
    idioma["international-patients.html"] = "en"
    urls = []
    for a in sorted(set(b.HECHAS)):
        loc = b.DOMINIO + "/" + ("" if a == "index.html" else a[:-5])
        x = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n" % (loc, fechas.get(a, hoy))
        if a in pares:
            otro = pares[a]
            es_a, en_a = (a, otro) if idioma.get(a, "es") == "es" else (otro, a)
            for hl, f in (("es", es_a), ("en", en_a), ("x-default", es_a)):
                x += '    <xhtml:link rel="alternate" hreflang="%s" href="%s/%s"/>\n' % (hl, b.DOMINIO, f[:-5])
        urls.append(x + "  </url>\n")
    with open(os.path.join(AQUI, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s</urlset>\n' % "".join(urls))
    with open(os.path.join(AQUI, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nDisallow: /capacitacion-comercial\nDisallow: /_agencia-seo/\n\nSitemap: %s/sitemap.xml\n" % b.DOMINIO)
