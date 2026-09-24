# -*- coding: utf-8 -*-
# noon Clinic · v3 clínica completa: cirugía plástica + medicina estética, sin precios, con especialistas
# Genera todas las páginas a partir de datos.py.   Uso:  python3 build.py
import os, time, json, re
from html import escape
from urllib.parse import quote
from datos import *
from datos_noon import *

AQUI = os.path.dirname(os.path.abspath(__file__))
CX = {c["slug"]: c for c in CIRUGIAS}
V = int(time.time())

CLARO = {"seda-clara", "seda-horizonte", "seda-champan"}  # fondos claros: texto oscuro encima
CX_N = {c["slug"]: c for c in CIRUGIAS_NOON}
TR_N = {t["slug"]: t for t in TRATAMIENTOS}
CAT_CX = {k: (n, d, f) for k, n, d, f in CATEGORIAS_CX}
CAT_ME = {k: (n, d, f) for k, n, d, f in CATEGORIAS_ME}


def wa(mensaje="Hola, quiero agendar mi cita de valoración en noon Clinic."):
    return "https://wa.me/" + WHATSAPP + "?text=" + quote(mensaje)


def img(nombre):
    return "assets/noon/%s.jpg" % nombre



# ---------------------------------------------------------------- piezas
def viva(fondo):
    return '<canvas class="seda-viva" data-p="%s" aria-hidden="true"></canvas>' % fondo[5:] if fondo.startswith("seda-") else ""


def hero(fondo, ceja, titulo, sub="", alto="medio", extra=""):
    tono = " sobre-claro" if fondo in CLARO else ""
    return '''<section class="hero %s%s"><div class="capa" style="background-image:url(%s)"></div>''' % (alto, tono, img(fondo)) + viva(fondo) + '''<div class="hero-in">
  <p class="ceja rev">%s</p><h1 class="rev">%s</h1>%s%s
</div></section>''' % (ceja, titulo, '<p class="sub rev">%s</p>' % sub if sub else "", extra)


def frase(ceja, texto, sub="", clase="", sid=""):
    return '<section class="frase %s"%s><div class="caja"><p class="ceja rev">%s</p><p class="grande rev">%s</p>%s</div></section>' % (
        clase, ' id="%s"' % sid if sid else "", ceja, texto, '<p class="sub rev">%s</p>' % sub if sub else "")


def dividir(foto, contenido, invertir=False, clase=""):
    return '<section class="dividir%s %s"><figure class="rev"><img src="%s" alt="" loading="lazy"></figure><div class="texto rev">%s</div></section>' % (
        " inv" if invertir else "", clase, img(foto), contenido)


def lineas(items, numerar=False):
    out = ""
    for i, it in enumerate(items, 1):
        t = it[0]
        d = it[1] if len(it) > 1 else ""
        n = '<span class="n">%s</span>' % ("%02d" % i) if numerar else ""
        out += '<li class="rev">%s<b>%s</b>%s</li>' % (n, t, "<span>%s</span>" % d if d else "")
    return '<ul class="lineas%s">%s</ul>' % (" num" if numerar else "", out)


def faq(items, filtrable=False):
    out = ""
    for cat, p, r, _ in items:
        out += '<details class="preg rev"%s><summary>%s</summary><div class="resp"><p>%s</p></div></details>' % (
            ' data-cat="%s"' % escape(cat) if filtrable else "", p, r)
    return '<div class="preguntas">%s</div>' % out


def seccion(ceja, titulo, contenido, clase="", intro="", sid=""):
    return '<section class="sec %s"%s><div class="sec-in"><header class="sec-cab"><p class="ceja rev">%s</p><h2 class="rev">%s</h2>%s</header><div class="sec-cuerpo">%s</div></div></section>' % (
        clase, ' id="%s"' % sid if sid else "", ceja, titulo, '<p class="sub rev">%s</p>' % intro if intro else "", contenido)


def cierre(titulo="Tu <em>valoración</em>", texto=None, boton=None, fondo="seda-clara", cx=None, nota=""):
    texto = texto or "Todo empieza con una conversación con nuestros especialistas."
    boton = boton or '<a class="boton lleno" href="valoracion.html%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (
        "?cx=" + cx["slug"] if cx else "", wa("Hola, quiero agendar mi valoración%s." % (" para " + cx["nombre"].lower() if cx else "")))
    tono = " sobre-claro" if fondo in CLARO else ""
    return '<section class="cierre%s"><div class="capa" style="background-image:url(%s)"></div>' % (tono, img(fondo)) + viva(fondo) + '<div class="caja"><p class="ceja rev">noon Clinic</p><h2 class="rev">%s</h2><p class="sub rev">%s</p><div class="botones rev">%s</div>%s</div></section>' % (
        titulo, texto, boton, nota)




def pagina(archivo, titulo, descripcion, cuerpo):
    menu_cx = "".join('<a href="cirugia-plastica.html#%s">%s</a>' % (k, n) for k, n, d, f in CATEGORIAS_CX)
    menu_me = "".join('<a href="medicina-estetica.html#%s">%s</a>' % (k, n) for k, n, d, f in CATEGORIAS_ME)
    menu = "".join('<a href="%s">%s</a>' % (h, t) for h, t in MENU)
    html = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#120d0a">
<link rel="icon" href="assets/favicon.png">
<script>document.documentElement.className="js"</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,400&family=Jost:wght@300;400&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/noon.css?v=%(v)s">
</head>
<body>
<header class="cab">
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span class="rayas" aria-hidden="true"></span><span class="txt">Menú</span></button>
  <a class="logo" href="index.html" aria-label="noon Clinic, inicio"><img src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295"></a>
  <div class="cab-der"><button class="buscar-btn" type="button" aria-label="Buscar procedimiento"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg><span class="txt">Buscar</span></button><a class="agendar" href="valoracion.html">Agendar</a></div>
</header>
<div class="buscador-capa" hidden role="dialog" aria-modal="true" aria-label="Buscar procedimiento">
  <div class="bc-in">
    <div class="bc-cab"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>
      <input class="bc-input" type="search" placeholder="¿Qué te gustaría mejorar? Ej: nariz, manchas, papada…" autocomplete="off" aria-label="Buscar">
      <button class="bc-cerrar" type="button" aria-label="Cerrar">Cerrar</button></div>
    <div class="bc-sug"><span>Lo más buscado</span><button type="button">Rinoplastia</button><button type="button">Lipo</button><button type="button">Senos</button><button type="button">Botox</button><button type="button">Manchas</button><button type="button">Abdomen</button></div>
    <ul class="bc-res" role="listbox"></ul>
    <p class="bc-vacio" hidden>No encontramos eso. <a href="#" class="bc-wa" target="_blank" rel="noopener">Pregúntanos por WhatsApp</a></p>
  </div>
</div>
<div class="menu" id="menu" hidden>
  <div class="menu-in tres">
    <div class="menu-col"><p class="ceja"><a href="cirugia-plastica.html">Cirugía plástica</a></p><nav class="grande">%(menu_cx)s</nav></div>
    <div class="menu-col"><p class="ceja"><a href="medicina-estetica.html">Medicina estética</a></p><nav class="grande">%(menu_me)s</nav></div>
    <div class="menu-col"><p class="ceja">noon Clinic</p><nav>%(menu)s</nav>
      <a class="boton" href="valoracion.html">Agendar valoración</a></div>
  </div>
</div>
<div class="progreso-scroll" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><span></span></div>
<div class="vista-previa" aria-hidden="true"></div>
<main>
%(cuerpo)s
</main>
<footer class="pie">
  <div class="pie-in">
    <a class="logo" href="index.html"><img src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295" loading="lazy"></a>
    <p class="lema">Cirugía plástica y medicina estética, con criterio.</p>
    <div class="pie-cols cuatro">
      <div><p class="ceja">Cirugía plástica</p>%(menu_cx)s<a href="cirugia-plastica.html">Todas las cirugías</a></div>
      <div><p class="ceja">Medicina estética</p>%(menu_me)s<a href="medicina-estetica.html">Todos los tratamientos</a></div>
      <div><p class="ceja">La clínica</p><a href="especialistas.html">Especialistas</a><a href="seguridad.html">Seguridad</a><a href="tu-proceso.html">Tu proceso</a><a href="formas-de-pago.html">Pagos</a><a href="otra-ciudad.html">Si vienes de lejos</a><a href="preguntas-frecuentes.html">Preguntas</a></div>
      <div><p class="ceja">Contacto</p><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp %(tel)s</a><a href="valoracion.html">Agendar valoración</a></div>
    </div>
    <a class="boton champan" href="terminos-y-condiciones.html">Términos y condiciones</a>
    <p class="legal">La información de este sitio es orientativa y no reemplaza una consulta médica. Todo procedimiento tiene riesgos y los resultados varían de una persona a otra. © noon Clinic</p>
  </div>
</footer>
<a class="wa-flota" href="%(wa)s" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3Z"/><path d="M8.8 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .6.5l.7 1.7c.1.2.1.4 0 .6l-.4.6c-.1.2-.1.4 0 .5.6 1 1.4 1.8 2.4 2.4.2.1.4.1.5 0l.6-.5c.2-.2.4-.2.6-.1l1.7.8c.3.1.4.3.4.5v.5c0 .4-.3 1-.9 1.2-.6.3-1.8.3-3.7-.8a9.6 9.6 0 0 1-3.4-3.5c-.9-1.6-.7-2.6-.4-3.1Z"/></svg><span>WhatsApp</span></a>
<script src="assets/catalogo.js?v=%(v)s" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="assets/noon.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"titulo": escape(titulo + (" · noon Clinic" if archivo != "index.html" else "")), "desc": escape(descripcion), "cuerpo": cuerpo,
       "menu_cx": menu_cx, "menu_me": menu_me, "menu": menu, "v": V, "wa": wa(), "tel": TELEFONO}
    html = re.sub(r'href="index\.html([?#][^"]*)?"', lambda m: 'href="./%s"' % (m.group(1) or ""), html)
    html = re.sub(r'href="([a-z0-9-]+)\.html([?#][^"]*)?"', lambda m: 'href="%s%s"' % (m.group(1), m.group(2) or ""), html)
    with open(os.path.join(AQUI, archivo), "w", encoding="utf-8") as f:
        f.write(html)
    HECHAS.append(archivo)


HECHAS = []

# ---------------------------------------------------------------- datos para el buscador, el explorador y el asistente
ASISTENTE = [
    ("rostro", "Rostro", [
        ("Mirada cansada o párpados caídos", ["blefaroplastia", "toxina-botulinica"]),
        ("Cambiar mi nariz", ["rinoplastia", "acido-hialuronico"]),
        ("Flacidez en cara o cuello", ["lifting-facial", "hifu", "hilos-tensores"]),
        ("Definir papada y mandíbula", ["lipopapada", "mentoplastia", "acido-hialuronico"]),
        ("Mejillas más definidas", ["bichectomia", "acido-hialuronico"]),
        ("Arrugas de expresión", ["toxina-botulinica", "skinboosters"]),
        ("Labios u ojeras", ["acido-hialuronico"]),
        ("Orejas", ["otoplastia"]),
    ]),
    ("senos", "Senos", [
        ("Más volumen", ["mamoplastia-de-aumento"]),
        ("Levantarlos", ["mastopexia"]),
        ("Reducirlos", ["mamoplastia-de-reduccion"]),
        ("Cambiar o retirar mis implantes", ["recambio-de-implantes"]),
        ("Pecho masculino", ["ginecomastia"]),
    ]),
    ("cuerpo", "Cuerpo", [
        ("Grasa localizada", ["liposuccion", "tratamientos-corporales"]),
        ("Más glúteos", ["lipotransferencia-glutea"]),
        ("Abdomen con piel sobrante", ["abdominoplastia", "mini-abdominoplastia"]),
        ("Recuperar mi cuerpo tras embarazos", ["mommy-makeover", "abdominoplastia"]),
        ("Brazos o muslos flácidos", ["braquioplastia", "lifting-de-muslos", "radiofrecuencia"]),
        ("Bajé mucho de peso", ["cirugia-post-bariatrica"]),
        ("Quiero bajar de peso", ["manejo-medico-del-peso", "nutricion"]),
        ("Celulitis", ["tratamientos-corporales", "radiofrecuencia"]),
    ]),
    ("piel", "Piel", [
        ("Manchas o melasma", ["manchas-y-melasma", "laser", "peelings"]),
        ("Poros, acné o cicatrices", ["microagujas", "peelings", "plasma-rico-en-plaquetas"]),
        ("Piel apagada o deshidratada", ["skinboosters", "limpieza-facial-medica"]),
        ("Firmeza sin cirugía", ["bioestimuladores", "hifu", "radiofrecuencia"]),
        ("Vello no deseado", ["depilacion-laser"]),
        ("Energía y bienestar", ["sueroterapia", "nutricion"]),
    ]),
]
ZONAS = [  # explorador del inicio: (clave, nombre, slugs)
    ("rostro", "Rostro", [c["slug"] for c in CIRUGIAS_NOON if c["cat"] == "rostro"]),
    ("senos", "Senos", [c["slug"] for c in CIRUGIAS_NOON if c["cat"] == "senos"]),
    ("cuerpo", "Cuerpo", [c["slug"] for c in CIRUGIAS_NOON if c["cat"] in ("cuerpo", "combinadas")]),
    ("inyectables", "Inyectables", [t["slug"] for t in TRATAMIENTOS if t["cat"] == "inyectables"]),
    ("piel", "Piel y tecnologías", [t["slug"] for t in TRATAMIENTOS if t["cat"] in ("piel", "tecnologias")]),
    ("bienestar", "Bienestar", [t["slug"] for t in TRATAMIENTOS if t["cat"] == "bienestar"]),
]
PALABRAS = {  # sinónimos para que el buscador entienda cómo habla la gente
    "blefaroplastia": "ojos parpados bolsas mirada", "rinoplastia": "nariz rino respirar tabique septoplastia",
    "lifting-facial": "cara flacidez cuello rejuvenecer arrugas", "bichectomia": "cachetes mejillas cara redonda",
    "mentoplastia": "menton barbilla perfil", "otoplastia": "orejas", "lipopapada": "papada cuello doble menton",
    "mamoplastia-de-aumento": "senos implantes busto pechos tetas aumento", "mastopexia": "senos caidos levantar pexia busto",
    "mamoplastia-de-reduccion": "senos grandes reducir espalda", "recambio-de-implantes": "implantes cambio retirar explante capsula",
    "ginecomastia": "hombre pecho masculino", "liposuccion": "lipo grasa abdomen cintura espalda lipoescultura",
    "lipotransferencia-glutea": "gluteos cola bbl trasero pompis", "abdominoplastia": "abdomen barriga piel diastasis panza",
    "mini-abdominoplastia": "abdomen bajo barriga", "braquioplastia": "brazos alas", "lifting-de-muslos": "piernas muslos",
    "cirugia-post-bariatrica": "bariatrica manga baje de peso piel sobrante body lift", "mommy-makeover": "embarazo mama postparto",
    "labioplastia": "intima vaginal ninfoplastia", "toxina-botulinica": "botox arrugas frente entrecejo bruxismo sudor",
    "acido-hialuronico": "rellenos labios ojeras surcos mandibula rinomodelacion", "bioestimuladores": "colageno radiesse sculptra firmeza",
    "hilos-tensores": "hilos lifting sin cirugia", "skinboosters": "hidratacion brillo piel", "plasma-rico-en-plaquetas": "prp plasma cabello caida",
    "peelings": "peeling manchas acne", "microagujas": "dermapen cicatrices poros", "limpieza-facial-medica": "limpieza facial",
    "manchas-y-melasma": "manchas melasma paño", "laser": "laser rejuvenecimiento", "depilacion-laser": "depilacion vellos pelos",
    "hifu": "ultrasonido tensar", "radiofrecuencia": "firmeza flacidez", "tratamientos-corporales": "celulitis moldear cuerpo",
    "sueroterapia": "sueros vitaminas", "manejo-medico-del-peso": "bajar de peso mounjaro semaglutida obesidad", "nutricion": "nutricionista dieta",
}


SEDAS = ["seda-clara", "seda-burdeos", "seda-cafe", "seda-champan", "seda-noche", "seda-horizonte"]
FONDO_ITEM = {sl: SEDAS[i % len(SEDAS)] for i, sl in enumerate([c["slug"] for c in CIRUGIAS_NOON] + [t["slug"] for t in TRATAMIENTOS])}


def datos_js():
    items = []
    for c in CIRUGIAS_NOON:
        items.append({"s": c["slug"], "n": c["nombre"], "c": c["corto"], "t": "Cirugía plástica", "k": CAT_CX[c["cat"]][0], "f": FONDO_ITEM[c["slug"]],
                      "d": c["datos"][0], "r": c["datos"][2], "p": PALABRAS.get(c["slug"], "")})
    for t in TRATAMIENTOS:
        items.append({"s": t["slug"], "n": t["nombre"], "c": t["corto"], "t": "Medicina estética", "k": CAT_ME[t["cat"]][0], "f": FONDO_ITEM[t["slug"]],
                      "d": t["datos"][0], "r": t["datos"][2], "p": PALABRAS.get(t["slug"], "")})
    data = {"items": items, "asistente": [{"k": k, "n": n, "o": [{"n": o, "s": ss} for o, ss in ops]} for k, n, ops in ASISTENTE],
            "wa": WHATSAPP}
    with open(os.path.join(AQUI, "assets", "catalogo.js"), "w", encoding="utf-8") as fh:
        fh.write("window.NOON=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")


datos_js()
MENU = [
    ("especialistas.html", "Especialistas"),
    ("seguridad.html", "Seguridad"),
    ("tu-proceso.html", "Tu proceso"),
    ("formas-de-pago.html", "Pagos"),
    ("otra-ciudad.html", "Si vienes de lejos"),
    ("preguntas-frecuentes.html", "Preguntas"),
]


# ---------------------------------------------------------------- piezas nuevas
def nota_tc(texto=None):
    texto = texto or "La valoración no se abona al procedimiento ni se devuelve. Si abonas para separar tu cirugía y luego decides no operarte, se devuelve lo abonado con una retención del %s por gastos administrativos." % RETENCION
    return '<div class="nota-tc rev"><p>%s</p><a href="terminos-y-condiciones.html">Leer términos y condiciones</a></div>' % texto


def tarjetas(items):
    """items: (href, ceja, nombre, sub, fondo)"""
    out = ""
    for href, ceja, nombre, sub, f in items:
        out += '''<a class="tile rev%s" href="%s"><span class="tile-img" style="background-image:url(%s)"></span>
  <span class="tile-txt"><span class="ceja">%s</span><span class="nom">%s</span><span class="desde">%s</span><span class="ir">Descubrir</span></span></a>''' % (
            " sobre-claro" if f in CLARO else "", href, img(f), ceja, nombre, sub)
    return '<div class="tiles">%s</div>' % out


def catalogo(lista, tipo):
    """Lista de procedimientos como filas-enlace."""
    out = ""
    for p in lista:
        d = p["datos"]
        meta = ("%s · Recuperación %s" % (d[0], d[2].lower())) if tipo == "cx" else ("%s · %s" % (d[0], d[1]))
        out += '<li class="rev" data-q="%s"><a href="%s.html" data-img="%s"><b>%s</b><span class="c">%s</span><span class="m">%s</span><span class="fl" aria-hidden="true">→</span></a></li>' % (escape((p["nombre"] + " " + p["corto"] + " " + PALABRAS.get(p["slug"], "")).lower()), p["slug"], img(FONDO_ITEM.get(p["slug"], "seda-oscura")), p["nombre"], p["corto"], meta)
    return '<ul class="catalogo">%s</ul>' % out


def foto_esp(e, clase=""):
    ruta = os.path.join(AQUI, "assets", "equipo", e["foto"])
    if e["foto"] and os.path.exists(ruta):
        return '<img class="%s" src="assets/equipo/%s" alt="%s, %s de noon Clinic" loading="lazy">' % (clase, e["foto"], e["nombre"], e["rol"].lower())
    ini = "".join(x[0] for x in e["nombre"].replace("Dr. ", "").replace("Dra. ", "").split()[:2])
    return '<span class="monograma %s" role="img" aria-label="%s">%s</span>' % (clase, e["nombre"], ini)


def esp_de(area):
    return [e for e in ESPECIALISTAS if e["area"] == area]


def bloque_especialista(area, texto):
    es = esp_de(area)
    if not es:
        return ""
    e = es[0]
    return '''<section class="esp-bloque" id="especialista"><div class="esp-in">
  <figure class="rev">%s</figure>
  <div class="texto rev"><p class="ceja">Tu especialista</p><h2>%s</h2><p class="rol">%s</p><p class="sub">%s</p>
  <a class="enlace" href="especialistas.html#%s">Conocer al especialista</a></div>
</div></section>''' % (foto_esp(e), e["nombre"], e["rol"], texto, e["slug"])


def explorador():
    tabs = "".join('<button class="ex-tab%s" type="button" role="tab" data-z="%s">%s</button>' % (" on" if i == 0 else "", k, n) for i, (k, n, _) in enumerate(ZONAS))
    cards = ""
    for k, n, slugs in ZONAS:
        for sl in slugs:
            it = CX_N.get(sl) or TR_N.get(sl)
            es_cx = sl in CX_N
            f = FONDO_ITEM[sl]
            meta = ("%s · Recuperación %s" % (it["datos"][0], it["datos"][2].lower())) if es_cx else it["datos"][0]
            cards += '''<a class="ex-card%s" data-z="%s" href="%s.html"><span class="ex-img" style="background-image:url(%s)"></span>
  <span class="ex-txt"><span class="ceja">%s</span><b>%s</b><span class="c">%s</span><span class="m">%s</span></span></a>''' % (
                " sobre-claro" if f in CLARO else "", k, sl, img(f), "Cirugía plástica" if es_cx else "Medicina estética", it["nombre"], it["corto"], meta)
    return '''<section class="explora" id="explora">
  <div class="ex-cab"><div><p class="ceja rev">Explora</p><h2 class="rev">¿Qué zona quieres <em>tratar</em>?</h2></div>
    <div class="ex-ctrl"><button class="ex-prev" type="button" aria-label="Anterior">←</button><button class="ex-next" type="button" aria-label="Siguiente">→</button></div></div>
  <div class="ex-tabs rev" role="tablist">%s</div>
  <div class="ex-pista"><div class="ex-track">%s</div></div>
  <div class="ex-pie"><a class="enlace" href="cirugia-plastica.html">Todas las cirugías</a><a class="enlace" href="medicina-estetica.html">Todos los tratamientos</a></div>
</section>''' % (tabs, cards)


def asistente():
    return '''<section class="asistente" id="encuentra"><div class="capa" style="background-image:url(%s)"></div><canvas class="seda-viva" data-p="noche" aria-hidden="true"></canvas>
  <div class="as-in">
    <p class="ceja rev">Encuentra tu procedimiento</p>
    <h2 class="rev">Dos toques<br>y te <em>orientamos</em>.</h2>
    <div class="as-caja rev" data-asistente>
      <ol class="as-prog"><li class="on">Zona</li><li>Objetivo</li><li>Para ti</li></ol>
      <div class="as-paso" data-paso="1"><p class="as-preg">¿Qué te gustaría mejorar?</p><div class="as-ops"></div></div>
      <div class="as-paso" data-paso="2" hidden><p class="as-preg"></p><div class="as-ops"></div><button class="as-atras" type="button">← Volver</button></div>
      <div class="as-paso" data-paso="3" hidden><p class="as-preg">Esto podría ser para ti</p><div class="as-res"></div>
        <p class="as-nota">Es una orientación: la indicación final la da el especialista en tu valoración.</p>
        <div class="botones izq"><a class="boton lleno as-wa" href="#" target="_blank" rel="noopener">Agendar valoración por WhatsApp</a><button class="boton as-reset" type="button">Empezar de nuevo</button></div></div>
    </div>
  </div>
</section>''' % img("seda-noche")


def filtro_hub(cats, ph):
    return '''<div class="filtro-hub"><div class="fh-in">
  <label class="fh-buscar"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg><input type="search" placeholder="%s" aria-label="Buscar"></label>
  <div class="fh-chips"><button type="button" class="on" data-c="">Todas</button>%s</div>
</div><p class="fh-vacio" hidden>No encontramos eso aquí. Prueba con el buscador de arriba o <a href="#" data-abrir-buscador>búscalo en toda la clínica</a>.</p></div>''' % (ph, "".join('<button type="button" data-c="%s">%s</button>' % (k, n) for k, n, d, f in cats))


def linea_tiempo(pasos):
    """Recuperación como línea de tiempo que se recorre tocando cada etapa."""
    marcas = "".join('<button type="button" class="lt-m%s" data-i="%d"><span class="lt-p"></span>%s</button>' % (" on" if i == 0 else "", i, t) for i, (t, _) in enumerate(pasos))
    textos = "".join('<p class="lt-t%s" data-i="%d">%s</p>' % (" on" if i == 0 else "", i, d) for i, (_, d) in enumerate(pasos))
    return '<div class="lt rev" data-lt><div class="lt-barra"><span class="lt-fill"></span></div><div class="lt-marcas">%s</div><div class="lt-textos">%s</div><div class="lt-nav"><button type="button" class="lt-ant" aria-label="Etapa anterior">←</button><button type="button" class="lt-sig" aria-label="Etapa siguiente">→</button></div></div>' % (marcas, textos)


def cinta(nombres, clase=""):
    fila = "".join('<span>%s</span><i aria-hidden="true">·</i>' % n for n in nombres)
    return '<div class="cinta-mov %s" aria-hidden="true"><div class="cm-track"><div class="cm-g">%s</div><div class="cm-g">%s</div></div></div>' % (clase, fila, fila)


def subnav(pares):
    return '<nav class="subnav" aria-label="En esta página">%s</nav>' % "".join('<a href="#%s">%s</a>' % p for p in pares)


def barra_cta(nombre, quien, slug, msj):
    return '''<div class="barra-cta" aria-label="Agendar">
  <div class="bc-t"><b>%s</b><span>%s</span></div>
  <a class="boton bc-w" href="%s" target="_blank" rel="noopener">WhatsApp</a><a class="boton lleno" href="valoracion.html?cx=%s">Agendar<span class="solo-grande"> valoración</span></a>
</div>''' % (nombre, quien, wa(msj), slug)


def datos_barra(pares):
    return '<section class="datos">%s</section>' % "".join('<div><span class="ceja">%s</span><b>%s</b></div>' % p for p in pares)


# ================================================================ INICIO
pagina("index.html", "noon Clinic · Cirugía plástica y medicina estética",
       "Clínica de cirugía plástica y medicina estética. Rostro, senos, contorno corporal, inyectables, piel y tecnologías, con médicos especializados.",
       '''<section class="hero completo portada"><div class="capa" style="background-image:url(%s)"></div><canvas class="seda-viva" data-p="oscura" aria-hidden="true"></canvas><div class="hero-in">
  <img class="logo-hero rev" src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295">
  <p class="ceja rev">Estética con criterio</p>
  <p class="sub rev">Cirugía plástica · Medicina estética</p>
  <button class="hero-buscar rev" type="button" data-abrir-buscador><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg><span>¿Qué te gustaría mejorar?</span></button>
  <div class="hero-acciones rev"><a class="boton lleno" href="#encuentra">Encuentra tu procedimiento</a><a class="boton" href="valoracion.html">Agendar valoración</a></div>
</div><a class="bajar" href="#explora" aria-label="Bajar">Descubrir</a></section>''' % img("seda-oscura")
       + explorador()
       + cinta([c["nombre"] for c in CIRUGIAS_NOON[:12]])
       + frase("Lo que creemos", "Primero <em>entendemos</em>.<br>Después hablamos de posibilidades.",
               "La recomendación nace del criterio clínico y de lo que cada persona quiere preservar.", sid="creemos")
       + asistente()
       + dividir("foto-luz", '''<p class="ceja">Medicina estética</p><h2>Realzar <em>lo tuyo</em>.</h2>
<p class="sub">Tratamientos médicos no quirúrgicos para la piel, el rostro y el cuerpo. Resultados naturales, con criterio clínico.</p>%s<a class="enlace" href="medicina-estetica.html">Ver todos los tratamientos</a>''' % (
           '<ul class="catalogo corto">%s</ul>' % "".join('<li><a href="medicina-estetica.html#%s"><b>%s</b><span class="c">%s</span><span class="fl" aria-hidden="true">→</span></a></li>' % (k, n, d) for k, n, d, f in CATEGORIAS_ME)))
       + seccion("Especialistas", "Médicos especializados.<br>Decisiones <em>personales</em>.", '<div class="esp-duo">%s</div><a class="enlace rev" href="especialistas.html">Conocer a los especialistas</a>' % "".join(
           '<a class="esp-card rev" href="especialistas.html#%s"><span class="esp-foto">%s</span><span class="esp-nom">%s</span><span class="esp-rol">%s</span></a>' % (e["slug"], foto_esp(e), e["nombre"], e["rol"]) for e in ESPECIALISTAS), "sin-borde")
       + '''<section class="foto-frase"><div class="capa" style="background-image:url(%s)"></div><div class="caja"><p class="ceja rev">Seguridad</p><p class="grande rev">Tu tranquilidad es parte <em>del resultado</em>.</p><a class="boton rev" href="seguridad.html">Cómo cuidamos tu procedimiento</a></div></section>''' % img("foto-espera")
       + seccion("Tu proceso", "Tres <em>pasos</em>.", '<ol class="pasos">%s</ol>' % "".join(
           '<li class="rev"><span class="n">%s</span><b>%s</b><span>%s</span></li>' % x for x in [
               ("I", "Valoración", "Te escuchamos, te examinamos y te decimos qué tiene sentido para ti."),
               ("II", "Tu plan por escrito", "Procedimiento, tiempos, cuidados y presupuesto, claros desde el principio."),
               ("III", "Procedimiento y seguimiento", "Con acompañamiento cercano hasta el alta.")]))
       + cierre())


# ================================================================ CIRUGÍA PLÁSTICA (hub)
bloques_cx = ""
for k, n, d, f in CATEGORIAS_CX:
    lista = [c for c in CIRUGIAS_NOON if c["cat"] == k]
    bloques_cx += '<section class="sec cat-bloque" id="%s"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">Cirugía plástica</p><h2 class="rev">%s</h2><p class="sub rev">%s</p></header><div class="sec-cuerpo">%s</div></div></section>' % (k, n, d, catalogo(lista, "cx"))
pagina("cirugia-plastica.html", "Cirugía plástica", "Cirugía plástica en noon Clinic: rostro, senos, contorno corporal y procedimientos combinados.",
       hero("seda-burdeos", "Cirugía plástica", "Cirugía plástica<br><em>con criterio</em>.", "Cada cirugía empieza entendiendo qué quieres lograr y qué quieres preservar.", "alto")
       + filtro_hub(CATEGORIAS_CX, "Busca una cirugía: nariz, abdomen, senos…")
       + cinta([c["nombre"] for c in CIRUGIAS_NOON], "suave")
       + bloques_cx
       + bloque_especialista("cirugia", "Te valora y te opera el mismo especialista, que te acompaña desde la primera consulta hasta el alta.")
       + cierre())

# ================================================================ UNA PÁGINA POR CIRUGÍA
for c in CIRUGIAS_NOON:
    cat_n, cat_d, f = CAT_CX[c["cat"]]
    f = FONDO_ITEM[c["slug"]]
    d = c["datos"]
    otras = [x for x in CIRUGIAS_NOON if x["cat"] == c["cat"] and x["slug"] != c["slug"]]
    msj = "Hola, quiero agendar mi valoración para %s en noon Clinic." % c["nombre"].lower()
    pagina(c["slug"] + ".html", c["nombre"], c["corto"],
           hero(f, "Cirugía plástica · " + cat_n, c["nombre"], c["corto"], "alto")
           + datos_barra([("Duración", d[0]), ("Anestesia", d[1]), ("Incapacidad aprox.", d[2]), ("Resultado final", d[3])])
           + subnav([("que-es", "Qué es"), ("para-ti", "Para ti"), ("recuperacion", "Recuperación"), ("especialista", "Especialista"), ("preguntas", "Preguntas")])
           + frase("El procedimiento", c["que_es"][0], c["que_es"][1] if len(c["que_es"]) > 1 else "", "media", sid="que-es")
           + seccion("Es para ti si", "Lo que buscas", lineas([(x,) for x in c["ideal"]]) + '<p class="pista rev">La indicación final la da tu cirujano en la valoración.</p>', sid="para-ti")
           + seccion("Recuperación", "Paso a paso", linea_tiempo(c["recuperacion"]) + '<p class="pista rev">Tiempos de guía. Tu cirujano te da los exactos.</p>', sid="recuperacion")
           + bloque_especialista("cirugia", "Tu valoración de %s es con el especialista que te opera." % c["nombre"].lower())
           + seccion("Preguntas", "Sobre " + c["nombre"].lower(), faq([("", q, r, []) for q, r in c["faq"]]) + '<a class="enlace rev" href="preguntas-frecuentes.html">Todas las preguntas</a>', "marfil", sid="preguntas")
           + (seccion("También en " + cat_n.lower(), "Otras cirugías", catalogo(otras, "cx")) if otras else "")
           + cierre(c["nombre"], "Todo empieza con tu valoración: te decimos si es para ti y recibes tu plan por escrito.",
                    '<a class="boton lleno" href="valoracion.html?cx=%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (c["slug"], wa(msj)), fondo=f)
           + barra_cta(c["nombre"], "Valoración con " + ESPECIALISTAS[0]["nombre"], c["slug"], msj))

# ================================================================ MEDICINA ESTÉTICA (hub)
bloques_me = ""
for k, n, d, f in CATEGORIAS_ME:
    lista = [t for t in TRATAMIENTOS if t["cat"] == k]
    bloques_me += '<section class="sec cat-bloque" id="%s"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">Medicina estética</p><h2 class="rev">%s</h2><p class="sub rev">%s</p></header><div class="sec-cuerpo">%s</div></div></section>' % (k, n, d, catalogo(lista, "me"))
pagina("medicina-estetica.html", "Medicina estética", "Medicina estética en noon Clinic: toxina botulínica, ácido hialurónico, bioestimuladores, piel, láser, HIFU y bienestar.",
       hero("seda-champan", "Medicina estética", "Realzar lo tuyo,<br><em>sin cambiar quién eres</em>.", "Tratamientos médicos no quirúrgicos con resultados naturales.", "alto")
       + filtro_hub(CATEGORIAS_ME, "Busca un tratamiento: botox, manchas, láser…")
       + cinta([t["nombre"] for t in TRATAMIENTOS], "suave")
       + bloques_me
       + bloque_especialista("estetica", "Cada tratamiento empieza con una valoración para definir qué necesita tu piel y qué no.")
       + cierre(fondo="seda-champan"))

# ================================================================ UNA PÁGINA POR TRATAMIENTO
for t in TRATAMIENTOS:
    cat_n, cat_d, f = CAT_ME[t["cat"]]
    f = FONDO_ITEM[t["slug"]]
    d = t["datos"]
    otras = [x for x in TRATAMIENTOS if x["cat"] == t["cat"] and x["slug"] != t["slug"]]
    msj = "Hola, quiero agendar una valoración para %s en noon Clinic." % t["nombre"].lower()
    pagina(t["slug"] + ".html", t["nombre"], t["corto"],
           hero(f, "Medicina estética · " + cat_n, t["nombre"], t["corto"], "medio")
           + datos_barra([("Sesiones", d[0]), ("Duración", d[1]), ("Recuperación", d[2]), ("Resultado", d[3])])
           + subnav([("que-es", "Qué es"), ("para-ti", "Indicado para"), ("especialista", "Especialista"), ("preguntas", "Preguntas")])
           + frase("El tratamiento", t["que_es"][0], t["que_es"][1] if len(t["que_es"]) > 1 else "", "media", sid="que-es")
           + seccion("Indicado para", "Lo que buscas", lineas([(x,) for x in t["ideal"]]) + '<p class="pista rev">La indicación final la da tu médica en la valoración.</p>', sid="para-ti")
           + bloque_especialista("estetica", "Tu valoración y tu tratamiento de %s los realiza la médica estética de noon." % t["nombre"].lower())
           + seccion("Preguntas", "Sobre " + t["nombre"].lower(), faq([("", q, r, []) for q, r in t["faq"]]), "marfil", sid="preguntas")
           + (seccion("También en " + cat_n.lower(), "Otros tratamientos", catalogo(otras, "me")) if otras else "")
           + cierre(t["nombre"], "Agenda tu valoración y armamos contigo el plan que tu piel necesita.",
                    '<a class="boton lleno" href="valoracion.html?cx=%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (t["slug"], wa(msj)), fondo=f)
           + barra_cta(t["nombre"], "Valoración con " + ESPECIALISTAS[1]["nombre"], t["slug"], msj))

# ================================================================ ESPECIALISTAS
fichas = ""
for i, e in enumerate(ESPECIALISTAS):
    area = ("cirugia-plastica.html", "Ver cirugías") if e["area"] == "cirugia" else ("medicina-estetica.html", "Ver tratamientos")
    fichas += '''<section class="esp-ficha%s" id="%s"><figure class="rev">%s</figure><div class="texto rev">
  <p class="ceja">%s</p><h2>%s</h2><p class="sub">%s</p>%s
  <div class="botones izq"><a class="boton lleno" href="%s" target="_blank" rel="noopener">Agendar con %s</a><a class="boton" href="%s">%s</a></div>
</div></section>''' % (" inv" if i % 2 else "", e["slug"], foto_esp(e), e["rol"], e["nombre"], e["bio"], lineas([(x,) for x in e["detalle"]]) if e["detalle"] else "",
                       wa("Hola, quiero agendar una valoración con %s en noon Clinic." % e["nombre"]), e["nombre"].split()[0] + " " + e["nombre"].split()[-1], area[0], area[1])
pagina("especialistas.html", "Especialistas", "Conoce a los especialistas de noon Clinic: Dr. Fernando Ruiz, cirujano plástico, y Dra. Valeria Enciso, médica estética.",
       hero("seda-noche", "Especialistas", "Médicos especializados.<br>Decisiones <em>personales</em>.", "Te escuchamos antes de proponer, te explicamos sin dramatizar y decidimos contigo.")
       + fichas
       + seccion("Cómo trabajamos", "Nuestros principios", lineas([("Escuchar antes de proponer",), ("Explicar sin dramatizar",), ("Decidir junto a la persona",), ("Cuidar también el seguimiento",)], numerar=True))
       + cierre())

# ================================================================ SEGURIDAD
ALERTAS = [
    ("Presupuesto sin detalle", "Si no te dicen por escrito qué incluye, lo que falta aparece después."),
    ("Fuera de un quirófano", "Una cirugía se hace en salas de cirugía. Un consultorio no lo es."),
    ("Sin exámenes", "Si nadie te pide exámenes, nadie está revisando si es seguro operarte."),
    ("Sin consentimiento informado", "Tienes derecho a conocer los riesgos antes de decidir."),
    ("Todo es “sí”", "Un buen especialista también te dice qué no se puede o no se debe hacer."),
    ("Afán para pagar", "Una decisión así se toma con calma y con toda la información."),
]
pagina("seguridad.html", "Seguridad", "Cirugías en quirófano habilitado, valoración presencial, exámenes previos, consentimiento informado y seguimiento hasta el alta.",
       hero("foto-pasillo", "Seguridad", "Tu tranquilidad<br>es parte del resultado.")
       + seccion("No negociables", "Cómo cuidamos tu procedimiento", lineas([
           ("Cirugías solo en quirófano", "En salas de cirugía habilitadas (%s). Nunca en consultorios." % SEDE_QX),
           ("Valoración presencial primero", "Nadie se opera ni se trata sin una valoración médica honesta."),
           ("Exámenes antes de operar", "Si tus exámenes no están en regla, la cirugía se aplaza. Sin excepciones."),
           ("Consentimiento informado", "Te explicamos los riesgos uno a uno antes de que decidas."),
           ("Plan por escrito", "Procedimiento, cuidados y presupuesto claros desde el principio."),
           ("Controles hasta el alta", "Te acompañamos hasta que todo esté bien."),
           ("Sabemos decir que no", "Si un procedimiento no es seguro o no tiene sentido para ti, te lo decimos."),
       ], numerar=True))
       + frase("Al elegir dónde tratarte", "Señales de alerta.", "Aplican para cualquier lugar, incluido el nuestro. Pregunta siempre.")
       + seccion("Presta atención a", "Seis señales", lineas(ALERTAS, numerar=True))
       + seccion("Preguntas", "Sobre seguridad", faq([(c, p, r, []) for c, p, r in FAQ_NOON if c == "Seguridad"]), "marfil")
       + cierre())

# ================================================================ TU PROCESO
PROCESO_N = [
    ("Valoración", "Con el especialista del área. Te examina, te escucha y te dice qué tiene sentido para ti."),
    ("Plan por escrito", "Procedimiento, tiempos, cuidados y presupuesto."),
    ("Exámenes (si es cirugía)", "Confirman que es seguro operarte."),
    ("Separas tu fecha", "Con un abono reservas tu cirugía en %s." % SEDE_QX),
    ("Preparación", "Te decimos qué suspender, el ayuno y qué llevar."),
    ("Procedimiento", "Con un equipo completo y todo explicado."),
    ("Seguimiento", "Controles hasta el alta y línea directa para tus dudas."),
]
pagina("tu-proceso.html", "Tu proceso", "De la valoración al resultado: así es el camino de tu procedimiento en noon Clinic.",
       hero("seda-oscura", "Tu proceso", "De la primera conversación<br>al resultado.", "Saber qué viene quita la mitad de los nervios.")
       + seccion("El camino", "Paso a paso", '<ol class="tiempo num">%s</ol>' % "".join('<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in PROCESO_N))
       + dividir("foto-recepcion", '<p class="ceja">El día de tu cirugía</p><h2>Qué llevar</h2>%s' % lineas([(x,) for x in QUE_LLEVAR]))
       + seccion("Preguntas", "Sobre la recuperación", faq([(c, p, r, []) for c, p, r in FAQ_NOON if c == "Recuperación"]), "marfil")
       + cierre())

# ================================================================ PAGOS
pagina("formas-de-pago.html", "Formas de pago", "Cómo se paga tu procedimiento en noon Clinic: valoración, abono para separar fecha y saldo.",
       hero("seda-cafe", "Pagos", "Cuentas claras<br>desde el primer día.")
       + seccion("Cómo se paga", "Tres momentos", '<ol class="pasos">%s</ol>' % "".join('<li class="rev"><span class="n">%s</span><b>%s</b><span>%s</span></li>' % x for x in [
           ("I", "Valoración", "Es el primer paso. No se abona al procedimiento y su valor no se devuelve."),
           ("II", "Abono para tu fecha", "Reservas tu fecha de cirugía. Si desistes, se devuelve con una retención del %s por gastos administrativos." % RETENCION),
           ("III", "Saldo", "Se paga antes del procedimiento, según tu plan por escrito.")]) + nota_tc())
       + seccion("Preguntas", "Sobre pagos", faq([(c, p, r, []) for c, p, r in FAQ_NOON if c in ("Pagos",) or p.startswith("¿Cuánto cuesta")]), "marfil")
       + cierre("Medios de pago", "Escríbenos y te contamos los medios de pago disponibles.",
                '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Preguntar por WhatsApp</a>' % wa("Hola, quiero conocer los medios de pago de noon Clinic.")))

# ================================================================ OTRA CIUDAD
pagina("otra-ciudad.html", "Si vienes de lejos", "Cómo tratarte en noon Clinic si vives en otra ciudad o en el exterior: fechas, estadía, controles y regreso.",
       hero("seda-horizonte", "Pacientes que viajan", "Vienes de lejos.<br>Te lo ponemos fácil.", "Organizamos tus fechas para que valoración, procedimiento y controles te queden en un solo viaje.")
       + seccion("Tu viaje", "Cómo se organiza", '<ol class="tiempo num">%s</ol>' % "".join('<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in [
           ("Escríbenos antes de viajar", "Cuéntanos qué te interesa y dejamos agendada tu valoración para cuando llegues."),
           ("Valoración y exámenes", "El especialista te valora en persona y, si es cirugía, te ordena los exámenes."),
           ("Procedimiento", "Cirugía en %s o tratamiento en la clínica." % SEDE_QX),
           ("Recuperación y controles", "Te quedas en la ciudad los días que tu especialista indique."),
           ("Regreso a casa", "Viajas cuando tu especialista lo autorice.")]))
       + dividir("foto-espera", '<p class="ceja">Guía de estadía</p><h2>¿Cuántos días me quedo?</h2>%s<p class="pista">Tiempos de referencia. El regreso lo autoriza tu especialista.</p>' % lineas([
           ("Cirugía de rostro", "Entre 1 y 2 semanas."), ("Cirugía de senos", "Entre 1 y 2 semanas."), ("Contorno corporal y combinadas", "Entre 2 y 3 semanas."), ("Medicina estética", "Por lo general, el mismo día o pocos días.")]))
       + seccion("Recomendaciones", "Para tu viaje", lineas([("Viaja acompañada", "Si es cirugía, necesitas un adulto contigo los primeros días."),
                                                               ("Hospédate cerca", "Entre más cerca de la clínica y de tus controles, más cómoda tu recuperación."),
                                                               ("Tiquetes flexibles", "La fecha de regreso depende de tu evolución, no del calendario."),
                                                               ("Trae tus exámenes", "Si tienes exámenes recientes, tráelos a la valoración.")]))
       + seccion("Preguntas", "De quienes viajan", faq([(c, p, r, []) for c, p, r in FAQ_NOON if c == "Vengo de lejos"]), "marfil")
       + cierre("Organicemos tu viaje", "Escríbenos y armamos tus fechas contigo.",
                '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % wa("Hola, vivo en otra ciudad y quiero información para tratarme en noon Clinic.")))

# ================================================================ PREGUNTAS
filtros = '<button class="filtro on" data-cat="todas" type="button">Todas</button>' + "".join('<button class="filtro" data-cat="%s" type="button">%s</button>' % (escape(x), x) for x in CATS_NOON)
pagina("preguntas-frecuentes.html", "Preguntas frecuentes", "Respuestas sobre valoración, seguridad, recuperación, requisitos, medicina estética y pagos en noon Clinic.",
       hero("seda-clara", "Preguntas frecuentes", "Todas tus dudas,<br><em>con calma</em>.", "%d respuestas. Busca por palabra o filtra por tema." % len(FAQ_NOON))
       + '''<section class="sec marfil"><div class="sec-in solo">
  <input class="buscador" type="search" placeholder="Busca: dolor, valoración, abono…" aria-label="Buscar en las preguntas">
  <div class="filtros">%s</div>%s<p class="vacio" hidden>No encontramos esa pregunta. Escríbenos por WhatsApp y te respondemos.</p>
</div></section>''' % (filtros, faq([(c, p, r, []) for c, p, r in FAQ_NOON], filtrable=True))
       + cierre("¿No encontraste tu pregunta?", "Escríbenos y te respondemos.",
                '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % wa("Hola, tengo una pregunta para noon Clinic."), fondo="seda-oscura"))

# ================================================================ VALORACIÓN
opciones = ('<optgroup label="Cirugía plástica">%s</optgroup>' % "".join('<option data-slug="%s">%s</option>' % (c["slug"], c["nombre"]) for c in CIRUGIAS_NOON)
            + '<optgroup label="Medicina estética">%s</optgroup>' % "".join('<option data-slug="%s">%s</option>' % (t["slug"], t["nombre"]) for t in TRATAMIENTOS))
pagina("valoracion.html", "Agenda tu valoración", "Todo empieza con tu valoración con nuestros especialistas. Agéndala por WhatsApp.",
       hero("seda-oscura", "Primer paso", "Tu <em>valoración</em>.", "Una conversación clínica empieza por entender qué quieres preservar.")
       + '''<section class="valoracion">
  <div class="texto rev"><p class="ceja">Qué pasa en tu valoración</p><h2 class="h-val">Una conversación, no una venta.</h2>%(lista)s%(tc)s</div>
  <form class="form rev" id="form-valoracion" data-wa="%(wa)s">
    <p class="ceja">Agenda por WhatsApp</p><h2>Empieza aquí</h2>
    <p class="sub">Tres datos y se abre WhatsApp con tu mensaje listo.</p>
    <label>Tu nombre<input id="nombre" name="nombre" required autocomplete="given-name"></label>
    <label>¿Qué te interesa?<select id="cirugia" name="cirugia">%(op)s<option>Aún no estoy segura</option></select></label>
    <label>Ciudad donde vives<input id="ciudad" name="ciudad" required autocomplete="address-level2"></label>
    <button class="boton lleno" type="submit">Continuar en WhatsApp</button>
    <p class="legal">Al escribirnos aceptas nuestros <a href="terminos-y-condiciones.html">términos y condiciones</a>. Este formulario no guarda tus datos.</p>
  </form>
</section>''' % {"wa": WHATSAPP, "op": opciones,
                 "tc": nota_tc("La valoración no se abona al procedimiento y su valor no se devuelve."),
                 "lista": lineas([("Te escuchamos", "Qué quieres lograr y qué quieres preservar."), ("Te examinamos", "Con el especialista del área."), ("Respuestas honestas", "Qué se puede lograr, qué no, y si eres candidata."), ("Tu plan por escrito", "Procedimiento, tiempos, cuidados y presupuesto.")])})

# ================================================================ PÁGINAS VIEJAS → redirección a las nuevas
for viejo, nuevo in [("cirugias", "cirugia-plastica"), ("todo-incluido", "cirugia-plastica"), ("mastopexia-con-implantes", "mastopexia"),
                     ("mastopexia-sin-implantes", "mastopexia"), ("lipo", "liposuccion"), ("nosotros", "especialistas")]:
    with open(os.path.join(AQUI, viejo + ".html"), "w", encoding="utf-8") as fh:
        fh.write('<!doctype html><html lang="es"><head><meta charset="utf-8"><title>noon Clinic</title><link rel="canonical" href="/%s"><meta http-equiv="refresh" content="0; url=/%s"><meta name="robots" content="noindex"></head><body><a href="/%s">Continuar</a></body></html>' % (nuevo, nuevo, nuevo))


# ================================================================ TÉRMINOS
def _contenido(ps):
    return "".join("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in p) if isinstance(p, list) else "<p>%s</p>" % p for p in ps)

bloques = "".join('<section id="t%d" class="termino%s"><h3>%s</h3>%s</section>' % (i + 1, " clave" if clave else "", t, _contenido(ps)) for i, (t, ps, clave) in enumerate(TERMINOS))
indice = "".join('<a href="#t%d"%s>%s</a>' % (i + 1, ' class="clave"' if clave else "", t) for i, (t, ps, clave) in enumerate(TERMINOS))
pagina("terminos-y-condiciones.html", "Términos y condiciones", "Condiciones de la cita de valoración, abonos, política de devoluciones y reprogramación.",
       hero("seda-horizonte", "Legal", "Términos y condiciones.", "Léelos completos antes de agendar o pagar. Están escritos para que se entiendan.")
       + '''<section class="sec marfil"><div class="sec-in solo terminos">
  <div class="resumen-tc"><p class="ceja">Lo más importante</p><ul>%s</ul><a class="boton champan" href="#t4">Política de devoluciones</a></div>
  <nav class="indice" aria-label="Contenido">%s</nav>%s
</div></section>''' % ("".join("<li>%s</li>" % x for x in RESUMEN_TC), indice, bloques))

print("Listo. %d páginas · %d cirugías · %d tratamientos · %d preguntas." % (len(HECHAS), len(CIRUGIAS_NOON), len(TRATAMIENTOS), len(FAQ_NOON)))
