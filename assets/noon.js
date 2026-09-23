// noon Clinic · interacciones mínimas
(function () {
  if (/[?&]captura/.test(location.search)) document.documentElement.classList.add("captura");
  // direcciones limpias si entran por un link viejo con .html
  if (/\.html$/.test(location.pathname)) history.replaceState(null, "", location.pathname.replace(/index\.html$|\.html$/, "") + location.search + location.hash);

  var cab = document.querySelector(".cab");
  var alScroll = function () { cab.classList.toggle("solida", window.scrollY > 40); };
  alScroll(); window.addEventListener("scroll", alScroll, { passive: true });

  // menú a pantalla completa
  var btn = document.querySelector(".menu-btn"), menu = document.getElementById("menu");
  function cerrar() { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); document.documentElement.classList.remove("menu-abierto"); btn.querySelector(".txt").textContent = "Menú"; }
  btn.addEventListener("click", function () {
    if (menu.hidden) { menu.hidden = false; btn.setAttribute("aria-expanded", "true"); document.documentElement.classList.add("menu-abierto"); btn.querySelector(".txt").textContent = "Cerrar"; }
    else cerrar();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !menu.hidden) cerrar(); });
  menu.addEventListener("click", function (e) { if (e.target.closest("a")) cerrar(); });

  var quieto = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var captura = document.documentElement.classList.contains("captura");

  // títulos: se parten en palabras para revelarlas una por una
  document.querySelectorAll(".hero h1, .frase .grande, .foto-frase .grande, .cierre h2, .sec-cab h2, .dividir h2").forEach(function (el) {
    var i = 0;
    (function partir(nodo) {
      [].slice.call(nodo.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (parte) {
            if (!parte) return;
            if (/^\s+$/.test(parte)) { frag.appendChild(document.createTextNode(" ")); return; }
            var w = document.createElement("span"); w.className = "w";
            var wi = document.createElement("span"); wi.className = "wi"; wi.style.setProperty("--i", i++); wi.textContent = parte;
            w.appendChild(wi); frag.appendChild(w);
          });
          nodo.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") partir(n);
      });
    })(el);
    el.classList.add("partido");
    if (!el.classList.contains("rev")) el.classList.add("rev");
  });

  // aparición suave (revisa posición al bajar; sin depender de IntersectionObserver)
  var pend = [].slice.call(document.querySelectorAll(".rev"));
  function revelar() {
    var h = window.innerHeight * 0.94;
    pend = pend.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < h && r.bottom > 0) { el.classList.add("on"); return false; }
      return true;
    });
  }
  revelar(); window.addEventListener("scroll", revelar, { passive: true }); window.addEventListener("resize", revelar);
  if (captura) pend.forEach(function (el) { el.classList.add("on"); });
  setTimeout(function () { pend.forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight * 3) el.classList.add("on"); }); }, 2500);

  // preguntas: buscador + filtros
  var buscador = document.querySelector(".buscador");
  if (buscador) {
    var cat = "todas", pregs = document.querySelectorAll(".preg[data-cat]"), vacio = document.querySelector(".vacio");
    var norm = function (s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
    var aplicar = function () {
      var q = norm(buscador.value.trim()), n = 0;
      pregs.forEach(function (p) {
        var ok = (cat === "todas" || p.dataset.cat === cat) && (!q || norm(p.textContent).indexOf(q) > -1);
        p.hidden = !ok; if (ok) { n++; p.classList.add("on"); }
      });
      vacio.hidden = n > 0;
    };
    buscador.addEventListener("input", aplicar);
    document.querySelectorAll(".filtro").forEach(function (b) {
      b.addEventListener("click", function () {
        document.querySelectorAll(".filtro").forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on"); cat = b.dataset.cat; aplicar();
      });
    });
  }

  // formulario de valoración → WhatsApp
  var form = document.getElementById("form-valoracion");
  if (form) {
    var sel = form.querySelector("#cirugia"), cx = new URLSearchParams(location.search).get("cx");
    if (cx) [].forEach.call(sel.options, function (o, i) { if (o.dataset.slug === cx) sel.selectedIndex = i; });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = "Hola, soy " + form.nombre.value.trim() + ". Quiero agendar mi valoración en noon Clinic. Me interesa: " + sel.value + ". Vivo en " + form.ciudad.value.trim() + ".";
      window.open("https://wa.me/" + form.dataset.wa + "?text=" + encodeURIComponent(msg), "_blank", "noopener");
    });
  }

  // scroll suave con inercia (Lenis), solo si no piden menos movimiento
  var lenis = null;
  window.addEventListener("load", function () {
    if (window.Lenis && !quieto && !captura) {
      lenis = new window.Lenis({ lerp: 0.085, anchors: { offset: -80 } });
      (function bucle(t) { lenis.raf(t); requestAnimationFrame(bucle); })(performance.now());
      var mb = document.querySelector(".menu-btn");
      mb.addEventListener("click", function () { setTimeout(function () { document.documentElement.classList.contains("menu-abierto") ? lenis.stop() : lenis.start(); }, 0); });
    }
  });

  // parallax: fondos más lentos que el texto; el texto del hero se desvanece al bajar
  var capas = [].slice.call(document.querySelectorAll(".capa, .dividir figure img"));
  var heroIn = document.querySelector(".hero .hero-in"), hero = document.querySelector(".hero");
  var pedido = false;
  function parallax() {
    pedido = false;
    var vh = window.innerHeight;
    capas.forEach(function (c) {
      var r = c.parentElement.getBoundingClientRect();
      if (r.bottom < -100 || r.top > vh + 100) return;
      var centro = r.top + r.height / 2 - vh / 2;
      c.style.setProperty("--py", (centro * -0.12).toFixed(1) + "px");
      if (c.tagName === "IMG") c.style.transform = "translate3d(0," + (centro * -0.06).toFixed(1) + "px,0) scale(1.08)";
    });
    if (heroIn && hero) {
      var y = Math.max(0, window.scrollY), h = hero.offsetHeight;
      if (y < h) { heroIn.style.transform = "translate3d(0," + (y * 0.28).toFixed(1) + "px,0)"; heroIn.style.opacity = Math.max(0, 1 - y / (h * 0.75)).toFixed(3); }
    }
  }
  if (!quieto && !captura) {
    window.addEventListener("scroll", function () { if (!pedido) { pedido = true; requestAnimationFrame(parallax); } }, { passive: true });
    parallax();
  }

  // procedimientos: la imagen sigue suavemente al mouse
  if (window.matchMedia("(hover: hover)").matches && !quieto) {
    document.querySelectorAll(".tile").forEach(function (t) {
      t.addEventListener("mousemove", function (e) {
        var r = t.getBoundingClientRect();
        t.style.setProperty("--mx", ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
        t.style.setProperty("--my", ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
      });
      t.addEventListener("mouseleave", function () { t.style.setProperty("--mx", 0); t.style.setProperty("--my", 0); });
    });
  }

  // seda viva en la portada (WebGL); si no hay soporte, queda la imagen fija
  var lienzo = document.querySelector(".seda-viva");
  if (lienzo && !quieto && !captura) sedaViva(lienzo);

  function sedaViva(cv) {
    var gl = cv.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" });
    if (!gl) return;
    var vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
    var fs = [
      "precision mediump float;uniform vec2 r;uniform float t;uniform vec2 m;",
      "vec2 h(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return -1.+2.*fract(sin(p)*43758.5453);}",
      "float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);",
      "return mix(mix(dot(h(i),f),dot(h(i+vec2(1,0)),f-vec2(1,0)),u.x),mix(dot(h(i+vec2(0,1)),f-vec2(0,1)),dot(h(i+vec2(1,1)),f-vec2(1,1)),u.x),u.y);}",
      "float fb(vec2 p){float v=0.,a=.5;for(int i=0;i<4;i++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}",
      "void main(){vec2 uv=gl_FragCoord.xy/r;vec2 p=(gl_FragCoord.xy-.5*r)/min(r.x,r.y)*.75;float tt=t*.03;",
      "p+=m*.05;",
      "vec2 q=vec2(fb(p*.9+vec2(0.,tt)),fb(p*.9+vec2(5.2,1.3)-tt*.7));",
      "vec2 w=vec2(fb(p+1.1*q+vec2(1.7,9.2)+tt*.5),fb(p+1.1*q+vec2(8.3,2.8)-tt*.4));",
      "float f=p.y*.9+p.x*.35+1.3*w.x+.6*q.y;",
      "float b=.5+.5*sin(f*3.4+tt*1.6);b=smoothstep(0.,1.,b);b=pow(b,1.6);",
      "vec3 esp=vec3(.063,.045,.035),caf=vec3(.21,.13,.09),car=vec3(.50,.35,.24),cre=vec3(.90,.85,.77);",
      "vec3 c=mix(esp,caf,smoothstep(.18,.55,b));c=mix(c,car,smoothstep(.55,.85,b));c=mix(c,cre,smoothstep(.86,1.,b)*.75);",
      "c+=pow(b,14.)*.10;",
      "float v=smoothstep(1.3,.2,length(uv-.5)*1.5);c*=.5+.5*v;",
      "c+=(fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5)*.03;",
      "gl_FragColor=vec4(c,1.);}"
    ].join("\n");
    function sh(tipo, src) { var o = gl.createShader(tipo); gl.shaderSource(o, src); gl.compileShader(o); return gl.getShaderParameter(o, gl.COMPILE_STATUS) ? o : null; }
    var a = sh(gl.VERTEX_SHADER, vs), b = sh(gl.FRAGMENT_SHADER, fs);
    if (!a || !b) return;
    var pr = gl.createProgram(); gl.attachShader(pr, a); gl.attachShader(pr, b); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var uR = gl.getUniformLocation(pr, "r"), uT = gl.getUniformLocation(pr, "t"), uM = gl.getUniformLocation(pr, "m");
    var escala = Math.min(1, 0.55 * (window.devicePixelRatio || 1)), visible = true, mx = 0, my = 0, tmx = 0, tmy = 0, t0 = performance.now() - 8000;
    function medir() { cv.width = Math.round(cv.clientWidth * escala); cv.height = Math.round(cv.clientHeight * escala); gl.viewport(0, 0, cv.width, cv.height); }
    medir(); window.addEventListener("resize", medir);
    window.addEventListener("mousemove", function (e) { tmx = e.clientX / window.innerWidth - 0.5; tmy = 0.5 - e.clientY / window.innerHeight; }, { passive: true });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(cv);
    var primero = true;
    (function cuadro(ahora) {
      if (visible && !document.hidden) {
        mx += (tmx - mx) * 0.03; my += (tmy - my) * 0.03;
        gl.uniform2f(uR, cv.width, cv.height); gl.uniform1f(uT, (ahora - t0) / 1000); gl.uniform2f(uM, mx, my);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        if (primero) { primero = false; cv.classList.add("lista"); }
      }
      requestAnimationFrame(cuadro);
    })(performance.now());
  }

  // ================= v4 · USABLE =================
  var html = document.documentElement;
  var N = null;
  function datos() { return N || (N = window.NOON || { items: [], asistente: [], wa: "" }); }
  function norm(t) { return (t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function fondo(f) { return "assets/noon/" + f + ".jpg"; }
  function paraLenis(stop) { if (lenis) stop ? lenis.stop() : lenis.start(); }

  // ---------- buscador (botón de arriba, portada, atajo ⌘K o "/")
  var capa = document.querySelector(".buscador-capa");
  if (capa) {
    var inp = capa.querySelector(".bc-input"), res = capa.querySelector(".bc-res"), vac = capa.querySelector(".bc-vacio"), act = -1;
    var abrir = function (q) {
      capa.hidden = false; html.classList.add("buscando"); paraLenis(true);
      inp.value = q || ""; pintar(); setTimeout(function () { inp.focus(); }, 30);
    };
    var cerrarB = function () { capa.hidden = true; html.classList.remove("buscando"); paraLenis(false); };
    var pintar = function () {
      var q = norm(inp.value.trim()), items = datos().items, out = [];
      if (q) {
        var partes = q.split(/\s+/);
        items.forEach(function (it) {
          var texto = norm(it.n + " " + it.c + " " + it.k + " " + it.p + " " + it.t), pts = 0;
          partes.forEach(function (pa) { if (texto.indexOf(pa) > -1) pts += norm(it.n).indexOf(pa) > -1 ? 3 : 1; });
          if (pts >= partes.length) out.push([pts, it]);
        });
        out.sort(function (a, b) { return b[0] - a[0]; });
      }
      res.innerHTML = out.slice(0, 12).map(function (o, i) {
        var it = o[1];
        return '<li><a href="' + it.s + '" data-i="' + i + '"><span class="mini" style="background-image:url(' + fondo(it.f) + ')"></span><span><b>' + it.n + '</b><small>' + it.c + '</small></span><em>' + it.t + '</em></a></li>';
      }).join("");
      act = -1;
      vac.hidden = !(q && !out.length);
      vac.querySelector("a").href = "https://wa.me/" + datos().wa + "?text=" + encodeURIComponent("Hola, quiero información sobre: " + inp.value.trim());
    };
    inp.addEventListener("input", pintar);
    inp.addEventListener("keydown", function (e) {
      var ls = res.querySelectorAll("a");
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); if (!ls.length) return;
        act = (act + (e.key === "ArrowDown" ? 1 : -1) + ls.length) % ls.length;
        ls.forEach(function (a, i) { a.classList.toggle("act", i === act); }); ls[act].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter") { var el = ls[act > -1 ? act : 0]; if (el) location.href = el.href; }
    });
    capa.querySelector(".bc-cerrar").addEventListener("click", cerrarB);
    capa.addEventListener("click", function (e) { if (e.target === capa) cerrarB(); });
    capa.querySelectorAll(".bc-sug button").forEach(function (b) { b.addEventListener("click", function () { inp.value = b.textContent; pintar(); inp.focus(); }); });
    document.querySelectorAll(".buscar-btn, [data-abrir-buscador]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); abrir(""); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !capa.hidden) cerrarB();
      var escribiendo = /INPUT|TEXTAREA|SELECT/.test((document.activeElement || {}).tagName);
      if (((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") || (e.key === "/" && !escribiendo)) { e.preventDefault(); abrir(""); }
    });
  }

  // ---------- explorador por zona (pestañas + carrusel que se arrastra)
  var ex = document.querySelector(".explora");
  if (ex) {
    var pista = ex.querySelector(".ex-pista"), cards = ex.querySelectorAll(".ex-card");
    var zona = function (z) {
      ex.querySelectorAll(".ex-tab").forEach(function (t) { t.classList.toggle("on", t.dataset.z === z); t.setAttribute("aria-selected", t.dataset.z === z); });
      var i = 0;
      cards.forEach(function (c) { var ok = c.dataset.z === z; c.hidden = !ok; if (ok) { c.style.animationDelay = (i++ * 60) + "ms"; c.style.animation = "none"; c.offsetHeight; c.style.animation = ""; } });
      pista.scrollTo({ left: 0, behavior: "smooth" });
    };
    ex.querySelectorAll(".ex-tab").forEach(function (t) { t.addEventListener("click", function () { zona(t.dataset.z); }); });
    zona(ex.querySelector(".ex-tab").dataset.z);
    var paso = function (d) { var c = ex.querySelector(".ex-card:not([hidden])"); pista.scrollBy({ left: d * ((c ? c.offsetWidth : 300) + 14), behavior: "smooth" }); };
    ex.querySelector(".ex-prev").addEventListener("click", function () { paso(-1); });
    ex.querySelector(".ex-next").addEventListener("click", function () { paso(1); });
    // arrastrar con el mouse
    var x0 = 0, s0 = 0, abajo = false, movio = false;
    pista.addEventListener("mousedown", function (e) { abajo = true; movio = false; x0 = e.pageX; s0 = pista.scrollLeft; });
    window.addEventListener("mousemove", function (e) { if (!abajo) return; var dx = e.pageX - x0; if (Math.abs(dx) > 5) { movio = true; pista.classList.add("arrastrando"); } pista.scrollLeft = s0 - dx; });
    window.addEventListener("mouseup", function () { abajo = false; setTimeout(function () { pista.classList.remove("arrastrando"); }, 0); });
    pista.addEventListener("click", function (e) { if (movio) { e.preventDefault(); movio = false; } }, true);
  }

  // ---------- asistente "Encuentra tu procedimiento"
  var as = document.querySelector("[data-asistente]");
  if (as) {
    var pasos = as.querySelectorAll(".as-paso"), prog = as.querySelectorAll(".as-prog li"), elegida = null;
    var ir = function (n) {
      pasos.forEach(function (p) { p.hidden = p.dataset.paso !== String(n); });
      prog.forEach(function (l, i) { l.classList.toggle("on", i < n); });
    };
    var porSlug = function (sl) { return datos().items.filter(function (it) { return it.s === sl; })[0]; };
    var pintar1 = function () {
      as.querySelector('[data-paso="1"] .as-ops').innerHTML = datos().asistente.map(function (z, i) { return '<button type="button" class="zona" data-i="' + i + '">' + z.n + "</button>"; }).join("");
      as.querySelectorAll('[data-paso="1"] button').forEach(function (b) { b.addEventListener("click", function () { elegida = datos().asistente[+b.dataset.i]; pintar2(); }); });
    };
    var pintar2 = function () {
      var p2 = as.querySelector('[data-paso="2"]');
      p2.querySelector(".as-preg").textContent = "¿Qué quieres lograr en " + elegida.n.toLowerCase() + "?";
      p2.querySelector(".as-ops").innerHTML = elegida.o.map(function (o, i) { return '<button type="button" data-i="' + i + '" style="animation-delay:' + (i * 40) + 'ms">' + o.n + "</button>"; }).join("");
      p2.querySelectorAll(".as-ops button").forEach(function (b) { b.addEventListener("click", function () { pintar3(elegida.o[+b.dataset.i]); }); });
      ir(2);
    };
    var pintar3 = function (op) {
      var its = op.s.map(porSlug).filter(Boolean);
      as.querySelector(".as-res").innerHTML = its.map(function (it, i) {
        return '<a href="' + it.s + '" style="background-image:url(' + fondo(it.f) + ');animation-delay:' + (i * 90) + 'ms"><em>' + it.t + "</em><b>" + it.n + "</b><small>" + it.c + "</small></a>";
      }).join("");
      as.querySelector(".as-wa").href = "https://wa.me/" + datos().wa + "?text=" + encodeURIComponent("Hola, quiero agendar una valoración en noon Clinic. Me interesa " + elegida.n.toLowerCase() + ": " + op.n.toLowerCase() + " (" + its.map(function (x) { return x.n; }).join(", ") + ").");
      ir(3);
    };
    as.querySelector(".as-atras").addEventListener("click", function () { ir(1); });
    as.querySelector(".as-reset").addEventListener("click", function () { ir(1); });
    var arrancar = function () { if (window.NOON) pintar1(); else setTimeout(arrancar, 50); };
    arrancar();
  }

  // ---------- línea de tiempo de recuperación
  document.querySelectorAll("[data-lt]").forEach(function (lt) {
    var ms = lt.querySelectorAll(".lt-m"), ts = lt.querySelectorAll(".lt-t"), fill = lt.querySelector(".lt-fill"), i0 = 0;
    var ver = function (i) {
      i0 = Math.max(0, Math.min(ms.length - 1, i));
      ms.forEach(function (m, k) { m.classList.toggle("on", k === i0); m.classList.toggle("pasado", k < i0); });
      ts.forEach(function (t, k) { t.classList.toggle("on", k === i0); });
      fill.style.width = (ms.length > 1 ? (i0 / (ms.length - 1)) * 100 : 100) + "%";
    };
    ms.forEach(function (m, k) { m.addEventListener("click", function () { ver(k); }); });
    lt.querySelector(".lt-ant").addEventListener("click", function () { ver(i0 - 1); });
    lt.querySelector(".lt-sig").addEventListener("click", function () { ver(i0 + 1); });
    var tx0 = null;
    lt.addEventListener("touchstart", function (e) { tx0 = e.touches[0].clientX; }, { passive: true });
    lt.addEventListener("touchend", function (e) { if (tx0 === null) return; var dx = e.changedTouches[0].clientX - tx0; if (Math.abs(dx) > 40) ver(i0 + (dx < 0 ? 1 : -1)); tx0 = null; });
    ver(0);
  });

  // ---------- menú de la ficha que sigue al bajar + barra de agendar
  var sn = document.querySelector(".subnav"), barra = document.querySelector(".barra-cta");
  if (barra) html.classList.add("con-barra");
  if (sn || barra) {
    var enlaces = sn ? [].slice.call(sn.querySelectorAll("a")) : [];
    var secciones = enlaces.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var heroF = document.querySelector(".hero"), cierreF = document.querySelector(".cierre");
    var espiar = function () {
      var y = window.innerHeight * 0.35, actual = -1;
      secciones.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < y) actual = i; });
      enlaces.forEach(function (a, i) { a.classList.toggle("on", i === actual); });
      if (sn && actual > -1 && enlaces[actual]) { var a = enlaces[actual]; if (a.offsetLeft < sn.scrollLeft || a.offsetLeft + a.offsetWidth > sn.scrollLeft + sn.clientWidth) sn.scrollTo({ left: a.offsetLeft - 20, behavior: "smooth" }); }
      if (barra) {
        var pasoHero = heroF ? heroF.getBoundingClientRect().bottom < 0 : true;
        var enCierre = cierreF ? cierreF.getBoundingClientRect().top < window.innerHeight * 0.8 : false;
        barra.classList.toggle("ver", pasoHero && !enCierre);
      }
    };
    window.addEventListener("scroll", espiar, { passive: true }); espiar();
  }

  // ---------- filtros de los catálogos (buscar + categorías)
  var fh = document.querySelector(".filtro-hub");
  if (fh) {
    var fin = fh.querySelector("input"), chips = fh.querySelectorAll(".fh-chips button"), bloques = document.querySelectorAll(".cat-bloque"), cat = "", fvac = fh.querySelector(".fh-vacio");
    var filtrar = function () {
      var q = norm(fin.value.trim()), total = 0;
      bloques.forEach(function (b) {
        var n = 0;
        b.querySelectorAll(".catalogo li").forEach(function (li) { var ok = !q || norm(li.dataset.q).indexOf(q) > -1; li.hidden = !ok; if (ok) { n++; li.classList.add("on"); } });
        b.hidden = (cat && b.id !== cat) || n === 0; if (!b.hidden) total += n;
        b.querySelectorAll(".rev").forEach(function (r) { r.classList.add("on"); });
      });
      fvac.hidden = total > 0;
    };
    fin.addEventListener("input", filtrar);
    chips.forEach(function (c) { c.addEventListener("click", function () {
      chips.forEach(function (x) { x.classList.toggle("on", x === c); }); cat = c.dataset.c; filtrar();
      var top = fh.getBoundingClientRect().top + window.scrollY - 58;
      if (window.scrollY > top) (lenis ? lenis.scrollTo(top) : window.scrollTo({ top: top, behavior: "smooth" }));
    }); });
    if (location.hash) { var h = location.hash.slice(1); chips.forEach(function (c) { if (c.dataset.c === h) c.click(); }); }
  }
})();
