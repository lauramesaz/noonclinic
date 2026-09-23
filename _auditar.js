// Revisor de responsive: se carga en cada página y devuelve problemas
window.__auditar = () => {
  const W = document.documentElement.clientWidth, out = [];
  const dentroDeScroll = (el) => { for (let p = el.parentElement; p; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll') return true; } return false; };
  const nombre = (el) => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  if (document.documentElement.scrollWidth > W + 1) out.push('DESBORDE página: ' + document.documentElement.scrollWidth + ' > ' + W);
  document.querySelectorAll('main *, footer *, header .barra > *').forEach((el) => {
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') return;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
    if ((r.right > W + 2 || r.left < -2) && !dentroDeScroll(el) && !el.closest('.hero::before')) out.push('SE SALE: ' + nombre(el) + ' [' + Math.round(r.left) + '→' + Math.round(r.right) + ']');
    if (['hidden', 'clip'].includes(cs.overflowX) && el.scrollWidth > el.clientWidth + 2 && el.children.length === 0) out.push('TEXTO CORTADO: ' + nombre(el) + ' "' + el.textContent.trim().slice(0, 30) + '"');
    if (W < 721 && el.matches('a.btn, button, summary, .tabs a, .chip') && r.height < 40) out.push('TOQUE PEQUEÑO (' + Math.round(r.height) + 'px): ' + nombre(el) + ' "' + el.textContent.trim().slice(0, 24) + '"');
    if (el.children.length === 0 && el.textContent.trim() && parseFloat(cs.fontSize) < 11.5) out.push('LETRA MUY PEQUEÑA (' + cs.fontSize + '): ' + nombre(el) + ' "' + el.textContent.trim().slice(0, 24) + '"');
  });
  return [...new Set(out)].slice(0, 14);
};
