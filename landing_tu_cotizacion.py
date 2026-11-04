# -*- coding: utf-8 -*-
# noon Clinic · PÁGINA "TU COTIZACIÓN" (noon.clinic/tu-cotizacion) · para cerrar después de la valoración.
# Plan del Comercializador Digital (4-nov-2026, "Lo que hago HOY", punto 1): la comercial la manda junto con cada cotización
# y en el primer mensaje de seguimiento. En una sola página responde lo que hoy se pregunta por chat: qué va en el precio,
# cómo separar la fecha, qué pasa si se arrepiente y cómo comparar. Hace el trabajo de la "hoja 2 del PDF" sin tocar el cotizador.
# DISEÑO de las promos ("A · Blanco y arco", assets/promos.css): blanco con grano, letra grande y apretada con la 2.ª línea en
# gris cálido, foto en ARCO, píldoras y un solo contraste (el botón negro). Sin menú. noindex y fuera del sitemap (no usa pagina()).
# DATOS: solo lo respaldado por los términos (datos.py: VALORACION, RETENCION, FECHA_LIMITE y TERMINOS 3, 4 y 5), por /promos
# (landing_promos.py) y por la página de pagos ("según tu plan por escrito"). El abono de $1.000.000 es la regla de la
# capacitación (capacitacion.py); la devolución sale de ahí y de la retención de los términos (sobre 1.000.000 → 800.000).
# QUITADO por falta de respaldo (4-nov): "Tu cotización está vigente 3 meses": los términos no lo dicen (solo el PDF del cotizador).
# CSS y JS en línea (no en assets/) para no mover la versión ?v= de las 200 páginas de la web. build.py llama a generar() al final.
import os, re, json
from html import escape
from urllib.parse import quote
from landing_promos import ico, RETHUS

ARCHIVO = "tu-cotizacion.html"
ORIGEN = "tu-cotizacion"   # origen de la medición (dataLayer y Clarity)
MSJ_SEPARAR = "Hola, ya tengo mi cotización de noon y quiero separar mi fecha"
MSJ_COMPARAR = "Hola, quiero que me ayuden a comparar una cotización"
ABONO = 1000000            # abono para separar la fecha (capacitacion.py: "El paciente abona su cirugía: $1.000.000")
FOTO_PORTADA = "/assets/clinica/recepcion.webp"   # la recepción real de noon, con el logo
FOTO_OG = "/assets/clinica/recepcion.jpg"         # para la vista previa del enlace en WhatsApp
# Video de 30 segundos del Dr. Fer (guion en el plan, sección 8.4). Mientras el archivo no exista, el espacio queda oculto;
# cuando lo grabe: se guarda con este nombre, se corre build.py y aparece solo.
VIDEO = "/assets/equipo/fernando-ruiz-30s.mp4"
GUIA_CIUDADES = "/operarte-en-medellin-desde-bogota-cali-o-barranquilla"
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}

ICONOS = {
    "mas": '<path d="M12 6.5v11M6.5 12h11"/>',
    "menos": '<path d="M6.5 12h11"/>',
}


def _ico(nombre, clase="ico"):
    if nombre in ICONOS:
        return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (clase, ICONOS[nombre])
    return ico(nombre, clase)


def pesos(n):
    return "$" + format(n, ",").replace(",", ".")


def _wa(b, msj):
    return "https://wa.me/" + b.WHATSAPP + "?text=" + quote(msj)


def _fecha_iso(texto):
    """'15 de enero de 2027' → ('2027-01-15', '15 de enero')."""
    d, mes, a = re.match(r"(\d+) de (\w+) de (\d{4})", texto).groups()
    return "%s-%02d-%02d" % (a, MESES[mes], int(d)), "%s de %s" % (d, mes)


# ---------------------------------------------------------------- textos (bloques del plan, tal cual, salvo lo quitado)
SIEMPRE = [
    ("Honorarios del cirujano plástico", ""),
    ("Instrumentador", ""),
    ("Quirófano con anestesia", "En Medellín trae la consulta preanestésica y los honorarios de anestesia."),
    ("Póliza de complicaciones", ""),
]
SEGUN = [
    ("Bomba de dolor", ""),
    ("Prenda posquirúrgica", "Faja o brasier."),
    ("Implantes", ""),
    ("Masajes", ""),
]
COMPARAR = [
    "¿Tu cirujano es cirujano plástico y aparece en el ReTHUS?",
    "¿Te operan en un quirófano habilitado o en un consultorio?",
    "¿El precio trae la anestesia?",
    "¿Trae póliza de complicaciones?",
    "¿Trae bomba de dolor, prenda y, si aplica, implantes y masajes?",
]
INDICE = [("incluye", "Qué incluye"), ("separar", "Cómo separar"), ("si-cambias", "Si cambio de opinión"),
          ("comparar", "Comparar"), ("cirujano", "Mi cirujano"), ("preguntas", "Preguntas")]


def _preguntas(b, abono, limite_corto):
    return [
        ("¿Me va a doler?", "Vas a sentir molestia los primeros días. Para eso es la bomba de dolor: da analgesia continua en los "
         "días más incómodos. Tu cotización dice si la tuya la lleva; en las promos de fin de año va incluida."),
        ("¿Puedo pagar por partes?", "Sí. Separas con %s y el saldo lo pagas según el plan que te damos por escrito, siempre "
         "completo antes de tu cirugía." % abono),
        ("¿Con qué medios pago?", "Escríbenos y te contamos los medios de pago disponibles."),
        ("Vengo de otra ciudad, ¿cómo hago?", 'Te organizamos las fechas para que todo quede en un mismo viaje. '
         '<a href="%s">Lee la guía para venir desde Bogotá, Cali o Barranquilla</a>.' % GUIA_CIUDADES),
        ("¿Puedo cambiar la fecha?", "Sí, avisando con anticipación por WhatsApp. La nueva fecha depende del quirófano y, si tu "
         "cirugía es de promo, tiene que ser antes del %s." % limite_corto),
    ]


CSS = r"""
[hidden] { display: none !important; }
.tc .pr-portada h1 { font-size: clamp(44px, 5.8vw, 80px); }
.tc-baja { margin: 24px 0 30px; max-width: 480px; color: var(--tenue); font-size: clamp(17px, 1.45vw, 19px); }
.tc .pr-portada .pr-arco > img { object-position: 50% 42%; }
.tc .pr-atajos p { margin-bottom: 12px; }
.tc-sec-cab { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 18px 40px; margin-bottom: clamp(26px, 4vw, 44px); }
.tc-sec-cab .pr-cabeza { margin-bottom: 0; }
.tc-sec-cab .tc-lead { max-width: 380px; margin: 0; color: var(--tenue); font-size: 16px; }

/* 2 · lo que va en tu precio */
.tc-inc { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.tc-caja { padding: clamp(24px, 3vw, 34px); border-radius: 28px; background: #fff; }
.tc-caja-cab { display: flex; align-items: baseline; justify-content: space-between; gap: 6px 16px; flex-wrap: wrap; }
.tc-caja h3 { font-size: 23px; letter-spacing: -.02em; }
.tc-caja-cab p { margin: 0; font-size: 14.5px; color: var(--tenue); }
.tc-items { list-style: none; margin: 22px 0 0; padding: 0; display: grid; gap: 0; }
.tc-items li { display: flex; gap: 14px; align-items: flex-start; padding: 14px 0; border-top: 1px solid var(--linea); }
.tc-items li:first-child { border-top: 0; padding-top: 4px; }
.tc-items .ico { width: 26px; height: 26px; padding: 5px; margin-top: 1px; border-radius: 50%; background: var(--tinta); color: #fff; stroke-width: 2.6; }
.tc-items.tc-seg .ico { background: var(--marfil); color: var(--tinta); stroke-width: 2.2; }
.tc-items b { display: block; font: 600 17.5px/1.3 var(--display); letter-spacing: -.01em; }
.tc-items span { display: block; margin-top: 3px; color: var(--tenue); font-size: 15px; line-height: 1.45; }
.tc-nota { margin: 18px 6px 0; max-width: 820px; font-size: 15px; color: var(--tenue); }
.tc-no { display: grid; grid-template-columns: minmax(0, .8fr) minmax(0, 2fr); gap: 10px 32px; align-items: center; max-width: var(--max); margin: 14px auto 0; padding: 24px 30px; border-radius: 28px; background: var(--gris); }
.tc-no h3 { display: flex; align-items: center; gap: 12px; font-size: 19px; letter-spacing: -.01em; }
.tc-no h3 .ico { width: 30px; height: 30px; padding: 6px; border-radius: 50%; background: #fff; stroke-width: 2.2; }
.tc-no p { margin: 0; font-size: 16px; color: var(--tenue); }

/* 4 · separa tu fecha */
.tc-pasos { list-style: none; margin: 0 auto; padding: 0; max-width: var(--max); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.tc-pasos li { padding: 28px 26px 30px; border-radius: 28px; background: var(--gris); }
.tc-pasos .pr-pn { margin: 0 0 20px; width: 48px; height: 48px; box-shadow: none; background: #fff; font-size: 18px; }
.tc-pasos li:nth-child(2) .pr-pn { background: var(--tinta); color: #fff; }
.tc-pasos h3 { margin-bottom: 8px; font-size: 22px; letter-spacing: -.02em; }
.tc-pasos p { margin: 0; color: var(--tenue); font-size: 16px; }
.tc-fecha { display: flex; flex-wrap: wrap; align-items: center; gap: 18px 44px; max-width: var(--max); margin: 14px auto 0; padding: 26px 32px; border-radius: 28px; background: var(--marfil); }
.tc-cuenta { display: grid; grid-template-columns: auto auto; grid-template-areas: "f f" "n u"; justify-content: start; align-items: end; gap: 6px 14px; margin: 0; padding-right: 44px; border-right: 1px solid var(--marfil-2); }
.tc-cuenta-f { grid-area: f; font: 500 13px/1 var(--display); letter-spacing: .1em; text-transform: uppercase; color: var(--tenue); }
.tc-cuenta b { grid-area: n; font: 600 clamp(60px, 6vw, 78px)/.84 var(--display); letter-spacing: -.045em; }
.tc-cuenta-u { grid-area: u; padding-bottom: 2px; font: 500 17px/1.25 var(--display); color: var(--tenue); }
.tc-cuenta-u span { color: var(--tinta); font-weight: 600; }
.tc-lineas { flex: 1; min-width: 260px; list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
.tc-lineas li { display: flex; gap: 10px; align-items: flex-start; font-size: 16px; }
.tc-lineas li::before { content: ""; flex: none; width: 6px; height: 6px; margin-top: 10px; border-radius: 50%; background: var(--champan); }

/* 5 · si cambias de opinión */
.tc-cambio { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(28px, 5vw, 80px); align-items: center; max-width: var(--max); margin: 0 auto; }
.tc-cambio .pr-cabeza { margin-bottom: 0; }
.tc-cambio-txt { margin: 22px 0 0; max-width: 500px; font-size: clamp(17px, 1.4vw, 19px); color: var(--tenue); }
.tc-cambio-txt b { color: var(--tinta); font-weight: 600; }
.tc-cascada { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
.tc-cascada li { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 22px 26px; border-radius: 24px; background: var(--gris); }
.tc-cascada span { font-size: 16px; color: var(--tenue); line-height: 1.35; }
.tc-cascada b { font: 600 clamp(26px, 2.6vw, 32px)/1 var(--display); letter-spacing: -.03em; white-space: nowrap; }
.tc-cascada .tc-vuelve { background: var(--marfil); box-shadow: inset 0 0 0 1.5px var(--champan); }
.tc-cascada .tc-vuelve span { color: var(--tinta); }
.tc-cascada .tc-flecha { justify-content: center; padding: 0; background: transparent; height: 18px; color: var(--calido); }
.tc-cascada .tc-flecha .ico { transform: rotate(90deg); width: 18px; height: 18px; }
.tc-cascada .tc-val { background: transparent; box-shadow: inset 0 0 0 1px var(--linea); }
.tc-link-tc { margin-top: 20px; }

/* 6 · comparar */
.tc-comparar { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: clamp(28px, 5vw, 72px); align-items: center; }
.tc-comparar .pr-cabeza { margin-bottom: 30px; }
.tc-check { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
.tc-check li { display: flex; gap: 14px; align-items: center; padding: 16px 20px 16px 16px; border-radius: 22px; background: #fff; font: 500 17px/1.35 var(--display); letter-spacing: -.005em; }
.tc-check li span { display: grid; place-items: center; flex: none; width: 32px; height: 32px; border-radius: 50%; background: var(--gris); font: 600 13.5px/1 var(--display); }
.tc-tapa { display: flex; align-items: center; gap: 8px; margin: 14px 0 0; font-size: 14.5px; color: var(--tenue); }
.tc-tapa i { flex: none; width: 7px; height: 7px; border-radius: 50%; background: var(--champan); }

/* 7 · tu cirujano */
.tc-doc-txt { margin: 22px 0 28px; max-width: 520px; font-size: clamp(17px, 1.4vw, 19px); color: var(--tenue); }
.tc-doc-txt b { color: var(--tinta); font-weight: 600; }
.tc-rethus { display: flex; flex-wrap: wrap; align-items: center; gap: 12px 18px; }
.tc-rethus .pr-btn-borde { gap: 10px; background: #fff; border-color: #d9d4cc; min-height: 50px; padding: 0 22px; font-size: 15px; }
.tc-rethus .pr-btn-borde .ico { width: 18px; height: 18px; }
.tc-rethus small { font-size: 14px; color: var(--tenue); }
.tc-video { margin: 28px 0 0; max-width: 300px; }
.tc-video video { display: block; width: 100%; height: auto; aspect-ratio: 9 / 16; object-fit: cover; border-radius: 26px; background: var(--gris); }
.tc-video figcaption { margin-top: 10px; font-size: 14px; color: var(--tenue); }

/* 8 · preguntas */
.tc .pr-preg p a { color: var(--tinta); text-decoration-color: var(--champan); text-underline-offset: 3px; }

/* 9 · cierre */
.tc .pr-cierre .pr-ya { justify-content: center; }

@media (max-width: 960px) {
  .tc-inc, .tc-comparar, .tc-cambio { grid-template-columns: 1fr; }
  .tc-pasos { grid-template-columns: 1fr; }
  .tc-no { grid-template-columns: 1fr; }
}
@media (max-width: 760px) {
  .tc .pr-portada h1 { font-size: clamp(36px, 10.4vw, 42px); }
  .tc-baja { margin: 16px 0 22px; font-size: 17px; }
  .tc .pr-portada-txt { text-align: left; }
  .tc .pr-atajos p { display: none; }
  .tc-sec-cab { margin-bottom: 22px; }
  .tc-caja { border-radius: 24px; padding: 22px 18px 10px; }
  .tc-items li { padding: 13px 0; }
  .tc-nota { margin: 16px 4px 0; font-size: 14.5px; }
  .tc-no { padding: 20px 20px 22px; border-radius: 24px; }
  .tc-pasos li { display: grid; grid-template-columns: 44px minmax(0, 1fr); gap: 0 16px; align-items: start; padding: 20px 18px 22px; border-radius: 24px; }
  .tc-pasos .pr-pn { grid-row: 1 / 3; width: 44px; height: 44px; margin: 0; }
  .tc-pasos h3 { font-size: 20px; margin: 9px 0 6px; }
  .tc-fecha { flex-direction: column; align-items: flex-start; gap: 14px; padding: 22px 20px 24px; border-radius: 24px; }
  .tc-cuenta { padding: 0 0 16px; border-right: 0; border-bottom: 1px solid var(--marfil-2); width: 100%; }
  .tc-cuenta b { font-size: 64px; }
  .tc-lineas { min-width: 0; }
  .tc-cascada li { padding: 18px 18px 18px 20px; border-radius: 20px; }
  .tc-cascada b { font-size: 26px; }
  .tc-check li { padding: 14px 16px 14px 12px; font-size: 16px; border-radius: 18px; }
  .tc-comparar .pr-btn { width: 100%; text-align: center; line-height: 1.25; }
  .tc .pr-ya, .tc-tapa { display: block; text-align: left; font-size: 14px; }
  .tc .pr-ya i, .tc-tapa i { display: inline-block; vertical-align: 1px; margin-right: 8px; }
  .tc .pr-cierre .pr-ya { text-align: center; }
  .tc-rethus .pr-btn-borde { width: 100%; justify-content: center; }
  .tc-video { max-width: 240px; margin-left: auto; margin-right: auto; }
}
"""

JS = r"""<script>(function () {
  var D = document, H = D.documentElement;
  var captura = /[?&]captura/.test(location.search);
  if (captura) H.classList.add("captura");
  var quieto = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $$(s) { return Array.prototype.slice.call(D.querySelectorAll(s)); }
  function marcar(n, v) { if (!window.clarity) return; if (v === undefined) clarity("event", n); else clarity("set", n, v); }

  // cuenta regresiva hasta la fecha límite de los términos (se calcula en el navegador; desaparece al llegar)
  var fin = new Date("__FIN__T00:00:00-05:00").getTime();  // hora de Colombia
  var dias = Math.ceil((fin - Date.now()) / 864e5);
  if (dias > 0) {
    // "Faltan 10 semanas para el 15 de enero" · en las 2 últimas semanas, en días · "Falta 1 día" el último
    var n = dias >= 14 ? Math.floor(dias / 7) : dias, u = dias >= 14 ? "semanas" : (dias > 1 ? "días" : "día");
    $$("[data-cuenta-f]").forEach(function (e) { e.textContent = dias > 1 ? "Faltan" : "Falta"; });
    $$("[data-cuenta-n]").forEach(function (e) { e.textContent = n; });
    $$("[data-cuenta-u]").forEach(function (e) { e.textContent = u; });
    $$("[data-cuenta]").forEach(function (e) { e.hidden = false; });
  }

  // cabecera con sombra al bajar + barra fija en celular (aparece al pasar la portada, se esconde en el cierre)
  var cab = D.querySelector(".pr-cab"), barra = D.querySelector(".pr-barra"), portada = D.querySelector(".pr-portada"), cierre = D.querySelector(".pr-cierre");
  var enCierre = false;
  function alBajar() {
    var y = window.scrollY || window.pageYOffset;
    cab.classList.toggle("solida", y > 10);
    var on = y > portada.offsetHeight * 0.8 && !enCierre;
    barra.classList.toggle("on", on);
    barra.setAttribute("aria-hidden", on ? "false" : "true");
  }
  if ("IntersectionObserver" in window && cierre) new IntersectionObserver(function (e) { enCierre = e[0].isIntersecting; alBajar(); }, {threshold: 0.1}).observe(cierre);
  addEventListener("scroll", alBajar, {passive: true});
  alBajar();

  // aparición suave
  var revs = $$(".pr-rev");
  if ("IntersectionObserver" in window && !quieto && !captura) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, {rootMargin: "0px 0px -6% 0px", threshold: 0.06});
    revs.forEach(function (e) { io.observe(e); });
  } else revs.forEach(function (e) { e.classList.add("on"); });

  // medición: el clic a WhatsApp ya lo cuenta la cabecera (clic_whatsapp en GA4 + conversión de Ads) y medicion-ads.js.
  // Antes de ese aviso se deja en el dataLayer de dónde viene (origen) y qué botón fue; en Clarity, el evento y el botón.
  addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="wa.me/"]') : null;
    if (!a) return;
    var boton = a.getAttribute("data-wa") || "";
    (window.dataLayer = window.dataLayer || []).push({origen: "__ORIGEN__", boton: boton});
    marcar("clic_whatsapp"); marcar("boton_wa", boton);
  }, true);
})();</script>"""


def _pagina(b):
    abono = pesos(ABONO)
    ret = int(b.RETENCION.strip().rstrip("%"))
    devolucion = pesos(ABONO * (100 - ret) // 100)       # 20 % de retención sobre 1.000.000 → 800.000
    fin_iso, fin_corto = _fecha_iso(b.FECHA_LIMITE)        # 15 de enero de 2027
    wa_sep = _wa(b, MSJ_SEPARAR)
    wa_comp = _wa(b, MSJ_COMPARAR)
    flecha = ico("flecha", "ico-f")
    doc = [e for e in b.ESPECIALISTAS if e["area"] == "cirugia"][0]
    doc_web = "/assets/equipo/" + doc["foto"].rsplit(".", 1)[0] + ".webp"
    titulo = "Tu cotización · noon Clinic"
    desc = "Qué ya va en tu precio, cómo separar tu fecha y qué preguntar si estás comparando."

    siempre = "".join('<li>%s<div><b>%s</b>%s</div></li>' % (ico("check"), t, '<span>%s</span>' % d if d else "") for t, d in SIEMPRE)
    segun = "".join('<li>%s<div><b>%s</b>%s</div></li>' % (_ico("mas"), t, '<span>%s</span>' % d if d else "") for t, d in SEGUN)
    comparar = "".join('<li><span>%d</span>%s</li>' % (i, escape(q)) for i, q in enumerate(COMPARAR, 1))
    preguntas = "".join('<details class="pr-preg pr-rev"><summary>%s<span class="pr-mas" aria-hidden="true"></span></summary><p>%s</p></details>' % (p, r)
                        for p, r in _preguntas(b, abono, fin_corto))
    indice = "".join('<a class="pr-pill" href="#%s">%s</a>' % (k, n) for k, n in INDICE)
    hay_video = os.path.exists(os.path.join(b.AQUI, VIDEO.lstrip("/")))
    video = ('<figure class="tc-video"%s><video controls playsinline preload="none" poster="%s" width="1080" height="1920"%s>'
             'Tu navegador no puede mostrar este video.</video><figcaption>%s te cuenta qué estás pagando, en 30 segundos.</figcaption></figure>') % (
        "" if hay_video else " hidden", doc_web, (' src="%s"' % VIDEO) if hay_video else "", doc["nombre"])

    clarity = ('<script>addEventListener("load",function(){setTimeout(function(){(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;'
               't.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");'
               'clarity("set","idioma","es");clarity("set","pagina","tu-cotizacion");clarity("set","tipo","cierre");clarity("set","origen","%s");},1200)});</script>') % (b.CLARITY_ID, ORIGEN)
    js = JS.replace("__FIN__", fin_iso).replace("__ORIGEN__", ORIGEN)

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<script>window.dataLayer=window.dataLayer||[];dataLayer.push({{origen:"{ORIGEN}"}});</script>
{b.HEAD_MEDICION}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(titulo)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="noon Clinic">
<meta property="og:title" content="Tu cotización, punto por punto">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{b.DOMINIO}{FOTO_OG}">
<meta property="og:locale" content="es_CO">
{clarity}
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/assets/favicon.png">
<script>document.documentElement.className="js"</script>
{b.FUENTES.replace("assets/fuentes/", "/assets/fuentes/")}
<link rel="preload" as="image" href="{FOTO_PORTADA}" fetchpriority="high">
<link rel="stylesheet" href="/assets/promos.css?v={b.V}">
<style>{CSS}</style>
</head>
<body class="pr tc">
<header class="pr-cab">
  <a class="pr-logo" href="/" aria-label="noon Clinic, inicio"><img src="/assets/logo-noon-s.webp" alt="noon Clinic" width="360" height="118"></a>
  <a class="pr-btn-borde" href="{wa_sep}" target="_blank" rel="noopener" data-wa="separar-cabecera">Separar mi fecha</a>
</header>
<main>

<!-- 1 · PORTADA -->
<section class="pr-portada" id="portada">
  <div class="pr-portada-in">
    <div class="pr-portada-txt">
      <p class="pr-ceja"><i></i>Cirugía plástica · noon Clinic</p>
      <h1>Tu cotización,<br><span>punto por punto.</span></h1>
      <p class="tc-baja">{desc}</p>
      <a class="pr-btn pr-btn-xl" href="{wa_sep}" target="_blank" rel="noopener" data-wa="separar-portada">Quiero separar mi fecha {flecha}</a>
      <p class="pr-ya"><i></i>Te respondemos en minutos por WhatsApp, en horario de atención.</p>
    </div>
    <figure class="pr-arco">
      <img src="{FOTO_PORTADA}" alt="Recepción de noon Clinic en Medellín" width="900" height="1200" fetchpriority="high">
      <div class="pr-doc"><img src="{doc_web}" alt="" width="900" height="1125"><div>{doc["nombre"]}<span>Tu cirujano plástico · ReTHUS</span></div></div>
    </figure>
  </div>
  <nav class="pr-atajos" aria-label="En esta página">
    <p>En esta página</p>
    <div class="pr-pills">{indice}</div>
  </nav>
</section>

<!-- 2 y 3 · LO QUE VA EN TU PRECIO / LO QUE NO VA -->
<section class="pr-sec" id="incluye">
  <div class="pr-panel pr-marfil">
    <div class="tc-sec-cab">
      <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>Lo que va en tu precio</p>
        <h2>Lo que ya va<br><span>en tu precio.</span></h2></header>
    </div>
    <div class="tc-inc">
      <div class="tc-caja pr-rev">
        <div class="tc-caja-cab"><h3>Siempre</h3><p>En todas las cotizaciones.</p></div>
        <ul class="tc-items">{siempre}</ul>
      </div>
      <div class="tc-caja pr-rev">
        <div class="tc-caja-cab"><h3>Según tu cirugía</h3><p>Tu cotización dice cuáles lleva la tuya.</p></div>
        <ul class="tc-items tc-seg">{segun}</ul>
      </div>
    </div>
    <p class="tc-nota pr-rev">En las promos de fin de año van todos los de tu cirugía. En Bogotá, la consulta preanestésica va aparte y está escrita en tu cotización.</p>
  </div>
  <div class="tc-no pr-rev">
    <h3>{_ico("menos")}Lo que no va</h3>
    <p>La valoración ({b.VALORACION}), los exámenes antes de la cirugía, los medicamentos para la casa y, si vienes de otra ciudad, tu viaje y tu hospedaje.</p>
  </div>
</section>

<!-- 4 · SEPARA TU FECHA -->
<section class="pr-sec" id="separar">
  <header class="pr-cabeza pr-centro pr-rev"><p class="pr-ceja"><i></i>Separa tu fecha</p>
    <h2>Separa tu fecha<br><span>en 3 pasos.</span></h2></header>
  <ol class="tc-pasos">
    <li class="pr-rev"><span class="pr-pn">1</span><h3>Escoge tu fecha</h3><p>Con tu asesora: te proponemos dos.</p></li>
    <li class="pr-rev"><span class="pr-pn">2</span><h3>Abona {abono}</h3><p>Reservamos a tu nombre el quirófano, el equipo quirúrgico y la póliza.</p></li>
    <li class="pr-rev"><span class="pr-pn">3</span><h3>Paga el saldo</h3><p>Según tu plan por escrito. Puede ser por partes; tiene que estar completo antes de tu cirugía.</p></li>
  </ol>
  <div class="tc-fecha pr-rev">
    <p class="tc-cuenta" data-cuenta hidden><span class="tc-cuenta-f" data-cuenta-f>Faltan</span> <b data-cuenta-n></b> <span class="tc-cuenta-u"><span data-cuenta-u></span><br> para el {fin_corto}</span></p>
    <ul class="tc-lineas">
      <li>Tu precio se respeta desde el día que abonas.</li>
      <li>Precios de fin de año: para cirugías hechas antes del {b.FECHA_LIMITE}.</li>
    </ul>
  </div>
</section>

<!-- 5 · SI CAMBIAS DE OPINIÓN -->
<section class="pr-sec" id="si-cambias">
  <div class="tc-cambio">
    <div class="pr-rev">
      <header class="pr-cabeza"><p class="pr-ceja"><i></i>Si cambias de opinión</p>
        <h2>Si cambias<br><span>de opinión.</span></h2></header>
      <p class="tc-cambio-txt">Si abonas <b>{abono}</b> y luego decides no operarte, te devolvemos <b>{devolucion}</b>. La valoración no se devuelve. Todo está en los términos y condiciones.</p>
      <a class="pr-link tc-link-tc" href="/terminos-y-condiciones#t4">Leer los términos y condiciones</a>
    </div>
    <ul class="tc-cascada pr-rev" aria-label="Ejemplo de devolución">
      <li><span>Abonas para separar tu fecha</span><b>{abono}</b></li>
      <li class="tc-flecha" aria-hidden="true">{ico("flecha")}</li>
      <li class="tc-vuelve"><span>Si decides no operarte, te devolvemos</span><b>{devolucion}</b></li>
      <li class="tc-val"><span>La valoración ({b.VALORACION}) no se devuelve.</span></li>
    </ul>
  </div>
</section>

<!-- 6 · SI ESTÁS COMPARANDO -->
<section class="pr-sec" id="comparar">
  <div class="pr-panel pr-gris tc-comparar">
    <div class="pr-rev">
      <header class="pr-cabeza"><p class="pr-ceja"><i></i>Si estás comparando</p>
        <h2>Si estás comparando,<br><span>pregunta esto.</span></h2></header>
      <a class="pr-btn" href="{wa_comp}" target="_blank" rel="noopener" data-wa="comparar">Mándanos la otra cotización y te la comparamos {flecha}</a>
      <p class="tc-tapa"><i></i>Tapa tu nombre y tu cédula antes de enviarla.</p>
    </div>
    <ol class="tc-check pr-rev">{comparar}</ol>
  </div>
</section>

<!-- 7 · TU CIRUJANO -->
<section class="pr-sec" id="cirujano">
  <div class="pr-panel pr-marfil pr-medico">
    <figure class="pr-arco pr-arco-doc pr-rev"><img src="{doc_web}" alt="{doc["nombre"]}, cirujano plástico de noon Clinic" width="900" height="1125" loading="lazy"></figure>
    <div class="pr-rev">
      <p class="pr-ceja"><i></i>Tu cirujano</p>
      <h2>{doc["nombre"]},<br><span>tu cirujano plástico.</span></h2>
      <p class="tc-doc-txt"><b>Cirujano plástico, estético y reconstructivo, con registro en ReTHUS.</b> Te opera siempre en quirófano, nunca en un consultorio.</p>
      <div class="tc-rethus">
        <a class="pr-btn-borde" href="{RETHUS}" target="_blank" rel="noopener">{ico("lupa")}Cómo verificarlo en ReTHUS</a>
        <small>Es el registro oficial del Ministerio de Salud.</small>
      </div>
      {video}
    </div>
  </div>
</section>

<!-- 8 · PREGUNTAS -->
<section class="pr-sec" id="preguntas">
  <div class="pr-faq-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>Preguntas</p><h2>Lo que más<br><span>nos preguntan.</span></h2></header>
    <div class="pr-faq">{preguntas}</div>
  </div>
</section>

<!-- 9 · CIERRE -->
<section class="pr-sec pr-cierre" id="agendar">
  <div class="pr-panel pr-marfil pr-cierre-in pr-rev">
    <p class="pr-ceja"><i></i>Tu fecha</p>
    <h2>¿Te ayudamos a<br><span>escoger tu fecha?</span></h2>
    <a class="pr-btn pr-btn-xl" href="{wa_sep}" target="_blank" rel="noopener" data-wa="separar-cierre">Quiero separar mi fecha {flecha}</a>
    <p class="pr-ya"><i></i>Te respondemos en minutos por WhatsApp, en horario de atención.</p>
  </div>
</section>

</main>
<!-- 10 · PIE -->
<footer class="pr-pie">
  <a class="pr-logo" href="/"><img src="/assets/logo-noon-s.webp" alt="noon Clinic" width="360" height="118" loading="lazy"></a>
  <nav><a href="/terminos-y-condiciones">Términos y condiciones</a><a href="{wa_sep}" target="_blank" rel="noopener" data-wa="separar-pie">WhatsApp {b.TEL_VISIBLE}</a></nav>
  <p class="pr-legal">Todo procedimiento tiene riesgos y los resultados varían en cada persona.</p>
</footer>
<div class="pr-barra" aria-hidden="true">
  <div class="pr-barra-txt"><b>Tu cotización</b><span>Separa con {abono}</span></div>
  <a class="pr-btn" href="{wa_sep}" target="_blank" rel="noopener" data-wa="separar-barra">Separar mi fecha</a>
</div>
{js}
<script src="/assets/medicion-ads.js?v={b.V}" defer></script>
</body>
</html>
"""


def generar(b):
    """b = módulo build (WHATSAPP, TEL_VISIBLE, DOMINIO, CLARITY_ID, HEAD_MEDICION, FUENTES, ESPECIALISTAS, VALORACION,
    RETENCION, FECHA_LIMITE, V, AQUI). Crea tu-cotizacion.html en la raíz (noon.clinic/tu-cotizacion)."""
    with open(os.path.join(b.AQUI, ARCHIVO), "w", encoding="utf-8") as f:
        f.write(_pagina(b))
    return ARCHIVO
