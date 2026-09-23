# -*- coding: utf-8 -*-
# noon Clinic · v2 editorial (referentes de Laura: oscuro cálido, imagen a pantalla completa, texto mínimo)
# Genera todas las páginas a partir de datos.py.   Uso:  python3 build.py
import os, time, json, re
from html import escape
from urllib.parse import quote
from datos import *

AQUI = os.path.dirname(os.path.abspath(__file__))
CX = {c["slug"]: c for c in CIRUGIAS}
V = int(time.time())

# Imagen de fondo de cada procedimiento (sedas generadas en la paleta Noon)
FONDO = {"mamoplastia-de-aumento": "seda-clara", "mastopexia-con-implantes": "seda-burdeos",
         "mastopexia-sin-implantes": "seda-horizonte", "lipo": "seda-cafe"}
CLARO = {"seda-clara", "seda-horizonte"}  # fondos claros: texto oscuro encima


def wa(mensaje="Hola, quiero agendar mi cita de valoración en noon Clinic."):
    return "https://wa.me/" + WHATSAPP + "?text=" + quote(mensaje)


def img(nombre):
    return "assets/noon/%s.jpg" % nombre


MENU = [
    ("cirugias.html", "Procedimientos"),
    ("todo-incluido.html", "Qué incluye"),
    ("seguridad.html", "Seguridad"),
    ("tu-proceso.html", "Tu proceso"),
    ("formas-de-pago.html", "Pagos"),
    ("otra-ciudad.html", "Si vienes de lejos"),
    ("nosotros.html", "Nosotros"),
    ("preguntas-frecuentes.html", "Preguntas"),
]


def pagina(archivo, titulo, descripcion, cuerpo):
    menu_cx = "".join('<a href="%s.html">%s</a>' % (c["slug"], c["nombre"]) for c in CIRUGIAS)
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
  <div class="menu-in">
    <div class="menu-col"><p class="ceja">Procedimientos</p><nav class="grande">%(menu_cx)s</nav></div>
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
    <p class="lema">Estética con criterio.</p>
    <div class="pie-cols">
      <div><p class="ceja">Procedimientos</p>%(pie_cx)s</div>
      <div><p class="ceja">Información</p><a href="todo-incluido.html">Qué incluye</a><a href="seguridad.html">Seguridad</a><a href="tu-proceso.html">Tu proceso</a><a href="formas-de-pago.html">Pagos</a><a href="otra-ciudad.html">Si vienes de lejos</a><a href="preguntas-frecuentes.html">Preguntas</a></div>
      <div><p class="ceja">Contacto</p><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp %(tel)s</a><a href="valoracion.html">Agendar valoración</a><a href="nosotros.html">Nosotros</a></div>
    </div>
    <a class="boton champan" href="terminos-y-condiciones.html">Términos y condiciones</a>
    <p class="legal">La información de este sitio es orientativa y no reemplaza una consulta médica. Toda cirugía tiene riesgos y los resultados varían de una persona a otra. © noon Clinic</p>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="assets/noon.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"titulo": escape(titulo + (" · noon Clinic" if archivo != "index.html" else "")), "desc": escape(descripcion), "cuerpo": cuerpo,
       "menu_cx": menu_cx, "menu": menu, "v": V, "wa": wa(), "tel": TELEFONO,
       "pie_cx": "".join('<a href="%s.html">%s</a>' % (c["slug"], c["nombre"]) for c in CIRUGIAS)}
    # Direcciones limpias: sin "index.html" ni ".html"
    html = re.sub(r'href="index\.html([?#][^"]*)?"', lambda m: 'href="./%s"' % (m.group(1) or ""), html)
    html = re.sub(r'href="([a-z0-9-]+)\.html([?#][^"]*)?"', lambda m: 'href="%s%s"' % (m.group(1), m.group(2) or ""), html)
    with open(os.path.join(AQUI, archivo), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓", archivo)


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
    texto = texto or "Todo empieza con una conversación con nuestros cirujanos. Valoración %s." % VALORACION
    boton = boton or '<a class="boton lleno" href="valoracion.html%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (
        "?cx=" + cx["slug"] if cx else "", wa("Hola, quiero agendar mi valoración%s." % (" para " + cx["nombre"].lower() if cx else "")))
    tono = " sobre-claro" if fondo in CLARO else ""
    return '<section class="cierre%s"><div class="capa" style="background-image:url(%s)"></div><div class="caja"><p class="ceja rev">noon Clinic</p><h2 class="rev">%s</h2><p class="sub rev">%s</p><div class="botones rev">%s</div>%s</div></section>' % (
        tono, img(fondo), titulo, texto, boton, nota)


NOMBRE_INC = {"cirujano": "Cirujano plástico", "instrumentador": "Instrumentador quirúrgico", "quirofano": "Quirófano en " + SEDE_QX, "implantes": "Implantes mamarios",
              "prenda": "Brasier posquirúrgico", "faja": "Prenda posquirúrgica", "poliza": "Póliza de complicaciones", "bomba": "Bomba de dolor", "masajes": "Masajes postoperatorios"}


def incluye(claves):
    return lineas([(NOMBRE_INC[k], INCLUIDOS[k][1]) for k in claves])


def no_incluye():
    return '<details class="plegable rev"><summary>Lo que no incluye</summary>%s</details>' % lineas(NO_INCLUYE)


def nota_tc(texto=None):
    texto = texto or "La valoración no se devuelve ni se abona. Si abonas y decides no operarte, se devuelve lo abonado con una retención del %s. Tu cirugía debe realizarse antes del %s." % (RETENCION, FECHA_LIMITE)
    return '<div class="nota-tc rev"><p>%s</p><a href="terminos-y-condiciones.html">Leer términos y condiciones</a></div>' % texto


def tiles(lista=None):
    out = ""
    for c in (lista or CIRUGIAS):
        f = FONDO[c["slug"]]
        out += '''<a class="tile rev%s" href="%s.html"><span class="tile-img" style="background-image:url(%s)"></span>
  <span class="tile-txt"><span class="ceja">%s</span><span class="nom">%s</span><span class="desde">Desde %s · todo incluido</span><span class="ir">Descubrir</span></span></a>''' % (
            " sobre-claro" if f in CLARO else "", c["slug"], img(f), c["duracion"], c["nombre"], c["precio"])
    return '<div class="tiles">%s</div>' % out


# ================================================================ INICIO
pagina("index.html", "noon Clinic · Cirugía plástica con criterio",
       "Mamoplastia, mastopexia y lipo con un solo precio que lo incluye todo: cirujano, quirófano en Q2, póliza y bomba de dolor. Agenda tu valoración.",
       '''<section class="hero completo portada"><div class="capa" style="background-image:url(%s)"></div><canvas class="seda-viva" aria-hidden="true"></canvas><div class="hero-in">
  <img class="logo-hero rev" src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295">
  <p class="ceja rev">Estética con criterio</p>
  <p class="sub rev">Cirugía plástica · Médicos especializados · Decisiones personales</p>
</div><a class="bajar" href="#creemos" aria-label="Bajar">Descubrir</a></section>''' % img("seda-oscura")
       + frase("Lo que creemos", "Primero entendemos.<br>Después hablamos de posibilidades.",
               "La recomendación nace del criterio clínico y de lo que cada persona quiere preservar.", "creemos").replace('class="frase creemos"', 'class="frase creemos" id="creemos"')
       + seccion("Procedimientos", "Cuatro cirugías.<br>Un solo precio cada una.", tiles(), "sin-borde")
       + dividir("foto-consulta", '''<p class="ceja">Todo incluido</p><h2>Sin letra pequeña.</h2>
<p class="sub">El precio que ves es el precio que pagas. Dentro de él:</p>%s<a class="enlace" href="todo-incluido.html">Ver qué incluye cada procedimiento</a>''' % lineas([
           ("Cirujano plástico e instrumentador",), ("Quirófano en " + SEDE_QX,), ("Póliza de complicaciones",), ("Bomba de dolor",), ("Prenda posquirúrgica",)]))
       + '''<section class="foto-frase"><div class="capa" style="background-image:url(%s)"></div><div class="caja"><p class="ceja rev">Seguridad</p><p class="grande rev">Un buen precio nunca debería costarte tu tranquilidad.</p><a class="boton rev" href="seguridad.html">Cómo cuidamos tu cirugía</a></div></section>''' % img("foto-espera")
       + seccion("Tu proceso", "Tres pasos.", '<ol class="pasos">%s</ol>' % "".join(
           '<li class="rev"><span class="n">%s</span><b>%s</b><span>%s</span></li>' % x for x in [
               ("I", "Valoración", "Nuestros cirujanos te examinan y te dicen qué es para ti. %s." % VALORACION),
               ("II", "Separas tu fecha", "Con un abono reservas tu quirófano."),
               ("III", "Tu cirugía", "En %s, con todo incluido y acompañamiento hasta el alta." % SEDE_QX)]))
       + cierre())

# ================================================================ PROCEDIMIENTOS
pagina("cirugias.html", "Procedimientos", "Mamoplastia de aumento, mastopexia con y sin implantes y lipo: un solo precio que lo incluye todo.",
       hero("seda-burdeos", "Procedimientos", "Cada cuerpo,<br>una decisión personal.", "Cuatro cirugías con un solo precio que lo incluye todo. Cuál es la tuya se define en la valoración.")
       + seccion("Elige", "Nuestros procedimientos", tiles(), "sin-borde")
       + seccion("Guía", "¿Cuál es para ti?", lineas([(x[0], x[2] + ' <a class="enlace" href="%s.html">%s</a>' % (x[1], CX[x[1]]["nombre"])) for x in SELECTOR]),
                 intro="Si dudas entre dos, no te preocupes: eso se resuelve en la valoración.")
       + seccion("Lado a lado", "Compara", '<div class="tabla-caja rev"><table><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table></div>' % (
           "".join('<th><a href="%s.html">%s</a></th>' % (c["slug"], c["corto"]) for c in CIRUGIAS),
           "<tr><td>Duración</td>%s</tr>" % "".join("<td>%s</td>" % c["duracion"] for c in CIRUGIAS)
           + "".join("<tr><td>%s</td>%s</tr>" % (NOMBRE_INC[k if k != "prenda" else "faja"], "".join(
               '<td>%s</td>' % ("Incluido" if (k in c["incluye"] or (k == "prenda" and "faja" in c["incluye"])) else "—") for c in CIRUGIAS))
               for k in ["cirujano", "instrumentador", "quirofano", "implantes", "prenda", "poliza", "bomba", "masajes"])
           + '<tr class="total"><td>Inversión total</td>%s</tr>' % "".join("<td>%s</td>" % c["precio"] for c in CIRUGIAS)))
       + cierre())

# ================================================================ UNA PÁGINA POR PROCEDIMIENTO
for c in CIRUGIAS:
    f = FONDO[c["slug"]]
    msj = "Hola, quiero agendar mi valoración para %s en noon Clinic." % c["nombre"].lower()
    datos = '<section class="datos"><div><span class="ceja">Duración</span><b>%s</b></div><div><span class="ceja">Incapacidad aprox.</span><b>%s</b></div><div><span class="ceja">Resultado final</span><b>%s</b></div><div><span class="ceja">Inversión total</span><b>%s</b></div></section>' % (
        c["duracion"], RAPIDOS[c["slug"]][0], RAPIDOS[c["slug"]][1], c["precio"])
    pagina(c["slug"] + ".html", c["nombre"], c["intro"],
           hero(f, "Procedimiento", c["nombre"], c["frase"], "alto")
           + datos
           + frase("El procedimiento", c["intro"])
           + seccion("Es para ti si", "Lo que buscas", lineas([(x,) for x in c["para_ti"]]) + '<p class="pista rev">%s</p>' % c["ojo"])
           + dividir("foto-luz" if "lipo" in c["slug"] else "foto-detalle", '<p class="ceja">Cómo es</p><h2>La cirugía</h2>%s%s' % (
               "".join("<p>%s</p>" % p for p in c["como_es"]), lineas([(t, d) for _, t, d in PUNTOS[c["slug"]]])), invertir=True)
           + seccion("Todo incluido", "Tu inversión lo incluye", incluye(c["incluye"]) + no_incluye(),
                     intro="Un solo precio: %s. Sin sumas de última hora." % c["precio"])
           + seccion("Recuperación", "Paso a paso", '<ol class="tiempo">%s</ol><p class="pista rev">Tiempos de guía. Tu cirujano te da los exactos.</p>' % "".join(
               '<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in c["recuperacion"]))
           + seccion("Preguntas", "Sobre " + c["nombre"].lower(), faq([q for q in FAQ if c["slug"] in q[3]]) + '<a class="enlace rev" href="preguntas-frecuentes.html">Todas las preguntas</a>', "marfil")
           + cierre(c["nombre"], "Inversión total %s, todo incluido. Todo empieza con tu valoración (%s)." % (c["precio"], VALORACION),
                    '<a class="boton lleno" href="valoracion.html?cx=%s">Agendar mi valoración</a><a class="boton" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % (c["slug"], wa(msj)),
                    fondo=f, nota=nota_tc()))

# ================================================================ QUÉ INCLUYE
todos = ["cirujano", "instrumentador", "quirofano", "poliza", "bomba", "prenda", "implantes", "masajes"]
pagina("todo-incluido.html", "Qué incluye tu inversión", "Cirujano, instrumentador, quirófano en Q2, póliza de complicaciones, bomba de dolor, prenda posquirúrgica, implantes y masajes.",
       hero("seda-horizonte", "Todo incluido", "El precio que ves<br>es el que pagas.", "Lo que ya viene dentro, explicado con calma. Y lo que no, para que no haya sorpresas.")
       + seccion("Dentro de tu inversión", "Lo que incluye", incluye(todos),
                 intro="Los implantes aplican en mamoplastia de aumento y mastopexia con implantes. Los masajes, en lipo.")
       + dividir("foto-objetos", '<p class="ceja">Aparte</p><h2>Lo que no incluye</h2><p class="sub">Son pocas cosas y es mejor saberlas desde hoy.</p>%s' % lineas(NO_INCLUYE))
       + seccion("Procedimientos", "Elige el tuyo", tiles(), "sin-borde")
       + cierre())

# ================================================================ SEGURIDAD
ALERTAS = [
    ("Precio sin detalle", "Si no te dicen por escrito qué incluye, lo que falta aparece después."),
    ("Sin póliza", "Operarte sin póliza de complicaciones es asumir sola todo el riesgo."),
    ("Fuera de un quirófano", "Una cirugía se hace en salas de cirugía. Un consultorio no lo es."),
    ("Sin exámenes", "Si nadie te pide exámenes, nadie está revisando si es seguro operarte."),
    ("Todo es “sí”", "Un buen cirujano también te dice qué no se puede o no se debe hacer."),
    ("Afán para pagar", "Una decisión así se toma con calma y con toda la información."),
]
pagina("seguridad.html", "Seguridad", "Operamos en quirófano en Q2, con póliza de complicaciones, exámenes prequirúrgicos y seguimiento hasta el alta.",
       hero("foto-pasillo", "Seguridad", "Un buen precio<br>nunca debería costarte<br>tu tranquilidad.")
       + seccion("No negociables", "Cómo cuidamos tu cirugía", lineas([
           ("Operamos solo en quirófano", "Todas las cirugías se hacen en las salas de cirugía de %s. Nunca en consultorios." % SEDE_QX),
           ("Te valoramos primero", "Nadie se opera sin una valoración médica presencial y honesta."),
           ("Exámenes antes de operar", "Si tus exámenes no están en regla, la cirugía se aplaza. Sin excepciones."),
           ("Póliza de complicaciones incluida", "Toda cirugía tiene riesgos. La póliza es tu respaldo si algo se presenta."),
           ("Dolor bajo control", "La bomba de dolor te acompaña en los días más incómodos."),
           ("Controles hasta el alta", "Te acompañamos hasta que todo esté bien."),
           ("Sabemos decir que no", "Si operarte no es seguro para ti, te lo decimos."),
       ], numerar=True))
       + frase("Al elegir dónde operarte", "Señales de alerta.", "Aplican para cualquier lugar, incluido el nuestro. Pregunta siempre.")
       + seccion("Presta atención a", "Seis señales", lineas(ALERTAS, numerar=True), "sin-cab-borde")
       + seccion("Preguntas", "Sobre seguridad", faq([q for q in FAQ if q[0] == "Seguridad"]), "marfil")
       + cierre())

# ================================================================ TU PROCESO
pagina("tu-proceso.html", "Tu proceso", "De la cita de valoración al resultado final: así es el camino de tu cirugía.",
       hero("seda-oscura", "Tu proceso", "De la primera conversación<br>al resultado.", "Saber qué viene quita la mitad de los nervios.")
       + seccion("El camino", "Paso a paso", '<ol class="tiempo num">%s</ol>' % "".join('<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in PROCESO)
                 + nota_tc("La valoración cuesta %s, no es abonable al tratamiento y su valor no se devuelve." % VALORACION))
       + dividir("foto-recepcion", '<p class="ceja">El día de tu cirugía</p><h2>Qué llevar</h2>%s' % lineas([(x,) for x in QUE_LLEVAR]))
       + seccion("Preguntas", "Sobre la recuperación", faq([q for q in FAQ if q[0] == "Dolor y recuperación"][:6]), "marfil")
       + cierre())

# ================================================================ PAGOS
pagina("formas-de-pago.html", "Formas de pago", "Cita de valoración, abono para separar fecha, saldo y política de devoluciones.",
       hero("seda-cafe", "Pagos", "Cuentas claras<br>desde el primer día.")
       + seccion("Cómo se paga", "Tres momentos", '<ol class="pasos">%s</ol>' % "".join('<li class="rev"><span class="n">%s</span><b>%s</b><span>%s</span></li>' % x for x in [
           ("I", "Valoración · " + VALORACION, "Es el primer paso. No es abonable al tratamiento y su valor no se devuelve."),
           ("II", "Abono para tu fecha", "Reservas tu fecha en %s. Si desistes, se devuelve con una retención del %s por gastos administrativos." % (SEDE_QX, RETENCION)),
           ("III", "Saldo", "Se paga antes de la cirugía. El precio se respeta desde que abonas.")]) + nota_tc())
       + seccion("Preguntas", "Sobre pagos", faq([q for q in FAQ if q[0] == "Pagos"] + [FAQ[2]]), "marfil")
       + cierre("Medios de pago", "Escríbenos y te contamos los medios de pago disponibles hoy.",
                '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Preguntar por WhatsApp</a>' % wa("Hola, quiero conocer los medios de pago de noon Clinic.")))

# ================================================================ OTRA CIUDAD
pagina("otra-ciudad.html", "Si vienes de lejos", "Cómo operarte con nosotros si vives en otra ciudad o en el exterior: días de estadía, controles y regreso.",
       hero("seda-horizonte", "Pacientes que viajan", "Vienes de lejos.<br>Te lo ponemos fácil.", "Organizamos tus fechas para que valoración, cirugía y controles te queden en un solo viaje.")
       + seccion("Tu viaje", "Cómo se organiza", '<ol class="tiempo num">%s</ol>' % "".join('<li class="rev"><b>%s</b><span>%s</span></li>' % x for x in [
           ("Escríbenos antes de viajar", "Cuéntanos qué te interesa y dejamos agendada tu valoración para cuando llegues."),
           ("Valoración y exámenes", "Nuestros cirujanos te valoran en persona y te ordenan los exámenes."),
           ("Cirugía en " + SEDE_QX, "Con todo lo de tu procedimiento incluido."),
           ("Recuperación y controles", "Te quedas en la ciudad los días que tu cirujano indique."),
           ("Regreso a casa", "Viajas cuando tu cirujano lo autorice.")]))
       + dividir("foto-espera", '<p class="ceja">Guía de estadía</p><h2>¿Cuántos días me quedo?</h2>%s<p class="pista">Tiempos de referencia. El regreso lo autoriza tu cirujano.</p>' % lineas([
           ("Mamoplastia de aumento", "Entre 1 y 2 semanas."), ("Mastopexia con o sin implantes", "Alrededor de 2 semanas."), ("Lipo", "Entre 2 y 3 semanas.")]))
       + seccion("Recomendaciones", "Para tu viaje", lineas([("Viaja acompañada", "Necesitas un adulto contigo el día de la cirugía y los primeros días."),
                                                               ("Hospédate cerca", "Entre más cerca de %s y de tus controles, más cómoda tu recuperación." % SEDE_QX),
                                                               ("Tiquetes flexibles", "La fecha de regreso depende de tu evolución, no del calendario."),
                                                               ("Trae tus exámenes", "Si tienes exámenes recientes, tráelos a la valoración.")]))
       + seccion("Preguntas", "De quienes viajan", faq([q for q in FAQ if q[0] == "Vengo de lejos"]), "marfil")
       + cierre("Organicemos tu viaje", "Escríbenos y armamos tus fechas contigo.",
                '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % wa("Hola, vivo en otra ciudad y quiero información para operarme en noon Clinic.")))

# ================================================================ PREGUNTAS
filtros = '<button class="filtro on" data-cat="todas" type="button">Todas</button>' + "".join('<button class="filtro" data-cat="%s" type="button">%s</button>' % (escape(x), x) for x in CATS)
pagina("preguntas-frecuentes.html", "Preguntas frecuentes", "Respuestas sobre precios, seguridad, dolor, recuperación, implantes, requisitos y pagos.",
       hero("seda-clara", "Preguntas frecuentes", "Todas tus dudas,<br>con calma.", "%d respuestas. Busca por palabra o filtra por tema." % len(FAQ))
       + '''<section class="sec marfil"><div class="sec-in solo">
  <input class="buscador" type="search" placeholder="Busca: dolor, implantes, abono…" aria-label="Buscar en las preguntas">
  <div class="filtros">%s</div>%s<p class="vacio" hidden>No encontramos esa pregunta. Escríbenos por WhatsApp y te respondemos.</p>
</div></section>''' % (filtros, faq(FAQ, filtrable=True))
       + cierre("¿No encontraste tu pregunta?", "Escríbenos y te respondemos.",
                '<a class="boton lleno" href="%s" target="_blank" rel="noopener">Escribir por WhatsApp</a>' % wa("Hola, tengo una pregunta para noon Clinic."), fondo="seda-oscura"))

# ================================================================ NOSOTROS
pagina("nosotros.html", "Nosotros", "noon Clinic: médicos especializados, decisiones personales y la seguridad primero.",
       hero("foto-consulta", "Nosotros", "Estética con criterio.", "Médicos especializados. Decisiones personales.", "alto")
       + frase("Quiet confidence", "La belleza se aborda con escucha,<br>precisión médica y decisiones personales.")
       + dividir("foto-detalle", '''<p class="ceja">Quién te opera</p><h2>Nuestros cirujanos</h2>
<p>Tu cirugía está en manos de nuestros cirujanos plásticos. Los conoces desde la valoración: te examinan, te escuchan y te explican qué se puede lograr y qué no, antes de que tomes cualquier decisión.</p>
<p>Trabajan con un equipo completo —instrumentador y personal de salas de cirugía— en los quirófanos de %s.</p>''' % SEDE_QX)
       + seccion("Principios", "Cómo trabajamos", lineas([("Escuchar antes de proponer",), ("Explicar sin dramatizar",), ("Decidir junto a la persona",), ("Cuidar también el seguimiento",)], numerar=True))
       + seccion("Lo que puedes esperar", "De nosotros", lineas([("Te decimos el precio completo desde el principio",), ("Te explicamos los riesgos, no solo los beneficios",),
                                                                 ("Si no eres candidata, te lo decimos",), ("Te acompañamos hasta el alta",)]))
       + cierre())

# ================================================================ VALORACIÓN
opciones = "".join('<option data-slug="%s">%s</option>' % (c["slug"], c["nombre"]) for c in CIRUGIAS)
pagina("valoracion.html", "Agenda tu valoración", "Todo empieza con tu cita de valoración con nuestros cirujanos. Agéndala por WhatsApp.",
       hero("seda-oscura", "Primer paso", "Tu valoración.", "Una conversación clínica empieza por entender qué quieres preservar.")
       + '''<section class="valoracion">
  <div class="texto rev"><p class="ceja">Valor de la cita</p><p class="precio">%(val)s</p>%(lista)s%(tc)s</div>
  <form class="form rev" id="form-valoracion" data-wa="%(wa)s">
    <p class="ceja">Agenda por WhatsApp</p><h2>Empieza aquí</h2>
    <p class="sub">Tres datos y se abre WhatsApp con tu mensaje listo.</p>
    <label>Tu nombre<input id="nombre" name="nombre" required autocomplete="given-name"></label>
    <label>Procedimiento que te interesa<select id="cirugia" name="cirugia">%(op)s<option>Aún no estoy segura</option></select></label>
    <label>Ciudad donde vives<input id="ciudad" name="ciudad" required autocomplete="address-level2"></label>
    <button class="boton lleno" type="submit">Continuar en WhatsApp</button>
    <p class="legal">Al escribirnos aceptas nuestros <a href="terminos-y-condiciones.html">términos y condiciones</a>. Este formulario no guarda tus datos.</p>
  </form>
</section>''' % {"val": VALORACION, "wa": WHATSAPP, "op": opciones,
                 "tc": nota_tc("El valor de la cita (%s) no se descuenta de la cirugía y no se devuelve en ningún caso." % VALORACION),
                 "lista": lineas([("Consulta con nuestros cirujanos", "Examen, medidas y un plan pensado para ti."), ("Respuestas honestas", "Qué se puede lograr, qué no, y si eres candidata."), ("Orden de exámenes", "Sales con lo que necesitas para el siguiente paso.")])})

# ================================================================ TÉRMINOS
def _contenido(ps):
    return "".join("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in p) if isinstance(p, list) else "<p>%s</p>" % p for p in ps)

bloques = "".join('<section id="t%d" class="termino%s"><h3>%s</h3>%s</section>' % (i + 1, " clave" if clave else "", t, _contenido(ps)) for i, (t, ps, clave) in enumerate(TERMINOS))
indice = "".join('<a href="#t%d"%s>%s</a>' % (i + 1, ' class="clave"' if clave else "", t) for i, (t, ps, clave) in enumerate(TERMINOS))
pagina("terminos-y-condiciones.html", "Términos y condiciones", "Condiciones de la cita de valoración, abonos, política de devoluciones, reprogramación y promociones.",
       hero("seda-horizonte", "Legal", "Términos y condiciones.", "Léelos completos antes de agendar o pagar. Están escritos para que se entiendan.")
       + '''<section class="sec marfil"><div class="sec-in solo terminos">
  <div class="resumen-tc"><p class="ceja">Lo más importante</p><ul>%s</ul><a class="boton champan" href="#t4">Política de devoluciones</a></div>
  <nav class="indice" aria-label="Contenido">%s</nav>%s
</div></section>''' % ("".join("<li>%s</li>" % x for x in RESUMEN_TC), indice, bloques))

print("\nListo. %d preguntas, %d procedimientos." % (len(FAQ), len(CIRUGIAS)))
