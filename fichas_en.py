# -*- coding: utf-8 -*-
# Versión en INGLÉS de las fichas de procedimientos (pacientes extranjeros y asistentes con IA).
# Textos en datos_noon_en.py (FICHAS_EN: slug español → campos en inglés, adaptados y verificados contra el español).
# build.py llama a generar(b) después de las fichas en español y antes de las guías (para que entren al sitemap).
import os, re

try:
    from datos_noon_en import FICHAS_EN
except ImportError:
    FICHAS_EN = {}

# dirección en inglés de cada ficha (español → inglés)
EN_SLUG = {
    "rinoplastia": "rhinoplasty-medellin", "liposuccion": "liposuction-medellin", "lipotransferencia-glutea": "brazilian-butt-lift-medellin",
    "abdominoplastia": "tummy-tuck-medellin", "mamoplastia-de-aumento": "breast-augmentation-medellin", "mommy-makeover": "mommy-makeover-medellin",
    "mastopexia": "breast-lift-medellin", "blefaroplastia": "eyelid-surgery-medellin", "mentoplastia": "chin-surgery-medellin",
    "lifting-facial": "facelift-medellin", "bichectomia": "buccal-fat-removal-medellin", "otoplastia": "ear-surgery-medellin",
    "lipopapada": "chin-liposuction-medellin", "mamoplastia-de-reduccion": "breast-reduction-medellin",
    "recambio-de-implantes": "breast-implant-exchange-medellin", "ginecomastia": "gynecomastia-surgery-medellin",
    "mini-abdominoplastia": "mini-tummy-tuck-medellin", "braquioplastia": "arm-lift-medellin", "lifting-de-muslos": "thigh-lift-medellin",
    "cirugia-post-bariatrica": "body-contouring-after-weight-loss-medellin", "labioplastia": "labiaplasty-medellin",
    "toxina-botulinica": "botox-medellin", "acido-hialuronico": "dermal-fillers-medellin", "bioestimuladores": "collagen-biostimulators-medellin",
    "hilos-tensores": "thread-lift-medellin", "skinboosters": "skin-boosters-medellin", "plasma-rico-en-plaquetas": "prp-medellin",
    "peelings": "chemical-peel-medellin", "microagujas": "microneedling-medellin", "limpieza-facial-medica": "medical-facial-medellin",
    "manchas-y-melasma": "melasma-treatment-medellin", "laser": "laser-skin-treatment-medellin", "depilacion-laser": "laser-hair-removal-medellin",
    "hifu": "hifu-medellin", "radiofrecuencia": "radiofrequency-skin-tightening-medellin", "tratamientos-corporales": "body-treatments-medellin",
    "sueroterapia": "iv-therapy-medellin", "manejo-medico-del-peso": "medical-weight-loss-medellin", "nutricion": "nutrition-medellin",
}
HUB_CX, HUB_ME = "plastic-surgery-medellin.html", "aesthetic-medicine-medellin.html"
CAT_EN = {"rostro": ("Face", "Eyelids, nose, chin, ears and facial rejuvenation."),
          "senos": ("Breasts", "Volume, lift, reduction and implant exchange."),
          "cuerpo": ("Body contouring", "Liposuction, tummy, buttocks, arms and thighs."),
          "combinadas": ("Combined and intimate", "Combined procedures and intimate surgery."),
          "inyectables": ("Injectables", "Botox, dermal fillers, biostimulators and threads."),
          "piel": ("Skin", "Skin quality, glow, dark spots and texture."),
          "tecnologias": ("Technologies", "Laser, HIFU, radiofrequency and body treatments."),
          "bienestar": ("Wellness", "IV therapy, medical weight management and nutrition.")}
# estadía de referencia (la misma de otra-ciudad.html y de la agencia)
ESTADIA = {"rostro": "1 to 2 weeks", "senos": "1 to 2 weeks", "cuerpo": "2 to 3 weeks", "combinadas": "2 to 3 weeks"}
EXTRA_EN = {"tu-proceso.html": "international-patients.html", "seguridad.html": "is-it-safe-to-get-plastic-surgery-in-colombia.html",
            "otra-ciudad.html": "international-patients.html", "cirugia-plastica.html": HUB_CX, "medicina-estetica.html": HUB_ME,
            "especialistas.html": "about-noon-clinic.html", "preguntas-frecuentes.html": "international-patients.html"}


def en_de(slug):
    """Archivo de la ficha en inglés (o None si aún no existe su texto)."""
    return EN_SLUG[slug] + ".html" if slug in FICHAS_EN and slug in EN_SLUG else None


def _sin_tags(t):
    return re.sub("<[^>]+>", "", t)


def generar(b):
    """b = módulo build. Devuelve {archivo español: archivo inglés} para el hreflang del sitemap."""
    pares = {}
    if not FICHAS_EN:
        return pares
    todas = [(p, "cx") for p in b.CIRUGIAS_NOON] + [(p, "me") for p in b.TRATAMIENTOS]
    wa_en = b.wa()

    def fila(p, tipo):
        e = FICHAS_EN[p["slug"]]
        d = e["datos"]
        meta = ("%s · Time off work %s" % (d[0], d[2].lower())) if tipo == "cx" else ("%s · %s" % (d[0], d[1]))
        return '<li class="rev"><a href="%s" data-img="%s"><b>%s</b><span class="c">%s</span><span class="m">%s</span><span class="fl" aria-hidden="true">→</span></a></li>' % (
            en_de(p["slug"]), b.img(b.FONDO_ITEM.get(p["slug"], "seda-oscura")), e["nombre"], e["corto"], meta)

    def catalogo_en(lista):
        return '<ul class="catalogo">%s</ul>' % "".join(fila(p, t) for p, t in lista if p["slug"] in FICHAS_EN)

    def especialista_en(area, texto):
        es = b.esp_de(area)
        if not es:
            return ""
        x = es[0]
        rol = "Plastic surgeon" if area == "cirugia" else "Aesthetic physician"
        nombre = x["nombre"].replace("Dra. ", "Dr. ")
        return '''<section class="esp-bloque" id="especialista"><div class="esp-in">
  <figure class="rev">%s</figure>
  <div class="texto rev"><p class="ceja">Your specialist</p><h2>%s</h2><p class="rol">%s</p><p class="sub">%s</p>
  <a class="enlace" href="about-noon-clinic.html">About noon Clinic</a></div>
</div></section>''' % (b.foto_esp(x), nombre, rol, texto)

    def linea_tiempo_en(pasos):
        return b.linea_tiempo(pasos).replace('aria-label="Etapa anterior"', 'aria-label="Previous stage"').replace('aria-label="Etapa siguiente"', 'aria-label="Next stage"')

    def subnav_en(pares_nav):
        return b.subnav(pares_nav).replace('aria-label="En esta página"', 'aria-label="On this page"')

    def faq_en(items):
        return b.faq([("", it["q"], it["a"], []) for it in items])

    def todo_en(e):
        if not e.get("todo"):
            return ""
        items = "".join('<details class="preg rev"><summary>%s</summary><div class="resp todo-resp">%s</div></details>' % (t["h"], t["p"]) for t in e["todo"])
        return b.seccion("Before you decide", e["todo_titulo"], '<div class="preguntas">%s</div>' % items, sid="todo")

    def guias_en(slug):
        g = [x for x in b.GUIAS if x["lang"] == "en" and x.get("tipo") != "ciudad" and slug in x.get("procedimientos", [])]
        return b.G.bloque_lecturas(g, "Guides", "Before you <em>travel</em>.", lang="en", sid="lecturas") if g else ""

    for p, tipo in todas:
        if p["slug"] not in FICHAS_EN:
            continue
        e = FICHAS_EN[p["slug"]]
        archivo = en_de(p["slug"])
        f = b.FONDO_ITEM[p["slug"]]
        d = e["datos"]
        cx = tipo == "cx"
        cat = CAT_EN[p["cat"]][0]
        otras = [(x, tipo) for x in (b.CIRUGIAS_NOON if cx else b.TRATAMIENTOS) if x["cat"] == p["cat"] and x["slug"] != p["slug"]]
        if cx:
            barra = [("Duration", d[0]), ("Anesthesia", d[1]), ("Time off work (approx.)", d[2]), ("Final result", d[3])]
            viaje = ("If you are flying in, plan to stay in Medellín for about %s for this surgery, and fly home only when your surgeon clears you. "
                     "Travel with an adult companion for the first days." % ESTADIA.get(p["cat"], "2 to 3 weeks"))
        else:
            barra = [("Sessions", d[0]), ("Session length", d[1]), ("Downtime", d[2]), ("Result", d[3])]
            viaje = "Aesthetic treatments usually take the same day or a few days, so they fit into a short trip. Your doctor confirms your plan at the consultation."
        nav = [("que-es", "What it is"), ("para-ti", "Is it for you")] + ([("recuperacion", "Recovery")] if cx else []) + \
              ([("todo", "Before you decide")] if e.get("todo") else []) + [("viaje", "Coming from abroad"), ("especialista", "Specialist"), ("preguntas", "FAQ")]
        quien = "Dr. Fernando Ruiz, plastic surgeon" if cx else "Dr. Valeria Enciso, aesthetic physician"
        cuerpo = (b.hero(f, ("Plastic surgery · " if cx else "Aesthetic medicine · ") + cat, e["nombre"], e["corto"], "alto" if cx else "medio")
                  + b.datos_barra(barra)
                  + subnav_en(nav)
                  + b.frase("The procedure" if cx else "The treatment", e["que_es"][0], e["que_es"][1] if len(e["que_es"]) > 1 else "", "media", sid="que-es")
                  + b.seccion("Is it for you", "What you're looking for", b.lineas([(x,) for x in e["ideal"]])
                              + '<p class="pista rev">%s</p>' % ("Your surgeon makes the final call at your consultation." if cx else "Your doctor makes the final call at your consultation."), sid="para-ti")
                  + (b.seccion("Recovery", "Step by step", linea_tiempo_en([(r["t"], r["d"]) for r in e["recuperacion"]])
                               + '<p class="pista rev">These are guideline times. Your surgeon gives you the exact ones.</p>', sid="recuperacion") if cx and e.get("recuperacion") else "")
                  + todo_en(e)
                  + b.seccion("Coming from abroad", "Plan your <em>trip</em>.", '<p class="sub rev">%s</p><a class="enlace rev" href="international-patients.html">How a trip to Medellín for surgery works</a>' % viaje, "marfil", sid="viaje")
                  + especialista_en("cirugia" if cx else "estetica", "Your consultation is in person in Medellín, with %s." % quien)
                  + b.seccion("FAQ", "Common <em>questions</em>", faq_en(list(e["faq"]) + list(e.get("faq_nuevas", []))), "marfil", sid="preguntas")
                  + guias_en(p["slug"])
                  + (b.seccion("Also in " + cat.lower(), "Other procedures" if cx else "Other treatments", catalogo_en(otras)) if otras else "")
                  + b.cierre(e["nombre"], e["cierre_txt"], '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Message us on WhatsApp</a>' % wa_en, fondo=f)
                  + '''<div class="barra-cta" aria-label="Book"><div class="bc-t"><b>%s</b><span>Consultation with %s</span></div>
  <a class="boton lleno" href="%s" target="_blank" rel="noopener">Book<span class="solo-grande"> on WhatsApp</span></a></div>''' % (e["nombre"], quien.split(",")[0], wa_en))
        url = b.DOMINIO + "/" + archivo[:-5]
        hub, hub_n = (HUB_CX, "Plastic surgery") if cx else (HUB_ME, "Aesthetic medicine")
        preguntas = list(e["faq"]) + list(e.get("faq_nuevas", []))
        esquema = [{"@context": "https://schema.org", "@type": "MedicalWebPage", "url": url, "name": e["nombre"], "inLanguage": "en-US",
                    "about": {"@type": "MedicalProcedure", "name": e["nombre"], "description": " ".join(e["que_es"])}, "publisher": {"@id": b.DOMINIO + "/#clinica"}},
                   {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                       {"@type": "ListItem", "position": 1, "name": "noon Clinic", "item": b.DOMINIO + "/about-noon-clinic"},
                       {"@type": "ListItem", "position": 2, "name": hub_n, "item": b.DOMINIO + "/" + hub[:-5]},
                       {"@type": "ListItem", "position": 3, "name": e["nombre"], "item": url}]},
                   {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                       {"@type": "Question", "name": _sin_tags(q["q"]), "acceptedAnswer": {"@type": "Answer", "text": _sin_tags(q["a"])}} for q in preguntas]}]
        b.SEO_TITULOS[archivo] = (e["seo_title"], e["seo_desc"])
        b.pagina(archivo, e["seo_title"], e["seo_desc"], cuerpo, lang="en", alterna=p["slug"] + ".html", esquema=esquema, foto=f, og_tipo="website",
                 etiquetas={"seccion": "procedimiento-en", "tipo": tipo})
        pares[p["slug"] + ".html"] = archivo

    # hubs en inglés
    for archivo, es, tipo, cats, titulo, desc, h1, sub, fondo in [
        (HUB_CX, "cirugia-plastica.html", "cx", b.CATEGORIAS_CX, "Plastic surgery in Medellín, Colombia",
         "Plastic surgery at noon Clinic in Medellín, Colombia: face, breasts, body contouring and combined procedures, always in licensed operating rooms.",
         "Plastic surgery<br><em>in Medellín</em>.", "Every surgery starts by understanding what you want to change and what you want to keep.", "seda-burdeos"),
        (HUB_ME, "medicina-estetica.html", "me", b.CATEGORIAS_ME, "Aesthetic medicine in Medellín, Colombia",
         "Non-surgical aesthetic medicine at noon Clinic in Medellín: Botox, dermal fillers, biostimulators, skin, laser, HIFU and wellness, after a consultation.",
         "Aesthetic medicine<br><em>in Medellín</em>.", "Non-surgical medical treatments for your skin, face and body.", "seda-champan")]:
        lista = b.CIRUGIAS_NOON if tipo == "cx" else b.TRATAMIENTOS
        bloques = "".join('<section class="sec cat-bloque" id="%s"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">%s</p><h2 class="rev">%s</h2><p class="sub rev">%s</p></header><div class="sec-cuerpo">%s</div></div></section>' % (
            k, "Plastic surgery" if tipo == "cx" else "Aesthetic medicine", CAT_EN[k][0], CAT_EN[k][1], catalogo_en([(x, tipo) for x in lista if x["cat"] == k])) for k, n, dd, ff in cats)
        cuerpo = (b.hero(fondo, "Plastic surgery" if tipo == "cx" else "Aesthetic medicine", h1, sub, "alto") + bloques
                  + b.cierre("Talk to <em>us</em>", "Message us on WhatsApp at %s and we will plan your consultation with you." % b.TEL_VISIBLE,
                             '<a class="boton lleno" href="%s" target="_blank" rel="noopener">WhatsApp %s</a>' % (wa_en, b.TEL_VISIBLE), fondo="seda-oscura"))
        b.SEO_TITULOS[archivo] = (titulo, desc)
        b.pagina(archivo, titulo, desc, cuerpo, lang="en", alterna=es, foto=fondo, og_tipo="website", etiquetas={"seccion": "procedimiento-en", "tipo": "hub"})
        pares[es] = archivo
    return pares
