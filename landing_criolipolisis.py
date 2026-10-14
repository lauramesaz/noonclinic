# -*- coding: utf-8 -*-
# noon Clinic · LANDING DE VENTA: Criolipólisis (noon.clinic/criolipolisis)
# Enfocada en lo que hace la criolipólisis (el resultado en el cuerpo), no en la máquina.
# Estructura de venta: promesa + botón en la 1ª pantalla → grasa terca por zonas → qué hace el frío (animación)
# → botón intermedio → lo que vas a vivir → ¿es para ti? (honesto) → médica → preguntas → cierre.
# Sin menú (no distrae), sin precios (regla de la web pública), todo a WhatsApp.
# build.py llama a generar() al final.
import json, os
from html import escape
from urllib.parse import quote

ARCHIVO = "criolipolisis.html"
TITULO = "Criolipólisis en Medellín: elimina la grasa localizada sin cirugía"
DESCRIPCION = ("Criolipólisis en Medellín con valoración médica: el frío controlado elimina la grasa localizada de abdomen, "
               "flancos, papada, brazos y muslos. Sin cirugía, sin agujas y sin incapacidad.")

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

# ---------------------------------------------------------------- lo que vas a vivir
VIVIR = [
    ("El día de tu sesión", "Sientes frío intenso los primeros minutos; después la zona se adormece. Puedes leer, trabajar o descansar. Al terminar, sigues con tu día."),
    ("Los primeros días", "La zona puede estar roja, sensible o adormecida. Es normal y pasa sola."),
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


def generar(b):
    """b = módulo build (WHATSAPP, TELEFONO, DOMINIO, CLARITY_ID, CLINICA_LD, ESPECIALISTAS, HECHAS, V, AQUI)."""
    v = b.V
    url = b.DOMINIO + "/criolipolisis"

    # ---------- zonas
    botones_z = "".join('<button type="button" class="cl-z%s" data-z="%d" aria-pressed="%s">%s</button>' % (
        " on" if i == 0 else "", i, "true" if i == 0 else "false", n) for i, (k, n, d, r) in enumerate(ZONAS))
    paneles_z = "".join('''<div class="cl-zp%s" data-z="%d"%s><p class="cl-zn">%s</p>
      <p class="cl-zl">Lo que notas</p><p class="cl-zt">%s</p>
      <p class="cl-zl">Lo que buscamos</p><p class="cl-zt">%s</p>
      <p class="cl-zl">Sesiones</p><p class="cl-zt">Normalmente de 1 a 3, según la cantidad de grasa. Lo defines en tu valoración.</p>
      %s</div>''' % (" on" if i == 0 else "", i, "" if i == 0 else " hidden", n, d, r,
                     _boton(b, "Quiero tratar " + BOTON_Z[k], "cl-btn cl-btn-linea", " para " + BOTON_Z[k].split(" ", 1)[1]))
        for i, (k, n, d, r) in enumerate(ZONAS))

    # ---------- etapas
    botones_e = "".join('<button type="button" class="cl-e%s" data-e="%d"><span class="cl-en">%02d</span>%s</button>' % (
        " on" if i == 0 else "", i, i + 1, t) for i, (t, d) in enumerate(ETAPAS))
    textos_e = "".join('<p class="cl-et%s" data-e="%d">%s</p>' % (" on" if i == 0 else "", i, d) for i, (t, d) in enumerate(ETAPAS))
    pasos = "".join('<li class="cl-rev"><span class="cl-pn">%02d</span><h3>%s</h3><p>%s</p></li>' % (i, t, d) for i, (t, d) in enumerate(PASOS, 1))

    vivir = "".join('<li class="cl-rev"><span class="cl-vp" aria-hidden="true"></span><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in VIVIR)

    si = "".join('<li>%s</li>' % x for x in SI)
    no = "".join('<li><b>%s</b> %s</li>' % (t, r) for t, r in NO)

    preguntas = "".join('<details class="preg cl-rev"><summary>%s</summary><div class="resp"><p>%s</p></div></details>' % (p, r) for p, r in PREGUNTAS)

    med = [e for e in b.ESPECIALISTAS if e["area"] == "estetica"][0]
    foto_med = "assets/equipo/" + med["foto"]

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
            '\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n<meta property="og:image" content="%s/assets/criolipolisis/silueta.jpg">'
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
<meta name="theme-color" content="#120d0a">
<link rel="icon" href="assets/favicon.png">
<script>document.documentElement.className="js"</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,400&family=Jost:wght@300;400&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="assets/criolipolisis/silueta.jpg">
<link rel="stylesheet" href="assets/noon.css?v=%(v)s">
<link rel="stylesheet" href="assets/criolipolisis.css?v=%(v)s">
</head>
<body class="cl">
<header class="cl-cab">
  <a class="cl-logo" href="./" aria-label="noon Clinic, inicio"><img src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295"></a>
  <a class="cl-agendar" href="%(wa)s" target="_blank" rel="noopener">Agendar</a>
</header>
<main>

<!-- 1 · PROMESA (todo lo importante cabe en la primera pantalla) -->
<section class="cl-hero">
  <figure class="cl-hero-foto"><img src="assets/criolipolisis/silueta.jpg" alt="Mujer con suéter de punto marfil y la mano sobre el abdomen" width="1200" height="1800"></figure>
  <div class="cl-hero-in">
    <p class="ceja">Criolipólisis · Medellín</p>
    <h1>La grasa que no se va con nada, se va con <em>frío</em>.</h1>
    <p class="cl-sub">Enfriamos la grasa localizada de forma controlada para que tu cuerpo la elimine por sí solo. Sin cirugía, sin agujas y sigues con tu día.</p>
    <div class="cl-acciones">%(btn_hero)s<a class="cl-link" href="#que-hace">Cómo funciona</a></div>
    <ul class="cl-sellos"><li>Sin cirugía</li><li>Sin incapacidad</li><li>Con valoración médica</li></ul>
  </div>
  <a class="cl-bajar" href="#zonas" aria-label="Bajar"><span></span></a>
</section>

<!-- 2 · EL PROBLEMA: la grasa terca, por zonas -->
<section class="cl-sec cl-marfil" id="zonas">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="ceja">La grasa terca</p>
      <h2>Ese <em>rollito</em> que sigue ahí, aunque hagas todo bien.</h2>
      <p class="cl-intro">Hay grasa que no responde a la dieta ni al ejercicio: se acumula en zonas puntuales, muchas veces por genética. Justo esa es la que trata la criolipólisis. ¿Dónde está la tuya?</p></header>
    <div class="cl-zonas cl-rev">
      <div class="cl-zbotones" role="group" aria-label="Elige una zona">%(botones_z)s</div>
      <div class="cl-zpaneles" aria-live="polite">%(paneles_z)s</div>
    </div>
  </div>
</section>

<!-- 3 · QUÉ HACE (la protagonista: el frío en tu grasa) -->
<section class="cl-sec cl-oscuro" id="que-hace">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="ceja">Qué hace</p>
      <h2>Lo que hace el <em>frío</em> en tu grasa.</h2>
      <p class="cl-intro">No es una dieta ni un masaje. La criolipólisis elimina células de grasa de la zona tratada, y tu cuerpo hace el resto.</p></header>
    <div class="cl-visual cl-rev" data-capas>
      <svg class="cl-svg" viewBox="0 0 800 380" role="img" aria-label="Corte de la piel, la grasa y el músculo: con el frío, la capa de grasa de la zona tratada se vuelve más delgada">
        <defs>
          <linearGradient id="cl-g-frio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF2F2" stop-opacity=".45"/><stop offset="1" stop-color="#EEF2F2" stop-opacity="0"/></linearGradient>
          <linearGradient id="cl-g-musc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a2e3c"/><stop offset="1" stop-color="#4a1a24"/></linearGradient>
          <clipPath id="cl-clip"><path class="cl-grasa-clip"/></clipPath>
        </defs>
        <rect x="0" y="320" width="800" height="60" fill="url(#cl-g-musc)"/>
        <g class="cl-fibras" stroke="rgba(255,255,255,.08)" stroke-width="1"></g>
        <path class="cl-grasa" fill="rgba(189,164,123,.07)"/>
        <g class="cl-celulas" clip-path="url(#cl-clip)"></g>
        <rect class="cl-frio" x="225" y="0" width="350" height="320" fill="url(#cl-g-frio)" clip-path="url(#cl-clip)"/>
        <path class="cl-piel" fill="none" stroke="#D8D0C3" stroke-width="15" stroke-linecap="round"/>
        <path class="cl-corchete" d="M235,40 V32 H565 V40" fill="none" stroke="#BDA47B" stroke-width="1.2"/>
        <text class="cl-et-svg cl-et-frio" x="400" y="20" text-anchor="middle">Zona tratada</text>
        <text class="cl-et-svg" x="16" y="114">Piel</text>
        <text class="cl-et-svg cl-et-grasa" x="20" y="240">Grasa</text>
        <text class="cl-et-svg cl-et-claro" x="16" y="358">Músculo</text>
      </svg>
      <div class="cl-etapas" role="group" aria-label="Etapas">%(botones_e)s</div>
      <div class="cl-etextos" aria-live="polite">%(textos_e)s</div>
    </div>
    <ol class="cl-pasos">%(pasos)s</ol>
  </div>
</section>

<!-- botón intermedio -->
<section class="cl-banda">
  <div class="cl-in cl-banda-in cl-rev"><p>¿Ya sabes qué zona quieres tratar?</p>%(btn_banda)s</div>
</section>

<!-- 4 · LO QUE VAS A VIVIR -->
<section class="cl-sec cl-oscuro cl-vivir-sec">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="ceja">Lo que vas a vivir</p>
      <h2>Una sesión, y tu vida <em>sigue</em>.</h2></header>
    <ol class="cl-vivir">%(vivir)s</ol>
  </div>
</section>

<!-- 5 · ¿ES PARA TI? (honesto: también decimos cuándo no) -->
<section class="cl-sec cl-marfil">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="ceja">¿Es para ti?</p>
      <h2>Te decimos la <em>verdad</em>, aunque no sea criolipólisis.</h2></header>
    <div class="cl-para">
      <div class="cl-col cl-rev"><p class="cl-col-t">Es para ti si…</p><ul class="cl-si">%(si)s</ul></div>
      <div class="cl-col cl-rev"><p class="cl-col-t">No es lo tuyo si…</p><ul class="cl-no">%(no)s</ul></div>
    </div>
  </div>
</section>

<!-- 6 · POR QUÉ EN NOON: primero un médico -->
<section class="cl-sec cl-oscuro">
  <div class="cl-in cl-medico">
    <figure class="cl-med-foto cl-rev"><img src="%(foto_med)s" alt="%(med_nombre)s, %(med_rol)s de noon Clinic" loading="lazy"></figure>
    <div class="cl-med-texto cl-rev">
      <p class="ceja">Por qué en noon</p>
      <h2>Antes del frío, un <em>médico</em>.</h2>
      <p class="cl-intro">La criolipólisis funciona cuando se indica bien. Por eso en noon no empieza en la máquina: empieza en tu valoración.</p>
      <ul class="cl-razones">
        <li><b>Valoración médica primero.</b> Con la %(med_nombre)s, %(med_rol_min)s: revisa la zona, tu historia y si eres candidata.</li>
        <li><b>Tu plan por escrito.</b> Qué zonas, cuántas sesiones, cada cuánto y qué resultado esperar.</li>
        <li><b>Te volvemos a ver.</b> Control entre la semana 8 y la 12 para medir el resultado contigo.</li>
      </ul>
      <a class="enlace" href="especialistas#%(med_slug)s">Conocer a la especialista</a>
    </div>
  </div>
</section>

<!-- 7 · PREGUNTAS -->
<section class="cl-sec cl-marfil" id="preguntas">
  <div class="cl-in cl-faq">
    <header class="cl-cabeza cl-rev"><p class="ceja">Preguntas</p><h2>Lo que todas <em>preguntan</em>.</h2></header>
    <div class="preguntas">%(preguntas)s</div>
  </div>
</section>

<!-- 8 · CIERRE -->
<section class="cl-cierre">
  <div class="cl-cierre-foto" style="background-image:url(assets/criolipolisis/silueta-2.jpg)"></div>
  <div class="cl-cierre-in cl-rev">
    <p class="ceja">noon Clinic</p>
    <h2>Empieza por tu <em>valoración</em>.</h2>
    <p class="cl-sub">Te decimos qué se puede lograr en tu zona, cuántas sesiones necesitas y si eres candidata. Sin compromiso de hacerte el tratamiento.</p>
    <div class="cl-acciones">%(btn_cierre)s</div>
    <p class="cl-nota">La valoración no se abona al tratamiento y su valor no se devuelve. <a href="terminos-y-condiciones">Términos y condiciones</a></p>
  </div>
</section>

</main>
<footer class="cl-pie">
  <a class="cl-logo" href="./"><img src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295" loading="lazy"></a>
  <p>Cirugía plástica y medicina estética, con criterio. Medellín, Colombia.</p>
  <nav><a href="./">Conoce noon</a><a href="medicina-estetica">Medicina estética</a><a href="especialistas">Especialistas</a><a href="terminos-y-condiciones">Términos</a><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp %(tel)s</a></nav>
  <p class="legal">La información de esta página es orientativa y no reemplaza una consulta médica. Los resultados varían de una persona a otra. Foto: sombre en Unsplash. © noon Clinic</p>
</footer>
<div class="cl-barra" aria-hidden="true">%(btn_barra)s</div>
<script src="assets/criolipolisis.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"titulo": escape(TITULO), "desc": escape(DESCRIPCION), "seo": seo, "v": v, "wa": _wa(b), "tel": b.TELEFONO,
       "btn_hero": _boton(b), "btn_banda": _boton(b, "Quiero mi valoración", "cl-btn cl-btn-claro"), "btn_cierre": _boton(b),
       "btn_barra": _boton(b, "Quiero mi valoración", "cl-btn"),
       "botones_z": botones_z, "paneles_z": paneles_z, "botones_e": botones_e, "textos_e": textos_e, "pasos": pasos,
       "vivir": vivir, "si": si, "no": no, "preguntas": preguntas,
       "foto_med": foto_med, "med_nombre": med["nombre"], "med_rol": med["rol"].lower(), "med_rol_min": med["rol"].lower(), "med_slug": med["slug"]}

    with open(os.path.join(b.AQUI, ARCHIVO), "w", encoding="utf-8") as f:
        f.write(html)
    b.HECHAS.append(ARCHIVO)
    return ARCHIVO
