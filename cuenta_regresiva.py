# -*- coding: utf-8 -*-
# noon Clinic · CUENTA REGRESIVA hasta el fin de las promos de fin de año (plan comercial del 4-nov-2026, arreglo 3).
# "Faltan 10 semanas para el 15 de enero." Se calcula EN EL NAVEGADOR con la hora de Colombia (UTC-5, sin horario de verano),
# así nunca queda vieja aunque la página no se vuelva a publicar:
#   - 14 días o más  → en semanas completas ("Faltan 10 semanas…").
#   - menos de 14    → en días ("Faltan 9 días…", "Falta 1 día…").
#   - desde el 15-ene-2027 (00:00 en Colombia) → desaparece.
# Sin JavaScript no se ve (va con hidden): mejor nada que una cuenta equivocada.
# Va EN LÍNEA (estilo + script) y no en assets/, para no mover la versión ?v= de las 200 páginas de la web (como wa_google.py).
# La usan las promos (landing_promos.py) y las de "¿Vienes en diciembre?" (landing_afuera.py).
from datos import FECHA_LIMITE

FIN = (2027, 1, 15)  # = FECHA_LIMITE de datos.py ("15 de enero de 2027"): las cirugías de promo deben hacerse ANTES de este día
assert FECHA_LIMITE == "15 de enero de 2027", "Cambió FECHA_LIMITE en datos.py: actualiza FIN aquí (y los textos '15 de enero')"


def bloque(despues="", lang="es", clase=""):
    """La línea de la cuenta. 'despues' = la frase que sigue (p. ej. 'Separa tu fecha con $1.000.000.').
    El número que trae es solo de relleno: va oculta y el script (al final de la página) pone el de hoy y la muestra."""
    return ('<p class="pr-cuenta%s" data-cuenta hidden><i aria-hidden="true"></i><span><b data-cuenta-n>%s</b>%s</span></p>' % (
        (" " + clase) if clase else "",
        "10 weeks left until January 15." if lang == "en" else "Faltan 10 semanas para el 15 de enero.",
        (" " + despues) if despues else ""))


CSS = """<style>
/* cuenta regresiva (cuenta_regresiva.py) */
.pr-cuenta{display:flex;align-items:flex-start;gap:10px;margin:0 0 22px;max-width:470px;font-size:15px;line-height:1.45;color:var(--tenue)}
.pr-cuenta[hidden]{display:none}
.pr-cuenta i{flex:none;width:8px;height:8px;margin-top:6.5px;border-radius:50%;background:var(--champan);box-shadow:0 0 0 4px rgba(201,168,118,.22)}
.pr-cuenta b{font:600 15px/1.45 var(--display);color:var(--tinta);letter-spacing:-.005em}
.pr-cierre .pr-cuenta{justify-content:center;margin:-14px auto 26px;text-align:left}
@media (max-width:760px){.pr-cuenta{margin-bottom:16px;font-size:14.5px}.pr-cuenta b{font-size:14.5px}.pr-cierre .pr-cuenta{margin-top:-18px}}
</style>"""


def script():
    y, m, d = FIN
    return """<script>(function () {
  // %(fecha)s, 00:00 en Colombia (UTC-5) = 05:00 UTC
  var fin = Date.UTC(%(y)d, %(m)d, %(d)d, 5, 0, 0), dias = Math.ceil((fin - Date.now()) / 864e5);
  var cuentas = document.querySelectorAll("[data-cuenta]");
  if (!cuentas.length) return;
  if (!(dias > 0)) { Array.prototype.forEach.call(cuentas, function (c) { c.parentNode.removeChild(c); }); return; }
  var en = (document.documentElement.lang || "").slice(0, 2) === "en", n, t;
  if (dias >= 14) { n = Math.floor(dias / 7); t = en ? n + " weeks left until January 15." : "Faltan " + n + " semanas para el 15 de enero."; }
  else { t = en ? dias + (dias === 1 ? " day" : " days") + " left until January 15." : (dias === 1 ? "Falta 1 día" : "Faltan " + dias + " días") + " para el 15 de enero."; }
  Array.prototype.forEach.call(cuentas, function (c) { var b = c.querySelector("[data-cuenta-n]"); if (b) b.textContent = t; c.hidden = false; });
})();</script>""" % {"fecha": "%04d-%02d-%02d" % (y, m, d), "y": y, "m": m - 1, "d": d}
