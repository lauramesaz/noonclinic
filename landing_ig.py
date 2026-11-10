# -*- coding: utf-8 -*-
# noon Clinic · PÁGINA DE LA BIO DE INSTAGRAM (noon.clinic/ig)
# Sale de la propuesta del 3-nov (_propuestas-ig/ig.html, estilo "A · Blanco y arco" de las promos) con los 2 cambios del plan
# del Comercializador Digital (4-nov-2026, "Lo que hago HOY", punto 6):
#   1. el botón "Bótox" pasa a "Líneas de expresión con la Dra. Valeria" (en publicidad no se nombra el medicamento: INVIMA);
#   2. quinto botón "¿Vienes en diciembre?" → /promos/vienes-en-diciembre (página de otro frente del mismo plan).
# Por qué: del 6-oct al 2-nov las visitas desde Instagram escribieron por WhatsApp mucho más que las de Google pagado
# (9 WhatsApp de 60 visitas frente a 37 de 594). Esta página lleva directo a lo que más se vende, en un toque.
# Los WhatsApp dicen "vengo de Instagram" (excepción al MENSAJE_WA único, decidida en el plan) para contar los chats de Instagram.
# Medición como el resto de la web: cabecera HEAD_MEDICION_WEB (Tag Manager → clic_whatsapp en GA4), la conversión de Ads
# la manda SOLO assets/medicion-ads.js (una por clic; antes iba doble) y Clarity; además el dataLayer lleva origen "instagram-bio" y el botón tocado.
# Sin menú, noindex y fuera del sitemap (no usa pagina()). CSS y JS en línea: no mueve la versión ?v= de la web.
import os
from html import escape
from urllib.parse import quote

ARCHIVO = "ig.html"
ORIGEN = "instagram-bio"
UTM = "utm_source=instagram&utm_medium=bio"
FLECHA = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# (título, línea chica, destino, mensaje de WhatsApp o None, clave para la medición, principal)
OPCIONES = [
    ("Promos de cirugía de fin de año", "Lipo, senos, abdomen, rostro. Precio con todo incluido.", "/promos/", None, "promos", True),
    ("Líneas de expresión con la Dra. Valeria", "Médica estética · cita por WhatsApp.", None,
     "Hola, vengo de Instagram y quiero mi cita de líneas de expresión", "lineas-de-expresion", False),
    ("Criolipólisis", "Grasa localizada, sin cirugía. Haz el test: ¿eres candidata?", "/criolipolisis", None, "criolipolisis", False),
    ("Agendar mi valoración", "Cirugía plástica o medicina estética.", None,
     "Hola, vengo de Instagram y quiero mi valoración", "valoracion", False),
    ("¿Vienes en diciembre?", "Valoración virtual si vives afuera.", "/promos/vienes-en-diciembre", None, "vienes-en-diciembre", False),
]
SELLOS = ["Cirujano plástico con registro en ReTHUS", "Cirugías en quirófano", "Póliza de complicaciones"]

CSS = r"""
[hidden]{display:none!important}
:root{--tinta:#1d1d1f;--tenue:#65656a;--calido:#8c8072;--marfil:#f6f1ea;--linea:#e8e2d8;--champan:#c9a876;--verde:#34c759;
  --display:"Jost",Futura,"Century Gothic",sans-serif;--texto:"Nunito Sans",-apple-system,"Helvetica Neue",Arial,sans-serif;--suave:cubic-bezier(.2,.8,.2,1)}
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0}
body{color:var(--tinta);font:400 16px/1.5 var(--texto);-webkit-font-smoothing:antialiased;
  background:url(/assets/grano-claro.png),radial-gradient(60% 40% at 90% 0%,#f6efe4 0%,rgba(246,239,228,0) 70%),#fff;min-height:100vh}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--champan);outline-offset:3px}
.caja{max-width:520px;margin:0 auto;padding:22px 20px 40px}
.cab{display:flex;align-items:center;justify-content:space-between}
.cab img{height:30px;width:auto;display:block}
.cab span{font:500 12px/1 var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--tenue)}
.portada{display:grid;grid-template-columns:1fr 96px;gap:16px;align-items:end;margin:22px 0 18px}
.ceja{display:inline-flex;align-items:center;gap:8px;font:500 12.5px/1 var(--display);letter-spacing:.04em;color:#7d6f5a;background:var(--marfil);border-radius:999px;padding:7px 12px;margin:0 0 14px}
.ceja::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--champan)}
h1{margin:0;font:600 clamp(26px,7.2vw,36px)/1.05 var(--display);letter-spacing:-.035em;text-wrap:balance}
h1 span{display:block;color:var(--calido)}
.arco{width:96px;height:128px;border-radius:48px 48px 16px 16px;overflow:hidden;background:var(--marfil)}
.arco img{width:100%;height:100%;object-fit:cover;object-position:50% 20%;display:block}
.opciones{display:grid;gap:10px;margin:0;padding:0;list-style:none}
.op{display:grid;grid-template-columns:1fr auto;align-items:center;gap:14px;min-height:64px;padding:15px 16px 15px 20px;border-radius:22px;background:var(--marfil);transition:transform .35s var(--suave),background .3s}
.op:active,.op:hover{transform:translateY(-2px);background:#efe7db}
.op b{display:block;font:600 18px/1.2 var(--display);letter-spacing:-.02em;text-wrap:balance}
.op small{display:block;margin-top:4px;color:var(--tenue);font-size:14px;line-height:1.35}
.op .flecha{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:#fff;flex:none}
.op.principal{background:var(--tinta);color:#fff}
.op.principal small{color:#c9c4bb}
.op.principal .flecha{background:rgba(255,255,255,.14)}
.op.principal:hover{background:#000}
.ico{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.wa-ok{display:flex;align-items:center;gap:8px;margin:12px 2px 0;color:var(--tenue);font-size:13.5px}
.wa-ok::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--verde)}
.sellos{display:flex;flex-wrap:wrap;gap:8px;margin:28px 0 0;padding:0;list-style:none}
.sellos li{font-size:13.5px;color:#5c5650;border:1px solid var(--linea);border-radius:999px;padding:7px 12px;background:rgba(255,255,255,.7)}
.pie{margin-top:26px}
.mas{display:flex;justify-content:space-between;gap:12px;padding-top:18px;border-top:1px solid var(--linea);font:500 14px/1.3 var(--display)}
.mas a{text-decoration:underline;text-decoration-color:var(--champan);text-decoration-thickness:1.5px;text-underline-offset:5px}
.legal{margin:22px 0 0;color:#8e8a84;font-size:12px}
"""

JS = r"""<script>(function () {
  // medición: el clic a WhatsApp ya lo cuenta la cabecera (clic_whatsapp en GA4) y medicion-ads.js (conversión de Ads, una sola).
  // Antes de ese aviso se deja en el dataLayer el origen y el botón; los botones que van a otra página de noon, como clic_bio.
  addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest(".op") : null;
    if (!a) return;
    var esWa = a.classList.contains("wa"), boton = a.getAttribute("data-origen") || "";
    var dl = (window.dataLayer = window.dataLayer || []);
    if (esWa) dl.push({origen: "__ORIGEN__", boton: boton});
    else dl.push({event: "clic_bio", origen: "__ORIGEN__", boton: boton});
    try { if (window.clarity) { clarity("event", esWa ? "clic_whatsapp" : "clic_bio"); clarity("set", "boton_bio", boton); } } catch (_) {}
  }, true);
})();</script>"""


def _pagina(b):
    doc = [e for e in b.ESPECIALISTAS if e["area"] == "cirugia"][0]
    doc_web = "/assets/equipo/" + doc["foto"].rsplit(".", 1)[0] + ".webp"
    ops = []
    for titulo, chica, destino, msj, clave, principal in OPCIONES:
        if msj:
            href = "https://wa.me/" + b.WHATSAPP + "?text=" + quote(msj)
            extra = ' target="_blank" rel="noopener"'
            clase = "op wa"
        else:
            href = destino + ("&" if "?" in destino else "?") + UTM
            extra = ""
            clase = "op"
        if principal:
            clase += " principal"
        ops.append('<li><a class="%s" href="%s"%s data-origen="%s"><span><b>%s</b><small>%s</small></span><span class="flecha">%s</span></a></li>' % (
            clase, escape(href), extra, clave, escape(titulo), escape(chica), FLECHA))
    sellos = "".join("<li>%s</li>" % escape(s) for s in SELLOS)
    tel = b.TEL_VISIBLE.replace("+57 ", "")
    clarity = ('<script>addEventListener("load",function(){setTimeout(function(){(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;'
               't.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");'
               'clarity("set","idioma","es");clarity("set","pagina","ig");clarity("set","tipo","bio");clarity("set","origen","%s");},1200)});</script>') % (b.CLARITY_ID, ORIGEN)
    desc = "Cirugía plástica y medicina estética en Medellín. Escríbenos por WhatsApp."
    return f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<script>window.dataLayer=window.dataLayer||[];dataLayer.push({{origen:"{ORIGEN}"}});</script>
{b.HEAD_MEDICION_WEB}
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>noon Clinic · Medellín</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="noon Clinic">
<meta property="og:title" content="noon Clinic · Medellín">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{b.DOMINIO}/assets/equipo/{doc["foto"]}">
<meta property="og:locale" content="es_CO">
{clarity}
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/assets/favicon.png">
{b.FUENTES.replace("assets/fuentes/", "/assets/fuentes/")}
<style>{CSS}</style>
</head>
<body>
<main class="caja">
  <header class="cab"><img src="/assets/logo-noon-s.webp" alt="noon Clinic" width="360" height="118"><span>Medellín</span></header>

  <section class="portada">
    <div>
      <p class="ceja">Desde Instagram</p>
      <h1>¿Qué te gustaría hacer? <span>Te respondemos por WhatsApp.</span></h1>
    </div>
    <div class="arco"><img src="{doc_web}" alt="{doc["nombre"]}, cirujano plástico de noon Clinic" width="900" height="1125"></div>
  </section>

  <section id="instagram-bio" aria-label="Opciones">
    <ul class="opciones">
      {"".join(ops)}
    </ul>
    <p class="wa-ok">Escríbenos por WhatsApp: {tel}</p>
  </section>

  <ul class="sellos">{sellos}</ul>

  <footer class="pie">
    <div class="mas"><a href="/?{escape(UTM)}">Ver todos los tratamientos</a><a href="/especialistas?{escape(UTM)}">Especialistas</a></div>
    <p class="legal">Todo procedimiento tiene riesgos y los resultados varían en cada persona. Toda indicación requiere valoración médica.</p>
  </footer>
</main>
{JS.replace("__ORIGEN__", ORIGEN)}
<script src="/assets/medicion-ads.js?v={b.V}" defer></script>
</body>
</html>
"""


def generar(b):
    """b = módulo build (WHATSAPP, TEL_VISIBLE, DOMINIO, CLARITY_ID, HEAD_MEDICION, FUENTES, ESPECIALISTAS, V, AQUI).
    Crea ig.html en la raíz (noon.clinic/ig)."""
    with open(os.path.join(b.AQUI, ARCHIVO), "w", encoding="utf-8") as f:
        f.write(_pagina(b))
    return ARCHIVO
