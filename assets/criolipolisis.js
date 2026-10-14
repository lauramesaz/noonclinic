/* noon Clinic · Landing Criolipólisis: zonas, capas que muestran qué hace el frío, aparición suave, barra fija y medición. */
(function () {
  var quieto = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (/[?&]captura/.test(location.search)) document.documentElement.classList.add("captura");

  // ---------- cabecera sólida al bajar + barra fija en celular
  var cab = document.querySelector(".cl-cab");
  var barra = document.querySelector(".cl-barra");
  var hero = document.querySelector(".cl-hero");
  var cierre = document.querySelector(".cl-cierre");
  var cierreVisible = false;
  function alBajar() {
    var y = window.scrollY || window.pageYOffset;
    cab.classList.toggle("solida", y > 40);
    if (barra) {
      var pasado = hero && y > hero.offsetHeight * 0.7;
      var on = pasado && !cierreVisible;
      barra.classList.toggle("on", !!on);
      barra.setAttribute("aria-hidden", on ? "false" : "true");
    }
  }
  if ("IntersectionObserver" in window && cierre) {
    new IntersectionObserver(function (e) { cierreVisible = e[0].isIntersecting; alBajar(); }, { threshold: 0.15 }).observe(cierre);
  }
  window.addEventListener("scroll", alBajar, { passive: true });
  alBajar();

  // ---------- aparición suave
  var revs = document.querySelectorAll(".cl-rev");
  if ("IntersectionObserver" in window && !quieto) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revs.forEach(function (el) { io.observe(el); });
  } else {
    revs.forEach(function (el) { el.classList.add("on"); });
  }

  // ---------- zonas
  var zBot = document.querySelectorAll(".cl-z");
  var zPan = document.querySelectorAll(".cl-zp");
  zBot.forEach(function (b) {
    b.addEventListener("click", function () {
      var i = b.dataset.z;
      zBot.forEach(function (x) { var on = x === b; x.classList.toggle("on", on); x.setAttribute("aria-pressed", on ? "true" : "false"); });
      zPan.forEach(function (p) { var on = p.dataset.z === i; p.classList.toggle("on", on); p.hidden = !on; });
      if (window.clarity) window.clarity("set", "zona", b.textContent);
    });
  });

  // ---------- capas: qué hace el frío en la grasa
  var vis = document.querySelector("[data-capas]");
  if (vis) {
    var NS = "http://www.w3.org/2000/svg";
    var svg = vis.querySelector(".cl-svg");
    var MUSC = 320, BASE = 135, SIGMA = 112, CENTRO = 400;
    var BULTO = [86, 86, 76, 30];           // altura del "rollito" en cada etapa
    var bulto = BULTO[0];

    function techo(x, b) { return BASE - b * Math.exp(-((x - CENTRO) * (x - CENTRO)) / (2 * SIGMA * SIGMA)); }
    function contorno(b) {
      var d = "";
      for (var x = -10; x <= 810; x += 10) d += (x === -10 ? "M" : "L") + x + "," + techo(x, b).toFixed(1);
      return d;
    }

    // fibras del músculo
    var fib = svg.querySelector(".cl-fibras");
    for (var fx = -40; fx < 820; fx += 13) {
      var l = document.createElementNS(NS, "line");
      l.setAttribute("x1", fx); l.setAttribute("y1", 324); l.setAttribute("x2", fx + 34); l.setAttribute("y2", 380);
      fib.appendChild(l);
    }

    // células de grasa (posiciones fijas con un aleatorio con semilla, para que siempre se vea igual)
    var semilla = 7;
    function azar() { semilla = (semilla * 9301 + 49297) % 233280; return semilla / 233280; }
    var grupo = svg.querySelector(".cl-celulas");
    var celulas = [];
    var fila = 0;
    for (var cy = MUSC - 17; cy > 20; cy -= 27, fila++) {
      for (var cx = (fila % 2 ? 16 : 31); cx < 800; cx += 30) {
        var x = cx + (azar() - 0.5) * 7, y = cy + (azar() - 0.5) * 6, r = 11.5 + azar() * 3;
        if (y - r < techo(x, BULTO[0]) + 9 || y + r > MUSC - 2) continue;
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("cx", x.toFixed(1)); c.setAttribute("cy", y.toFixed(1)); c.setAttribute("r", r.toFixed(1));
        // se apagan tantas células como grosor pierde la capa en ese punto (un poco más, para que se note);
        // las que quedan se acomodan en la capa más delgada, sin dejar huecos
        var g0 = MUSC - techo(x, BULTO[0]), g3 = MUSC - techo(x, BULTO[3]);
        var p = Math.min(0.55, 1.8 * (1 - g3 / g0));
        if (Math.abs(x - CENTRO) < 175 && azar() < p) c.setAttribute("class", "af");
        grupo.appendChild(c);
        celulas.push({ el: c, x: x, y: y, prof: MUSC - y, grosor: MUSC - techo(x, BULTO[0]) });
      }
    }

    var piel = svg.querySelector(".cl-piel"), grasa = svg.querySelector(".cl-grasa"), clip = svg.querySelector(".cl-grasa-clip");
    function dibujar(b) {
      var top = contorno(b);
      piel.setAttribute("d", top);
      var area = top + "L810," + MUSC + "L-10," + MUSC + "Z";
      grasa.setAttribute("d", area);
      clip.setAttribute("d", area);
      // las células que quedan bajan con la piel (la capa se vuelve más delgada)
      celulas.forEach(function (c) {
        var nuevo = MUSC - techo(c.x, b);
        c.el.setAttribute("cy", (MUSC - c.prof * (nuevo / c.grosor)).toFixed(1));
      });
    }
    dibujar(bulto);

    // fondo detrás de la etiqueta "Grasa" para que se lea sobre las células (se recalcula si cambia el tamaño de letra)
    var etGrasa = svg.querySelector(".cl-et-grasa"), fondoEt = null;
    function fondoEtiqueta() {
      if (!etGrasa || !etGrasa.getBBox) return;
      var bb = etGrasa.getBBox();
      if (!fondoEt) { fondoEt = document.createElementNS(NS, "rect"); fondoEt.setAttribute("fill", "#1b1411"); svg.insertBefore(fondoEt, etGrasa); }
      var px = bb.height * 0.45, py = bb.height * 0.22;
      fondoEt.setAttribute("x", (bb.x - px).toFixed(1)); fondoEt.setAttribute("y", (bb.y - py).toFixed(1));
      fondoEt.setAttribute("width", (bb.width + 2 * px).toFixed(1)); fondoEt.setAttribute("height", (bb.height + 2 * py).toFixed(1));
    }
    // en celular el dibujo se encuadra en la zona tratada para que se vea más grande
    var etiquetas = svg.querySelectorAll(".cl-et-svg:not(.cl-et-frio)");
    function encuadre() {
      var movil = window.innerWidth < 761, x0 = movil ? 110 : 0, w = movil ? 580 : 800;
      svg.setAttribute("viewBox", x0 + " 0 " + w + " 380");
      etiquetas.forEach(function (t) { t.setAttribute("x", x0 + (t === etGrasa ? 20 : 16)); });
      fondoEtiqueta();
    }
    encuadre();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fondoEtiqueta);
    var trs = 0;
    window.addEventListener("resize", function () { clearTimeout(trs); trs = setTimeout(encuadre, 150); });

    var anim = 0;
    function irA(b) {
      cancelAnimationFrame(anim);
      if (quieto) { bulto = b; dibujar(b); return; }
      var desde = bulto, t0 = performance.now(), dur = 1500;
      (function paso(t) {
        var k = Math.min(1, (t - t0) / dur);
        k = 1 - Math.pow(1 - k, 3);
        bulto = desde + (b - desde) * k;
        dibujar(bulto);
        if (k < 1) anim = requestAnimationFrame(paso);
      })(t0);
    }

    var eBot = vis.querySelectorAll(".cl-e"), eTxt = vis.querySelectorAll(".cl-et");
    var etapa = 0;
    function poner(i) {
      etapa = i;
      vis.setAttribute("data-etapa", i);
      eBot.forEach(function (b) { b.classList.toggle("on", +b.dataset.e === i); });
      eTxt.forEach(function (p) { p.classList.toggle("on", +p.dataset.e === i); });
      irA(BULTO[i]);
    }
    poner(0);

    // Recorre las etapas una sola vez cuando se ve (sin repetir en bucle: menos ruido). Al tocar, manda la persona.
    var PASO = 3200, reloj = 0, tocado = false, visto = false;
    vis.style.setProperty("--cl-paso", PASO + "ms");
    function avanzar() {
      if (tocado) return;
      if (etapa < 3) {
        reloj = setTimeout(function () { poner(etapa + 1); avanzar(); }, PASO);
      } else {
        vis.classList.remove("auto");
      }
    }
    function arrancar() {
      if (visto || tocado || quieto) return;
      visto = true;
      vis.classList.add("auto");
      poner(0);
      avanzar();
    }
    eBot.forEach(function (b) {
      b.addEventListener("click", function () {
        tocado = true; clearTimeout(reloj); vis.classList.remove("auto");
        poner(+b.dataset.e);
        if (window.clarity) window.clarity("event", "crio_etapa");
      });
    });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { if (es[0].isIntersecting) arrancar(); }, { threshold: 0.45 }).observe(vis);
    }
  }

  // ---------- medición: clic a WhatsApp (mismo evento que el resto de la web)
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (a && window.clarity) { window.clarity("event", "clic_whatsapp"); window.clarity("upgrade", "clic_whatsapp"); }
  });
})();
