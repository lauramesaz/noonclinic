# -*- coding: utf-8 -*-
# noon Clinic · LANDING DE VENTA: Criolipólisis (noon.clinic/criolipolisis)
# Enfocada en lo que hace la criolipólisis (el resultado en el cuerpo), no en la máquina.
# Estructura de venta: promesa + botón en la 1ª pantalla → grasa terca por zonas → qué hace el frío (animación)
# → botón intermedio → lo que vas a vivir → ¿es para ti? (honesto) → médica → preguntas → cierre.
# Sin menú (no distrae), sin precios (regla de la web pública), todo a WhatsApp.
# v2 (14-oct): estilo editorial sobre luz líquida (referencia monopo saigon) con la línea gráfica de noon.
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


def generar(b):
    """b = módulo build (WHATSAPP, TELEFONO, DOMINIO, CLARITY_ID, CLINICA_LD, ESPECIALISTAS, HECHAS, V, AQUI).
    v2 (14-oct): dirección editorial tipo galería monocromática sobre luz líquida, en la línea de noon:
    marfil/espresso, Jost delgada monumental + una palabra en cursiva Cormorant, botones en píldora (lo único redondo),
    un solo gesto de color: la luz líquida del inicio (espresso → vino → rosado → champaña → perla fría)."""
    v = b.V
    url = b.DOMINIO + "/criolipolisis"

    # ---------- zonas: lista editorial que se despliega
    filas_z = "".join('''<li class="cl-fila cl-rev%(on)s">
      <button type="button" class="cl-fila-b" aria-expanded="%(exp)s" aria-controls="cl-z-%(k)s"><span class="cl-fila-n">%(n)02d</span><span class="cl-fila-t">%(nombre)s</span><span class="cl-fila-x" aria-hidden="true"></span></button>
      <div class="cl-fila-d" id="cl-z-%(k)s"%(oculto)s><div class="cl-fila-in">
        <div><p class="cl-mini">Lo que notas</p><p>%(nota)s</p></div>
        <div><p class="cl-mini">Lo que buscamos</p><p>%(busca)s</p></div>
        <div><p class="cl-mini">Sesiones</p><p>Normalmente de 1 a 3, según la cantidad de grasa. Lo defines en tu valoración.</p></div>
        <div class="cl-fila-cta">%(cta)s</div>
      </div></div></li>''' % {"on": " abierta" if i == 0 else "", "exp": "true" if i == 0 else "false", "k": k, "n": i + 1, "nombre": n,
                             "oculto": "" if i == 0 else " hidden", "nota": d, "busca": r,
                             "cta": _boton(b, "Quiero tratar " + BOTON_Z[k], "cl-pill cl-pill-lleno", " para " + BOTON_Z[k].split(" ", 1)[1])}
        for i, (k, n, d, r) in enumerate(ZONAS))

    # ---------- etapas del dibujo
    botones_e = "".join('<button type="button" class="cl-e%s" data-e="%d"><span class="cl-en">%02d</span>%s</button>' % (
        " on" if i == 0 else "", i, i + 1, t) for i, (t, d) in enumerate(ETAPAS))
    textos_e = "".join('<p class="cl-et%s" data-e="%d">%s</p>' % (" on" if i == 0 else "", i, d) for i, (t, d) in enumerate(ETAPAS))
    pasos = "".join('<li class="cl-rev"><span class="cl-pn">%02d</span><h3>%s</h3><p>%s</p></li>' % (i, t, d) for i, (t, d) in enumerate(PASOS, 1))

    vivir = "".join('<li class="cl-rev"><p class="cl-vivir-t">%s</p><p class="cl-vivir-d">%s</p></li>' % (t, d) for t, d in VIVIR)

    si = "".join('<li>%s</li>' % x for x in SI)
    no = "".join('<li><b>%s</b> %s</li>' % (t, r) for t, r in NO)

    preguntas = "".join('<details class="cl-preg cl-rev"><summary>%s<span class="cl-fila-x" aria-hidden="true"></span></summary><div class="cl-resp"><p>%s</p></div></details>' % (p, r) for p, r in PREGUNTAS)

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

    # texto que gira en la insignia de "desliza"
    insignia = "DESLIZA · CRIOLIPÓLISIS · NOON CLINIC · "

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
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,400&family=Jost:wght@200;300;400&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/noon.css?v=%(v)s">
<link rel="stylesheet" href="assets/criolipolisis.css?v=%(v)s">
</head>
<body class="cl">
<header class="cl-cab" data-tema="oscuro">
  <a class="cl-logo" href="./" aria-label="noon Clinic, inicio"><img class="cl-logo-claro" src="assets/logo-noon-claro.png" alt="noon Clinic" width="900" height="295"><img class="cl-logo-oscuro" src="assets/logo-noon.png" alt="" width="900" height="295"></a>
  <span class="cl-cab-centro" aria-hidden="true"></span>
  <a class="cl-pill cl-pill-linea cl-cab-btn" href="%(wa)s" target="_blank" rel="noopener">Agendar</a>
</header>
<main>

<!-- 1 · PROMESA sobre luz líquida (el único gesto de color de la página) -->
<section class="cl-hero" data-tema="oscuro">
  <canvas class="cl-liquido" aria-hidden="true"></canvas>
  <div class="cl-hero-in">
    <h1><span class="cl-hero-ceja">Criolipólisis en Medellín</span><span class="cl-hero-pre">La grasa que no se va con nada,</span><span class="cl-hero-mon">se va con <em>frío</em>.</span></h1>
    <p class="cl-hero-sub">Enfriamos la grasa localizada de forma controlada para que tu cuerpo la elimine por sí solo. Sin cirugía, sin agujas y sigues con tu día.</p>
    <div class="cl-acciones">%(btn_hero)s<a class="cl-pill cl-pill-linea" href="#que-hace">Cómo funciona</a></div>
  </div>
  <a class="cl-insignia" href="#zonas" aria-label="Bajar">
    <svg viewBox="0 0 120 120" aria-hidden="true"><defs><path id="cl-circulo" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs>
      <text><textPath href="#cl-circulo">%(insignia)s</textPath></text></svg>
    <span class="cl-insignia-f">↓</span>
  </a>
  <ul class="cl-sellos"><li>Sin cirugía</li><li>Sin incapacidad</li><li>Con valoración médica</li></ul>
</section>

<!-- 2 · EL PROBLEMA: la grasa terca, por zonas -->
<section class="cl-sec cl-claro" id="zonas" data-tema="claro">
  <div class="cl-in cl-intro-zonas">
    <header class="cl-rev"><p class="ceja">La grasa terca</p>
      <h2 class="cl-h2">Ese <em>rollito</em> que sigue ahí, aunque hagas todo bien.</h2>
      <p class="cl-texto">Hay grasa que no responde a la dieta ni al ejercicio: se acumula en zonas puntuales, muchas veces por genética. Justo esa es la que trata la criolipólisis.</p></header>
    <figure class="cl-foto cl-rev"><img src="assets/criolipolisis/silueta.jpg" alt="Mujer con suéter de punto marfil y la mano sobre el abdomen" width="1200" height="1800" loading="lazy"></figure>
  </div>
  <div class="cl-in">
    <p class="cl-lista-t cl-rev">¿Dónde está la tuya? <span>Toca tu zona.</span></p>
    <ol class="cl-filas">%(filas_z)s</ol>
  </div>
</section>

<!-- 3 · QUÉ HACE: el frío en tu grasa (dibujo que se recorre una vez) -->
<section class="cl-sec cl-oscuro" id="que-hace" data-tema="oscuro">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="ceja">Qué hace</p>
      <h2 class="cl-h2">Lo que hace el <em>frío</em> en tu grasa.</h2>
      <p class="cl-texto">No es una dieta ni un masaje. La criolipólisis elimina células de grasa de la zona tratada, y tu cuerpo hace el resto.</p></header>
    <div class="cl-visual cl-rev" data-capas>
      <svg class="cl-svg" viewBox="0 0 800 380" role="img" aria-label="Corte de la piel, la grasa y el músculo: con el frío, la capa de grasa de la zona tratada se vuelve más delgada">
        <defs>
          <linearGradient id="cl-g-frio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9EEEE" stop-opacity=".32"/><stop offset="1" stop-color="#E9EEEE" stop-opacity="0"/></linearGradient>
          <clipPath id="cl-clip"><path class="cl-grasa-clip"/></clipPath>
          <pattern id="cl-rayas" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="9" stroke="rgba(242,239,232,.22)" stroke-width="1"/></pattern>
        </defs>
        <rect x="0" y="320" width="800" height="60" fill="#3a1820"/>
        <rect x="0" y="320" width="800" height="60" fill="url(#cl-rayas)"/>
        <line x1="0" y1="320.5" x2="800" y2="320.5" stroke="rgba(242,239,232,.35)" stroke-width="1"/>
        <path class="cl-grasa" fill="rgba(242,239,232,.03)"/>
        <g class="cl-celulas" clip-path="url(#cl-clip)"></g>
        <rect class="cl-frio" x="225" y="0" width="350" height="320" fill="url(#cl-g-frio)" clip-path="url(#cl-clip)"/>
        <path class="cl-piel" fill="none" stroke="#D8D0C3" stroke-width="9" stroke-linecap="round"/>
        <path class="cl-corchete" d="M235,40 V32 H565 V40" fill="none" stroke="#BDA47B" stroke-width="1"/>
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

<!-- 4 · RUPTURA: bloque tipográfico + botón -->
<section class="cl-sec cl-claro cl-ruptura" data-tema="claro">
  <div class="cl-in cl-ruptura-in">
    <p class="cl-bloque cl-rev" aria-label="Sin cirugía. Sin agujas. Sin pausa.">Sin cirugía.<br>Sin agujas.<br>Sin <em>pausa</em>.</p>
    <div class="cl-ruptura-cta cl-rev"><p>¿Ya sabes qué zona quieres tratar? Empieza por tu valoración médica.</p>%(btn_ruptura)s</div>
  </div>
</section>

<!-- 5 · LO QUE VAS A VIVIR -->
<section class="cl-sec cl-claro cl-vivir-sec" data-tema="claro">
  <div class="cl-in cl-dos-col">
    <header class="cl-rev"><p class="ceja">Lo que vas a vivir</p><h2 class="cl-h2">Una sesión, y tu vida <em>sigue</em>.</h2></header>
    <ol class="cl-vivir">%(vivir)s</ol>
  </div>
</section>

<!-- 6 · ¿ES PARA TI? (honesto: también decimos cuándo no) -->
<section class="cl-sec cl-oscuro" data-tema="oscuro">
  <div class="cl-in">
    <header class="cl-cabeza cl-rev"><p class="ceja">¿Es para ti?</p>
      <h2 class="cl-h2">Te decimos la <em>verdad</em>, aunque no sea criolipólisis.</h2></header>
    <div class="cl-para">
      <div class="cl-rev"><p class="cl-col-t">Es para ti si…</p><ul class="cl-si">%(si)s</ul></div>
      <div class="cl-rev"><p class="cl-col-t">No es lo tuyo si…</p><ul class="cl-no">%(no)s</ul></div>
    </div>
  </div>
</section>

<!-- 7 · POR QUÉ EN NOON: primero un médico -->
<section class="cl-sec cl-claro" data-tema="claro">
  <div class="cl-in cl-medico">
    <figure class="cl-med-foto cl-rev"><img src="%(foto_med)s" alt="%(med_nombre)s, %(med_rol)s de noon Clinic" loading="lazy"></figure>
    <div class="cl-rev">
      <p class="ceja">Por qué en noon</p>
      <h2 class="cl-h2">Antes del frío, un <em>médico</em>.</h2>
      <p class="cl-texto">La criolipólisis funciona cuando se indica bien. Por eso en noon no empieza en la máquina: empieza en tu valoración.</p>
      <ul class="cl-razones">
        <li><b>Valoración médica primero.</b> Con la %(med_nombre)s, %(med_rol)s: revisa la zona, tu historia y si eres candidata.</li>
        <li><b>Tu plan por escrito.</b> Qué zonas, cuántas sesiones, cada cuánto y qué resultado esperar.</li>
        <li><b>Te volvemos a ver.</b> Control entre la semana 8 y la 12 para medir el resultado contigo.</li>
      </ul>
      <a class="cl-pill cl-pill-linea" href="especialistas#%(med_slug)s">Conocer a la especialista</a>
    </div>
  </div>
</section>

<!-- 8 · PREGUNTAS -->
<section class="cl-sec cl-claro cl-faq-sec" id="preguntas" data-tema="claro">
  <div class="cl-in cl-dos-col">
    <header class="cl-rev cl-pegado"><p class="ceja">Preguntas</p><h2 class="cl-h2">Lo que todas <em>preguntan</em>.</h2></header>
    <div class="cl-faq">%(preguntas)s</div>
  </div>
</section>

<!-- 9 · CIERRE -->
<section class="cl-cierre" data-tema="oscuro">
  <div class="cl-cierre-in cl-rev">
    <p class="ceja">noon Clinic</p>
    <h2 class="cl-cierre-h">Empieza por tu <em>valoración</em>.</h2>
    <p class="cl-texto">Te decimos qué se puede lograr en tu zona, cuántas sesiones necesitas y si eres candidata. Sin compromiso de hacerte el tratamiento.</p>
    <div class="cl-acciones">%(btn_cierre)s</div>
    <p class="cl-nota">La valoración no se abona al tratamiento y su valor no se devuelve. <a href="terminos-y-condiciones">Términos y condiciones</a></p>
  </div>
</section>

</main>
<footer class="cl-pie" data-tema="claro">
  <div class="cl-pie-in">
    <a class="cl-logo" href="./"><img src="assets/logo-noon.png" alt="noon Clinic" width="900" height="295" loading="lazy"></a>
    <div><p class="cl-mini">Clínica</p><p>Cirugía plástica y medicina estética, con criterio.<br>Medellín, Colombia.</p></div>
    <div><p class="cl-mini">Contacto</p><p><a href="%(wa)s" target="_blank" rel="noopener">WhatsApp %(tel)s</a></p></div>
    <nav><p class="cl-mini">noon</p><a href="./">Conoce noon</a><a href="medicina-estetica">Medicina estética</a><a href="especialistas">Especialistas</a><a href="terminos-y-condiciones">Términos</a></nav>
  </div>
  <p class="cl-legal">La información de esta página es orientativa y no reemplaza una consulta médica. Los resultados varían de una persona a otra. Foto: sombre en Unsplash. © noon Clinic</p>
</footer>
<div class="cl-barra" aria-hidden="true">%(btn_barra)s</div>
<script src="assets/criolipolisis.js?v=%(v)s" defer></script>
</body>
</html>
""" % {"titulo": escape(TITULO), "desc": escape(DESCRIPCION), "seo": seo, "v": v, "wa": _wa(b), "tel": b.TELEFONO, "insignia": insignia * 2,
       "btn_hero": _boton(b, "Quiero mi valoración", "cl-pill cl-pill-lleno"), "btn_ruptura": _boton(b, "Quiero mi valoración", "cl-pill cl-pill-lleno"),
       "btn_cierre": _boton(b, "Quiero mi valoración", "cl-pill cl-pill-lleno"), "btn_barra": _boton(b, "Quiero mi valoración", "cl-pill cl-pill-lleno"),
       "filas_z": filas_z, "botones_e": botones_e, "textos_e": textos_e, "pasos": pasos,
       "vivir": vivir, "si": si, "no": no, "preguntas": preguntas,
       "foto_med": foto_med, "med_nombre": med["nombre"], "med_rol": med["rol"].lower(), "med_slug": med["slug"]}

    with open(os.path.join(b.AQUI, ARCHIVO), "w", encoding="utf-8") as f:
        f.write(html)
    b.HECHAS.append(ARCHIVO)
    return ARCHIVO
