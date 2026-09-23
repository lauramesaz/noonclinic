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
})();
