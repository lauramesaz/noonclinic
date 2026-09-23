// Direcciones limpias: si alguien entra por un link viejo con .html, se limpia la barra
if (/^https?:$/.test(location.protocol) && /\.html$/.test(location.pathname)) {
  history.replaceState(null, '', location.pathname.replace(/(^|\/)index\.html$/, '$1').replace(/\.html$/, '') + location.search + location.hash);
}

// Menú móvil
const hamb = document.querySelector('.hamb');
const nav = document.querySelector('.nav');
if (hamb) hamb.addEventListener('click', () => {
  const abierto = nav.classList.toggle('abierto');
  hamb.setAttribute('aria-expanded', abierto);
  hamb.textContent = abierto ? '×' : '☰';
});

// Aparición suave al hacer scroll
let pendientes = [...document.querySelectorAll('.ver')];
const revelar = () => {
  const alto = window.innerHeight;
  pendientes = pendientes.filter((el) => {
    if (el.getBoundingClientRect().top < alto * 0.92) { el.classList.add('ya'); return false; }
    return true;
  });
  if (!pendientes.length) window.removeEventListener('scroll', revelar);
};
window.addEventListener('scroll', revelar, { passive: true });
window.addEventListener('resize', revelar);
window.addEventListener('load', revelar);
revelar();

// Preguntas frecuentes: buscador + filtros por tema
const caja = document.querySelector('[data-faq]');
if (caja) {
  const items = [...caja.querySelectorAll('details')];
  const botones = [...document.querySelectorAll('.filtros button')];
  const buscador = document.querySelector('.buscador');
  const vacio = document.querySelector('.vacio');
  let tema = 'todas';
  const limpio = (t) => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  const aplicar = () => {
    const q = limpio(buscador.value.trim());
    let n = 0;
    items.forEach((d) => {
      const ok = (tema === 'todas' || d.dataset.cat === tema) && (!q || limpio(d.textContent).includes(q));
      d.hidden = !ok;
      if (ok) n++;
    });
    vacio.hidden = n > 0;
  };
  botones.forEach((b) => b.addEventListener('click', () => {
    tema = b.dataset.cat;
    botones.forEach((x) => x.classList.toggle('on', x === b));
    aplicar();
  }));
  buscador.addEventListener('input', aplicar);
}

// Formulario de valoración: arma el mensaje y abre WhatsApp (no guarda datos en ninguna parte)
const form = document.querySelector('#form-valoracion');
if (form) {
  const pre = new URLSearchParams(location.search).get('cx');
  if (pre) { const op = [...form.cirugia.options].find((o) => o.dataset.slug === pre); if (op) op.selected = true; }
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const msj = `Hola, soy ${d.get('nombre')}. Quiero agendar mi cita de valoración para: ${d.get('cirugia')}. Estoy en ${d.get('ciudad')}.`;
    window.open(`https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(msj)}`, '_blank', 'noopener');
  });
}

// Selector "¿Qué quieres lograr?" del inicio
const sel = document.querySelector('[data-selector]');
if (sel) {
  const datos = JSON.parse(sel.dataset.selector);
  const chips = [...sel.querySelectorAll('.chip')];
  const caja = sel.querySelector('.resultado');
  const pintar = (i) => {
    const d = datos[i];
    chips.forEach((c, n) => c.classList.toggle('on', n === i));
    caja.querySelector('.nom').textContent = d.nombre;
    caja.querySelector('p').textContent = d.por;
    caja.querySelector('.valor').textContent = d.precio;
    caja.querySelector('a').href = d.slug;
    const tl = caja.querySelector('.trae-linea');
    if (tl) tl.innerHTML = d.trae.map((x) => '<span>' + x + '</span>').join('') + '<span class="n">+ ' + d.mas + ' más</span>';
  };
  chips.forEach((c, i) => c.addEventListener('click', () => pintar(i)));
  pintar(0);
}

// Barra de acción fija: aparece al bajar y se esconde al llegar al cierre
const accion = document.querySelector('.accion');
if (accion) {
  const fin = document.querySelector('.cierre') || document.querySelector('.pie');
  const mover = () => {
    const cerca = fin.getBoundingClientRect().top < window.innerHeight * 0.8;
    accion.classList.toggle('visible', window.scrollY > 520 && !cerca);
  };
  window.addEventListener('scroll', mover, { passive: true });
  mover();
}

// Cerrar menú móvil al elegir un enlace
document.querySelectorAll('.nav a').forEach((a) => a.addEventListener('click', () => nav.classList.remove('abierto')));

// Foco de luz que sigue el cursor sobre las tarjetas
document.querySelectorAll('a.tarjeta').forEach((t) => t.addEventListener('pointermove', (e) => {
  const r = t.getBoundingClientRect();
  t.style.setProperty('--mx', (e.clientX - r.left) + 'px');
  t.style.setProperty('--my', (e.clientY - r.top) + 'px');
}));

// Precios que cuentan hacia arriba al aparecer
const cuentas = [...document.querySelectorAll('[data-cuenta]')];
if (cuentas.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const fmt = (n) => '$' + Math.round(n).toLocaleString('es-CO').replace(/,/g, '.');
  const animar = (el) => {
    const fin = parseInt(el.textContent.replace(/\D/g, ''), 10), t0 = performance.now(), dur = 1100, texto = el.textContent;
    const paso = (t) => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      el.textContent = p < 1 ? fmt(fin * (0.6 + 0.4 * e)) : texto;
      if (p < 1) requestAnimationFrame(paso);
    };
    requestAnimationFrame(paso);
    setTimeout(() => { el.textContent = texto; }, dur + 300); // seguro: el precio real siempre queda
  };
  const revisar = () => {
    for (let i = cuentas.length - 1; i >= 0; i--) {
      if (cuentas[i].getBoundingClientRect().top < innerHeight * 0.9) { animar(cuentas[i]); cuentas.splice(i, 1); }
    }
    if (!cuentas.length) removeEventListener('scroll', revisar);
  };
  addEventListener('scroll', revisar, { passive: true });
  revisar();
}

// Titular vivo: la palabra rota y el precio cambia con ella
const rota = document.querySelector('[data-rota]');
if (rota && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const lista = JSON.parse(rota.dataset.rota), et = document.querySelector('.rota-et'), pr = document.querySelector('.rota-precio');
  let n = 0;
  setInterval(() => {
    n = (n + 1) % lista.length;
    [rota, et, pr].forEach((el) => el.classList.add('sale'));
    setTimeout(() => {
      rota.innerHTML = '<em>' + lista[n].p + '</em>,'; et.textContent = lista[n].e; pr.textContent = lista[n].v;
      [rota, et, pr].forEach((el) => el.classList.remove('sale'));
    }, 380);
  }, 2600);
}

// Frase gigante que se ilumina palabra por palabra al bajar
const ilu = document.querySelector('[data-ilumina]');
if (ilu) {
  const palabras = [...ilu.querySelectorAll('span')];
  const pintarFrase = () => {
    const r = ilu.getBoundingClientRect(), alto = innerHeight;
    const p = Math.min(1, Math.max(0, (alto * 0.85 - r.top) / (alto * 0.55 + r.height)));
    palabras.forEach((w, i) => w.classList.toggle('on', i < Math.round(p * palabras.length)));
  };
  addEventListener('scroll', pintarFrase, { passive: true });
  pintarFrase();
}
