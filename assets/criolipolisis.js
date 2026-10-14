/* noon Clinic · Landing Criolipólisis (v2 editorial): luz líquida del inicio, cabecera que cambia de tono por sección,
   zonas en lista que se despliega, dibujo de capas (qué hace el frío), aparición suave, barra fija y medición. */
(function () {
  var quieto = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var captura = /[?&]captura/.test(location.search);
  if (captura) document.documentElement.classList.add("captura");

  // ---------- cabecera: tono según la sección que pasa por debajo + barra fija en celular
  var cab = document.querySelector(".cl-cab");
  var secciones = Array.prototype.slice.call(document.querySelectorAll("main > [data-tema], .cl-pie"));
  var barra = document.querySelector(".cl-barra");
  var hero = document.querySelector(".cl-hero");
  var cierre = document.querySelector(".cl-cierre");
  var cierreVisible = false;
  function alBajar() {
    var y = window.scrollY || window.pageYOffset, medio = cab.offsetHeight / 2;
    cab.classList.toggle("solida", y > hero.offsetHeight - 80);
    for (var i = 0; i < secciones.length; i++) {
      var r = secciones[i].getBoundingClientRect();
      if (r.top <= medio && r.bottom > medio) { cab.setAttribute("data-tema", secciones[i].getAttribute("data-tema")); break; }
    }
    if (barra) {
      var on = y > hero.offsetHeight * 0.7 && !cierreVisible;
      barra.classList.toggle("on", on);
      barra.setAttribute("aria-hidden", on ? "false" : "true");
    }
  }
  if ("IntersectionObserver" in window && cierre) {
    new IntersectionObserver(function (e) { cierreVisible = e[0].isIntersecting; alBajar(); }, { threshold: 0.15 }).observe(cierre);
  }
  window.addEventListener("scroll", alBajar, { passive: true });
  window.addEventListener("resize", alBajar);
  alBajar();

  // ---------- aparición suave
  var revs = document.querySelectorAll(".cl-rev");
  if ("IntersectionObserver" in window && !quieto && !captura) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    revs.forEach(function (el) { io.observe(el); });
  } else {
    revs.forEach(function (el) { el.classList.add("on"); });
  }

  // ---------- luz líquida del inicio (WebGL). Blanco y negro con vetas de vino (el acento).
  // arranca después de que aparece el título (primero se lee, luego entra la luz con un fundido)
  var lienzo = document.querySelector(".cl-liquido");
  if (lienzo) setTimeout(function () { luzLiquida(lienzo); }, captura ? 0 : 900);

  function luzLiquida(cv) {
    var gl = cv.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" });
    if (!gl) { cv.remove(); return; }   // queda la luz fija del CSS
    var vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
    var fs = [
      "precision mediump float;uniform vec2 r;uniform float t;uniform vec2 m;",
      "vec2 h(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return -1.+2.*fract(sin(p)*43758.5453);}",
      "float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);",
      "return mix(mix(dot(h(i),f),dot(h(i+vec2(1,0)),f-vec2(1,0)),u.x),mix(dot(h(i+vec2(0,1)),f-vec2(0,1)),dot(h(i+vec2(1,1)),f-vec2(1,1)),u.x),u.y);}",
      "float fb(vec2 p){float v=0.,a=.55;for(int i=0;i<3;i++){v+=a*n(p);p=p*1.9+vec2(1.7,9.2);a*=.45;}return v;}",
      "void main(){vec2 uv=gl_FragCoord.xy/r;vec2 p=(gl_FragCoord.xy-.5*r)/min(r.x,r.y)*.78;float tt=t*.04;",
      "p+=m*.08;",
      "vec2 q=vec2(fb(p*1.1+vec2(0.,tt)),fb(p*1.1+vec2(5.2,1.3)-tt*.8));",
      "vec2 w=vec2(fb(p+1.7*q+vec2(1.7,9.2)+tt*.6),fb(p+1.7*q+vec2(8.3,2.8)-tt*.5));",
      "float f=fb(p+1.9*w);",
      "float b=clamp(.36+f*1.45+.10*sin(p.x*1.3+p.y*.7+tt*1.8),0.,1.);",
      // vetas suaves que fluyen (luz líquida, no solo desenfoque)
      "float rib=sin(f*7.5+p.y*1.1+tt*1.3);b=clamp(b+rib*.06,0.,1.);",
      // blanco y negro (negro → gris → perla) con pozos de vino que fluyen: el vino es el único color
      "vec3 negro=vec3(.035),gris=vec3(.38),perla=vec3(.92),vino=vec3(.50,.17,.24),vinoh=vec3(.24,.06,.10);",
      "vec3 c=mix(negro,gris,smoothstep(.24,.64,b));c=mix(c,perla,smoothstep(.68,.97,b)*.85);",
      "float vz=smoothstep(-.02,.34,fb(p*.7+q*1.4+vec2(3.1,7.7)+tt*.3));",
      "c=mix(c,mix(vinoh,vino,smoothstep(.2,.6,b)),vz*.9*(1.-smoothstep(.6,.9,b)));",
      "c+=pow(b,9.)*.10;",
      "float v=smoothstep(1.25,.25,length(uv-.5)*1.45);c*=.62+.38*v;",
      "c+=(fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5)*.035;",
      "gl_FragColor=vec4(c,1.);}"
    ].join("\n");
    function sh(tipo, src) { var o = gl.createShader(tipo); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; }
    var a = sh(gl.VERTEX_SHADER, vs), b = sh(gl.FRAGMENT_SHADER, fs);
    if (!a || !b) { cv.remove(); return; }
    var pr = gl.createProgram(); gl.attachShader(pr, a); gl.attachShader(pr, b); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { cv.remove(); return; }
    gl.useProgram(pr);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var uR = gl.getUniformLocation(pr, "r"), uT = gl.getUniformLocation(pr, "t"), uM = gl.getUniformLocation(pr, "m");
    var escala = 0.5, visible = true, mx = 0, my = 0, tmx = 0, tmy = 0, t0 = performance.now() - 30000;
    function medir() { cv.width = Math.max(1, Math.round(cv.clientWidth * escala)); cv.height = Math.max(1, Math.round(cv.clientHeight * escala)); gl.viewport(0, 0, cv.width, cv.height); }
    medir(); window.addEventListener("resize", medir);
    window.addEventListener("mousemove", function (e) { tmx = e.clientX / window.innerWidth - 0.5; tmy = 0.5 - e.clientY / window.innerHeight; }, { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }, { rootMargin: "60px" }).observe(cv);
    function pintar(ahora) {
      mx += (tmx - mx) * 0.03; my += (tmy - my) * 0.03;
      gl.uniform2f(uR, cv.width, cv.height); gl.uniform1f(uT, (ahora - t0) / 1000); gl.uniform2f(uM, mx, my);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    if (quieto || captura) { pintar(performance.now()); cv.classList.add("vivo"); return; }   // un solo cuadro quieto
    requestAnimationFrame(function () { cv.classList.add("vivo"); });
    (function cuadro(ahora) {
      if (visible && !document.hidden) pintar(ahora);
      requestAnimationFrame(cuadro);
    })(performance.now());
  }

  // ---------- zonas: lista que se despliega (una abierta a la vez)
  var filas = document.querySelectorAll(".cl-fila");
  filas.forEach(function (fila) {
    var btn = fila.querySelector(".cl-fila-b"), det = fila.querySelector(".cl-fila-d");
    btn.addEventListener("click", function () {
      var abrir = !fila.classList.contains("abierta");
      filas.forEach(function (f) {
        var on = f === fila && abrir;
        f.classList.toggle("abierta", on);
        f.querySelector(".cl-fila-b").setAttribute("aria-expanded", on ? "true" : "false");
        f.querySelector(".cl-fila-d").hidden = !on;
      });
      if (abrir && window.clarity) window.clarity("set", "zona", fila.querySelector(".cl-fila-t").textContent);
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
      if (!fondoEt) { fondoEt = document.createElementNS(NS, "rect"); fondoEt.setAttribute("fill", "#120d0a"); svg.insertBefore(fondoEt, etGrasa); }
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
