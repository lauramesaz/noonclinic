# -*- coding: utf-8 -*-
# noon Clinic · LANDING DE VENTA: Criolipólisis (noon.clinic/criolipolisis)
# Enfocada en lo que hace la criolipólisis (el resultado en el cuerpo), no en la máquina.
# v5 (19-oct): la v4 negra/vino ya no le gustó a Laura ("no me gusta ni 5"). De 3 primeras pantallas (_propuestas-crio/)
# eligió la B "Frío y vidrio": fondo perla con un aura de luz fría, tarjetas de vidrio, frase clave en degradé hielo → vino
# y botones vinotinto. Foto nueva a color hecha en Higgsfield (assets/criolipolisis/portada*.webp).
# Se mantienen el test "¿eres candidata?", el dibujo de capas, las zonas (ahora en pestañas), el paso a paso, la médica y las preguntas.
# Sin menú (no distrae), sin precios (regla de la web pública), todo a WhatsApp.
# build.py llama a generar() al final.
import json, os
from html import escape
from urllib.parse import quote

ARCHIVO = "criolipolisis.html"
TITULO = "Criolipólisis en Medellín sin cirugía"  # + " · noon Clinic" = 51 caracteres (Google corta en ~60)
DESCRIPCION = ("Criolipólisis en Medellín con valoración médica: el frío controlado elimina la grasa localizada de abdomen, "
               "flancos, papada, brazos y muslos. Sin cirugía, sin agujas y sin incapacidad.")

# Línea de inmediatez junto al botón: dato real confirmado por Laura el 19-oct ("respondemos en minutos en horario de atención").
INMEDIATO = "Te respondemos en minutos por WhatsApp, en horario de atención."

MSJ = "Hola, vengo de la web y quiero una cita de criolipólisis"  # mismo inicio que el resto de la web (MENSAJE_WA)

# ---------------------------------------------------------------- zonas (la grasa "terca")
# (clave, nombre, cómo lo vive la paciente, qué se busca)
ZONAS = [
    ("abdomen", "Abdomen", "La parte baja del abdomen, la que se marca con el pantalón o el vestido.",
     "Un abdomen más plano y una silueta más limpia de perfil."),
    ("flancos", "Cintura y flancos", "Los “gorditos” de los lados, que se salen por encima del pantalón.",
     "Una cintura más definida, de frente y de espalda."),
    ("espalda", "Espalda", "El pliegue que aparece con el brasier o justo debajo de él.",
     "Una espalda más lisa, que se nota con ropa ajustada."),
    ("papada", "Papada", "La grasa debajo del mentón que borra el ángulo del cuello.",
     "Un perfil más definido entre la mandíbula y el cuello."),
    ("brazos", "Brazos", "La parte de atrás del brazo, la que se mueve al saludar.",
     "Brazos más estilizados, con menos volumen atrás."),
    ("muslos", "Muslos", "La cara interna, donde se rozan, o la externa (cartucheras).",
     "Muslos con un contorno más armónico."),
    ("rodillas", "Rodillas", "La grasa que se acumula justo encima de la rodilla.",
     "Piernas más definidas cuando usas falda o short."),
]

CORTO_Z = {"flancos": "Cintura"}  # nombre corto en las pestañas

BOTON_Z = {"abdomen": "mi abdomen", "flancos": "mi cintura", "espalda": "mi espalda", "papada": "mi papada",
           "brazos": "mis brazos", "muslos": "mis muslos", "rodillas": "mis rodillas"}

# ---------------------------------------------------------------- qué hace (animación por etapas)
ETAPAS = [
    ("Antes", "La grasa localizada vive en la capa que está debajo de la piel. Esa es la que forma el “rollito”."),
    ("Durante la sesión", "El frío controlado llega a la grasa de la zona. La piel y el músculo quedan protegidos."),
    ("Semanas 1 a 3", "Las células de grasa que se enfriaron se apagan y tu cuerpo empieza a retirarlas, de forma natural."),
    ("Semanas 8 a 12", "Quedan menos células de grasa en la zona: la capa es más delgada y se nota en tu silueta."),
]

PASOS = [
    ("Enfría solo la grasa", "Las células de grasa se afectan con el frío antes que la piel o el músculo. Por eso se pueden enfriar sin lastimar lo demás."),
    ("La célula de grasa se apaga", "No se encoge ni se “derrite”: deja de funcionar y entra en un proceso natural de eliminación."),
    ("Tu cuerpo la elimina", "En las semanas siguientes tu organismo la retira solo, como hace con cualquier célula que ya cumplió su ciclo."),
]

# ---------------------------------------------------------------- ¿te pasa esto? (dolores)
DOLORES = [
    "Haces dieta y ejercicio, y ese rollito sigue ahí.",
    "La ropa ajustada te marca los gorditos de los lados.",
    "Quieres un cambio, pero no quieres cirugía ni incapacidad.",
    "Te da miedo pagar por un tratamiento que no te sirva.",
]

# ---------------------------------------------------------------- cifras (franja vino)
CIFRAS = [
    ("1 a 3", "sesiones por zona, según tu caso"),
    ("0", "días de incapacidad: sigues con tu día"),
    ("Semana 3", "empiezas a notar el cambio"),
    ("Semana 12", "ves el resultado completo"),
]

# ---------------------------------------------------------------- paso a paso
CAMINO = [
    ("Valoración médica", "La médica revisa la zona, tu historia y si eres candidata. Sales con tu plan por escrito."),
    ("Tu sesión", "El aplicador va sobre la zona y enfría la grasa mientras descansas. Al terminar, sigues con tu día."),
    ("Las semanas siguientes", "Tu cuerpo elimina las células de grasa. Desde la semana 3 lo notas en la ropa."),
    ("Control", "Entre la semana 8 y la 12 medimos el resultado contigo y, si hace falta, planeamos otra sesión."),
]

# ---------------------------------------------------------------- lo que vas a vivir
VIVIR = [
    ("El día de tu sesión", "Sientes frío intenso los primeros minutos; después la zona se adormece. Puedes leer, trabajar o descansar. Al terminar, sigues con tu día."),
    ("Primeros días", "La zona puede estar roja, sensible o adormecida. Es normal y pasa sola."),
    ("Semana 3", "Empiezas a notar el cambio, sobre todo en cómo te queda la ropa."),
    ("Semanas 8 a 12", "Ves el resultado completo. Te revisamos y, si hace falta, planeamos otra sesión."),
]

# ---------------------------------------------------------------- ¿es para ti?
SI = [
    "Estás cerca de tu peso ideal, pero hay una zona que no cambia.",
    "Puedes pellizcar esa grasa con los dedos.",
    "Quieres un cambio sin cirugía, sin agujas y sin incapacidad.",
    "Tienes paciencia para ver el resultado en semanas, no en días.",
]
NO = [
    ("Buscas bajar de peso.", 'Para eso está el <a href="manejo-medico-del-peso">manejo médico del peso</a>.'),
    ("Lo que te molesta es la piel suelta.", 'La firmeza se trabaja con <a href="radiofrecuencia">radiofrecuencia</a>.'),
    ("Quieres un cambio grande en una sola vez.", 'Puede que lo tuyo sea una <a href="liposuccion">liposucción</a>.'),
    ("Estás embarazada o lactando.", "Lo dejamos para más adelante."),
]

# ---------------------------------------------------------------- preguntas
PREGUNTAS = [
    ("¿Duele?", "Los primeros minutos se siente frío intenso y algo de presión; luego la zona se adormece. La mayoría de las personas lo describe como tolerable. Al retirar el frío puede haber un hormigueo que pasa en pocos minutos."),
    ("¿Cuántas sesiones necesito?", "Depende de la zona y de cuánta grasa tengas ahí. Muchas personas necesitan entre 1 y 3 sesiones por zona, separadas de 6 a 8 semanas. En tu valoración te decimos cuántas y por qué."),
    ("¿Cuándo veo el resultado?", "Desde la tercera semana empiezas a notar el cambio, y el resultado completo se ve entre la semana 8 y la 12, cuando tu cuerpo termina de eliminar las células."),
    ("¿La grasa vuelve?", "Las células de grasa que se eliminan no regresan. Las que quedan sí pueden crecer si subes de peso, por eso el resultado se cuida con tus hábitos."),
    ("¿Sirve para bajar de peso?", "No. La criolipólisis moldea zonas puntuales; no cambia tu peso en la báscula. Si tu meta es bajar de peso, te orientamos con el manejo médico del peso."),
    ("¿Tiene riesgos?", "Lo habitual es enrojecimiento, sensibilidad o adormecimiento temporal en la zona. Muy rara vez la grasa de la zona puede reaccionar al revés y aumentar; si pasa, tiene manejo. Por eso la indica y la controla un médico."),
    ("¿Quién no se la puede hacer?", "No se recomienda en embarazo o lactancia, en personas con enfermedades que reaccionan al frío (como urticaria por frío), con hernias en la zona o con problemas de circulación en el área. Lo revisamos en tu valoración."),
    ("¿Puedo combinarla con otros tratamientos?", "Sí. Se combina muy bien con radiofrecuencia para mejorar la firmeza de la piel, y con hábitos de alimentación y ejercicio para mantener el resultado."),
    ("¿Cuánto cuesta?", "Depende de las zonas que quieras tratar y del número de sesiones. El valor se define el día de tu cita de valoración, con tu plan completo por escrito."),
]


def _wa(b, extra=""):
    return "https://wa.me/" + b.WHATSAPP + "?text=" + quote(MSJ + extra)


def _boton(b, texto="Quiero mi valoración", clase="cl-btn", extra=""):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (clase, _wa(b, extra), texto)


# ---------------------------------------------------------------- íconos (trazo fino, toman el color del texto)
ICONOS = {
    "x": '<path d="M7 7l10 10M17 7L7 17"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "frio": '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9M9.5 4.5L12 7l2.5-2.5M9.5 19.5L12 17l2.5 2.5"/>',
    "reloj": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "medica": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4.5 20.5c.8-3.6 3.8-6 7.5-6s6.7 2.4 7.5 6"/><path d="M16.5 17.5v3M15 19h3"/>',
    "plan": '<path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10A.5.5 0 0 1 7 20Z"/><path d="M14 3.5v4h4M9.5 12h6M9.5 15.5h6"/>',
    "control": '<path d="M4 19.5h16M7 16V11M12 16V7M17 16v-3"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "sin": '<circle cx="12" cy="12" r="8.5"/><path d="M6 18L18 6"/>',
}


def ico(nombre, clase="ico"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (clase, ICONOS[nombre])


# ---------------------------------------------------------------- test "¿eres candidata?"
# Cada opción suma una "bandera" que decide el resultado (ver criolipolisis.js). La decisión final la toma la médica.
TEST = [
    {"id": "zona", "p": "¿Dónde está la grasa que más te molesta?", "o": [[n, k] for k, n, d, r in ZONAS]},
    {"id": "pellizco", "p": "¿Puedes pellizcar esa grasa con los dedos?",
     "o": [["Sí, se pellizca", "ok"], ["No, es más piel suelta", "piel"], ["No estoy segura", "ok"]]},
    {"id": "peso", "p": "¿Qué tan cerca estás de tu peso ideal?",
     "o": [["Cerca: me faltan menos de 5 kilos", "ok"], ["Me faltan entre 5 y 10 kilos", "ok"], ["Me faltan más de 10 kilos", "peso"]]},
    {"id": "meta", "p": "¿Qué cambio buscas?",
     "o": [["Uno sin cirugía y sin incapacidad", "ok"], ["Uno grande, de una sola vez", "lipo"]]},
    {"id": "embarazo", "p": "¿Estás embarazada o lactando?",
     "o": [["No", "ok"], ["Sí", "embarazo"]]},
]
RESULTADOS = {
    "ok": {"t": "Eres buena candidata para criolipólisis", "d": "Por lo que cuentas, tu grasa es localizada y buscas un cambio sin cirugía. Eso es justo lo que trata la criolipólisis. En tu valoración la médica lo confirma y te dice cuántas sesiones necesitas."},
    "piel": {"t": "Puede que lo tuyo sea firmeza de la piel", "d": "Si lo que te molesta es la piel suelta, la criolipólisis sola no es lo ideal: la firmeza se trabaja con radiofrecuencia. En tu valoración la médica revisa la zona y te dice qué te conviene.", "link": ["radiofrecuencia", "Ver radiofrecuencia"]},
    "peso": {"t": "Primero, un plan para tu peso", "d": "La criolipólisis moldea zonas puntuales, no baja de peso. Con más de 10 kilos por bajar te conviene empezar con el manejo médico del peso y dejar la criolipólisis para el final.", "link": ["manejo-medico-del-peso", "Ver manejo médico del peso"]},
    "lipo": {"t": "Puede que lo tuyo sea una liposucción", "d": "La criolipólisis da un cambio progresivo, zona por zona. Si buscas un cambio grande de una sola vez, vale la pena que valoremos una liposucción.", "link": ["liposuccion", "Ver liposucción"]},
    "embarazo": {"t": "Por ahora, mejor esperar", "d": "Durante el embarazo y la lactancia no se recomienda. Escríbenos y te contamos cuándo es un buen momento para empezar."},
}


def generar(b):
    """b = módulo build (WHATSAPP, TELEFONO, DOMINIO, CLARITY_ID, CLINICA_LD, ESPECIALISTAS, HECHAS, V, AQUI)."""
    v = b.V
    url = b.DOMINIO + "/criolipolisis"
    flecha = ico("flecha", "ico-f")
    cta = lambda texto="Quiero mi valoración", clase="cl-btn", extra="": _boton(b, texto + ' ' + flecha, clase, extra)

    dolores = "".join('<li class="cl-dolor cl-vidrio cl-rev"><span class="cl-dolor-i">%s</span><p>%s</p></li>' % (ico("x"), t) for t in DOLORES)
    cifras = "".join('<li><b>%s</b><span>%s</span></li>' % (n, t) for n, t in CIFRAS)
    # atajo de zonas en la portada: lleva a la pestaña de esa zona
    atajo = "".join('<a href="#zona-%s" data-zona="%s">%s</a>' % (k, k, CORTO_Z.get(k, n)) for k, n, d, r in ZONAS)
    pestanas = "".join('<button type="button" role="tab" id="tab-%s" aria-controls="zona-%s" aria-selected="%s" data-zona="%s"%s>%s</button>' % (
        k, k, "true" if i == 0 else "false", k, ' class="on"' if i == 0 else "", CORTO_Z.get(k, n)) for i, (k, n, d, r) in enumerate(ZONAS))
    paneles = "".join('''<article class="cl-zona" id="zona-%s" role="tabpanel" aria-labelledby="tab-%s" data-zona="%s">
        <div><span class="cl-zona-n">%02d / %02d</span><h3>%s</h3></div>
        <div><dl><div><dt>Cómo lo vives</dt><dd>%s</dd></div><div><dt>Lo que buscamos</dt><dd>%s</dd></div></dl>%s</div>
      </article>''' % (k, k, k, i + 1, len(ZONAS), n, d, r,
                       _boton(b, "Quiero tratar " + BOTON_Z[k] + " " + flecha, "cl-btn", " para " + BOTON_Z[k].split(" ", 1)[1]))
        for i, (k, n, d, r) in enumerate(ZONAS))
    botones_e = "".join('<button type="button" class="cl-e%s" data-e="%d"><span class="cl-en">%02d</span>%s</button>' % (
        " on" if i == 0 else "", i, i + 1, t) for i, (t, d) in enumerate(ETAPAS))
    textos_e = "".join('<p class="cl-et%s" data-e="%d">%s</p>' % (" on" if i == 0 else "", i, d) for i, (t, d) in enumerate(ETAPAS))
    pasos = "".join('<li class="cl-vidrio cl-rev"><span class="cl-pn">%s</span><h3>%s</h3><p>%s</p></li>' % (ico(ic), t, d)
                    for (t, d), ic in zip(PASOS, ["frio", "sin", "check"]))
    camino = "".join('<li class="cl-vidrio cl-rev"><span class="cl-cn">%d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i, t, d) for i, (t, d) in enumerate(CAMINO, 1))
    preguntas = "".join('<details class="cl-preg cl-vidrio cl-rev"><summary>%s<span class="cl-mas" aria-hidden="true"></span></summary><div class="cl-resp"><p>%s</p></div></details>' % (p, r) for p, r in PREGUNTAS)
    test = json.dumps({"preguntas": TEST, "resultados": RESULTADOS, "wa": b.WHATSAPP, "msj": MSJ}, ensure_ascii=False)

    med = [e for e in b.ESPECIALISTAS if e["area"] == "estetica"][0]

    # ---------- SEO
    esquema = [
        {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": TITULO, "url": url, "inLanguage": "es-CO",
         "about": {"@type": "MedicalProcedure", "name": "Criolipólisis", "alternateName": ["Criolipolisis", "Lipoescultura con frío"],
                   "procedureType": "https://schema.org/NoninvasiveProcedure", "bodyLocation": "Abdomen, flancos, espalda, papada, brazos, muslos, rodillas",
                   "howPerformed": "Enfriamiento controlado de la grasa localizada para que el cuerpo elimine las células de grasa de forma natural.",
                   "preparation": "Valoración médica previa.", "followup": "Control entre la semana 8 y la 12."},
         "provider": {"@id": b.DOMINIO + "/#clinica"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in PREGUNTAS]},
    ]
    seo = '<link rel="canonical" href="%s">' % url
    seo += ('\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="noon Clinic">\n<meta property="og:title" content="%s">'
            '\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n<meta property="og:image" content="%s/assets/criolipolisis/portada-ancha.jpg">'
            '\n<meta property="og:locale" content="es_CO">') % (escape(TITULO), escape(DESCRIPCION), url, b.DOMINIO)
    for bloque in [b.CLINICA_LD] + esquema:
        seo += '\n<script type="application/ld+json">%s</script>' % json.dumps(bloque, ensure_ascii=False)
    seo += ('\n<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;'
            't.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");'
            'clarity("set","idioma","es");clarity("set","pagina","criolipolisis");clarity("set","tipo","landing");</script>') % b.CLARITY_ID

    html = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s · noon Clinic</title>
<meta name="description" content="%(desc)s">
%(seo)s
<meta name="theme-color" content="#f6f8f8">
<link rel="icon" href="assets/favicon.png">
<script>document.documentElement.className="js"</script>
<link rel="preload" as="image" href="assets/criolipolisis/portada.webp" fetchpriority="high">
%(fuentes)s
<link rel="stylesheet" href="assets/criolipolisis.css?v=%(v)s">
</head>
<body class="cl">
<div class="cl-aura" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div class="cl-grano" aria-hidden="true"></div>
<header class="cl-cab">
  <a class="cl-logo" href="./" aria-label="noon Clinic, inicio"><img src="assets/logo-noon.png" alt="noon Clinic" width="900" height="295"></a>
  <a class="cl-btn2 cl-vidrio" href="%(wa)s" target="_blank" rel="noopener">Agendar</a>
</header>
<main>

<!-- 1 · PORTADA: promesa + botón + prueba, todo en la primera pantalla -->
<section class="cl-portada">
  <div class="cl-portada-in">
    <div class="cl-portada-txt">
      <p class="cl-ceja cl-vidrio">%(ico_frio)s Criolipólisis · Medellín</p>
      <h1>La grasa que no se va con nada, <span class="cl-hielo">se va con frío.</span></h1>
      <p class="cl-lead">Enfriamos la grasa localizada y tu cuerpo la elimina solo. <b>Sin cirugía, sin agujas y sin incapacidad.</b></p>
      <div class="cl-acciones">%(btn_portada)s<a class="cl-btn2 cl-vidrio" href="#test"><i></i>¿Soy candidata? Test de 1 min</a></div>
      <p class="cl-inmediato">%(ico_reloj)s %(inmediato)s</p>
    </div>
    <figure class="cl-foto">
      <img src="assets/criolipolisis/portada.webp" fetchpriority="high" alt="Paciente recostada durante una sesión de criolipólisis en la cintura" width="1200" height="1500">
      <div class="cl-tarjeta cl-proceso cl-vidrio">
        <p>Tu proceso</p>
        <ol class="cl-linea"><li><b>Hoy</b><span>Una sesión y sigues tu día</span></li><li><b>Semana 3</b><span>Empiezas a notarlo</span></li><li><b>Semana 12</b><span>Ves el resultado completo</span></li></ol>
      </div>
      <div class="cl-tarjeta cl-cero cl-vidrio"><b>0</b><span>días de<br>incapacidad</span></div>
    </figure>
  </div>
  <div class="cl-atajo">
    <p>¿Qué zona te molesta?</p>
    <nav class="cl-seg cl-vidrio" aria-label="Zonas">%(atajo)s</nav>
  </div>
</section>

<!-- 2 · ¿TE PASA ESTO? (dolores) -->
<section class="cl-sec" id="te-pasa">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="cl-ceja cl-vidrio">%(ico_frio)s Si esto te pasa</p>
      <h2>No es falta de disciplina. Es <span class="cl-hielo">grasa terca.</span></h2>
      <p class="cl-sub">Hay grasa que no responde a la dieta ni al ejercicio: se acumula en zonas puntuales, muchas veces por genética.</p></header>
    <ul class="cl-dolores">%(dolores)s</ul>
    <div class="cl-respuesta cl-vidrio cl-rev"><p>La criolipólisis trata <b>justo esa grasa</b>: la localizada, la que se pellizca.</p>%(btn_dolores)s</div>
  </div>
</section>

<!-- 3 · QUÉ HACE: el frío en tu grasa -->
<section class="cl-sec" id="que-hace">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="cl-ceja cl-vidrio">%(ico_frio)s Cómo funciona</p>
      <h2>Lo que hace el <span class="cl-hielo">frío</span> en tu grasa.</h2>
      <p class="cl-sub">No es una dieta ni un masaje: la criolipólisis elimina células de grasa de la zona tratada, y tu cuerpo hace el resto.</p></header>
    <div class="cl-visual cl-vidrio cl-rev" data-capas>
      <svg class="cl-svg" viewBox="0 0 800 380" role="img" aria-label="Corte de la piel, la grasa y el músculo: con el frío, la capa de grasa de la zona tratada se vuelve más delgada">
        <defs>
          <linearGradient id="cl-g-frio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcdbe6" stop-opacity=".75"/><stop offset="1" stop-color="#bcdbe6" stop-opacity="0"/></linearGradient>
          <linearGradient id="cl-g-grasa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbeedd"/><stop offset="1" stop-color="#f5e3cc"/></linearGradient>
          <clipPath id="cl-clip"><path class="cl-grasa-clip"/></clipPath>
          <pattern id="cl-rayas" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="9" stroke="rgba(255,255,255,.18)" stroke-width="1"/></pattern>
        </defs>
        <rect x="0" y="320" width="800" height="60" fill="#7a2f3d"/>
        <rect x="0" y="320" width="800" height="60" fill="url(#cl-rayas)"/>
        <path class="cl-grasa" fill="url(#cl-g-grasa)"/>
        <g class="cl-celulas" clip-path="url(#cl-clip)"></g>
        <rect class="cl-frio" x="225" y="0" width="350" height="320" fill="url(#cl-g-frio)" clip-path="url(#cl-clip)"/>
        <path class="cl-piel" fill="none" stroke="#e2c6b6" stroke-width="10" stroke-linecap="round"/>
        <path class="cl-corchete" d="M235,40 V32 H565 V40" fill="none" stroke="#6D2835" stroke-width="1.5"/>
        <text class="cl-et-svg cl-et-frio" x="400" y="20" text-anchor="middle">Zona tratada</text>
        <text class="cl-et-svg" x="16" y="114">Piel</text>
        <text class="cl-et-svg cl-et-grasa" x="20" y="240">Grasa</text>
        <text class="cl-et-svg" x="16" y="358" style="fill:#fff">Músculo</text>
      </svg>
      <div class="cl-etapas" role="group" aria-label="Etapas">%(botones_e)s</div>
      <div class="cl-etextos" aria-live="polite">%(textos_e)s</div>
    </div>
    <ol class="cl-pasos">%(pasos)s</ol>
  </div>
</section>

<!-- 4 · CIFRAS + botón (ruptura) -->
<section class="cl-sec cl-sec-cifras">
  <div class="cl-in">
    <ul class="cl-cifras cl-vidrio cl-rev">%(cifras)s</ul>
    <div class="cl-centro cl-mas-btn cl-rev">%(btn_cifras)s</div>
  </div>
</section>

<!-- 5 · TEST: ¿eres candidata? -->
<section class="cl-sec" id="test">
  <div class="cl-in cl-test-in">
    <header class="cl-cabeza cl-rev"><p class="cl-ceja cl-vidrio">%(ico_frio)s Test de 1 minuto</p>
      <h2>¿Eres <span class="cl-hielo">candidata</span> a criolipólisis?</h2>
      <p class="cl-sub">Cinco preguntas de un toque. Al final te decimos qué te conviene, con honestidad.</p></header>
    <div class="cl-test cl-vidrio cl-rev" data-test aria-live="polite">
      <div class="cl-test-barra" aria-hidden="true"></div>
      <p class="cl-test-paso"></p>
      <h3 class="cl-test-p"></h3>
      <div class="cl-test-o"></div>
      <div class="cl-test-r" hidden>
        <span class="cl-test-r-i"></span>
        <h3 class="cl-test-r-t"></h3>
        <p class="cl-test-r-d"></p>
        <div class="cl-acciones"><a class="cl-btn cl-test-wa" href="#" target="_blank" rel="noopener">Quiero mi valoración %(ico_flecha)s</a><a class="cl-link cl-test-link" href="#" hidden></a></div>
        <p class="cl-test-nota">La decisión final la toma la médica en tu valoración.</p>
        <button type="button" class="cl-test-otra">Hacer el test otra vez</button>
      </div>
    </div>
  </div>
  <script type="application/json" id="cl-test-datos">%(test)s</script>
</section>

<!-- 6 · ZONAS (pestañas) -->
<section class="cl-sec" id="zonas">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="cl-ceja cl-vidrio">%(ico_frio)s Zonas que tratamos</p>
      <h2>¿Dónde está <span class="cl-hielo">tu</span> grasa terca?</h2>
      <p class="cl-sub">Elige tu zona: te contamos qué buscamos ahí y nos escribes con un toque.</p></header>
    <div class="cl-rev">
      <div class="cl-seg cl-zonas-seg cl-vidrio" role="tablist" aria-label="Zonas">%(pestanas)s</div>
      <div class="cl-zona-panel cl-vidrio" data-zonas>%(paneles)s</div>
      <p class="cl-zona-nota">¿No sabes cuál es la tuya? <a href="#test">Haz el test de 1 minuto</a>.</p>
    </div>
  </div>
</section>

<!-- 7 · PASO A PASO -->
<section class="cl-sec" id="paso-a-paso">
  <div class="cl-in cl-camino-grid">
    <figure class="cl-camino-foto cl-rev"><img src="assets/criolipolisis/portada-2.webp" alt="Sesión de criolipólisis en el abdomen, en una sala de noon" width="1200" height="1500" loading="lazy"><figcaption class="cl-vidrio">Sin agujas, sin cortes y sin incapacidad.</figcaption></figure>
    <div>
      <header class="cl-cabeza cl-rev"><p class="cl-ceja cl-vidrio">%(ico_frio)s Paso a paso</p>
        <h2>Una sesión, y tu vida <span class="cl-hielo">sigue.</span></h2></header>
      <ol class="cl-camino">%(camino)s</ol>
      <div class="cl-mas-btn cl-rev">%(btn_camino)s</div>
    </div>
  </div>
</section>

<!-- 8 · MÉDICA -->
<section class="cl-sec">
  <div class="cl-in cl-medico">
    <figure class="cl-med-foto cl-rev"><img src="assets/equipo/%(med_foto)s" alt="%(med_nombre)s, %(med_rol)s de noon Clinic" loading="lazy"><figcaption class="cl-vidrio"><b>%(med_nombre)s</b><span>%(med_rol_m)s · noon Clinic</span></figcaption></figure>
    <div class="cl-rev">
      <p class="cl-ceja cl-vidrio">%(ico_frio)s Por qué en noon</p>
      <h2>Antes del frío, <span class="cl-hielo">una médica.</span></h2>
      <p class="cl-sub">La criolipólisis funciona cuando se indica bien. Por eso en noon no empieza en la máquina: empieza en tu valoración.</p>
      <ul class="cl-razones">
        <li class="cl-vidrio">%(ico_medica)s<div><b>Valoración médica primero</b><span>Revisa la zona, tu historia y si eres candidata.</span></div></li>
        <li class="cl-vidrio">%(ico_plan)s<div><b>Tu plan por escrito</b><span>Qué zonas, cuántas sesiones, cada cuánto y qué esperar.</span></div></li>
        <li class="cl-vidrio">%(ico_control)s<div><b>Te volvemos a ver</b><span>Control entre la semana 8 y la 12 para medir el resultado.</span></div></li>
      </ul>
      %(btn_medico)s
    </div>
  </div>
</section>

<!-- 9 · PREGUNTAS -->
<section class="cl-sec" id="preguntas">
  <div class="cl-in">
    <header class="cl-cabeza cl-centro cl-rev"><p class="cl-ceja cl-vidrio">%(ico_frio)s Antes de que preguntes</p><h2>Lo que todas <span class="cl-hielo">preguntan.</span></h2></header>
    <div class="cl-faq">%(preguntas)s</div>
  </div>
</section>

<!-- 10 · CIERRE -->
<section class="cl-cierre" id="agendar">
  <div class="cl-cierre-in cl-rev">
    <p class="cl-ceja">%(ico_frio)s noon Clinic · Medellín</p>
    <h2>Tu primer paso es la <span>valoración.</span></h2>
    <p class="cl-sub">Te decimos qué se puede lograr en tu zona, cuántas sesiones necesitas y si eres candidata. Sin compromiso de hacerte el tratamiento.</p>
    %(btn_cierre)s
    <p class="cl-inmediato">%(ico_reloj)s %(inmediato)s</p>
    <p class="cl-nota">La valoración no se abona al tratamiento y su valor no se devuelve. <a href="terminos-y-condiciones">Términos y condiciones</a></p>
  </div>
</section>

</main>
<footer class="cl-pie">
  <div class="cl-in cl-pie-in">
    <a class="cl-logo" href="./"><img src="assets/logo-noon.png" alt="noon Clinic" width="900" height="295" loading="lazy"></a>
    <nav><a href="./">Conoce noon</a><a href="medicina-estetica">Medicina estética</a><a href="especialistas">Especialistas</a><a href="terminos-y-condiciones">Términos</a><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp %(tel)s</a></nav>
  </div>
  <p class="cl-in cl-legal">La información de esta página es orientativa y no reemplaza una consulta médica. Los resultados varían de una persona a otra. Las fotos de las sesiones son ilustrativas. © noon Clinic</p>
</footer>
<div class="cl-barra cl-vidrio" aria-hidden="true">%(btn_barra)s</div>
<script src="assets/medicion-ads.js?v=%(v)s" defer></script>
<script src="assets/criolipolisis.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"titulo": escape(TITULO), "desc": escape(DESCRIPCION), "seo": seo, "v": v, "fuentes": b.FUENTES, "wa": _wa(b), "tel": b.TELEFONO,
       "btn_portada": cta("Quiero mi valoración", "cl-btn cl-btn-xl"), "btn_dolores": cta("Quiero mi valoración", "cl-btn"),
       "btn_cifras": cta("Agendar mi valoración", "cl-btn cl-btn-xl"),
       "btn_camino": cta("Agendar mi valoración", "cl-btn"), "btn_medico": cta("Quiero mi valoración", "cl-btn"),
       "btn_cierre": cta("Quiero mi valoración", "cl-btn cl-btn-xl cl-btn-blanco"), "btn_barra": cta("Quiero mi valoración", "cl-btn"),
       "ico_frio": ico("frio"), "ico_flecha": flecha, "ico_reloj": ico("reloj"), "inmediato": INMEDIATO,
       "ico_medica": ico("medica"), "ico_plan": ico("plan"), "ico_control": ico("control"),
       "dolores": dolores, "cifras": cifras, "atajo": atajo, "pestanas": pestanas, "paneles": paneles,
       "botones_e": botones_e, "textos_e": textos_e, "pasos": pasos,
       "camino": camino, "preguntas": preguntas, "test": test.replace("</", "<\\/"),
       "med_foto": med["foto"], "med_nombre": med["nombre"], "med_rol": med["rol"].lower(), "med_rol_m": med["rol"]}

    with open(os.path.join(b.AQUI, ARCHIVO), "w", encoding="utf-8") as f:
        f.write(html)
    b.HECHAS.append(ARCHIVO)
    return ARCHIVO
