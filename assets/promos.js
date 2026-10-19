/* noon Clinic · Landing de promos de fin de año (promos/*.html): cada página llega abierta en la cirugía del anuncio;
   al tocar otra cirugía cambian la portada, la barra fija, los botones de WhatsApp y la dirección (sin recargar).
   También: cabecera, aparición suave, pestañas por zona y medición en Clarity. */
(function () {
  var quieto = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var captura = /[?&]captura/.test(location.search);
  if (captura) document.documentElement.classList.add("captura");
  var D = JSON.parse(document.getElementById("pr-datos").textContent);
  function marcar(nombre, valor) { if (!window.clarity) return; if (valor === undefined) window.clarity("event", nombre); else window.clarity("set", nombre, valor); }
  function $(sel, raiz) { return (raiz || document).querySelector(sel); }
  function $$(sel, raiz) { return Array.prototype.slice.call((raiz || document).querySelectorAll(sel)); }
  function wa(it) { return "https://wa.me/" + D.wa + "?text=" + encodeURIComponent(it ? D.msj + it.nombre.toLowerCase() : D.msjGeneral); }
  var CHECK = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  var ESCUDO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5l7 2.6v5.4c0 4.3-2.9 7.7-7 9-4.1-1.3-7-4.7-7-9V6.1Z"/><path d="M9 12l2.2 2.2L15.5 10"/></svg>';
  function esc(t) { var d = document.createElement("div"); d.textContent = t; return d.innerHTML; }

  // ---------- cabecera + barra fija en celular (aparece al pasar la portada, se esconde en el cierre)
  var cab = $(".pr-cab"), barra = $(".pr-barra"), portada = $(".pr-portada"), cierre = $(".pr-cierre");
  var cierreVisible = false;
  function alBajar() {
    var y = window.scrollY || window.pageYOffset;
    cab.classList.toggle("solida", y > 10);
    var on = y > portada.offsetHeight * 0.7 && !cierreVisible;
    barra.classList.toggle("on", on);
    barra.setAttribute("aria-hidden", on ? "false" : "true");
  }
  if ("IntersectionObserver" in window && cierre) {
    new IntersectionObserver(function (e) { cierreVisible = e[0].isIntersecting; alBajar(); }, { threshold: 0.1 }).observe(cierre);
  }
  window.addEventListener("scroll", alBajar, { passive: true });
  alBajar();

  // ---------- aparición suave
  var revs = $$(".pr-rev");
  if ("IntersectionObserver" in window && !quieto && !captura) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    revs.forEach(function (el) { io.observe(el); });
  } else {
    revs.forEach(function (el) { el.classList.add("on"); });
  }

  // ---------- pestañas por zona
  var lista = $(".pr-lista");
  function zona(z) {
    lista.setAttribute("data-zona", z);
    $$(".pr-tab").forEach(function (t) { var on = t.getAttribute("data-zona") === z; t.classList.toggle("on", on); t.setAttribute("aria-pressed", on ? "true" : "false"); });
  }
  $$(".pr-tab").forEach(function (t) {
    t.addEventListener("click", function () { zona(t.getAttribute("data-zona")); marcar("zona", t.getAttribute("data-zona")); });
  });

  // ---------- elegir cirugía: portada, barra, botones y dirección
  var foto = $('[data-h="foto"]');
  function elegir(slug) {
    var it = D.items[slug];
    if (!it) return;
    document.body.classList.remove("pr-general");
    document.body.setAttribute("data-cx", slug);
    $('[data-h="titulo"]').innerHTML = D.titulo[slug];
    $('[data-h="precio"]').innerHTML = D.precio[slug];
    var inc = it.incluye.length ? it.incluye : ["Cirujano plástico", "Quirófano", "Póliza de complicaciones"];
    $('[data-h="incluye"]').innerHTML = inc.map(function (x) { return "<li>" + CHECK + esc(x) + "</li>"; }).join("");
    $('[data-h="flota"]').innerHTML = ESCUDO + "<span>" + (it.precio ? "<b>Póliza y bomba de dolor</b> incluidas" : "<b>Póliza de complicaciones</b> en tu cirugía") + "</span>";
    if (foto.getAttribute("src") !== it.foto) {
      foto.classList.add("cambia");
      var nueva = new Image();
      nueva.onload = nueva.onerror = function () { foto.src = it.foto; foto.classList.remove("cambia"); };
      nueva.src = it.foto;
    }
    $('[data-h="barra-n"]').textContent = it.nombre;
    $('[data-h="barra-p"]').textContent = it.precio ? (it.desde ? "Desde " : "") + it.precio : "Precio en tu valoración";
    // los botones generales llevan la cirugía elegida (los de cada fila ya tienen la suya)
    $$("a[data-wa]").forEach(function (a) { if (!a.closest(".pr-cx")) a.href = wa(it); });
    document.title = it.nombre + " en Medellín · Promo de fin de año · noon Clinic";
    if (history.replaceState && /^https?:/.test(location.protocol)) {
      history.replaceState(null, "", "/promos/" + slug + location.search);
    }
    marcar("cx", slug);
  }

  // abrir una fila = elegir esa cirugía (y cerrar las demás, para navegadores sin <details name>)
  $$(".pr-cx").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      $$(".pr-cx[open]").forEach(function (o) { if (o !== d) o.open = false; });
      elegir(d.getAttribute("data-slug"));
    });
  });

  // tarjetas de precio de la portada general: eligen la cirugía y la dejan abierta en la lista
  $$(".pr-tarj").forEach(function (b) {
    b.addEventListener("click", function () {
      var slug = b.getAttribute("data-ir"), fila = $('.pr-cx[data-slug="' + slug + '"]');
      zona(fila.getAttribute("data-zona"));
      fila.open = true;
      elegir(slug);
      marcar("tarjeta_portada", slug);
    });
  });

  // ---------- medición: clic a WhatsApp con la cirugía
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-wa]");
    if (a) { marcar("cx_whatsapp", document.body.getAttribute("data-cx") || "general"); marcar("clic_whatsapp"); }
  });
})();
