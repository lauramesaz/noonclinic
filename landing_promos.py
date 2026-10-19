# -*- coding: utf-8 -*-
# noon Clinic · LANDING DE PROMOS DE FIN DE AÑO · cirugía plástica (noon.clinic/promos/)
# Una sola landing para TODAS las cirugías: cada pauta cae "pre abierta" en su cirugía (noon.clinic/promos/lipo,
# /promos/mamoplastia-de-aumento, …) y desde ahí la paciente puede mirar las demás sin salir de la página.
# Pedido de Laura (19-oct-2026): promos de fin de año, cirujano plástico reconstructivo con ReTHUS, los mejores
# quirófanos de la ciudad, la misión (precios bajos para combatir la ilegalidad) y los precios de promo.
# Estilo de landing de venta (ver criolipolisis): ALTO CONTRASTE negro / blanco / VINOTINTO, títulos gruesos con
# palabras resaltadas, botones llenos, barra fija en celular. Sin menú. Todo a WhatsApp.
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
MSJ = "Hola, vengo de la promo de fin de año y quiero una cita de valoración para "
MSJ_GENERAL = "Hola, vengo de la promo de fin de año y quiero información de las cirugías"

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
        "nombre": "Lipo y lipotransferencia", "foto": "c:abdomen-bn",
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
FOTO = {"abdominoplastia": "mini-abdominoplastia", "mini-abdominoplastia": "abdominoplastia"}  # para no repetir la foto de lipo
H1 = {"lifting-facial": "lifting facial", "recambio-de-implantes": "recambio de implantes", "cirugia-post-bariatrica": "cirugía tras bajar de peso"}

# ---------------------------------------------------------------- misión
MISION = [
    ("medico", "Cirujano plástico certificado", "Especialista en cirugía plástica, estética y reconstructiva, con registro en ReTHUS."),
    ("cruz", "En quirófano, nunca en un consultorio", "Te operamos en los mejores quirófanos de la ciudad."),
    ("escudo", "Póliza de complicaciones", "Si algo pasa, no lo enfrentas sola ni con tu bolsillo."),
]
REVISA = [
    "Busca a tu cirujano en ReTHUS: debe aparecer como especialista en cirugía plástica.",
    "Pregunta dónde te van a operar: tiene que ser una sala de cirugía habilitada.",
    "Pide por escrito qué incluye el precio y si trae póliza de complicaciones.",
]
CIFRAS = [
    ("1", "precio cerrado, sin sumas de última hora"),
    ("100%", "de las cirugías en quirófano"),
    ("Póliza", "de complicaciones en tu cirugía"),
    ("15 ene", "fecha límite para operarte con la promo"),
]
PASOS = [
    ("Escríbenos", "Por WhatsApp te contamos la promo y agendamos tu valoración."),
    ("Valoración con el cirujano", "Te examina, resuelve tus dudas y define tu plan. Cuesta " + VALORACION + "."),
    ("Exámenes y tu fecha", "Con los exámenes prequirúrgicos al día, separas tu fecha con un abono."),
    ("Tu cirugía", "En quirófano, con todo lo que incluye tu promo, antes del " + VIGENCIA + "."),
]
PREGUNTAS = [
    ("¿El precio de la promo es el precio final?", "Sí. Es un paquete cerrado: incluye los honorarios del cirujano, el instrumentador, el quirófano, la póliza de complicaciones, la bomba de dolor y tu prenda posquirúrgica; además los implantes o los masajes cuando tu cirugía los lleva. Si en la valoración se define algo adicional, te lo cotizamos por escrito antes de que decidas."),
    ("¿Qué no está incluido?", "La cita de valoración (" + VALORACION + "), los exámenes prequirúrgicos, los medicamentos para tomar en casa y, si vienes de otra ciudad, tu viaje y hospedaje."),
    ("¿Por qué es más barato que en otros lugares?", "Porque es nuestra misión: que el precio no empuje a nadie a operarse con quien no es cirujano plástico o en un lugar que no es un quirófano. Es el mismo cirujano, el mismo quirófano y los mismos estándares; lo que cambia es que te damos un solo precio con todo adentro."),
    ("¿Quién me opera?", "El Dr. Fernando Ruiz, cirujano plástico, estético y reconstructivo, con registro en ReTHUS. Te conoce desde la valoración y te acompaña en tus controles."),
    ("¿Dónde me operan?", "En los mejores quirófanos de la ciudad, en salas de cirugía habilitadas. Nunca operamos en consultorios."),
    ("¿Hasta cuándo es la promo?", "Los precios de fin de año aplican para cirugías realizadas antes del " + VIGENCIA + ". Escríbenos y te confirmamos las fechas de quirófano disponibles."),
    ("¿Y las cirugías que no muestran precio?", "Te las cotizamos en tu valoración, con todo por escrito y antes de que tomes cualquier decisión."),
    ("¿Me va a doler?", "Vas a sentir molestia los primeros días, y para eso está la bomba de dolor: entrega analgesia de forma continua en los días más incómodos. Va incluida en las promos."),
    ("¿La valoración tiene costo?", "Sí, " + VALORACION + ". Es una consulta médica completa con el cirujano: te examina y te dice qué cirugía es para ti, o si no eres candidata. No se abona a la cirugía y su valor no se devuelve."),
    ("Si abono y me arrepiento, ¿me devuelven el dinero?", "Sí, con una retención del 20% de lo abonado por gastos administrativos. El detalle está en los términos y condiciones."),
]

# ---------------------------------------------------------------- íconos (trazo fino, toman el color del texto)
ICONOS = {
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "abajo": '<path d="M12 5v14M6 13l6 6 6-6"/>',
    "brillo": '<path d="M12 3.5l1.9 5.6 5.6 1.9-5.6 1.9L12 18.5l-1.9-5.6L4.5 11l5.6-1.9Z"/>',
    "medico": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4.5 20.5c.8-3.6 3.8-6 7.5-6s6.7 2.4 7.5 6"/><path d="M16.5 17.5v3M15 19h3"/>',
    "cruz": '<rect x="3.5" y="3.5" width="17" height="17" rx="4"/><path d="M12 8v8M8 12h8"/>',
    "escudo": '<path d="M12 3.5l7 2.6v5.4c0 4.3-2.9 7.7-7 9-4.1-1.3-7-4.7-7-9V6.1Z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
    "lupa": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
    "reloj": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "mas": '<path d="M12 5v14M5 12h14"/>',
}


def ico(nombre, clase="ico"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (clase, ICONOS[nombre])


def _items(b):
    """Arma la lista completa de cirugías: las del catálogo de noon + las promos (con precio)."""
    cat = {c["slug"]: c for c in b.CIRUGIAS_NOON}
    out = []
    for zona, slugs in ORDEN.items():
        for s in slugs:
            p = PROMOS.get(s)
            c = cat.get(s, {})
            d = c.get("datos", ("", "", "", ""))
            it = {
                "slug": s, "zona": zona,
                "nombre": (p or {}).get("nombre") or c.get("nombre"),
                "corto": (p or {}).get("corto") or c.get("corto"),
                "ideal": (p or {}).get("ideal") or c.get("ideal", [])[:3],
                "datos": list((p or {}).get("datos") or (d[1], d[2], d[3])),
                "precio": (p or {}).get("precio", ""),
                "desde": bool((p or {}).get("desde")),
                "incluye": [INC[k] for k in (p or {}).get("incluye", [])],
                "h1": (p or {}).get("h1") or H1.get(s) or c.get("nombre", "").lower(),
            }
            f = (p or {}).get("foto") or FOTO.get(s, s)
            it["foto"] = "/assets/criolipolisis/%s.jpg" % f[2:] if f.startswith("c:") else "/assets/capacitacion/%s.jpg" % f
            out.append(it)
    return out


def _wa(b, nombre=None):
    texto = MSJ + nombre.lower() if nombre else MSJ_GENERAL
    return "https://wa.me/" + b.WHATSAPP + "?text=" + quote(texto)


def _precio_html(it):
    """Bloque de precio de la portada."""
    if it and it["precio"]:
        return ('<p class="pr-precio-et">Precio de fin de año</p><p class="pr-precio-n">%s<b>%s</b></p>'
                '<p class="pr-precio-s">Todo incluido · precio cerrado</p>') % ('<span>Desde</span>' if it["desde"] else "", it["precio"])
    if it:
        return ('<p class="pr-precio-et">Precio</p><p class="pr-precio-n pr-precio-txt"><b>Según tu caso</b></p>'
                '<p class="pr-precio-s">Te lo damos en tu valoración, por escrito</p>')
    return ('<p class="pr-precio-et">Precios de fin de año</p><p class="pr-precio-n"><span>Desde</span><b>$10.900.000</b></p>'
            '<p class="pr-precio-s">Todo incluido · precio cerrado</p>')


def _incluye_html(it):
    lista = it["incluye"] if it and it["incluye"] else ["Cirujano plástico", "Quirófano", "Póliza de complicaciones"]
    return "".join("<li>%s%s</li>" % (ico("check"), escape(x)) for x in lista)


def _titulo(it):
    if not it:
        return "Promos de fin de año en <mark>cirugía plástica</mark>."
    if it["precio"]:
        return "Tu <mark>%s</mark> a precio de fin de año." % escape(it["h1"])
    return "Tu <mark>%s</mark>, en manos de un cirujano plástico." % escape(it["h1"])


def _fila(b, it, abierta):
    precio = ('<span class="pr-cx-p">%s%s</span>' % ("<small>Desde</small>" if it["desde"] else "", it["precio"])) if it["precio"] \
        else '<span class="pr-cx-p pr-cx-p0">Cotízala</span>'
    datos = "".join('<li><span>%s</span><b>%s</b></li>' % (t, escape(v)) for t, v in zip(["Anestesia", "Incapacidad", "Resultado final"], it["datos"]) if v)
    ideal = "".join("<li>%s%s</li>" % (ico("check"), escape(x)) for x in it["ideal"])
    if it["incluye"]:
        incluye = '<p class="pr-mini">Incluye</p><ul class="pr-chips">%s</ul>' % "".join("<li>%s</li>" % escape(x) for x in it["incluye"])
    else:
        incluye = '<p class="pr-nota-cx">El valor se define en tu valoración, con todo por escrito antes de que decidas.</p>'
    return '''<details class="pr-cx%(cls)s" name="cx" data-slug="%(slug)s" data-zona="%(zona)s"%(open)s>
  <summary><span class="pr-cx-n"><b>%(nombre)s</b><span>%(corto)s</span></span>%(precio)s<span class="pr-mas" aria-hidden="true"></span></summary>
  <div class="pr-cx-in">
    <img src="%(foto)s" alt="" width="1200" height="900" loading="lazy">
    <div class="pr-cx-txt">
      <p class="pr-mini">Es para ti si</p><ul class="pr-ideal">%(ideal)s</ul>
      <ul class="pr-datos">%(datos)s</ul>
      %(incluye)s
      <div class="pr-acciones"><a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a></div>
    </div>
  </div>
</details>''' % {"cls": " pr-cx-promo" if it["precio"] else "", "slug": it["slug"], "zona": it["zona"], "open": " open" if abierta else "",
                 "nombre": escape(it["nombre"]), "corto": escape(it["corto"]), "precio": precio, "foto": it["foto"], "ideal": ideal,
                 "datos": datos, "incluye": incluye, "wa": _wa(b, it["nombre"]), "flecha": ico("flecha", "ico-f")}


def _pagina(b, items, actual):
    """actual = slug abierto (o None para la página general /promos/)."""
    it = next((x for x in items if x["slug"] == actual), None)
    zona = it["zona"] if it else "senos"
    doc = [e for e in b.ESPECIALISTAS if e["area"] == "cirugia"][0]
    promos = [x for x in items if x["precio"]]

    if it:
        titulo = "%s en Medellín · Promo de fin de año" % it["nombre"]
        desc = "%s en Medellín con cirujano plástico certificado, en quirófano y con póliza de complicaciones.%s" % (
            it["nombre"], (" Precio de fin de año %s%s, todo incluido." % ("desde " if it["desde"] else "", it["precio"])) if it["precio"] else "")
    else:
        titulo = "Promos de fin de año en cirugía plástica · Medellín"
        desc = "Precios de fin de año en cirugía plástica en Medellín: aumento de senos, mastopexia y lipo con todo incluido, cirujano plástico certificado y póliza de complicaciones."

    tabs = "".join('<button type="button" class="pr-tab%s" data-zona="%s" aria-pressed="%s">%s <span>%d</span></button>' % (
        " on" if k == zona else "", k, "true" if k == zona else "false", n, len(ORDEN[k])) for k, n in ZONAS)
    filas = "".join(_fila(b, x, x["slug"] == actual) for x in items)
    tarjetas = "".join('''<button type="button" class="pr-tarj" data-ir="%s"><span>%s</span><b>%s%s</b>%s</button>''' % (
        x["slug"], escape(x["nombre"]), "<small>Desde</small>" if x["desde"] else "", x["precio"], ico("flecha", "ico-f")) for x in promos)
    mision = "".join('<li class="pr-rev"><span class="pr-mi-i">%s</span><h3>%s</h3><p>%s</p></li>' % (ico(i), t, d) for i, t, d in MISION)
    revisa = "".join("<li>%s<span>%s</span></li>" % (ico("check"), t) for t in REVISA)
    cifras = "".join('<li class="pr-rev"><b>%s</b><span>%s</span></li>' % (n, t) for n, t in CIFRAS)
    pasos = "".join('<li class="pr-rev"><span class="pr-pn">%d</span><h3>%s</h3><p>%s</p></li>' % (i, t, d) for i, (t, d) in enumerate(PASOS, 1))
    preguntas = "".join('<details class="pr-preg pr-rev"><summary>%s<span class="pr-mas" aria-hidden="true"></span></summary><div class="pr-resp"><p>%s</p></div></details>' % (p, r) for p, r in PREGUNTAS)
    datos = json.dumps({"items": {x["slug"]: x for x in items}, "titulo": {x["slug"]: _titulo(x) for x in items},
                        "precio": {x["slug"]: _precio_html(x) for x in items}, "general": {"titulo": _titulo(None), "precio": _precio_html(None)},
                        "wa": b.WHATSAPP, "msj": MSJ, "msjGeneral": MSJ_GENERAL}, ensure_ascii=False).replace("</", "<\\/")

    foto = it["foto"] if it else "/assets/equipo/%s" % doc["foto"]
    flota2 = ("<b>Póliza y bomba de dolor</b> incluidas" if it["precio"] else "<b>Póliza de complicaciones</b> en tu cirugía") if it else "<b>Cirujano reconstructivo</b> con ReTHUS"
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
<meta name="theme-color" content="#0b0b0b">
<link rel="icon" href="/assets/favicon.png">
<script>document.documentElement.className="js"</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="%(foto)s">
<link rel="stylesheet" href="/assets/promos.css?v=%(v)s">
</head>
<body class="pr%(general)s" data-cx="%(actual)s">
<header class="pr-cab">
  <a class="pr-logo" href="/" aria-label="noon Clinic, inicio"><img src="/assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295"></a>
  <p class="pr-cinta">%(ico_brillo)s Promos de fin de año</p>
  <a class="pr-btn pr-btn-sm" href="%(wa)s" target="_blank" rel="noopener" data-wa>Agendar %(flecha)s</a>
</header>
<main>

<!-- 1 · PORTADA: la cirugía del anuncio (o la promo general), precio, botón y sellos -->
<section class="pr-portada">
  <div class="pr-in pr-portada-in">
    <div class="pr-portada-txt">
      <p class="pr-insignia">%(ico_brillo)s Promo de fin de año · Medellín</p>
      <h1 data-h="titulo">%(h1)s</h1>
      <div class="pr-precio" data-h="precio">%(precio)s</div>
      <ul class="pr-incluye" data-h="incluye">%(incluye)s</ul>
      <div class="pr-tarjetas" data-h="tarjetas">%(tarjetas)s</div>
      <div class="pr-acciones">
        <a class="pr-btn pr-btn-xl" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
        <a class="pr-link pr-link-claro" href="#cirugias">Ver todas las cirugías y precios %(ico_abajo)s</a>
      </div>
    </div>
    <figure class="pr-portada-foto">
      <img data-h="foto" src="%(foto)s" alt="" width="1200" height="900">
      <div class="pr-flota pr-flota-1"><span>Cirugías hasta el</span><b>15 de enero</b></div>
      <div class="pr-flota pr-flota-2" data-h="flota">%(ico_escudo)s<span>%(flota2)s</span></div>
    </figure>
  </div>
  <ul class="pr-in pr-sellos">
    <li>%(ico_medico)s<span><b>Cirujano plástico reconstructivo</b> con ReTHUS</span></li>
    <li>%(ico_cruz)s<span><b>Los mejores quirófanos</b> de la ciudad</span></li>
    <li>%(ico_escudo)s<span><b>Póliza de complicaciones</b> incluida</span></li>
  </ul>
</section>

<!-- 2 · TODAS LAS CIRUGÍAS: la del anuncio llega abierta; las demás, a un toque -->
<section class="pr-sec pr-claro" id="cirugias">
  <div class="pr-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja">Todas las cirugías</p>
      <h2>Mira las demás <mark>cirugías</mark>.</h2>
      <p class="pr-sub">Toca cualquiera para ver qué incluye y para quién es. Las que están en promo muestran su precio de fin de año; las demás te las cotizamos en tu valoración.</p></header>
    <div class="pr-tabs" role="group" aria-label="Zonas">%(tabs)s</div>
    <div class="pr-lista" data-zona="%(zona)s">%(filas)s</div>
  </div>
</section>

<!-- 3 · MISIÓN: precios bajos para combatir la ilegalidad -->
<section class="pr-sec pr-negro" id="mision">
  <div class="pr-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja">Nuestra misión</p>
      <h2>Precios bajos para <mark>combatir la ilegalidad</mark>.</h2>
      <p class="pr-sub">Mucha gente termina operándose con quien no es cirujano plástico, o en un lugar que no es un quirófano, porque es lo que puede pagar. Bajamos los precios para que operarte bien no sea un lujo.</p></header>
    <ul class="pr-mision">%(mision)s</ul>
    <div class="pr-revisa pr-rev">
      <div><p class="pr-ceja">Antes de operarte en cualquier lugar</p><h3>Revisa estas tres cosas.</h3></div>
      <ul>%(revisa)s</ul>
      <a class="pr-link pr-link-claro" href="%(rethus)s" target="_blank" rel="noopener">%(ico_lupa)s Buscar un cirujano en ReTHUS</a>
    </div>
  </div>
</section>

<!-- 4 · CIFRAS (franja vino) -->
<section class="pr-cifras"><ul class="pr-in">%(cifras)s</ul></section>

<!-- 5 · QUIÉN Y DÓNDE: el cirujano y los quirófanos -->
<section class="pr-sec pr-claro" id="cirujano">
  <div class="pr-in pr-medico">
    <figure class="pr-med-foto pr-rev"><img src="/assets/equipo/%(doc_foto)s" alt="%(doc)s, cirujano plástico de noon Clinic" width="1120" height="1400" loading="lazy"><figcaption><b>%(doc)s</b><span>Cirujano plástico, estético y reconstructivo</span></figcaption></figure>
    <div class="pr-rev">
      <p class="pr-ceja">Quién te opera y dónde</p>
      <h2>Un cirujano plástico <mark>reconstructivo</mark>, con ReTHUS.</h2>
      <p class="pr-sub">El %(doc)s es especialista en cirugía plástica, estética y reconstructiva. Te valora, te opera y te acompaña en tus controles.</p>
      <ul class="pr-razones">
        <li>%(ico_medico)s<div><b>Registro en ReTHUS</b><span>El registro oficial del Ministerio de Salud. <a href="%(rethus)s" target="_blank" rel="noopener">Verifícalo tú misma</a>.</span></div></li>
        <li>%(ico_cruz)s<div><b>Los mejores quirófanos de la ciudad</b><span>Salas de cirugía habilitadas. Nunca operamos en consultorios.</span></div></li>
        <li>%(ico_reloj)s<div><b>Exámenes antes de operarte</b><span>Si no es seguro para ti, no te operamos. Primero tu salud.</span></div></li>
      </ul>
      <a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
    </div>
  </div>
</section>

<!-- 6 · CÓMO FUNCIONA -->
<section class="pr-sec pr-negro" id="como">
  <div class="pr-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja">Cómo funciona</p><h2>De tu mensaje a tu cirugía, en <mark>4 pasos</mark>.</h2></header>
    <ol class="pr-pasos">%(pasos)s</ol>
    <div class="pr-centro pr-rev"><a class="pr-btn pr-btn-xl" href="%(wa)s" target="_blank" rel="noopener" data-wa>Empezar por WhatsApp %(flecha)s</a></div>
  </div>
</section>

<!-- 7 · PREGUNTAS -->
<section class="pr-sec pr-gris" id="preguntas">
  <div class="pr-in pr-faq-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja">Antes de que preguntes</p><h2>Lo que todas <mark>preguntan</mark>.</h2></header>
    <div class="pr-faq">%(preguntas)s</div>
  </div>
</section>

<!-- 8 · CIERRE -->
<section class="pr-cierre" id="agendar">
  <div class="pr-in pr-cierre-in pr-rev">
    <p class="pr-ceja">%(ico_brillo)s Promos de fin de año</p>
    <h2>Cierra el año con la cirugía que <mark>llevas tiempo</mark> pensando.</h2>
    <p class="pr-sub">Escríbenos, te contamos la promo y agendamos tu valoración con el %(doc)s.</p>
    <a class="pr-btn pr-btn-xl pr-btn-blanco" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración %(flecha)s</a>
    <p class="pr-nota">Precios de fin de año para cirugías realizadas antes del %(vigencia)s. La valoración (%(valoracion)s) no se abona a la cirugía y su valor no se devuelve. <a href="/terminos-y-condiciones">Términos y condiciones</a></p>
  </div>
</section>

</main>
<footer class="pr-pie">
  <div class="pr-in pr-pie-in">
    <a class="pr-logo" href="/"><img src="/assets/logo-noon.png" alt="noon Clinic" width="900" height="295" loading="lazy"></a>
    <nav><a href="/">Conoce noon</a><a href="/cirugia-plastica">Cirugía plástica</a><a href="/especialistas">Especialistas</a><a href="/terminos-y-condiciones">Términos</a><a href="%(wa)s" target="_blank" rel="noopener" data-wa>WhatsApp %(tel)s</a></nav>
  </div>
  <p class="pr-in pr-legal">La información de esta página es orientativa y no reemplaza una consulta médica. Toda cirugía tiene riesgos y los resultados varían de una persona a otra. Fotos ilustrativas: Unsplash y Pexels. © noon Clinic</p>
</footer>
<div class="pr-barra" aria-hidden="true">
  <div class="pr-barra-txt"><b data-h="barra-n">%(barra_n)s</b><span data-h="barra-p">%(barra_p)s</span></div>
  <a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>Quiero mi valoración</a>
</div>
<script type="application/json" id="pr-datos">%(datos)s</script>
<script src="/assets/medicion-ads.js?v=%(v)s" defer></script>
<script src="/assets/promos.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"titulo": escape(titulo), "desc": escape(desc), "dominio": b.DOMINIO, "foto": foto, "clarity": clarity, "v": b.V,
       "general": "" if it else " pr-general", "actual": actual or "", "wa": wa_actual, "flecha": ico("flecha", "ico-f"),
       "ico_brillo": ico("brillo"), "ico_abajo": ico("abajo", "ico-f"), "ico_escudo": ico("escudo"), "ico_medico": ico("medico"),
       "ico_cruz": ico("cruz"), "ico_lupa": ico("lupa"), "ico_reloj": ico("reloj"),
       "h1": _titulo(it), "precio": _precio_html(it), "incluye": _incluye_html(it), "tarjetas": tarjetas, "flota2": flota2,
       "tabs": tabs, "zona": zona, "filas": filas, "mision": mision, "revisa": revisa, "cifras": cifras, "pasos": pasos,
       "preguntas": preguntas, "rethus": RETHUS, "doc": doc["nombre"], "doc_foto": doc["foto"], "vigencia": VIGENCIA,
       "valoracion": VALORACION, "tel": b.TELEFONO, "barra_n": barra_n, "barra_p": barra_p, "datos": datos}


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
