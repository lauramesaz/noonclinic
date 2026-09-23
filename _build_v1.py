# -*- coding: utf-8 -*-
# Genera todas las páginas del sitio a partir de datos.py
# Uso:  python3 build.py
import os, time, json, re
from html import escape
from urllib.parse import quote
from datos import *

AQUI = os.path.dirname(os.path.abspath(__file__))
CX = {c["slug"]: c for c in CIRUGIAS}
V = int(time.time())
MARCA_HTML = '<img src="assets/logo-noon.png" alt="noon Clinic" width="900" height="295">'


def wa(mensaje="Hola, quiero agendar mi cita de valoración."):
    return "https://wa.me/" + WHATSAPP + "?text=" + quote(mensaje)


NAV = [
    ("todo-incluido.html", "Qué incluye"),
    ("seguridad.html", "Seguridad"),
    ("tu-proceso.html", "Proceso"),
    ("formas-de-pago.html", "Pagos"),
    ("preguntas-frecuentes.html", "Preguntas"),
]


def tc_aviso(titulo="Devoluciones: se retiene el %s" % RETENCION, texto=None):
    """Aviso grande de términos y condiciones, con botón de color. Va en todas las páginas."""
    texto = texto or "La cita de valoración no se devuelve. Si abonas y luego decides no operarte, se te devuelve lo abonado reteniendo el %s por gastos administrativos. Tu cirugía debe realizarse antes del %s." % (RETENCION, FECHA_LIMITE)
    return '<div class="tc-caja"><div><span class="tc-ceja">Importante · léelo antes de pagar</span><h2>%s</h2><p>%s</p></div><a class="btn tc" href="terminos-y-condiciones.html">Leer términos y condiciones →</a></div>' % (titulo, texto)


def pagina(archivo, titulo, descripcion, cuerpo, accion=None):
    """accion = (título, subtítulo, texto botón, enlace) para la barra fija inferior."""
    activo = lambda h: ' class="activo"' if h == archivo else ""
    menu_cx = "".join('<a href="%s.html">%s <span>%s</span></a>' % (c["slug"], c["nombre"], c["precio"]) for c in CIRUGIAS)
    nav = "".join('<a href="%s"%s>%s</a>' % (h, activo(h), t) for h, t in NAV)
    a = accion or ("Agenda tu valoración", "Primer paso · " + VALORACION, "Agendar", "valoracion.html")
    barra = "" if archivo == "valoracion.html" else '<div class="accion%s"><div class="t"><b>%s</b><span>%s</span></div><a class="btn pri ch" href="%s"%s>%s</a></div>' % (
        " solo-movil" if accion else "", a[0], a[1], a[3], ' target="_blank" rel="noopener"' if a[3].startswith("http") else "", a[2])
    html = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s · noon Clinic</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#F2EFE8">
<link rel="icon" href="assets/favicon.png">
<script>document.documentElement.className="js"</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css?v=%(v)s">
</head>
<body>
<header class="cab"><div class="barra">
  <a class="marca" href="index.html">%(marca)s</a>
  <button class="hamb" aria-label="Abrir menú" aria-expanded="false">☰</button>
  <nav class="nav">
    <div class="desple"><button class="grupo" type="button">Cirugías ▾</button>
      <div class="menu">%(menu_cx)s<a href="cirugias.html">Comparar las 4 promos <span>→</span></a></div></div>
    %(nav)s
    <a class="btn pri ch" href="valoracion.html">Quiero mi valoración</a>
  </nav>
</div></header>
<main>
%(cuerpo)s
</main>
%(tc)s
<footer class="pie"><div class="cont">
  <div class="cols">
    <div><a class="marca" href="index.html">%(marca)s</a><p class="bajada" style="font-size:15px;margin-top:14px;max-width:340px">Promos de cirugía plástica con un solo precio: lo que ves es lo que pagas.</p><a class="btn ch" style="display:inline-flex;margin-top:8px" href="%(wa)s" target="_blank" rel="noopener">WhatsApp %(tel)s</a></div>
    <div><h4>Cirugías</h4>%(pie_cx)s<a href="cirugias.html">Comparar promos</a></div>
    <div><h4>Información</h4><a href="todo-incluido.html">Qué incluye tu precio</a><a href="formas-de-pago.html">Formas de pago</a><a href="otra-ciudad.html">Vienes de otra ciudad</a><a href="nosotros.html">Nosotros</a><a href="preguntas-frecuentes.html">Preguntas frecuentes</a></div>
  </div>
  <a class="btn tc" href="terminos-y-condiciones.html">Términos y condiciones →</a>
  <p class="fin">La información de este sitio es orientativa y no reemplaza una consulta médica. Toda cirugía tiene riesgos y los resultados varían de una persona a otra.</p>
</div></footer>
%(barra)s
<nav class="tabs" aria-label="Navegación rápida">%(tabs)s</nav>
<script src="assets/app.js?v=%(v)s"></script>
</body>
</html>
""" % {
        "titulo": escape(titulo), "desc": escape(descripcion), "cuerpo": cuerpo, "nav": nav, "menu_cx": menu_cx, "v": V,
        "tabs": "".join('<a href="%s" class="%s"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>%s</a>' % (h, ("centro-tab" if h == "valoracion.html" else "activo" if (h == archivo or (h == "cirugias.html" and archivo[:-5] in CX)) else ""), ICONOS[i], t)
                        for h, i, t in [("index.html", "casa", "Inicio"), ("cirugias.html", "brillo", "Cirugías"), ("valoracion.html", "calendario", "Agendar"), ("todo-incluido.html", "lista", "Incluye"), ("preguntas-frecuentes.html", "duda", "Dudas")]),
        "tc": "" if archivo in ("terminos-y-condiciones.html", "valoracion.html", "formas-de-pago.html") else '<section class="tc-banda"><div class="cont">%s</div></section>' % tc_aviso(),
        "marca": MARCA_HTML, "wa": wa(), "tel": TELEFONO, "barra": barra,
        "pie_cx": "".join('<a href="%s.html">%s</a>' % (c["slug"], c["nombre"]) for c in CIRUGIAS),
    }
    # Direcciones limpias: los enlaces internos salen sin "index.html" ni ".html"
    html = re.sub(r'href="index\.html([?#][^"]*)?"', lambda m: 'href="./%s"' % (m.group(1) or ""), html)
    html = re.sub(r'href="([a-z0-9-]+)\.html([?#][^"]*)?"', lambda m: 'href="%s%s"' % (m.group(1), m.group(2) or ""), html)
    with open(os.path.join(AQUI, archivo), "w", encoding="utf-8") as f:
        f.write(html)
    print("✓", archivo)


# ---------- piezas reutilizables ----------
def hero_interna(etiqueta, h1, bajada, migas=None):
    m = '<p class="migas"><a href="index.html">Inicio</a>%s</p>' % "".join(" &nbsp;/&nbsp; " + x for x in (migas or []))
    return '<section class="hero interna">' + CURVAS + '<div class="cont">%s<span hidden>%s</span><h1>%s</h1><p class="bajada">%s</p></div></section>' % (m, etiqueta, h1, bajada)


def cab(h2, bajada="", centro=False, etiqueta=""):
    return '<div class="sec-cab ver%s">%s<h2>%s</h2>%s</div>' % (
        " centro" if centro else "", '<span class="etiqueta">%s</span><br>' % etiqueta if etiqueta else "", h2, '<p class="bajada">%s</p>' % bajada if bajada else "")


ICONOS = {
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/>',
    "team": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 3-6 6-6s6 3 6 6"/><circle cx="17" cy="9" r="2"/><path d="M17 14c2 0 4 2 4 5"/>',
    "cruz": '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M12 8v8M8 12h8"/>',
    "implantes": '<circle cx="8" cy="12" r="4"/><circle cx="16" cy="12" r="4"/>',
    "prenda": '<path d="M8 4l4 3 4-3 4 4-3 3v9H7v-9L4 8z"/>',
    "escudo": '<path d="M12 3l8 3v6c0 5-3 8-8 9-5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "gota": '<path d="M12 3s6 6 6 11a6 6 0 0 1-12 0c0-5 6-11 6-11z"/>',
    "brillo": '<path d="M12 4v4M12 16v4M4 12h4M16 12h4M7 7l2 2M15 15l2 2M17 7l-2 2M9 15l-2 2"/>',
    "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calendario": '<rect x="4" y="5" width="16" height="15" rx="3"/><path d="M4 10h16M9 3v4M15 3v4"/>',
    "luna": '<path d="M20 14a8 8 0 1 1-10-10 6 6 0 0 0 10 10z"/>',
    "regla": '<path d="M5 19L19 5M8 16l2 2M11 13l2 2M14 10l2 2"/>',
    "pastilla": '<rect x="3" y="9" width="18" height="6" rx="3" transform="rotate(-45 12 12)"/>',
    "frasco": '<path d="M10 3h4M11 3v6l-5 9a2 2 0 0 0 2 3h8a2 2 0 0 0 2-3l-5-9V3"/>',
    "mas": '<path d="M12 5v14M5 12h14"/>',
    "avion": '<path d="M3 13l18-8-6 16-3-7z"/>',
    "casa": '<path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z"/>',
    "duda": '<circle cx="12" cy="12" r="9"/><path d="M9 10a3 3 0 1 1 4 3c-1 .5-1 1-1 2M12 18v.5"/>',
    "lista": '<path d="M9 6h11M9 12h11M9 18h11M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
}


def ico(nombre):
    return '<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span>' % ICONOS[nombre]


TITULOS = {"cirujano": "Cirujano plástico", "instrumentador": "Instrumentador", "quirofano": "Quirófano en " + SEDE_QX, "implantes": "Implantes", "prenda": "Brasier posquirúrgico",
           "faja": "Prenda posquirúrgica", "poliza": "Póliza", "bomba": "Bomba de dolor", "masajes": "Masajes post"}


def mosaico(claves):
    """Qué incluye, para escanear: icono + nombre + frase corta. El detalle se abre al tocar."""
    out = ""
    for k in claves:
        icono, corto = INCLUIDOS_CORTO[k]
        out += '<details><summary>%s<span>%s<small hidden>%s</small></span></summary><p class="mas-info">%s</p></details>' % (ico(icono), TITULOS[k], corto, INCLUIDOS[k][1])
    return '<div class="mosaico">%s</div>' % out


def mosaico_no():
    out = "".join('<details><summary>%s<span>%s</span></summary><p class="mas-info">%s</p></details>' % (ico(NO_INCLUYE_ICONOS[i]), t, d) for i, (t, d) in enumerate(NO_INCLUYE))
    return '<div class="mosaico no">%s</div>' % out


def puntos(items):
    return '<div class="puntos">%s</div>' % "".join('<div class="punto">%s<div><b>%s</b><br><span>%s</span></div></div>' % (ico(i), t, d) for i, t, d in items)


def resaltar(a):
    """Primera frase en claro, para que la respuesta corta se lea de un vistazo."""
    m = re.match(r"^(.{2,90}?[.:])\s+(.+)$", a)
    return "<strong>%s</strong> %s" % (m.group(1), m.group(2)) if m else a


CORTOS = {"cirujano": "Cirujano", "instrumentador": "Instrumentador", "quirofano": "Quirófano " + SEDE_QX, "implantes": "Implantes", "prenda": "Brasier post",
          "faja": "Prenda post", "poliza": "Póliza", "bomba": "Bomba de dolor", "masajes": "Masajes post"}


def promos(lista=None):
    out = ""
    for c in (lista or CIRUGIAS):
        destacados = [k for k in c["incluye"] if k in ("implantes", "masajes")]
        resto = [k for k in ("quirofano", "poliza", "bomba") if k in c["incluye"]]
        clave = (destacados + [k for k in ("poliza", "bomba", "quirofano") if k in c["incluye"]])[:3]
        pildoras = '<ul class="ticks uno">%s<li class="mas-n">y %d cosas más</li></ul>' % ("".join('<li%s>%s</li>' % (' class="top"' if k in destacados else "", TITULOS[k]) for k in clave), len(c["incluye"]) - len(clave))
        out += '<a class="tarjeta promo ver%s" href="%s.html"><span class="sello">%s</span><div class="arriba"><h3>%s</h3><span class="ir">→</span></div><p>%s</p>%s<div class="abajo"><div class="valor"><small>Precio total, todo incluido</small><span data-cuenta>%s</span></div><span class="pildora">%s</span></div></a>' % (
            " estrella" if c["slug"] == CIRUGIAS[0]["slug"] and not lista else "", c["slug"], SELLOS[c["slug"]], c["nombre"], c["frase"], pildoras, c["precio"], c["duracion"])
    return out


def lista(claves):
    return '<ul class="lista">%s</ul>' % "".join("<li><div><b>%s</b><span>%s</span></div></li>" % INCLUIDOS[k] for k in claves)


def lista_libre(items, no=False):
    return '<ul class="lista%s">%s</ul>' % (" no" if no else "", "".join(
        "<li><div><b>%s</b>%s</div></li>" % (x[0], "<span>%s</span>" % x[1] if len(x) > 1 and x[1] else "") for x in items))


def tiempo(pasos):
    return '<div class="tiempo">%s</div>' % "".join(
        '<div class="paso ver"><div class="bola">%d</div><div class="txt"><h3>%s</h3><p>%s</p></div></div>' % (i, t, d) for i, (t, d) in enumerate(pasos, 1))


def carril(pasos):
    return '<div class="carril ver">%s</div>' % "".join(
        '<div class="tarjeta"><span class="num">%02d</span><h3>%s</h3><p>%s</p></div>' % (i, t, d) for i, (t, d) in enumerate(pasos, 1))


def acordeon(items, filtrable=False):
    out = "".join('<details data-cat="%s"><summary>%s</summary><div class="resp"><p>%s</p></div></details>' % (escape(cat), q, resaltar(a)) for cat, q, a, _ in items)
    return '<div class="acordeon"%s>%s</div>' % (" data-faq" if filtrable else "", out)


def franja():
    items = [("cruz", "Quirófano en " + SEDE_QX, "Nunca en consultorio"), ("escudo", "Póliza incluida", "Tu respaldo"), ("gota", "Bomba de dolor", "Menos dolor"), ("check", "Controles hasta el alta", "Con nuestros cirujanos")]
    return '<div class="franja ver">%s</div>' % "".join('<div>%s<span><b>%s</b>%s</span></div>' % (ico(a), b, c) for a, b, c in items)


CURVAS = ""  # las líneas curvas de fondo se quitaron: a Laura no le gustaron

SELLOS = {"mamoplastia-de-aumento": "Precio más bajo", "mastopexia-con-implantes": "2 en 1: levanta + volumen", "mastopexia-sin-implantes": "Sin implantes", "lipo": "Incluye masajes"}


MICRO = '<p class="micro"><span>Respuesta por WhatsApp</span><span>Sin compromiso</span><span>Precio cerrado</span></p>'


def miedos():
    return '<div class="filas">%s</div>' % "".join('<div class="fila ver"><span>%s</span><b>%s</b></div>' % (q, r.rstrip(".")) for q, i, r, d in MIEDOS)


def pila(c):
    return '<ul class="pila">%s<li class="suma"><span>Todo por</span><span>%s</span></li></ul>' % ("".join("<li><span>%s</span><span>Incluido</span></li>" % TITULOS[k] for k in c["incluye"]), c["precio"])


def cierre(h2="¿Damos el <em>primer paso</em>?", p=None, mensaje=None, cx=None, preguntar=False):
    if preguntar:
        boton = '<a class="btn pri" href="%s" target="_blank" rel="noopener">Escríbenos por WhatsApp →</a>' % wa(mensaje or "Hola, tengo una pregunta sobre las promos de cirugía.")
        nota = "Respuesta por WhatsApp · sin compromiso"
    else:
        boton = '<a class="btn pri" href="valoracion.html%s">Quiero mi valoración →</a>' % ("?cx=" + cx["slug"] if cx else "")
        nota = "Valoración %s · no abonable" % VALORACION
    return '<section class="banda champan cierre"><div class="cont"><div class="panel ver"><h2>%s</h2>%s<div class="fila-btn" style="justify-content:center">%s</div><p class="micro" style="justify-content:center">%s</p></div></div></section>' % (
        h2, '<div class="valor" style="margin-top:20px">%s</div>' % cx["precio"] if cx else "", boton, nota)


def tabla_comparativa():
    filas = ""
    for k in ["cirujano", "instrumentador", "quirofano", "implantes", "prenda", "poliza", "bomba", "masajes"]:
        nombre = "Prenda posquirúrgica" if k == "prenda" else INCLUIDOS[k][0]
        celdas = ""
        for c in CIRUGIAS:
            tiene = k in c["incluye"] or (k == "prenda" and "faja" in c["incluye"])
            celdas += '<td class="%s">%s</td>' % (("si", "✓") if tiene else ("nn", "—"))
        filas += "<tr><td>%s</td>%s</tr>" % (nombre, celdas)
    return '<div class="tabla-caja ver"><table><thead><tr><th></th>%s</tr></thead><tbody><tr><td>Duración</td>%s</tr>%s<tr class="total"><td>Precio total</td>%s</tr></tbody></table></div><p class="deslizar">Desliza la tabla para comparar →</p>' % (
        "".join('<th><a href="%s.html">%s</a></th>' % (c["slug"], c["corto"]) for c in CIRUGIAS),
        "".join("<td>%s</td>" % c["duracion"] for c in CIRUGIAS), filas,
        "".join("<td>%s</td>" % c["precio"] for c in CIRUGIAS))


def recibo():
    c = CIRUGIAS[0]
    otros = "".join("<li><span>%s</span><span>+ $ ?</span></li>" % TITULOS[k] for k in c["incluye"] if k not in ("cirujano", "instrumentador")) + "<li><span>Otros “imprevistos”</span><span>+ $ ?</span></li>"
    aqui = "".join("<li><span>%s</span><span>Incluido ✓</span></li>" % TITULOS[k] for k in c["incluye"])
    return """<div class="recibos">
  <div class="recibo otros ver"><h3>En otros lugares</h3><ul><li><span>“Precio de la cirugía”</span><span>$ ?</span></li>%s</ul><div class="total"><span>Total</span><b>Sorpresa</b></div><p class="nota-r">Te dan un número… y los extras aparecen después.</p></div>
  <div class="recibo aqui ver"><h3>Aquí · %s</h3><ul>%s</ul><div class="total"><span>Total</span><b>%s</b></div><p class="nota-r">Lo que ves es lo que pagas.</p></div>
</div>""" % (otros, c["nombre"], aqui, c["precio"])


# ============================================================ INICIO
sel_datos = [{"t": t, "slug": s, "nombre": CX[s]["nombre"], "precio": CX[s]["precio"], "por": p,
              "trae": [TITULOS[k] for k in ([k for k in CX[s]["incluye"] if k in ("implantes", "masajes")] + ["poliza", "bomba"])][:3], "mas": len(CX[s]["incluye"]) - 3} for t, s, p in SELECTOR]
selector = """<div class="selector grande ver" data-selector='%s'>
  <h2>¿Qué quieres <em>lograr</em>?</h2>
  <div class="chips">%s</div>
  <div class="resultado" aria-live="polite">
    <div><div class="nom"></div><p></p><div class="trae-linea"></div></div>
    <div class="lado-r"><div class="valor"></div><small>Todo incluido</small><a class="btn pri" href="#">Ver esta promo →</a></div>
  </div>
  <a class="enlace" href="cirugias.html" style="margin-top:22px">Comparar las 4 promos →</a>
</div>""" % (escape(json.dumps(sel_datos, ensure_ascii=False), quote=True),
             "".join('<button class="chip%s" type="button" data-i="%d">%s</button>' % (" on" if i == 0 else "", i, x["t"]) for i, x in enumerate(sel_datos)))

pagina("index.html", "Promos de cirugía plástica con todo incluido",
       "Mamoplastia, mastopexia y lipo con un solo precio: cirujano, quirófano en Q2, póliza, bomba de dolor y más. Agenda tu valoración.",
       """
<section class="hero limpio noon-hero">%(curvas)s<div class="cont hero-grid"><div class="hero-txt">
  <p class="ceja">Cirugía plástica · todo incluido</p>
  <h1>Tu <span class="rota" data-rota='%(rota)s'><em>cirugía</em>,</span><br>con todo incluido.</h1>
  <div class="desde"><span class="rota-et">Desde</span><b class="rota-precio">%(desde)s</b></div>
  <div class="fila-btn"><a class="btn pri" href="valoracion.html">Quiero mi valoración →</a></div>
</div><figure class="hero-foto"><img src="assets/fotos/recepcion.jpg" alt="Recepción de noon Clinic con luz natural" width="1122" height="1402"></figure></div></section>

<section class="sec pegada" id="promos"><div class="cont">
  %(selector)s
</div></section>

<section class="banda salvia frase"><div class="cont"><p class="ceja">Sin letra pequeña</p><p class="gigante" data-ilumina>%(frase)s</p></div></section>

<section class="sec pegada"><div class="cont angosto">
  %(cabm)s
  %(miedos)s
</div></section>

<section class="editorial"><div class="cont ed-grid"><figure class="ver"><img src="assets/fotos/consulta.jpg" alt="Consulta privada con una de nuestras especialistas" loading="lazy" width="1536" height="1024"></figure><div class="ver"><p class="ceja">Lo que creemos</p><p class="ed-frase">Primero entendemos. Después hablamos de posibilidades.</p><p class="bajada">La recomendación nace del criterio clínico y de lo que cada persona quiere preservar.</p></div></div></section>

<section class="banda clara"><div class="cont">
  %(cab3)s
  <div class="rejilla r3">%(pasos)s</div>
</div></section>
%(cierre)s
""" % {
           "desde": min((c["precio"] for c in CIRUGIAS), key=lambda p: int(re.sub(r"[^0-9]", "", p))),
           "rota": escape(json.dumps([
               {"p": "cirugía", "e": "Desde", "v": CX["mamoplastia-de-aumento"]["precio"]},
               {"p": "mamoplastia", "e": "Aumento ·", "v": CX["mamoplastia-de-aumento"]["precio"]},
               {"p": "mastopexia", "e": "Desde", "v": CX["mastopexia-sin-implantes"]["precio"]},
               {"p": "lipo", "e": "Con masajes ·", "v": CX["lipo"]["precio"]},
           ], ensure_ascii=False), quote=True),
           "frase": "".join("<span>%s</span> " % w for w in "El precio que ves es el precio que pagas.".split(" ")),
           "miedos": miedos(), "cabm": cab("Tus miedos, <em>resueltos</em>"),
           "curvas": CURVAS, "selector": selector,
           "cab3": cab("Tres pasos y <em>listo</em>"),
           "pasos": "".join('<div class="tarjeta ver"><span class="num">%d</span><h3>%s</h3></div>' % (n, t) for n, t in enumerate(["Valoración · " + VALORACION, "Separas tu fecha", "Tu cirugía en " + SEDE_QX], 1)),
           "cierre": cierre(),
       })

# ============================================================ CIRUGÍAS (resumen + comparador)
pagina("cirugias.html", "Las 4 promos de cirugía", "Compara las promos de mamoplastia de aumento, mastopexia con y sin implantes y lipo: precio, duración y qué incluye cada una.",
       hero_interna("Cirugías", "Cuatro promos, <em>un solo precio</em> cada una", "Compara qué trae cada cirugía y entra a la que te interesa.", ["Cirugías"]) + """
<section class="sec pegada"><div class="cont"><div class="rejilla r2 desliza">%s</div><p class="deslizar">Desliza para ver las 4 →</p></div></section>
<section class="banda clara"><div class="cont">%s%s</div></section>
<section class="banda salvia"><div class="cont">%s
  <div class="rejilla r3">
    <a class="tarjeta ver" href="mamoplastia-de-aumento.html"><span class="num">“Quiero más volumen”</span><h3>Mamoplastia de aumento</h3><p>Tus senos están en su lugar; lo que buscas es tamaño y forma.</p><span class="mas">Ver promo →</span></a>
    <a class="tarjeta ver" href="mastopexia-con-implantes.html"><span class="num">“Quiero levantar y rellenar”</span><h3>Mastopexia con implantes</h3><p>El seno cayó y además lo sientes vacío.</p><span class="mas">Ver promo →</span></a>
    <a class="tarjeta ver" href="mastopexia-sin-implantes.html"><span class="num">“Quiero levantar, sin implantes”</span><h3>Mastopexia sin implantes</h3><p>Te gusta tu volumen; solo quieres el seno firme y en su lugar.</p><span class="mas">Ver promo →</span></a>
  </div>
  <div class="aviso ver"><div><b>¿Dudas entre dos?</b> Eso se resuelve en la valoración: nuestros cirujanos te dicen cuál es la tuya.</div></div>
</div></section>
%s""" % (promos(), cab("Compara <em>lado a lado</em>", "En todas, la misma seguridad. Lo que cambia es la cirugía."), tabla_comparativa(),
         cab("¿Cuál es <em>para ti</em>?"), cierre()))

# ============================================================ UNA PÁGINA POR CIRUGÍA
for c in CIRUGIAS:
    faqs = [f for f in FAQ if c["slug"] in f[3]]
    msj = "Hola, quiero agendar mi valoración para la promo de %s." % c["nombre"]
    resumen = """<aside class="lado"><div class="resumen">
  <div class="valor"><small>Precio total, todo incluido</small>%s</div>
  <dl><div><dt>Dónde</dt><dd>Quirófano en %s</dd></div><div><dt>Incluye</dt><dd>%d cosas · <a href="#incluye" style="color:var(--acento)">ver</a></dd></div><div><dt>Primer paso</dt><dd>Valoración · %s</dd></div></dl>
  <a class="btn pri" href="%s" target="_blank" rel="noopener">Quiero esta promo →</a>
  <a class="btn" href="valoracion.html?cx=%s">Agendar valoración</a>
  <p class="nota">✓ Precio cerrado · ✓ Póliza · ✓ Bomba de dolor<br>Primer paso: valoración de %s (no abonable).</p>
  <a class="tc-link" href="terminos-y-condiciones.html"><b>Devoluciones con retención del %s.</b> Lee los términos y condiciones →</a>
</div></aside>""" % (c["precio"], SEDE_QX, len(c["incluye"]), VALORACION, wa(msj), c["slug"], VALORACION, RETENCION)
    hermanas = ""
    if c["hermanas"]:
        hermanas = '<section class="sec pegada"><div class="cont">%s<div class="rejilla r2">%s</div></div></section>' % (
            cab("También te puede <em>interesar</em>"), promos([CX[s] for s in c["hermanas"]]))
    rapidos = '<section class="banda clara delgada"><div class="cont"><div class="datos" style="margin-top:0"><div class="dato"><span>Duración</span><b>%s</b></div><div class="dato"><span>Incapacidad aprox.</span><b>%s</b></div><div class="dato"><span>Resultado final</span><b>%s</b></div></div></div></section>' % (
        c["duracion"], RAPIDOS[c["slug"]][0], RAPIDOS[c["slug"]][1])
    pagina(c["slug"] + ".html", c["nombre"] + " · " + c["precio"] + " todo incluido", c["intro"],
           hero_interna("Promo todo incluido", c["titular"], c["frase"], ['<a href="cirugias.html">Cirugías</a>', c["nombre"]]) + rapidos + """
<section class="sec pegada"><div class="cont ficha-cx">
  <div>
    <div class="bloque primero ver" id="para-ti"><h2>Es para ti <em>si…</em></h2>%s<p class="pista">%s</p></div>
    <div class="bloque ver" id="incluye"><h2>Tu precio <em>lo incluye todo</em></h2>%s<details class="plegable"><summary>¿Y qué no incluye?</summary>%s</details></div>
    <div class="bloque ver" id="cirugia"><h2>¿Cómo es <em>la cirugía</em>?</h2>%s</div>
    <div class="bloque" id="recuperacion"><h2 class="ver">Tu recuperación, <em>paso a paso</em></h2>%s<p class="pista">Tiempos de guía. Tu cirujano te da los exactos.</p></div>
    <div class="bloque ver" id="preguntas"><h2>Preguntas sobre <em>%s</em></h2>%s<div class="fila-btn"><a class="enlace" href="preguntas-frecuentes.html">Ver todas las preguntas →</a></div></div>
  </div>
  %s
</div></section>
%s
%s""" % (
               lista_libre([(x,) for x in c["para_ti"]]), c["ojo"],
               mosaico(c["incluye"]), mosaico_no(),
               puntos(PUNTOS[c["slug"]]),
               tiempo(c["recuperacion"]),
               c["nombre"].lower(), acordeon(faqs),
               resumen, "",
               cierre("Tu <em>%s</em>, todo incluido" % c["nombre"].lower(), mensaje=msj, cx=c)),
           accion=(c["nombre"], c["precio"] + " · todo incluido", "La quiero", wa(msj)))

# ============================================================ TODO INCLUIDO
todos = ["cirujano", "instrumentador", "quirofano", "poliza", "bomba", "prenda", "implantes", "masajes"]
pagina("todo-incluido.html", "Qué incluye tu precio", "Cirujano, instrumentador, quirófano en Q2, póliza de complicaciones, bomba de dolor, prenda posquirúrgica, implantes y masajes: esto trae tu promo.",
       hero_interna("Qué incluye", "El precio que ves es <em>el precio que pagas</em>", "Esto es lo que ya viene dentro de tu promo, explicado sin tecnicismos. Y también lo que no, para que no haya sorpresas.", ["Qué incluye"]) + """
<section class="sec pegada"><div class="cont dos">
  <div class="fija ver"><h2>Lo que ya <em>trae</em> tu promo</h2><p class="bajada" style="margin-top:20px">Los implantes aplican en mamoplastia de aumento y mastopexia con implantes. Los masajes postoperatorios aplican en lipo.</p></div>
  <div class="ver">%s</div>
</div></section>
<section class="banda clara"><div class="cont dos">
  <div class="fija ver"><h2>Lo que <em>no</em> incluye</h2><p class="bajada" style="margin-top:20px">Son pocas cosas, y es mejor que las sepas desde hoy para hacer bien tus cuentas.</p></div>
  <div class="ver">%s</div>
</div></section>
<section class="sec pegada"><div class="cont">%s%s</div></section>
%s""" % (mosaico(todos) + '<div style="height:clamp(50px,7vw,90px)"></div>' + cab("La diferencia está en <em>el recibo</em>") + recibo(), mosaico_no(), cab("Cada promo, <em>lado a lado</em>"), tabla_comparativa(), cierre()))

# ============================================================ SEGURIDAD
ALERTAS = [
    ("Precio sin detalle", "Si no te dicen por escrito qué incluye, lo que falta aparece después."),
    ("Sin póliza", "Operarte sin póliza de complicaciones es asumir tú sola todo el riesgo."),
    ("Fuera de un quirófano", "Una cirugía se hace en salas de cirugía. Un consultorio no lo es."),
    ("Sin exámenes", "Si nadie te pide exámenes, nadie está revisando si es seguro operarte."),
    ("Todo es “sí”", "Un buen cirujano también te dice qué no se puede o no se debe hacer."),
    ("Afán para pagar", "Una decisión así se toma con calma y con toda la información."),
]
pagina("seguridad.html", "Tu seguridad primero", "Operamos en quirófano en Q2, con póliza de complicaciones, exámenes prequirúrgicos y seguimiento. Así cuidamos tu cirugía.",
       hero_interna("Seguridad", "Un buen precio nunca debería costarte <em>tu tranquilidad</em>", "Esto es lo que hacemos en cada cirugía, sin excepciones. Un precio de promo no cambia ninguna de estas reglas.", ["Seguridad"]) + """
<section class="sec pegada"><div class="cont">%s</div></section>
<section class="banda clara"><div class="cont dos">
  <div class="fija ver"><span class="etiqueta">No negociables</span><h2>Cómo cuidamos <em>tu cirugía</em></h2></div>
  <div class="ver">%s</div>
</div></section>
<section class="sec pegada"><div class="cont">
  %s
  <div class="rejilla r3">%s</div>
</div></section>
<section class="banda salvia"><div class="cont dos"><div class="fija ver"><h2>Preguntas sobre <em>seguridad</em></h2></div><div class="ver">%s</div></div></section>
%s""" % (franja(),
         lista_libre([
             ("Operamos solo en quirófano", "Todas las cirugías se hacen en las salas de cirugía de %s. Nunca en consultorios ni en sitios adaptados." % SEDE_QX),
             ("Nuestros cirujanos te valoran primero", "Nadie se opera sin una valoración médica presencial y honesta."),
             ("Exámenes antes de operar", "Si tus exámenes no están en regla, la cirugía se aplaza. Sin excepciones."),
             ("Póliza de complicaciones incluida", "Toda cirugía tiene riesgos. La póliza es tu respaldo si algo se presenta."),
             ("Dolor bajo control", "La bomba de dolor te acompaña en los días más incómodos."),
             ("Controles hasta el alta", "No te soltamos después de la cirugía: te vemos hasta que todo esté bien."),
             ("Sabemos decir que no", "Si operarte no es seguro para ti, te lo decimos, aunque eso signifique no hacer la cirugía."),
         ]),
         cab("Señales de alerta al elegir <em>dónde operarte</em>", "Aplican para cualquier lugar, incluido el nuestro. Pregunta siempre."),
         "".join('<div class="tarjeta ver"><span class="num">Alerta %02d</span><h3>%s</h3><p>%s</p></div>' % (i, t, d) for i, (t, d) in enumerate(ALERTAS, 1)),
         acordeon([f for f in FAQ if f[0] == "Seguridad"]), cierre()))

# ============================================================ TU PROCESO
pagina("tu-proceso.html", "Tu proceso paso a paso", "De la cita de valoración al resultado final: así es el camino de tu cirugía.",
       hero_interna("Tu proceso", "De la primera cita al resultado, <em>paso a paso</em>", "Saber qué viene quita la mitad de los nervios. Este es el camino completo.", ["Tu proceso"]) + """
<section class="sec pegada"><div class="cont angosto">%s
  <div class="aviso ver"><div><b>Sobre la valoración:</b> cuesta %s, no es abonable al tratamiento y su valor no se devuelve.</div></div>
</div></section>
<section class="banda clara"><div class="cont dos">
  <div class="fija ver"><span class="etiqueta">Lista de chequeo</span><h2>Qué llevar el día de <em>tu cirugía</em></h2></div>
  <div class="ver">%s</div>
</div></section>
<section class="sec pegada"><div class="cont dos"><div class="fija ver"><h2>Preguntas sobre la <em>recuperación</em></h2></div><div class="ver">%s</div></div></section>
%s""" % (tiempo(PROCESO), VALORACION, lista_libre([(x,) for x in QUE_LLEVAR]),
         acordeon([f for f in FAQ if f[0] == "Dolor y recuperación"][:6]), cierre()))

# ============================================================ FORMAS DE PAGO
pagina("formas-de-pago.html", "Formas de pago", "Cómo se paga tu cirugía: cita de valoración, abono para separar fecha, saldo y política de devoluciones.",
       hero_interna("Pagos", "Cuentas claras <em>desde el primer día</em>", "Así funciona el pago de tu cirugía, con las condiciones dichas de frente.", ["Formas de pago"]) + """
<section class="sec pegada"><div class="cont">
  <div class="rejilla r3">
    <div class="tarjeta ver"><span class="num">01</span><h3>Cita de valoración</h3><div class="valor" style="font-size:40px">%s</div><p>Es el primer paso. No es abonable al tratamiento y su valor no se devuelve.</p></div>
    <div class="tarjeta ver"><span class="num">02</span><h3>Abono para tu fecha</h3><p>Con un abono reservas tu fecha de cirugía en %s. Si desistes, se te devuelve con una retención del %s por gastos administrativos.</p></div>
    <div class="tarjeta ver"><span class="num">03</span><h3>Saldo</h3><p>El saldo se paga antes de la cirugía. El precio de tu promo se respeta desde que abonas.</p></div>
  </div>
  <div class="ver" style="margin-top:28px">%s</div>
</div></section>
<section class="banda clara"><div class="cont dos"><div class="fija ver"><h2>Preguntas sobre <em>pagos</em></h2></div><div class="ver">%s</div></div></section>
%s""" % (VALORACION, SEDE_QX, RETENCION, tc_aviso(),
         acordeon([f for f in FAQ if f[0] == "Pagos"] + [FAQ[2], FAQ[5]]),
         cierre("¿Quieres conocer los <em>medios de pago</em>?", preguntar=True, mensaje="Hola, quiero conocer los medios de pago de las promos de cirugía.")))

# ============================================================ OTRA CIUDAD
pagina("otra-ciudad.html", "Vienes de otra ciudad o país", "Cómo operarte con nosotros si vives en otra ciudad o en el exterior: días de estadía, controles y viaje de regreso.",
       hero_interna("Pacientes que viajan", "Vienes de lejos. <em>Te lo ponemos fácil</em>", "Muchas pacientes viajan para operarse. Así organizamos tu viaje para que valoración, cirugía y controles te rindan.", ["Vienes de otra ciudad"]) + """
<section class="sec pegada"><div class="cont">%s</div></section>
<section class="banda clara"><div class="cont dos">
  <div class="fija ver"><span class="etiqueta">Guía de estadía</span><h2>¿Cuántos días <em>me quedo</em>?</h2><p class="bajada" style="margin-top:20px">Son tiempos de referencia. El regreso lo autoriza tu cirujano en el control.</p></div>
  <div class="ver">%s</div>
</div></section>
<section class="sec pegada"><div class="cont dos">
  <div class="fija ver"><h2>Recomendaciones para <em>tu viaje</em></h2></div>
  <div class="ver">%s</div>
</div></section>
<section class="banda salvia"><div class="cont dos"><div class="fija ver"><h2>Preguntas de quienes <em>viajan</em></h2></div><div class="ver">%s</div></div></section>
%s""" % (carril([
    ("Escríbenos antes de viajar", "Cuéntanos qué cirugía te interesa y dejamos agendada tu valoración para cuando llegues."),
    ("Valoración y exámenes", "Nuestros cirujanos te valoran en persona y te ordenan los exámenes prequirúrgicos."),
    ("Cirugía en " + SEDE_QX, "Con todo lo de tu promo incluido."),
    ("Recuperación y controles", "Te quedas en la ciudad los días que tu cirujano indique."),
    ("Regreso a casa", "Viajas cuando tu cirujano lo autorice, con tus indicaciones claras."),
]),
         lista_libre([("Mamoplastia de aumento", "Entre 1 y 2 semanas."), ("Mastopexia con o sin implantes", "Alrededor de 2 semanas."), ("Lipo", "Entre 2 y 3 semanas, para cumplir tus primeros masajes y controles.")]),
         lista_libre([("Viaja acompañada", "Necesitas un adulto contigo el día de la cirugía y los primeros días."), ("Hospédate cerca", "Entre más cerca de %s y de tus controles, más cómoda tu recuperación." % SEDE_QX),
                      ("Compra tiquetes flexibles", "La fecha de regreso depende de tu evolución, no del calendario."), ("Trae tus exámenes", "Si ya tienes exámenes recientes, tráelos a la valoración.")]),
         acordeon([f for f in FAQ if f[0] == "Vengo de lejos"]),
         cierre("¿Organizamos <em>tu viaje</em>?", preguntar=True, mensaje="Hola, vivo en otra ciudad y quiero información para operarme con ustedes.")))

# ============================================================ PREGUNTAS FRECUENTES
filtros = '<button class="chip on" data-cat="todas">Todas</button>' + "".join('<button class="chip" data-cat="%s">%s</button>' % (escape(x), x) for x in CATS)
pagina("preguntas-frecuentes.html", "Preguntas frecuentes", "Todas las respuestas sobre precios, seguridad, dolor, recuperación, implantes, requisitos y pagos de tu cirugía.",
       hero_interna("Preguntas frecuentes", "Todas tus dudas, <em>resueltas</em>", "%d respuestas claras. Busca por palabra o filtra por tema." % len(FAQ), ["Preguntas frecuentes"]) + """
<section class="sec pegada"><div class="cont angosto">
  <input class="buscador" type="search" placeholder="Busca: dolor, implantes, abono, incapacidad…" aria-label="Buscar en las preguntas">
  <div class="chips filtros">%s</div>
  %s
  <p class="vacio" hidden>No encontramos esa pregunta. Escríbenos por WhatsApp y te respondemos.</p>
</div></section>
%s""" % (filtros, acordeon(FAQ, filtrable=True), cierre("¿No encontraste <em>tu pregunta</em>?", preguntar=True)))

# ============================================================ NOSOTROS
pagina("nosotros.html", "Nosotros", "Nuestros cirujanos, nuestra forma de trabajar y por qué la seguridad va primero.",
       hero_interna("Nosotros", "Estética sí, pero <em>nunca a costa de tu salud</em>", "Trabajamos con una idea simple: verte mejor no debería ponerte en riesgo.", ["Nosotros"]) + """
<section class="sec pegada"><div class="cont dos">
  <div class="fija ver"><span class="etiqueta">Quién te opera</span><h2>Nuestros <em>cirujanos</em></h2></div>
  <div class="prosa ver"><p>Tu cirugía está en manos de nuestros cirujanos plásticos. Los conoces desde la valoración: te examinan, te escuchan y te explican qué se puede lograr y qué no, antes de que tomes cualquier decisión.</p><p>Trabajan con un equipo completo —instrumentador y personal de salas de cirugía— en los quirófanos de %s.</p></div>
</div></section>
<section class="editorial"><div class="cont ed-grid"><figure class="ver"><img src="assets/fotos/espera.jpg" alt="Sala de espera de noon Clinic" loading="lazy" width="1672" height="941"></figure><div class="ver"><p class="ceja">Quiet confidence</p><p class="ed-frase">Estética con criterio.</p><p class="bajada">Médicos especializados. Decisiones personales. Escuchamos antes de proponer, explicamos sin dramatizar y decidimos junto a ti.</p></div></div></section>
<section class="sec pegada"><div class="cont">%s</div></section>
<section class="banda clara"><div class="cont dos">
  <div class="fija ver"><h2>Lo que puedes <em>esperar</em> de nosotros</h2></div>
  <div class="ver">%s</div>
</div></section>
%s""" % (SEDE_QX, franja(), lista_libre([("Te decimos el precio completo desde el principio",), ("Te explicamos los riesgos, no solo los beneficios",), ("Si no eres candidata, te lo decimos",), ("Te acompañamos hasta el alta",)]), cierre()))

# ============================================================ VALORACIÓN
opciones = "".join('<option data-slug="%s">%s</option>' % (c["slug"], c["nombre"]) for c in CIRUGIAS)
pagina("valoracion.html", "Agenda tu cita de valoración", "Todo empieza con tu cita de valoración con nuestros cirujanos. Agéndala por WhatsApp.",
       hero_interna("Primer paso", "Todo empieza con <em>tu cita de valoración</em>", "Nuestros cirujanos te examinan, resuelven tus dudas y te dicen qué cirugía es para ti.", ["Valoración"]) + """
<section class="sec pegada"><div class="cont dos">
  <div class="ver">
    <div class="valor"><small>Valor de la cita</small>%(val)s</div>
    <div style="margin-top:28px">%(lista)s</div>
    <div style="margin-top:24px">%(tc)s</div>
  </div>
  <form class="tarjeta ver" id="form-valoracion" data-wa="%(wa)s">
    <div class="progreso"><div class="on">1 · Escríbenos<br>(30 segundos)</div><div>2 · Tu valoración</div><div>3 · Tu fecha de cirugía</div></div>
    <h2 style="font-size:30px">Empieza por aquí</h2>
    <p style="margin-bottom:14px">Tres datos y se abre WhatsApp con tu mensaje listo.</p>
    <div class="campo"><label for="nombre">Tu nombre</label><input id="nombre" name="nombre" required autocomplete="given-name"></div>
    <div class="campo"><label for="cirugia">Cirugía que te interesa</label><select id="cirugia" name="cirugia">%(op)s<option>Aún no estoy segura</option></select></div>
    <div class="campo"><label for="ciudad">Ciudad donde vives</label><input id="ciudad" name="ciudad" required autocomplete="address-level2"></div>
    <button class="btn pri" type="submit">Quiero mi valoración →</button>
    <p class="legal grande">Al escribirnos aceptas nuestros <a href="terminos-y-condiciones.html">términos y condiciones</a>.</p>
    <p class="legal">Este formulario no guarda tus datos: solo arma tu mensaje.</p>
  </form>
</div></section>
""" % {"val": VALORACION, "wa": WHATSAPP, "op": opciones,
       "tc": tc_aviso("La cita no se devuelve ni se abona", "El valor de la cita (%s) no se descuenta de la cirugía y no se devuelve en ningún caso." % VALORACION),
       "lista": lista_libre([("Consulta con nuestros cirujanos", "Examen, medidas y un plan pensado para tu cuerpo."), ("Respuestas honestas", "Qué se puede lograr, qué no, y si eres candidata."), ("Orden de exámenes", "Sales con lo que necesitas para dar el siguiente paso.")])})

# ============================================================ TÉRMINOS
def _contenido(ps):
    return "".join("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in p) if isinstance(p, list) else "<p>%s</p>" % p for p in ps)

bloques = "".join('<section id="t%d" class="termino%s"><h3>%s</h3>%s</section>' % (i + 1, " clave" if clave else "", t, _contenido(ps)) for i, (t, ps, clave) in enumerate(TERMINOS))
indice = "".join('<a href="#t%d"%s>%s</a>' % (i + 1, ' class="clave"' if clave else "", t) for i, (t, ps, clave) in enumerate(TERMINOS))
pagina("terminos-y-condiciones.html", "Términos y condiciones", "Condiciones de la cita de valoración, abonos, política de devoluciones, reprogramación y promociones de cirugía.",
       hero_interna("Legal", "Términos y <em>condiciones</em>", "Léelos completos antes de agendar o pagar. Están escritos para que se entiendan.", ["Términos y condiciones"]) + """
<section class="sec pegada"><div class="cont angosto">
  <div class="tc-resumen ver">
    <span class="tc-ceja">Lo más importante</span>
    <h2>Devoluciones y fecha límite</h2>
    <ul>%s</ul>
    <a class="btn tc" href="#t4">Ver la política completa ↓</a>
  </div>
  <nav class="tc-indice ver" aria-label="Contenido de los términos">%s</nav>
  <div class="prosa terminos">%s</div>
</div></section>
""" % ("".join("<li>%s</li>" % x for x in RESUMEN_TC), indice, bloques))

print("\nListo. %d preguntas frecuentes, %d cirugías." % (len(FAQ), len(CIRUGIAS)))
