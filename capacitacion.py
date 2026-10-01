# -*- coding: utf-8 -*-
# noon Clinic · página INTERNA "Capacitación comercial" (con código de acceso, no indexada, sin enlace desde la web).
# Se genera sola al correr build.py. Toma los procedimientos de datos_noon.py.
import os, json, hashlib
from datos_noon import CIRUGIAS_NOON, TRATAMIENTOS, CATEGORIAS_CX, CATEGORIAS_ME

AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGO = "noon2026"  # código de acceso para el equipo comercial

DOCTORES = [
    {"id": "fernando", "nombre": "Dr. Fernando Ruiz", "area": "Cirugía plástica", "foto": "assets/equipo/fernando-ruiz.jpg"},
    {"id": "valeria", "nombre": "Dra. Valeria Enciso", "area": "Medicina estética", "foto": "assets/equipo/valeria-enciso.jpg"},
]
# Horarios de valoración. Vacío = "Por definir". Ej: "Lunes": "8:00 a. m. – 12:00 m."
DISPONIBILIDAD = {
    "fernando": {"Lunes": "", "Martes": "", "Miércoles": "", "Jueves": "", "Viernes": "", "Sábado": ""},
    "valeria": {"Lunes": "", "Martes": "", "Miércoles": "", "Jueves": "", "Viernes": "", "Sábado": ""},
}

PRECIO = ("Cada plan es personal, así que el valor depende de ti: de tu cuerpo, de lo que quieres lograr y de la técnica que "
          "el especialista te recomiende. Por eso el primer paso es tu cita de valoración con {doc}. Ahí te examina, te explica "
          "tus opciones y sales con tu presupuesto por escrito. ¿Te agendo? Tengo espacio el ___ o el ___.")


def _faq_cx(c, doc):
    d = c["datos"]
    return ([("¿Cuánto cuesta?", PRECIO.format(doc=doc))]
            + [(p, r) for p, r in c["faq"]]
            + [("¿Cuánto dura la cirugía?", "Aproximadamente %s. El tiempo exacto lo define el cirujano en la valoración." % d[0].lower()),
               ("¿Qué anestesia usan?", "%s. Se decide en la valoración según tu caso y tus exámenes." % d[1]),
               ("¿Cuántos días de incapacidad necesito?", "Como guía, %s. Tu cirujano te lo confirma según tu trabajo y tu recuperación." % d[2].lower()),
               ("¿Cuándo veo el resultado final?", "%s, aproximadamente. Los primeros cambios se ven antes, pero el cuerpo necesita ese tiempo para asentarse." % d[3]),
               ("¿Dónde me operan?", "En salas de cirugía habilitadas, nunca en un consultorio. Antes te pedimos exámenes prequirúrgicos: sin exámenes en regla no hay cirugía."),
               ("¿Necesito acompañante?", "Sí: un adulto que te acompañe el día de la cirugía y como mínimo la primera noche.")])


def _faq_me(t, doc):
    d = t["datos"]
    return ([("¿Cuánto cuesta?", PRECIO.format(doc=doc))]
            + [(p, r) for p, r in t["faq"]]
            + [("¿Cuántas sesiones necesito?", "Como guía: %s. La cantidad exacta la define la médica en la valoración según tu piel y tu objetivo." % d[0].lower()),
               ("¿Cuánto dura cada sesión?", "%s, aproximadamente." % d[1]),
               ("¿Puedo volver a mi rutina el mismo día?", "Recuperación: %s." % d[2].lower()),
               ("¿Cuándo se ve el resultado y cuánto dura?", "%s." % d[3]),
               ("¿Lo puedo combinar con otro tratamiento?", "Muchas veces sí, y los mejores resultados vienen de combinar. El plan se arma en la valoración.")])


def _proc(x, tipo, cats):
    doc = DOCTORES[0]["nombre"] if tipo == "cx" else DOCTORES[1]["nombre"]
    etiquetas = ("Duración", "Anestesia", "Incapacidad", "Resultado final") if tipo == "cx" else ("Sesiones", "Duración", "Recuperación", "Resultado")
    return {"slug": x["slug"], "tipo": tipo, "cat": cats[x["cat"]], "nombre": x["nombre"], "corto": x["corto"],
            "que_es": x["que_es"], "datos": list(zip(etiquetas, x["datos"])), "ideal": x["ideal"],
            "recuperacion": x.get("recuperacion", []), "doc": doc,
            "faq": _faq_cx(x, doc) if tipo == "cx" else _faq_me(x, doc),
            "cierre": "Lo mejor es que %s te valore: así sabes si eres candidata, qué resultado puedes esperar y el valor exacto de tu plan. ¿Te queda mejor el ___ o el ___?" % doc}


OBJECIONES = [
    ("“Solo dime un precio aproximado”",
     "No damos cifras sin valorar porque cada cuerpo es distinto y no queremos darte un número que después cambie. En la valoración sales con tu presupuesto exacto y por escrito. ¿Te agendo esta semana?"),
    ("“¿Por qué cobran la valoración?”",
     "Porque es una consulta médica real con el especialista: te examina, resuelve tus dudas y te entrega un plan por escrito. No es una charla de ventas."),
    ("“En otro lugar me dieron precio por WhatsApp”",
     "Un precio sin examinarte puede sonar fácil, pero no te dice si eres candidata ni qué incluye. Aquí primero te valora el especialista para que decidas con información completa y segura."),
    ("“Lo voy a pensar”",
     "¡Claro! Justamente la valoración es para eso: decidir con toda la información. No te compromete a operarte. ¿Te separo un espacio y lo piensas con tu presupuesto en la mano?"),
    ("“Vivo en otra ciudad”",
     "Te ayudamos a organizar tus fechas para que valoración, procedimiento y controles te queden en un mismo viaje. ¿En qué fechas podrías venir?"),
    ("“¿Me puedo operar ya / esta semana?”",
     "Antes de cualquier cirugía necesitas tu valoración y tus exámenes prequirúrgicos. Empecemos por la valoración y desde ahí te damos la fecha más cercana posible."),
]

REGLAS = [
    ("Tu meta es agendar la valoración", "No vendes la cirugía ni el tratamiento: vendes la cita de valoración. Ahí el especialista arma el plan y el presupuesto."),
    ("Nunca des precios", "Ni aproximados, ni rangos, ni “desde”. La respuesta es siempre: depende de ti, por eso necesitamos verte en tu valoración."),
    ("No diagnostiques ni prometas resultados", "Explica el procedimiento en general. Si la paciente pregunta “¿yo soy candidata?”, la respuesta es: eso lo define el especialista en la valoración."),
    ("Cierra siempre con dos fechas", "No preguntes “¿quieres agendar?”. Pregunta “¿te queda mejor el martes o el jueves?”."),
]

PASOS = [
    ("Saluda y escucha", "Pregunta su nombre y qué le gustaría mejorar. Deja que cuente."),
    ("Conecta", "Repite lo que quiere con sus palabras y explica en dos líneas en qué consiste el procedimiento."),
    ("Responde dudas", "Usa las preguntas frecuentes de cada procedimiento. Si preguntan precio, usa el guion."),
    ("Agenda", "Ofrece dos fechas concretas de la pestaña Disponibilidad y confirma nombre, ciudad y teléfono."),
]


def generar():
    procs = ([_proc(c, "cx", {k: n for k, n, d, f in CATEGORIAS_CX}) for c in CIRUGIAS_NOON]
             + [_proc(t, "me", {k: n for k, n, d, f in CATEGORIAS_ME}) for t in TRATAMIENTOS])
    datos = {"procs": procs, "cats_cx": [n for k, n, d, f in CATEGORIAS_CX], "cats_me": [n for k, n, d, f in CATEGORIAS_ME],
             "doctores": DOCTORES, "disp": DISPONIBILIDAD, "objeciones": OBJECIONES, "reglas": REGLAS, "pasos": PASOS,
             "precio": PRECIO}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.replace("%%DATOS%%", js).replace("%%HASH%%", hashlib.sha256(CODIGO.encode()).hexdigest())
    with open(os.path.join(AQUI, "capacitacion-comercial.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(procs)


PLANTILLA = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Capacitación comercial · noon Clinic</title>
<meta name="theme-color" content="#120d0a">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,400&family=Jost:wght@300;400&family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,600&display=swap" rel="stylesheet">
<style>
:root { --negro:#120d0a; --cafe:#1b1411; --ivory:#F2EFE8; --bone:#D8D0C3; --taupe:#A69A8B; --burgundy:#6D2835; --champagne:#BDA47B;
  --tenue:rgba(242,239,232,.62); --linea:rgba(242,239,232,.13); --display:"Jost",Futura,sans-serif; --serif:"Cormorant Garamond",Georgia,serif;
  --texto:"Nunito Sans","Avenir Next",-apple-system,sans-serif; --lado:clamp(16px,4vw,48px); --ease:cubic-bezier(.2,.7,.1,1); }
*,*::before,*::after { box-sizing:border-box; }
html { -webkit-text-size-adjust:100%; }
body { margin:0; background:var(--negro); color:var(--ivory); font:300 16px/1.65 var(--texto); -webkit-font-smoothing:antialiased; }
button,input { font:inherit; color:inherit; }
a { color:inherit; }
h1,h2,h3 { margin:0; font-family:var(--display); font-weight:300; }
h1 em,h2 em { font-family:var(--serif); font-style:italic; font-weight:300; }
p { margin:0 0 1em; }
:focus-visible { outline:1px solid var(--champagne); outline-offset:3px; }
.ceja { font:400 11px/1.4 var(--display); letter-spacing:.3em; text-transform:uppercase; color:var(--tenue); margin:0 0 18px; display:flex; align-items:center; gap:14px; }
.ceja::before { content:""; width:30px; height:1px; background:currentColor; opacity:.7; }
[hidden] { display:none !important; }

/* acceso */
.acceso { min-height:100vh; min-height:100dvh; display:grid; place-items:center; padding:24px var(--lado); background:var(--negro) url(assets/noon/seda-oscura.jpg) center/cover; position:relative; }
.acceso::before { content:""; position:absolute; inset:0; background:rgba(18,13,10,.7); }
.acceso form { position:relative; width:min(400px,100%); display:grid; gap:20px; }
.acceso img { height:34px; width:auto; margin-bottom:26px; }
.acceso h1 { font-size:clamp(34px,7vw,46px); line-height:1.1; margin-bottom:4px; }
.acceso p { color:var(--tenue); margin:0; }
.acceso input { width:100%; background:transparent; border:0; border-bottom:1px solid var(--linea); padding:14px 0; font-size:18px; letter-spacing:.08em; outline:none; transition:border-color .3s; }
.acceso input:focus { border-color:var(--champagne); }
.acceso .error { color:#e3a3ad; font-size:14px; min-height:1.4em; }
.boton { display:inline-flex; align-items:center; justify-content:center; gap:10px; padding:16px 28px; border:1px solid currentColor; background:transparent; font:400 11.5px/1 var(--display); letter-spacing:.24em; text-transform:uppercase; text-decoration:none; cursor:pointer; transition:background .3s,color .3s; }
.boton.lleno, .boton:hover { background:var(--ivory); color:var(--negro); border-color:var(--ivory); }
.boton.lleno:hover { background:transparent; color:var(--ivory); }

/* cabecera */
.cab { position:sticky; top:0; z-index:30; display:grid; grid-template-columns:1fr auto 1fr; align-items:center; padding:14px var(--lado); background:rgba(18,13,10,.88); backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); border-bottom:1px solid var(--linea); }
.hamb { justify-self:start; display:flex; align-items:center; gap:12px; background:none; border:0; cursor:pointer; padding:8px 0; font:400 11px var(--display); letter-spacing:.28em; text-transform:uppercase; }
.rayas { width:24px; height:8px; border-block:1px solid currentColor; }
.cab .logo img { height:24px; width:auto; display:block; }
.cab .etq { justify-self:end; font:400 10.5px var(--display); letter-spacing:.26em; text-transform:uppercase; color:var(--champagne); text-align:right; }

/* menú lateral */
.velo { position:fixed; inset:0; z-index:40; background:rgba(0,0,0,.5); opacity:0; pointer-events:none; transition:opacity .35s; }
.cajon { position:fixed; inset:0 auto 0 0; z-index:41; width:min(340px,86vw); background:var(--cafe); border-right:1px solid var(--linea); transform:translateX(-100%); transition:transform .45s var(--ease); display:flex; flex-direction:column; padding:26px 26px 30px; overflow-y:auto; }
.abierto .velo { opacity:1; pointer-events:auto; }
.abierto .cajon { transform:none; }
.cajon .cerrar { align-self:flex-end; background:none; border:0; cursor:pointer; font:400 11px var(--display); letter-spacing:.26em; text-transform:uppercase; color:var(--tenue); padding:6px 0; }
.cajon nav { display:grid; margin-top:30px; }
.cajon nav a { display:grid; gap:4px; padding:15px 0; border-bottom:1px solid var(--linea); text-decoration:none; font:300 22px/1.25 var(--display); transition:color .25s; }
.cajon nav a small { font:400 10.5px var(--display); letter-spacing:.2em; text-transform:uppercase; color:var(--tenue); }
.cajon nav a:hover, .cajon nav a.activo { color:var(--champagne); }
.cajon .salir { margin-top:auto; padding-top:30px; background:none; border:0; text-align:left; cursor:pointer; color:var(--tenue); font:400 11px var(--display); letter-spacing:.24em; text-transform:uppercase; }

/* contenido */
main { max-width:900px; margin:0 auto; padding:clamp(34px,6vw,64px) var(--lado) 90px; }
.titulo { margin-bottom:34px; }
.titulo h1 { font-size:clamp(34px,6.5vw,56px); line-height:1.08; letter-spacing:-.01em; }
.titulo .sub { color:var(--tenue); margin-top:14px; max-width:600px; }
.migas { display:flex; flex-wrap:wrap; gap:8px; font:400 11px var(--display); letter-spacing:.2em; text-transform:uppercase; color:var(--tenue); margin-bottom:22px; }
.migas a { text-decoration:none; } .migas a:hover { color:var(--champagne); }

.busca { display:flex; align-items:center; gap:12px; border-bottom:1px solid var(--linea); margin:0 0 30px; }
.busca svg { width:18px; height:18px; fill:none; stroke:var(--tenue); stroke-width:1.4; flex:none; }
.busca input { flex:1; background:transparent; border:0; outline:none; padding:14px 0; font-size:16px; }
.grupo { margin-bottom:36px; }
.grupo h2 { font:400 11px var(--display); letter-spacing:.3em; text-transform:uppercase; color:var(--champagne); margin-bottom:6px; }
.fila { display:grid; grid-template-columns:1fr auto; gap:6px 18px; align-items:center; padding:18px 0; border-bottom:1px solid var(--linea); text-decoration:none; }
.fila b { font:300 21px/1.3 var(--display); }
.fila span { grid-column:1; color:var(--tenue); font-size:14.5px; line-height:1.5; }
.fila i { grid-row:1/3; grid-column:2; font-style:normal; color:var(--tenue); transition:transform .3s var(--ease),color .3s; }
.fila:hover i { transform:translateX(4px); color:var(--champagne); }
.vacio { color:var(--tenue); }

/* guion de precio y cierre */
.guion { border:1px solid rgba(189,164,123,.45); background:rgba(109,40,53,.16); padding:22px 22px 18px; margin:0 0 38px; }
.guion .ceja { color:var(--champagne); margin-bottom:12px; }
.guion p { font-size:16.5px; margin-bottom:14px; }
.copiar { background:none; border:0; border-bottom:1px solid currentColor; padding:0 0 4px; cursor:pointer; font:400 10.5px var(--display); letter-spacing:.22em; text-transform:uppercase; color:var(--champagne); }

.bloque { margin:0 0 40px; }
.bloque > h2 { font-size:clamp(24px,4vw,30px); margin-bottom:16px; }
.bloque p { color:rgba(242,239,232,.86); }
.ficha { display:grid; grid-template-columns:repeat(4,1fr); border-top:1px solid var(--linea); border-bottom:1px solid var(--linea); margin:6px 0 0; }
.ficha div { padding:16px 14px 16px 0; }
.ficha div + div { padding-left:14px; border-left:1px solid var(--linea); }
.ficha small { display:block; font:400 10px var(--display); letter-spacing:.22em; text-transform:uppercase; color:var(--tenue); margin-bottom:6px; }
.ficha b { font-weight:400; font-size:15px; line-height:1.4; }
.lista { list-style:none; margin:0; padding:0; }
.lista li { padding:12px 0 12px 26px; border-bottom:1px solid var(--linea); position:relative; }
.lista li::before { content:""; position:absolute; left:0; top:24px; width:12px; height:1px; background:var(--champagne); }
.pasos { display:grid; gap:0; counter-reset:p; }
.pasos div { display:grid; grid-template-columns:120px 1fr; gap:14px; padding:13px 0; border-bottom:1px solid var(--linea); }
.pasos b { font-weight:400; color:var(--champagne); font-size:14.5px; }
.pasos span { color:rgba(242,239,232,.86); }

details { border-bottom:1px solid var(--linea); }
details:first-of-type { border-top:1px solid var(--linea); }
summary { list-style:none; cursor:pointer; display:flex; justify-content:space-between; gap:16px; padding:17px 0; font:300 18px/1.4 var(--display); }
summary::-webkit-details-marker { display:none; }
summary::after { content:"+"; color:var(--champagne); font-size:20px; line-height:1; transition:transform .3s; }
details[open] summary::after { transform:rotate(45deg); }
details .resp { padding:0 0 18px; color:rgba(242,239,232,.86); }
details.precio summary { color:var(--champagne); }

/* inicio */
.puertas { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:46px; }
.puerta { position:relative; min-height:170px; padding:22px; display:flex; flex-direction:column; justify-content:flex-end; text-decoration:none; background:center/cover; overflow:hidden; isolation:isolate; }
.puerta::before { content:""; position:absolute; inset:0; z-index:-1; background:linear-gradient(180deg,rgba(18,13,10,.15),rgba(18,13,10,.82)); }
.puerta b { font:300 25px/1.15 var(--display); }
.puerta span { font:400 10.5px var(--display); letter-spacing:.22em; text-transform:uppercase; color:var(--bone); margin-top:8px; }
.reglas { display:grid; grid-template-columns:1fr 1fr; gap:0 28px; }
.regla { padding:18px 0; border-top:1px solid var(--linea); }
.regla b { display:block; font:400 17px/1.35 var(--display); margin-bottom:6px; }
.regla span { color:var(--tenue); font-size:15px; }

/* disponibilidad */
.docs { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
.doc { border:1px solid var(--linea); padding:22px; }
.doc .quien { display:flex; gap:16px; align-items:center; margin-bottom:18px; }
.doc img { width:64px; height:80px; object-fit:cover; flex:none; }
.doc h2 { font-size:22px; line-height:1.2; }
.doc .area { font:400 10.5px var(--display); letter-spacing:.22em; text-transform:uppercase; color:var(--champagne); margin-top:6px; }
.dia { display:flex; justify-content:space-between; gap:12px; padding:11px 0; border-top:1px solid var(--linea); font-size:15px; }
.dia span:last-child { text-align:right; }
.dia .pend { color:var(--tenue); font-style:italic; }
.nota { color:var(--tenue); font-size:14px; margin-top:26px; }

.aviso { position:fixed; left:50%; bottom:24px; transform:translate(-50%,20px); opacity:0; background:var(--ivory); color:var(--negro); padding:12px 20px; font:400 11px var(--display); letter-spacing:.2em; text-transform:uppercase; transition:.35s var(--ease); pointer-events:none; z-index:60; }
.aviso.ver { opacity:1; transform:translate(-50%,0); }

@media (max-width:700px) {
  .cab .etq { font-size:9.5px; letter-spacing:.18em; }
  .cab .hamb .txt { display:none; }
  .ficha { grid-template-columns:1fr 1fr; }
  .ficha div:nth-child(3) { padding-left:0; border-left:0; }
  .ficha div:nth-child(n+3) { border-top:1px solid var(--linea); }
  .puertas, .reglas, .docs { grid-template-columns:1fr; }
  .pasos div { grid-template-columns:1fr; gap:2px; }
}
@media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
</style>
</head>
<body>
<section class="acceso" id="acceso">
  <form id="form-acceso" autocomplete="off">
    <img src="assets/logo-noon-claro.png" alt="noon Clinic">
    <p class="ceja">Uso interno</p>
    <h1>Capacitación <em>comercial</em></h1>
    <p>Escribe el código de acceso del equipo.</p>
    <input id="codigo" type="password" inputmode="text" placeholder="Código de acceso" aria-label="Código de acceso" autofocus>
    <p class="error" id="error" role="alert"></p>
    <button class="boton lleno" type="submit">Entrar</button>
  </form>
</section>

<div id="app" hidden>
  <header class="cab">
    <button class="hamb" id="hamb" type="button" aria-expanded="false" aria-controls="cajon"><span class="rayas" aria-hidden="true"></span><span class="txt">Menú</span></button>
    <a class="logo" href="#inicio" aria-label="Inicio de la capacitación"><img src="assets/logo-noon-claro.png" alt="noon Clinic"></a>
    <span class="etq">Capacitación<br>comercial</span>
  </header>
  <div class="velo" id="velo"></div>
  <aside class="cajon" id="cajon" aria-label="Menú">
    <button class="cerrar" id="cerrar" type="button">Cerrar ✕</button>
    <nav id="nav">
      <a href="#inicio" data-r="inicio">Inicio <small>Cómo vender</small></a>
      <a href="#cirugia" data-r="cirugia">Cirugía plástica <small id="n-cx"></small></a>
      <a href="#estetica" data-r="estetica">Medicina estética <small id="n-me"></small></a>
      <a href="#objeciones" data-r="objeciones">Cómo responder <small>Precio y dudas</small></a>
      <a href="#disponibilidad" data-r="disponibilidad">Disponibilidad <small>Agenda</small></a>
    </nav>
    <button class="salir" id="salir" type="button">Salir</button>
  </aside>
  <main id="vista"></main>
</div>
<div class="aviso" id="aviso">Copiado</div>

<script>
const D = %%DATOS%%;
const HASH = "%%HASH%%";
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const norm = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

async function sha(t) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, "0")).join("");
}
function entrar() { $("#acceso").hidden = true; $("#app").hidden = false; ruta(); }
function guardado() { try { return localStorage.getItem("noon-cap") === HASH; } catch (e) { return false; } }
$("#form-acceso").addEventListener("submit", async e => {
  e.preventDefault();
  const h = await sha($("#codigo").value.trim().toLowerCase());
  if (h === HASH) { try { localStorage.setItem("noon-cap", HASH); } catch (e) {} entrar(); }
  else { $("#error").textContent = "Código incorrecto. Pídeselo a tu coordinadora."; $("#codigo").select(); }
});
$("#salir").addEventListener("click", () => { try { localStorage.removeItem("noon-cap"); } catch (e) {} location.hash = ""; location.reload(); });

// menú hamburguesa
const abrir = si => { document.body.classList.toggle("abierto", si); $("#hamb").setAttribute("aria-expanded", si); };
$("#hamb").onclick = () => abrir(true); $("#cerrar").onclick = () => abrir(false); $("#velo").onclick = () => abrir(false);
document.addEventListener("keydown", e => { if (e.key === "Escape") abrir(false); });
$("#n-cx").textContent = D.procs.filter(p => p.tipo === "cx").length + " cirugías";
$("#n-me").textContent = D.procs.filter(p => p.tipo === "me").length + " tratamientos";

// copiar guiones
document.addEventListener("click", e => {
  const b = e.target.closest(".copiar"); if (!b) return;
  navigator.clipboard.writeText(b.dataset.t).then(() => { const a = $("#aviso"); a.classList.add("ver"); setTimeout(() => a.classList.remove("ver"), 1400); });
});
const copiar = t => '<button class="copiar" type="button" data-t="' + esc(t) + '">Copiar mensaje</button>';

// vistas
function inicio() {
  return `<div class="titulo"><p class="ceja">Bienvenida al equipo</p><h1>Vendemos la <em>valoración</em>.</h1>
    <p class="sub">Aquí aprendes cada procedimiento de noon Clinic, qué responder a las preguntas de los pacientes y cómo llevar cada conversación a una cita de valoración.</p></div>
  <div class="puertas">
    <a class="puerta" href="#cirugia" style="background-image:url(assets/noon/seda-cafe.jpg)"><b>Cirugía plástica</b><span>${D.procs.filter(p => p.tipo === "cx").length} procedimientos · ${esc(D.doctores[0].nombre)}</span></a>
    <a class="puerta" href="#estetica" style="background-image:url(assets/noon/seda-champan.jpg)"><b>Medicina estética</b><span>${D.procs.filter(p => p.tipo === "me").length} tratamientos · ${esc(D.doctores[1].nombre)}</span></a>
  </div>
  <div class="bloque"><p class="ceja">Las 4 reglas de oro</p><div class="reglas">${D.reglas.map(([t, x]) => `<div class="regla"><b>${esc(t)}</b><span>${esc(x)}</span></div>`).join("")}</div></div>
  <div class="guion"><p class="ceja">Si te preguntan “¿cuánto vale?”</p><p>${esc(D.precio.replace("{doc}", "el especialista"))}</p>${copiar(D.precio.replace("{doc}", "el especialista"))}</div>
  <div class="bloque"><h2>Una conversación en <em>4 pasos</em></h2><div class="pasos">${D.pasos.map(([t, x], i) => `<div><b>${i + 1}. ${esc(t)}</b><span>${esc(x)}</span></div>`).join("")}</div></div>`;
}

function listado(tipo) {
  const cx = tipo === "cx", cats = cx ? D.cats_cx : D.cats_me, doc = D.doctores[cx ? 0 : 1];
  const ps = D.procs.filter(p => p.tipo === tipo);
  const grupos = cats.map(c => { const it = ps.filter(p => p.cat === c); return `<div class="grupo"><h2>${esc(c)}</h2>${it.map(p =>
    `<a class="fila" href="#p/${p.slug}" data-b="${esc(norm(p.nombre + " " + p.corto + " " + c))}"><b>${esc(p.nombre)}</b><span>${esc(p.corto)}</span><i>→</i></a>`).join("")}</div>`; }).join("");
  return `<div class="titulo"><p class="ceja">${esc(doc.nombre)} · ${esc(doc.area)}</p><h1>${cx ? "Cirugía <em>plástica</em>" : "Medicina <em>estética</em>"}</h1>
    <p class="sub">Toca un procedimiento para ver qué es, en qué consiste y las preguntas que más hacen los pacientes.</p></div>
  <label class="busca"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg><input id="filtro" type="search" placeholder="Buscar procedimiento…"></label>
  <div id="grupos">${grupos}</div><p class="vacio" hidden>No hay procedimientos con ese nombre.</p>`;
}

function detalle(slug) {
  const p = D.procs.find(x => x.slug === slug); if (!p) return inicio();
  const cx = p.tipo === "cx";
  return `<nav class="migas"><a href="#${cx ? "cirugia" : "estetica"}">${cx ? "Cirugía plástica" : "Medicina estética"}</a><span>/</span><span>${esc(p.cat)}</span></nav>
  <div class="titulo"><h1>${esc(p.nombre)}</h1><p class="sub">${esc(p.corto)}</p></div>
  <div class="guion"><p class="ceja">Si preguntan el valor</p><p>${esc(D.precio.replace("{doc}", p.doc))}</p>${copiar(D.precio.replace("{doc}", p.doc))}</div>
  <div class="bloque"><h2>¿Qué <em>es</em>?</h2>${p.que_es.map(x => `<p>${esc(x)}</p>`).join("")}</div>
  <div class="bloque"><h2>¿En qué <em>consiste</em>?</h2><p>Datos orientativos para explicarle al paciente. El plan exacto lo define ${esc(p.doc)} en la valoración.</p>
    <div class="ficha">${p.datos.map(([k, v]) => `<div><small>${esc(k)}</small><b>${esc(v)}</b></div>`).join("")}</div></div>
  <div class="bloque"><h2>¿Para <em>quién</em> es?</h2><ul class="lista">${p.ideal.map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>
  ${p.recuperacion.length ? `<div class="bloque"><h2>La <em>recuperación</em></h2><div class="pasos">${p.recuperacion.map(([t, x]) => `<div><b>${esc(t)}</b><span>${esc(x)}</span></div>`).join("")}</div></div>` : ""}
  <div class="bloque"><h2>Preguntas <em>frecuentes</em></h2>${p.faq.map(([q, r], i) => `<details class="${i === 0 ? "precio" : ""}"><summary>${esc(q)}</summary><div class="resp"><p>${esc(r)}</p>${copiar(r)}</div></details>`).join("")}</div>
  <div class="guion"><p class="ceja">Cómo cerrar</p><p>${esc(p.cierre)}</p>${copiar(p.cierre)}</div>`;
}

function objeciones() {
  return `<div class="titulo"><p class="ceja">Guiones</p><h1>Cómo <em>responder</em></h1><p class="sub">Las dudas más comunes y una respuesta lista para copiar. Úsalas con tus palabras y termina siempre ofreciendo dos fechas.</p></div>
  <div class="guion"><p class="ceja">“¿Cuánto vale?”</p><p>${esc(D.precio.replace("{doc}", "el especialista"))}</p>${copiar(D.precio.replace("{doc}", "el especialista"))}</div>
  <div class="bloque">${D.objeciones.map(([q, r]) => `<details><summary>${esc(q)}</summary><div class="resp"><p>${esc(r)}</p>${copiar(r)}</div></details>`).join("")}</div>`;
}

function disponibilidad() {
  return `<div class="titulo"><p class="ceja">Agenda de valoraciones</p><h1><em>Disponibilidad</em></h1><p class="sub">Horarios para ofrecer citas de valoración. Ofrece siempre dos opciones concretas.</p></div>
  <div class="docs">${D.doctores.map(d => `<div class="doc"><div class="quien"><img src="${d.foto}" alt=""><div><h2>${esc(d.nombre)}</h2><p class="area">(${esc(d.area)})</p></div></div>
    ${Object.entries(D.disp[d.id]).map(([dia, h]) => `<div class="dia"><span>${esc(dia)}</span><span class="${h ? "" : "pend"}">${h ? esc(h) : "Por definir"}</span></div>`).join("")}</div>`).join("")}</div>
  <p class="nota">Los horarios se actualizan aquí. Si un horario no aparece, confirma con la coordinación antes de ofrecerlo.</p>`;
}

function ruta() {
  if ($("#app").hidden) return;
  const h = location.hash.slice(1) || "inicio";
  let html, r = h;
  if (h.startsWith("p/")) { html = detalle(h.slice(2)); r = (D.procs.find(x => x.slug === h.slice(2)) || {}).tipo === "me" ? "estetica" : "cirugia"; }
  else html = ({ cirugia: () => listado("cx"), estetica: () => listado("me"), objeciones, disponibilidad }[h] || inicio)();
  $("#vista").innerHTML = html;
  document.querySelectorAll("#nav a").forEach(a => a.classList.toggle("activo", a.dataset.r === r));
  abrir(false); window.scrollTo(0, 0);
  const f = $("#filtro");
  if (f) f.addEventListener("input", () => {
    const q = norm(f.value.trim()); let n = 0;
    document.querySelectorAll(".fila").forEach(a => { const ok = !q || a.dataset.b.includes(q); a.hidden = !ok; n += ok; });
    document.querySelectorAll(".grupo").forEach(g => g.hidden = !g.querySelector(".fila:not([hidden])"));
    $(".vacio").hidden = n > 0;
  });
}
addEventListener("hashchange", ruta);
if (guardado()) entrar();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("Capacitación comercial: %d procedimientos." % generar())
