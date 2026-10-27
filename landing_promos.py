# -*- coding: utf-8 -*-
# noon Clinic · LANDING DE PROMOS DE FIN DE AÑO · cirugía plástica (noon.clinic/promos/)
# Una sola landing para TODAS las cirugías: cada pauta cae "pre abierta" en su cirugía (noon.clinic/promos/lipo,
# /promos/mamoplastia-de-aumento, …) y desde ahí la paciente puede mirar las demás sin salir de la página.
# Pedido de Laura (19-oct-2026): promos de fin de año, cirujano plástico reconstructivo con ReTHUS, los mejores
# quirófanos de la ciudad, la misión (precios bajos para combatir la ilegalidad) y los precios de promo.
# DISEÑO "A · Blanco y arco" (elegido por Laura el 19-oct entre 3 propuestas; la v1 negra/vino le pareció horrible):
# estilo Apple (blanco, mucho aire, letra grande y apretada con la 2.ª línea en gris cálido), toques marfil, foto en ARCO,
# un solo contraste = botón NEGRO, punto champaña como detalle de fin de año. Sin menú. Todo a WhatsApp.
# OJO: aquí van SOLO precios de venta. Nunca costos internos, honorarios ni márgenes.
# Fuera del sitemap y con noindex: es la página de la pauta (la web pública sigue sin precios).
# build.py llama a generar() al final.
import json, os
from html import escape
from urllib.parse import quote

CARPETA = "promos"
VIGENCIA = "15 de enero de 2027"   # = FECHA_LIMITE de datos.py (términos): la cirugía debe hacerse antes de esta fecha
VALORACION = "$200.000"
RETHUS = "https://web.sispro.gov.co/THS/Cliente/ConsultasPublicas/ConsultaPublicaDeTHxIdentificacion.aspx"
from datos import MENSAJE_WA as MSJ  # el mismo mensaje de toda la web, en todas las cirugías (decisión de Laura, 19-oct-2026)
# EXCEPCIÓN (Laura, 27-oct-2026): quien llega del anuncio de Google escribe "vengo de Google (<cirugía abierta>)" para que el
# equipo cuente los chats de la pauta. La cirugía = su "h1" (lipo, aumento de senos…); sin cirugía elegida = TEMA_GENERAL.
import wa_google
MSJ_GOOGLE = "Hola, vengo de Google (%s) y quiero información de la promo"
TEMA_GENERAL = "cirugía plástica"

ZONAS = [("senos", "Senos"), ("cuerpo", "Cuerpo"), ("rostro", "Rostro"), ("combinadas", "Combinadas e íntima")]

# ---------------------------------------------------------------- lo que trae cada promo (etiquetas cortas)
INC = {
    "cirujano": "Honorarios del cirujano",
    "instrumentador": "Instrumentador",
    "quirofano": "Quirófano",
    "implantes": "Implantes",
    "brasier": "Brasier posquirúrgico",
    "faja": "Faja posquirúrgica",
    "poliza": "Póliza de complicaciones",
    "bomba": "Bomba de dolor",
    "masajes": "Masajes postoperatorios",
    "preconsulta": "Preconsulta",
}

# versión corta para la línea "Todo incluido: …" (se escanea, no se lee). En la portada se omite el instrumentador.
INC_CORTO = {"cirujano": "cirujano", "instrumentador": "instrumentador", "quirofano": "quirófano", "implantes": "implantes",
             "brasier": "brasier", "faja": "faja", "poliza": "póliza", "bomba": "bomba de dolor", "masajes": "masajes",
             "preconsulta": "preconsulta"}

# ---------------------------------------------------------------- PROMOS CON PRECIO (precios de venta de la capacitación / piezas)
# slug: datos de la promo. "h1" = cómo se nombra en el título ("Tu ___ a precio de fin de año").
PROMOS = {
    "mamoplastia-de-aumento": {"precio": "$10.900.000", "desde": False, "h1": "aumento de senos",
        "incluye": ["cirujano", "instrumentador", "quirofano", "implantes", "brasier", "poliza", "bomba", "preconsulta"],
        "corto": "Más volumen y mejor forma, con los implantes dentro del precio.",
        "ideal": ["Sientes tus senos pequeños para tu cuerpo.", "Perdiste volumen tras un embarazo, la lactancia o una baja de peso.", "Tus senos están en su lugar: lo que buscas es volumen."],
        "datos": ("General", "Aprox. 1 semana", "3 a 6 meses")},
    "mastopexia-con-implantes": {"precio": "$17.900.000", "desde": True, "h1": "mastopexia con implantes",
        "nombre": "Mastopexia con implantes", "foto": "mastopexia-con-implantes",
        "incluye": ["cirujano", "instrumentador", "quirofano", "implantes", "brasier", "poliza", "bomba"],
        "corto": "Levanta, reafirma y devuelve el volumen en una sola cirugía.",
        "ideal": ["Tus senos cayeron tras embarazos, lactancia o cambios de peso.", "Los sientes “vacíos” en la parte de arriba.", "Quieres levantar y también ganar volumen."],
        "datos": ("General", "2 a 3 semanas", "Aprox. 6 meses")},
    "mastopexia-sin-implantes": {"precio": "$15.900.000", "desde": True, "h1": "mastopexia sin implantes",
        "nombre": "Mastopexia sin implantes", "foto": "mastopexia-sin-implantes",
        "incluye": ["cirujano", "instrumentador", "quirofano", "brasier", "poliza", "bomba"],
        "corto": "Levanta y reafirma con tu propio tejido, sin implantes.",
        "ideal": ["Tus senos cayeron, pero te gusta tu volumen.", "No quieres implantes.", "Buscas un seno firme y en su lugar, con resultado natural."],
        "datos": ("General", "2 a 3 semanas", "Aprox. 6 meses")},
    "lipo": {"precio": "$18.900.000", "desde": True, "h1": "lipo",
        "nombre": "Lipo y lipotransferencia", "foto": "abdominoplastia",
        "incluye": ["cirujano", "instrumentador", "quirofano", "faja", "poliza", "bomba", "masajes"],
        "corto": "Retira la grasa que no se va con nada y define tu contorno. Con los masajes de la recuperación.",
        "ideal": ["Tienes grasa localizada que no cede con dieta ni ejercicio.", "Estás en un peso estable, cerca de tu peso saludable.", "Quieres definir cintura, abdomen, espalda o glúteos."],
        "datos": ("General", "2 a 3 semanas", "3 a 6 meses")},
}

# ---------------------------------------------------------------- orden de la lista (por zona; las de precio primero)
ORDEN = {
    "senos": ["mamoplastia-de-aumento", "mastopexia-con-implantes", "mastopexia-sin-implantes", "mamoplastia-de-reduccion", "recambio-de-implantes", "ginecomastia"],
    "cuerpo": ["lipo", "abdominoplastia", "mini-abdominoplastia", "braquioplastia", "lifting-de-muslos", "cirugia-post-bariatrica"],
    "rostro": ["rinoplastia", "blefaroplastia", "lifting-facial", "bichectomia", "mentoplastia", "otoplastia", "lipopapada"],
    "combinadas": ["mommy-makeover", "labioplastia"],
}
FOTO = {"abdominoplastia": "mini-abdominoplastia", "mini-abdominoplastia": "liposuccion"}  # para no repetir la foto de lipo
H1 = {"lifting-facial": "lifting facial", "recambio-de-implantes": "recambio de implantes", "cirugia-post-bariatrica": "cirugía tras bajar de peso"}

# ---------------------------------------------------------------- misión
MISION = [
    ("medico", "Cirujano plástico certificado", "Especialista en cirugía plástica, estética y reconstructiva, con registro en ReTHUS."),
    ("cruz", "En quirófano, nunca en consultorio", "Te operamos en los mejores quirófanos de la ciudad."),
    ("escudo", "Póliza de complicaciones", "Si algo pasa, no lo enfrentas sola ni con tu bolsillo."),
]
REVISA = [
    "Busca a tu cirujano en ReTHUS.",
    "Pregunta dónde te van a operar.",
    "Pide por escrito qué incluye el precio.",
]
PASOS = [
    ("Escríbenos", "Te contamos la promo por WhatsApp."),
    ("Valoración", "Con el cirujano. Cuesta " + VALORACION + "."),
    ("Exámenes y fecha", "Separas tu fecha con un abono."),
    ("Tu cirugía", "Antes del 15 de enero."),
]
PREGUNTAS = [
    ("¿El precio de la promo es el precio final?", "Sí. Es un paquete cerrado: incluye los honorarios del cirujano, el instrumentador, el quirófano, la póliza de complicaciones, la bomba de dolor y tu prenda posquirúrgica; además los implantes o los masajes cuando tu cirugía los lleva. Si en la valoración se define algo adicional, te lo cotizamos por escrito antes de que decidas."),
    ("¿Qué no está incluido?", "La cita de valoración (" + VALORACION + "), los exámenes prequirúrgicos, los medicamentos para tomar en casa y, si vienes de otra ciudad, tu viaje y hospedaje."),
    ("¿Por qué es más barato que en otros lugares?", "Porque es nuestra misión: que el precio no empuje a nadie a operarse con quien no es cirujano plástico o en un lugar que no es un quirófano. Es el mismo cirujano, el mismo quirófano y los mismos estándares; lo que cambia es que te damos un solo precio con todo adentro."),
    ("¿Dónde me operan?", "En los mejores quirófanos de la ciudad, en salas de cirugía habilitadas. Nunca operamos en consultorios."),
    ("¿Hasta cuándo es la promo?", "Los precios de fin de año aplican para cirugías realizadas antes del " + VIGENCIA + ". Escríbenos y te confirmamos las fechas de quirófano disponibles."),
    ("¿Me va a doler?", "Vas a sentir molestia los primeros días, y para eso está la bomba de dolor: entrega analgesia de forma continua en los días más incómodos. Va incluida en las promos."),
    ("¿Y las cirugías que no muestran precio?", "Te las cotizamos en tu valoración, con todo por escrito y antes de que tomes cualquier decisión."),
    ("¿La valoración tiene costo?", "Sí, " + VALORACION + ". Es una consulta médica completa con el cirujano: te examina y te dice qué cirugía es para ti, o si no eres candidata. No se abona a la cirugía y su valor no se devuelve."),
    ("Si abono y me arrepiento, ¿me devuelven el dinero?", "Sí, con una retención del 20% de lo abonado por gastos administrativos. El detalle está en los términos y condiciones."),
]
# atajos de la portada (las más buscadas); "Ver las 21" lleva a la lista completa
ATAJOS = ["lipo", "mamoplastia-de-aumento", "mastopexia-con-implantes", "abdominoplastia", "rinoplastia"]
CORTOS = {"lipo": "Lipo", "mamoplastia-de-aumento": "Aumento de senos", "mastopexia-con-implantes": "Mastopexia", "abdominoplastia": "Abdomen", "rinoplastia": "Rinoplastia"}

# ---------------------------------------------------------------- íconos (trazo fino, toman el color del texto)
ICONOS = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "medico": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4.5 20.5c.8-3.6 3.8-6 7.5-6s6.7 2.4 7.5 6"/><path d="M16.5 17.5v3M15 19h3"/>',
    "cruz": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><path d="M12 8v8M8 12h8"/>',
    "escudo": '<path d="M12 3.5l7 2.6v5.4c0 4.3-2.9 7.7-7 9-4.1-1.3-7-4.7-7-9V6.1Z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
    "lupa": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
    "reloj": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
}


def ico(nombre, clase="ico"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (clase, ICONOS[nombre])


def _items(b):
    """Arma la lista completa de cirugías: las del catálogo de noon + las promos (con precio)."""
    cat = {c["slug"]: c for c in b.CIRUGIAS_NOON}
    out = []
    for zona, slugs in ORDEN.items():
        for s in slugs:
            p = PROMOS.get(s) or {}
            c = cat.get(s, {})
            d = c.get("datos", ("", "", "", ""))
            it = {
                "slug": s, "zona": zona,
                "nombre": p.get("nombre") or c.get("nombre"),
                "corto": p.get("corto") or c.get("corto"),
                "ideal": p.get("ideal") or c.get("ideal", [])[:3],
                "datos": list(p.get("datos") or (d[1], d[2], d[3])),
                "precio": p.get("precio", ""),
                "desde": bool(p.get("desde")),
                "incluye": [INC[k] for k in p.get("incluye", [])],
                "inc": p.get("incluye", []),
                "h1": p.get("h1") or H1.get(s) or c.get("nombre", "").lower(),
                "foto": "/assets/capacitacion/%s.jpg" % (p.get("foto") or FOTO.get(s, s)),
            }
            out.append(it)
    return out


def _wa(b, nombre=None):
    return "https://wa.me/" + b.WHATSAPP + "?text=" + quote(MSJ)


def _lista_texto(xs):
    return ", ".join(xs[:-1]) + " y " + xs[-1] if len(xs) > 1 else "".join(xs)


# ---------------------------------------------------------------- piezas de la portada (también van al JSON para el cambio en vivo)
def _titulo(it):
    if not it:
        return "Promos de fin de año<br><span>en cirugía plástica.</span>"
    if it["precio"]:
        return "Tu %s,<br><span>a precio de fin de año.</span>" % escape(it["h1"])
    return "Tu %s,<br><span>con un cirujano plástico certificado.</span>" % escape(it["h1"])


def _precio(it):
    if not it:
        return '<small>Desde</small><b>$10.900.000</b>'
    if it["precio"]:
        return ('<small>Desde</small>' if it["desde"] else "") + '<b>%s</b>' % it["precio"]
    return '<b class="pr-sin">Precio según tu caso</b>'


def _incluye(it, portada=False):
    if not it:
        return "Todo incluido: cirujano, quirófano, póliza y bomba de dolor."
    if it["inc"]:
        claves = [k for k in it["inc"] if not (portada and k == "instrumentador")]
        return "Todo incluido: %s." % escape(_lista_texto([INC_CORTO[k] for k in claves]))
    return "En quirófano y con póliza de complicaciones. El valor te lo damos por escrito en tu valoración."


def _fila(b, it, abierta):
    if it["precio"]:
        precio = '<span class="pr-cx-p">%s%s</span>' % ("<small>Desde</small>" if it["desde"] else "", it["precio"])
    else:
        precio = '<span class="pr-cx-p pr-cx-p0">Cotízala</span>'
    datos = "".join('<li><span>%s</span>%s</li>' % (t, escape(v)) for t, v in zip(["Anestesia", "Incapacidad", "Resultado"], it["datos"]) if v)
    ideal = "".join("<li>%s%s</li>" % (ico("check"), escape(x)) for x in it["ideal"])
    return '''<details class="pr-cx" name="cx" data-slug="%(slug)s" data-zona="%(zona)s"%(open)s>
  <summary><span class="pr-cx-n"><b>%(nombre)s</b><span>%(corto)s</span></span>%(precio)s<span class="pr-mas" aria-hidden="true"></span></summary>
  <div class="pr-cx-in">
    <img src="%(foto)s" alt="" width="1200" height="900" loading="lazy">
    <div>
      <p class="pr-mini">Es para ti si</p><ul class="pr-ideal">%(ideal)s</ul>
      <ul class="pr-datos">%(datos)s</ul>
      <p class="pr-cx-inc">%(incluye)s</p>
      <a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
    </div>
  </div>
</details>''' % {"slug": it["slug"], "zona": it["zona"], "open": " open" if abierta else "", "nombre": escape(it["nombre"]),
                 "corto": escape(it["corto"]), "precio": precio, "foto": it["foto"], "ideal": ideal, "datos": datos,
                 "incluye": _incluye(it), "wa": _wa(b, it["nombre"]), "flecha": ico("flecha", "ico-f")}


def _pagina(b, items, actual):
    """actual = slug abierto (o None para la página general /promos/)."""
    it = next((x for x in items if x["slug"] == actual), None)
    zona = it["zona"] if it else "senos"
    doc = [e for e in b.ESPECIALISTAS if e["area"] == "cirugia"][0]
    doc_foto = "/assets/equipo/" + doc["foto"]

    if it:
        titulo = "%s en Medellín · Promo de fin de año" % it["nombre"]
        desc = "%s en Medellín con cirujano plástico certificado, en quirófano y con póliza de complicaciones.%s" % (
            it["nombre"], (" Precio de fin de año %s%s, todo incluido." % ("desde " if it["desde"] else "", it["precio"])) if it["precio"] else "")
    else:
        titulo = "Promos de fin de año en cirugía plástica · Medellín"
        desc = "Precios de fin de año en cirugía plástica en Medellín: aumento de senos, mastopexia y lipo con todo incluido, cirujano plástico certificado y póliza de complicaciones."

    atajos = "".join('<button type="button" class="pr-pill%s" data-ir="%s">%s</button>' % (" on" if s == actual else "", s, CORTOS[s]) for s in ATAJOS)
    tabs = "".join('<button type="button" class="pr-tab%s" data-zona="%s" aria-pressed="%s">%s</button>' % (
        " on" if k == zona else "", k, "true" if k == zona else "false", n) for k, n in ZONAS)
    filas = "".join(_fila(b, x, x["slug"] == actual) for x in items)
    mision = "".join('<li class="pr-rev"><span class="pr-ic">%s</span><h3>%s</h3><p>%s</p></li>' % (ico(i), t, d) for i, t, d in MISION)
    revisa = "".join("<li><span>%d</span>%s</li>" % (i, t) for i, t in enumerate(REVISA, 1))
    pasos = "".join('<li class="pr-rev"><span class="pr-pn">%d</span><h3>%s</h3><p>%s</p></li>' % (i, t, d) for i, (t, d) in enumerate(PASOS, 1))
    preguntas = "".join('<details class="pr-preg pr-rev"><summary>%s<span class="pr-mas" aria-hidden="true"></span></summary><p>%s</p></details>' % (p, r) for p, r in PREGUNTAS)
    datos = json.dumps({"items": {x["slug"]: x for x in items}, "titulo": {x["slug"]: _titulo(x) for x in items},
                        "precio": {x["slug"]: _precio(x) for x in items}, "incluye": {x["slug"]: _incluye(x, True) for x in items},
                        "wa": b.WHATSAPP, "msj": MSJ}, ensure_ascii=False).replace("</", "<\\/")

    foto = it["foto"] if it else doc_foto
    wa_actual = _wa(b, it["nombre"]) if it else _wa(b)
    barra_n = escape(it["nombre"]) if it else "Promos de fin de año"
    barra_p = (("Desde " if it["desde"] else "") + it["precio"] if it["precio"] else "Precio en tu valoración") if it else "Desde $10.900.000"

    clarity = ('<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;'
               't.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");'
               'clarity("set","idioma","es");clarity("set","pagina","promos");clarity("set","tipo","landing");clarity("set","cx",%s);</script>') % (
        b.CLARITY_ID, json.dumps(actual or "general"))

    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
%(medicion)s
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s · noon Clinic</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="noon Clinic">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(dominio)s%(foto)s">
<meta property="og:locale" content="es_CO">
%(clarity)s
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/assets/favicon.png">
<script>document.documentElement.className="js"</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="%(foto)s">
<link rel="stylesheet" href="/assets/promos.css?v=%(v)s">
</head>
<body class="pr%(general)s" data-cx="%(actual)s">
<header class="pr-cab">
  <a class="pr-logo" href="/" aria-label="noon Clinic, inicio"><img src="/assets/logo-noon.png" alt="noon Clinic" width="900" height="295"></a>
  <a class="pr-btn-borde" href="%(wa)s" target="_blank" rel="noopener" data-wa>Agendar</a>
</header>
<main>

<!-- 1 · PORTADA: la cirugía del anuncio, precio, botón y foto en arco -->
<section class="pr-portada">
  <div class="pr-portada-in">
    <div class="pr-portada-txt">
      <p class="pr-ceja"><i></i>Promos de fin de año · Medellín</p>
      <h1 data-h="titulo">%(h1)s</h1>
      <p class="pr-precio" data-h="precio">%(precio)s</p>
      <p class="pr-inc" data-h="incluye">%(incluye)s</p>
      <a class="pr-btn pr-btn-xl" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
      <p class="pr-ya"><i></i>Te respondemos en minutos por WhatsApp</p>
    </div>
    <figure class="pr-arco">
      <img data-h="foto" src="%(foto)s" alt="" width="1200" height="900">
      <div class="pr-doc"><img src="%(doc_foto)s" alt="" width="1120" height="1400"><div>%(doc)s<span>Cirujano plástico reconstructivo · ReTHUS</span></div></div>
    </figure>
  </div>
  <div class="pr-atajos">
    <p>¿Buscas otra cirugía?</p>
    <div class="pr-pills">%(atajos)s<a class="pr-pill pr-pill-todas" href="#cirugias">Ver las %(total)d</a></div>
  </div>
</section>

<!-- 2 · TODAS LAS CIRUGÍAS: la del anuncio llega abierta -->
<section class="pr-sec" id="cirugias">
  <div class="pr-panel pr-marfil">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>Todas las cirugías</p>
      <h2>Elige la tuya,<br><span>mira qué incluye.</span></h2></header>
    <div class="pr-tabs" role="group" aria-label="Zonas">%(tabs)s</div>
    <div class="pr-lista" data-zona="%(zona)s">%(filas)s</div>
  </div>
</section>

<!-- 3 · MISIÓN -->
<section class="pr-sec pr-mision-sec" id="mision">
  <header class="pr-cabeza pr-centro pr-rev"><p class="pr-ceja"><i></i>Nuestra misión</p>
    <h2>Precios bajos para<br><span>combatir la ilegalidad.</span></h2>
    <p class="pr-sub">Mucha gente se opera con quien no es cirujano plástico, o en un lugar que no es un quirófano, porque es lo que puede pagar. Bajamos los precios para que operarte bien no sea un lujo.</p></header>
  <ul class="pr-mision">%(mision)s</ul>
  <div class="pr-revisa pr-rev">
    <h3>Antes de operarte en cualquier lugar:</h3>
    <ol>%(revisa)s</ol>
    <a class="pr-link" href="%(rethus)s" target="_blank" rel="noopener">%(ico_lupa)s Buscar un cirujano en ReTHUS</a>
  </div>
</section>

<!-- 4 · EL CIRUJANO -->
<section class="pr-sec" id="cirujano">
  <div class="pr-panel pr-gris pr-medico">
    <figure class="pr-arco pr-arco-doc pr-rev"><img src="%(doc_foto)s" alt="%(doc)s, cirujano plástico de noon Clinic" width="1120" height="1400" loading="lazy"></figure>
    <div class="pr-rev">
      <p class="pr-ceja"><i></i>Quién te opera</p>
      <h2>%(doc)s,<br><span>cirujano plástico reconstructivo.</span></h2>
      <ul class="pr-razones">
        <li>%(ico_medico)s<div><b>Registro en ReTHUS</b><span>El registro oficial del Ministerio de Salud. <a href="%(rethus)s" target="_blank" rel="noopener">Verifícalo tú misma</a></span></div></li>
        <li>%(ico_cruz)s<div><b>Los mejores quirófanos de la ciudad</b><span>Salas de cirugía habilitadas, nunca un consultorio.</span></div></li>
        <li>%(ico_reloj)s<div><b>Te ve antes, durante y después</b><span>Te valora, te opera y te acompaña en tus controles.</span></div></li>
      </ul>
      <a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
    </div>
  </div>
</section>

<!-- 5 · CÓMO FUNCIONA -->
<section class="pr-sec" id="como">
  <header class="pr-cabeza pr-centro pr-rev"><p class="pr-ceja"><i></i>Cómo funciona</p><h2>Cuatro pasos,<br><span>sin enredos.</span></h2></header>
  <ol class="pr-pasos">%(pasos)s</ol>
</section>

<!-- 6 · PREGUNTAS -->
<section class="pr-sec" id="preguntas">
  <div class="pr-faq-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>Preguntas</p><h2>Lo que todas<br><span>preguntan.</span></h2></header>
    <div class="pr-faq">%(preguntas)s</div>
  </div>
</section>

<!-- 7 · CIERRE -->
<section class="pr-sec pr-cierre" id="agendar">
  <div class="pr-panel pr-marfil pr-cierre-in pr-rev">
    <p class="pr-ceja"><i></i>Promos de fin de año</p>
    <h2>Cierra el año con la cirugía<br><span>que llevas tiempo pensando.</span></h2>
    <a class="pr-btn pr-btn-xl" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
    <p class="pr-nota">Precios para cirugías realizadas antes del %(vigencia)s. La valoración (%(valoracion)s) no se abona a la cirugía y su valor no se devuelve. <a href="/terminos-y-condiciones">Términos y condiciones</a></p>
  </div>
</section>

</main>
<footer class="pr-pie">
  <a class="pr-logo" href="/"><img src="/assets/logo-noon.png" alt="noon Clinic" width="900" height="295" loading="lazy"></a>
  <nav><a href="/">Conoce noon</a><a href="/especialistas">Especialistas</a><a href="/terminos-y-condiciones">Términos</a><a href="%(wa)s" target="_blank" rel="noopener" data-wa>WhatsApp %(tel)s</a></nav>
  <p class="pr-legal">La información de esta página es orientativa y no reemplaza una consulta médica. Toda cirugía tiene riesgos y los resultados varían de una persona a otra. Fotos ilustrativas: Unsplash. © noon Clinic</p>
</footer>
<div class="pr-barra" aria-hidden="true">
  <div class="pr-barra-txt"><b data-h="barra-n">%(barra_n)s</b><span data-h="barra-p">%(barra_p)s</span></div>
  <a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración</a>
</div>
<script type="application/json" id="pr-datos">%(datos)s</script>
%(google)s
<script src="/assets/medicion-ads.js?v=%(v)s" defer></script>
<script src="/assets/promos.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"medicion": b.HEAD_MEDICION, "titulo": escape(titulo), "desc": escape(desc), "dominio": b.DOMINIO, "foto": foto, "clarity": clarity, "v": b.V,
       "general": "" if it else " pr-general", "actual": actual or "", "wa": wa_actual, "flecha": ico("flecha", "ico-f"),
       "ico_lupa": ico("lupa"), "ico_medico": ico("medico"), "ico_cruz": ico("cruz"), "ico_reloj": ico("reloj"),
       "h1": _titulo(it), "precio": _precio(it), "incluye": _incluye(it, True), "atajos": atajos, "total": len(items),
       "tabs": tabs, "zona": zona, "filas": filas, "mision": mision, "revisa": revisa, "pasos": pasos, "preguntas": preguntas,
       "rethus": RETHUS, "doc": doc["nombre"], "doc_foto": doc_foto, "vigencia": VIGENCIA, "valoracion": VALORACION,
       "tel": b.TELEFONO, "barra_n": barra_n, "barra_p": barra_p, "datos": datos,
       "google": wa_google.script({"": MSJ_GOOGLE % TEMA_GENERAL, **{x["slug"]: MSJ_GOOGLE % x["h1"] for x in items}})}


def generar(b):
    """b = módulo build (WHATSAPP, TELEFONO, DOMINIO, CLARITY_ID, ESPECIALISTAS, CIRUGIAS_NOON, V, AQUI).
    Crea promos/index.html (general) y promos/<cirugía>.html (cada una llega abierta en su cirugía)."""
    items = _items(b)
    carpeta = os.path.join(b.AQUI, CARPETA)
    os.makedirs(carpeta, exist_ok=True)
    for actual in [None] + [x["slug"] for x in items]:
        with open(os.path.join(carpeta, (actual or "index") + ".html"), "w", encoding="utf-8") as f:
            f.write(_pagina(b, items, actual))
    return len(items) + 1
