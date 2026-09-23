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
def hero(fondo, ceja, titulo, sub="", alto="medio", extra=""):
    tono = " sobre-claro" if fondo in CLARO else ""
    return '''<section class="hero %s%s"><div class="capa" style="background-image:url(%s)"></div><div class="hero-in">
  <p class="ceja rev">%s</p><h1 class="rev">%s</h1>%s%s
</div></section>''' % (alto, tono, img(fondo), ceja, titulo, '<p class="sub rev">%s</p>' % sub if sub else "", extra)


def frase(ceja, texto, sub="", clase=""):
    return '<section class="frase %s"><div class="caja"><p class="ceja rev">%s</p><p class="grande rev">%s</p>%s</div></section>' % (
        clase, ceja, texto, '<p class="sub rev">%s</p>' % sub if sub else "")


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


def seccion(ceja, titulo, contenido, clase="", intro=""):
    return '<section class="sec %s"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">%s</p><h2 class="rev">%s</h2>%s</header><div class="sec-cuerpo">%s</div></div></section>' % (
        clase, ceja, titulo, '<p class="sub rev">%s</p>' % intro if intro else "", contenido)


def cierre(titulo="Tu valoración", texto=None, boton=None, fondo="seda-clara", cx=None, nota=""):
    texto = texto or "Todo empieza con una conversación con nuestros especialistas."
    boton = boton or '<a class="boton lleno" href="valoracion.html%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (
        "?cx=" + cx["slug"] if cx else "", wa("Hola, quiero agendar mi valoración%s." % (" para " + cx["nombre"].lower() if cx else "")))
    tono = " sobre-claro" if fondo in CLARO else ""
    return '<section class="cierre%s"><div class="capa" style="background-image:url(%s)"></div><div class="caja"><p class="ceja rev">noon Clinic</p><h2 class="rev">%s</h2><p class="sub rev">%s</p><div class="botones rev">%s</div>%s</div></section>' % (
        tono, img(fondo), titulo, texto, boton, nota)




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
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/noon.css?v=%(v)s">
</head>
<body>
<header class="cab">
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span class="rayas" aria-hidden="true"></span><span class="txt">Menú</span></button>
  <a class="logo" href="index.html" aria-label="noon Clinic, inicio"><img src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295"></a>
  <a class="agendar" href="valoracion.html">Agendar</a>
</header>
<div class="menu" id="menu" hidden>
  <div class="menu-in tres">
    <div class="menu-col"><p class="ceja"><a href="cirugia-plastica.html">Cirugía plástica</a></p><nav class="grande">%(menu_cx)s</nav></div>
    <div class="menu-col"><p class="ceja"><a href="medicina-estetica.html">Medicina estética</a></p><nav class="grande">%(menu_me)s</nav></div>
    <div class="menu-col"><p class="ceja">noon Clinic</p><nav>%(menu)s</nav>
      <a class="boton" href="valoracion.html">Agendar valoración</a></div>
  </div>
</div>
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
        out += '<li class="rev"><a href="%s.html"><b>%s</b><span class="c">%s</span><span class="m">%s</span><span class="fl" aria-hidden="true">→</span></a></li>' % (p["slug"], p["nombre"], p["corto"], meta)
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
    return '''<section class="esp-bloque"><div class="esp-in">
  <figure class="rev">%s</figure>
  <div class="texto rev"><p class="ceja">Tu especialista</p><h2>%s</h2><p class="rol">%s</p><p class="sub">%s</p>
  <a class="enlace" href="especialistas.html#%s">Conocer al especialista</a></div>
</div></section>''' % (foto_esp(e), e["nombre"], e["rol"], texto, e["slug"])


def datos_barra(pares):
    return '<section class="datos">%s</section>' % "".join('<div><span class="ceja">%s</span><b>%s</b></div>' % p for p in pares)


# ================================================================ INICIO
pagina("index.html", "noon Clinic · Cirugía plástica y medicina estética",
       "Clínica de cirugía plástica y medicina estética. Rostro, senos, contorno corporal, inyectables, piel y tecnologías, con médicos especializados.",
       '''<section class="hero completo portada"><div class="capa" style="background-image:url(%s)"></div><canvas class="seda-viva" aria-hidden="true"></canvas><div class="hero-in">
  <img class="logo-hero rev" src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295">
  <p class="ceja rev">Estética con criterio</p>
  <p class="sub rev">Cirugía plástica · Medicina estética</p>
</div><a class="bajar" href="#creemos" aria-label="Bajar">Descubrir</a></section>''' % img("seda-oscura")
       + frase("Lo que creemos", "Primero entendemos.<br>Después hablamos de posibilidades.",
               "La recomendación nace del criterio clínico y de lo que cada persona quiere preservar.").replace('class="frase "', 'class="frase" id="creemos"')
       + seccion("Cirugía plástica", "Cirugía plástica.", tarjetas([("cirugia-plastica.html#%s" % k, "Cirugía plástica", n, d, f) for k, n, d, f in CATEGORIAS_CX])
                 + '<a class="enlace rev" href="cirugia-plastica.html">Ver todas las cirugías</a>', "sin-borde",
                 intro="Rostro, senos y contorno corporal, con un plan pensado para ti y acompañamiento hasta el alta.")
       + dividir("foto-luz", '''<p class="ceja">Medicina estética</p><h2>Realzar lo tuyo.</h2>
<p class="sub">Tratamientos médicos no quirúrgicos para la piel, el rostro y el cuerpo. Resultados naturales, con criterio clínico.</p>%s<a class="enlace" href="medicina-estetica.html">Ver todos los tratamientos</a>''' % (
           '<ul class="catalogo corto">%s</ul>' % "".join('<li><a href="medicina-estetica.html#%s"><b>%s</b><span class="c">%s</span><span class="fl" aria-hidden="true">→</span></a></li>' % (k, n, d) for k, n, d, f in CATEGORIAS_ME)))
       + seccion("Especialistas", "Médicos especializados.<br>Decisiones personales.", '<div class="esp-duo">%s</div><a class="enlace rev" href="especialistas.html">Conocer a los especialistas</a>' % "".join(
           '<a class="esp-card rev" href="especialistas.html#%s"><span class="esp-foto">%s</span><span class="esp-nom">%s</span><span class="esp-rol">%s</span></a>' % (e["slug"], foto_esp(e), e["nombre"], e["rol"]) for e in ESPECIALISTAS), "sin-borde")
       + '''<section class="foto-frase"><div class="capa" style="background-image:url(%s)"></div><div class="caja"><p class="ceja rev">Seguridad</p><p class="grande rev">Tu tranquilidad es parte del resultado.</p><a class="boton rev" href="seguridad.html">Cómo cuidamos tu procedimiento</a></div></section>''' % img("foto-espera")
       + seccion("Tu proceso", "Tres pasos.", '<ol class="pasos">%s</ol>' % "".join(
           '<li class="rev"><span class="n">%s</span><b>%s</b><span>%s</span></li>' % x for x in [
               ("I", "Valoración", "Te escuchamos, te examinamos y te decimos qué tiene sentido para ti."),
               ("II", "Tu plan por escrito", "Procedimiento, tiempos, cuidados y presupuesto, claros desde el principio."),
               ("III", "Procedimiento y seguimiento", "Con acompañamiento cercano hasta el alta.")]))
       + cierre())


# ================================================================ CIRUGÍA PLÁSTICA (hub)
bloques_cx = ""
for k, n, d, f in CATEGORIAS_CX:
    lista = [c for c in CIRUGIAS_NOON if c["cat"] == k]
    bloques_cx += '<section class="sec" id="%s"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">Cirugía plástica</p><h2 class="rev">%s</h2><p class="sub rev">%s</p></header><div class="sec-cuerpo">%s</div></div></section>' % (k, n, d, catalogo(lista, "cx"))
pagina("cirugia-plastica.html", "Cirugía plástica", "Cirugía plástica en noon Clinic: rostro, senos, contorno corporal y procedimientos combinados.",
       hero("seda-burdeos", "Cirugía plástica", "Cirugía plástica<br>con criterio.", "Cada cirugía empieza entendiendo qué quieres lograr y qué quieres preservar.", "alto")
       + '<nav class="saltos" aria-label="Categorías">%s</nav>' % "".join('<a href="#%s">%s</a>' % (k, n) for k, n, d, f in CATEGORIAS_CX)
       + bloques_cx
       + bloque_especialista("cirugia", "Te valora y te opera el mismo especialista, que te acompaña desde la primera consulta hasta el alta.")
       + cierre())

# ================================================================ UNA PÁGINA POR CIRUGÍA
for c in CIRUGIAS_NOON:
    cat_n, cat_d, f = CAT_CX[c["cat"]]
    d = c["datos"]
    otras = [x for x in CIRUGIAS_NOON if x["cat"] == c["cat"] and x["slug"] != c["slug"]]
    msj = "Hola, quiero agendar mi valoración para %s en noon Clinic." % c["nombre"].lower()
    pagina(c["slug"] + ".html", c["nombre"], c["corto"],
           hero(f, "Cirugía plástica · " + cat_n, c["nombre"], c["corto"], "alto")
           + datos_barra([("Duración", d[0]), ("Anestesia", d[1]), ("Incapacidad aprox.", d[2]), ("Resultado final", d[3])])
           + frase("El procedimiento", c["que_es"][0], c["que_es"][1] if len(c["que_es"]) > 1 else "", "media")
           + seccion("Es para ti si", "Lo que buscas", lineas([(x,) for x in c["ideal"]]) + '<p class="pista rev">La indicación final la da tu cirujano en la valoración.</p>')
           + seccion("Recuperación", "Paso a paso", '<ol class="tiempo">%s</ol><p class="pista rev">Tiempos de guía. Tu cirujano te da los exactos.</p>' % "".join('<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in c["recuperacion"]))
           + bloque_especialista("cirugia", "Tu valoración de %s es con el especialista que te opera." % c["nombre"].lower())
           + seccion("Preguntas", "Sobre " + c["nombre"].lower(), faq([("", q, r, []) for q, r in c["faq"]]) + '<a class="enlace rev" href="preguntas-frecuentes.html">Todas las preguntas</a>', "marfil")
           + (seccion("También en " + cat_n.lower(), "Otras cirugías", catalogo(otras, "cx")) if otras else "")
           + cierre(c["nombre"], "Todo empieza con tu valoración: te decimos si es para ti y recibes tu plan por escrito.",
                    '<a class="boton lleno" href="valoracion.html?cx=%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (c["slug"], wa(msj)), fondo=f))

# ================================================================ MEDICINA ESTÉTICA (hub)
bloques_me = ""
for k, n, d, f in CATEGORIAS_ME:
    lista = [t for t in TRATAMIENTOS if t["cat"] == k]
    bloques_me += '<section class="sec" id="%s"><div class="sec-in"><header class="sec-cab"><p class="ceja rev">Medicina estética</p><h2 class="rev">%s</h2><p class="sub rev">%s</p></header><div class="sec-cuerpo">%s</div></div></section>' % (k, n, d, catalogo(lista, "me"))
pagina("medicina-estetica.html", "Medicina estética", "Medicina estética en noon Clinic: toxina botulínica, ácido hialurónico, bioestimuladores, piel, láser, HIFU y bienestar.",
       hero("seda-champan", "Medicina estética", "Realzar lo tuyo,<br>sin cambiar quién eres.", "Tratamientos médicos no quirúrgicos con resultados naturales.", "alto")
       + '<nav class="saltos" aria-label="Categorías">%s</nav>' % "".join('<a href="#%s">%s</a>' % (k, n) for k, n, d, f in CATEGORIAS_ME)
       + bloques_me
       + bloque_especialista("estetica", "Cada tratamiento empieza con una valoración para definir qué necesita tu piel y qué no.")
       + cierre(fondo="seda-champan"))

# ================================================================ UNA PÁGINA POR TRATAMIENTO
for t in TRATAMIENTOS:
    cat_n, cat_d, f = CAT_ME[t["cat"]]
    d = t["datos"]
    otras = [x for x in TRATAMIENTOS if x["cat"] == t["cat"] and x["slug"] != t["slug"]]
    msj = "Hola, quiero agendar una valoración para %s en noon Clinic." % t["nombre"].lower()
    pagina(t["slug"] + ".html", t["nombre"], t["corto"],
           hero(f, "Medicina estética · " + cat_n, t["nombre"], t["corto"], "medio")
           + datos_barra([("Sesiones", d[0]), ("Duración", d[1]), ("Recuperación", d[2]), ("Resultado", d[3])])
           + frase("El tratamiento", t["que_es"][0], t["que_es"][1] if len(t["que_es"]) > 1 else "", "media")
           + seccion("Indicado para", "Lo que buscas", lineas([(x,) for x in t["ideal"]]) + '<p class="pista rev">La indicación final la da tu médica en la valoración.</p>')
           + bloque_especialista("estetica", "Tu valoración y tu tratamiento de %s los realiza la médica estética de noon." % t["nombre"].lower())
           + seccion("Preguntas", "Sobre " + t["nombre"].lower(), faq([("", q, r, []) for q, r in t["faq"]]), "marfil")
           + (seccion("También en " + cat_n.lower(), "Otros tratamientos", catalogo(otras, "me")) if otras else "")
           + cierre(t["nombre"], "Agenda tu valoración y armamos contigo el plan que tu piel necesita.",
                    '<a class="boton lleno" href="valoracion.html?cx=%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (t["slug"], wa(msj)), fondo=f))

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
       hero("seda-noche", "Especialistas", "Médicos especializados.<br>Decisiones personales.", "Te escuchamos antes de proponer, te explicamos sin dramatizar y decidimos contigo.")
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
       hero("seda-clara", "Preguntas frecuentes", "Todas tus dudas,<br>con calma.", "%d respuestas. Busca por palabra o filtra por tema." % len(FAQ_NOON))
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
       hero("seda-oscura", "Primer paso", "Tu valoración.", "Una conversación clínica empieza por entender qué quieres preservar.")
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
