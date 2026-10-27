# -*- coding: utf-8 -*-
# noon Clinic · WhatsApp que dice "vengo de Google" en las landings de la pauta (promos/ y criolipolisis).
# Pedido de Laura (27-oct-2026): que el equipo distinga en WhatsApp qué chats vienen de Google Ads.
# Las campañas usan etiquetado automático: quien llega del anuncio trae gclid / gbraid / wbraid / gad_source en la URL.
# Se guarda una marca para la visita (sessionStorage) y los enlaces a wa.me cambian SOLO el texto (nunca el número): al
# cargar, cada vez que la página cambia un enlace en vivo y otra vez en el clic (por si acaso). Sin la marca, nada cambia.
# La medición de Ads (assets/medicion-ads.js) solo mira el número, así que la conversión sigue contando igual.
# Va EN LÍNEA en cada landing (no en assets/) para no mover la versión ?v= de las 200 páginas de la web; queda fuera de
# <main>, así que tampoco cambia la fecha del sitemap.
import json


def script(mensajes):
    """mensajes = {slug: texto}; "" = el texto cuando no hay cirugía elegida (o la landing no tiene cirugías).
    La cirugía sale de la fila donde está el botón (promos: <details class="pr-cx" data-slug>) o, si el botón es
    general, de <body data-cx> (la cirugía abierta en ese momento; promos.js la cambia al tocar otra)."""
    datos = json.dumps(mensajes, ensure_ascii=False).replace("</", "<\\/")
    return r"""<script>(function () {
  var M = %s;
  var g = /[?&](gclid|gbraid|wbraid|gad_source)=/.test(location.search);
  try { if (g) sessionStorage.setItem("noon_google", "1"); else g = sessionStorage.getItem("noon_google") === "1"; } catch (_) {}
  if (!g) return;
  function poner(a) {
    var h = a.getAttribute("href") || "";
    if (!/^https:\/\/wa\.me\/\d/.test(h)) return;
    var fila = a.closest(".pr-cx[data-slug]");
    var cx = fila ? fila.getAttribute("data-slug") : document.body.getAttribute("data-cx") || "";
    var t = "text=" + encodeURIComponent(M[cx] || M[""]);
    var nuevo = /[?&]text=/.test(h) ? h.replace(/([?&])text=[^&]*/, "$1" + t) : h + (h.indexOf("?") > -1 ? "&" : "?") + t;
    if (nuevo !== h) a.setAttribute("href", nuevo);
  }
  function alClic(e) { var a = e.target && e.target.closest ? e.target.closest("a[href]") : null; if (a) poner(a); }
  document.addEventListener("click", alClic, true);
  document.addEventListener("auxclick", alClic, true);
  // si la página cambia un enlace después (promos.js al elegir otra cirugía, el resultado del test), se corrige al instante
  if (window.MutationObserver) new MutationObserver(function (ms) {
    ms.forEach(function (m) { if (m.target.tagName === "A") poner(m.target); });
  }).observe(document.documentElement, {subtree: true, attributes: true, attributeFilter: ["href"]});
  function todos() { Array.prototype.forEach.call(document.querySelectorAll('a[href^="https://wa.me/"]'), poner); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", todos); else todos();
})();</script>""" % datos
