# -*- coding: utf-8 -*-
# noon Clinic · "¿VIENES EN DICIEMBRE?" · promos de fin de año para quien vive fuera de Colombia (plan comercial del 4-nov-2026,
# punto 5 de "Lo que hago HOY" y jugada 8). Dos páginas, mismo contenido, cada una escrita en su idioma (no traducida palabra
# por palabra):
#   promos/vienes-en-diciembre.html → noon.clinic/promos/vienes-en-diciembre (español)
#   promos/holidays.html            → noon.clinic/promos/holidays (inglés)
# Diseño "Blanco y arco" de las promos (assets/promos.css, prefijo pr-) + lo propio de estas páginas en línea (prefijo af-),
# para no mover la versión ?v= de toda la web. Sin menú, todo a WhatsApp, noindex y fuera del sitemap (como las promos).
# REGLAS de estas páginas (las mismas de la capacitación, "Pacientes del exterior", y de _agencia-seo/hechos.md):
#   - SOLO PESOS COLOMBIANOS: nunca convertidos a dólares. Una línea: "Pagas en pesos colombianos; tu banco lo convierte…".
#   - La VALORACIÓN MÉDICA ES PRESENCIAL al llegar a Medellín. Desde allá se adelanta la preconsulta por video y las fotos con
#     el equipo médico, que da un valor ESTIMADO por escrito; la valoración presencial con el Dr. Fernando Ruiz confirma el plan
#     antes de la cirugía. Nada de "valoración virtual" ni "consulta por video con el cirujano".
#   - Cada página tiene su propio mensaje de WhatsApp (para contar los chats "vivo afuera") y el clic se mide como en toda la
#     web (evento clic_whatsapp del encabezado de medición) con origen promo-diaspora-es / promo-diaspora-en.
#   - NO se nombran Florida ni Puerto Rico (la alianza con la agencia de allá pide exclusividad). Los vuelos van por ciudad,
#     como dato de viaje.
#   - Ética médica: nada de "el mejor", nada de resultados prometidos.
# Fuentes: precios, abono y devolución = landing_promos.py y términos (datos.py); visa, vuelos y aeropuerto = hechos.md y
# capacitación; días de estadía, "un solo viaje" y seguimiento al volver = preguntas y guías de la web.
# landing_promos.generar() llama a generar() al final.
import json, os
from html import escape
from urllib.parse import quote

import cuenta_regresiva
import landing_promos as LP
from datos import FECHA_LIMITE, SEDE_QX

# Casa de recuperación cerca de Q2 (Recovery House, https://www.recoveryhouseinmedellin.com/, consultada el 4-nov-2026):
# "3 - 19 days … 390.000 COP / day". No es un servicio de noon: solo sirve para el ejemplo del costo del viaje.
CASA_URL = "https://www.recoveryhouseinmedellin.com/"
CASA_DIA = 390000
CASA_DIAS = 10
EJEMPLO = "mamoplastia-de-aumento"
ORDEN = ["mamoplastia-de-aumento", "mastopexia-sin-implantes", "mastopexia-con-implantes", "lipo"]  # las 4 con precio
VALORACION = 200000  # = VALORACION de datos.py ($200.000): la valoración presencial, que se hace en Medellín (va en el viaje)
GUIA = {"es": "/cuantos-dias-quedarse-en-colombia-despues-de-una-cirugia-plastica", "en": "/how-long-to-stay-in-colombia-after-plastic-surgery"}
TEL = "+57 302 249 1937"

assert FECHA_LIMITE == "15 de enero de 2027", "Cambió la fecha límite: revisa los textos '15 de enero' de esta página"
assert LP.ABONO == 1000000 and LP.DEVUELVE == 800000, "Cambió el abono o la devolución: revisa los textos de esta página"


def _n(x, lang):
    """Número con separador de miles del idioma: es 1.000.000 · en 1,000,000."""
    s = "{:,}".format(int(x))
    return s.replace(",", ".") if lang == "es" else s


def cop(x, lang):
    """Siempre en pesos colombianos: '$10.900.000' en español, 'COP 10,900,000' en inglés."""
    return ("$" + _n(x, lang)) if lang == "es" else ("COP " + _n(x, lang))


def _precio_int(p):
    return int(p.replace("$", "").replace(".", ""))


def _lista(xs, lang):
    y = " y " if lang == "es" else " and "
    return ", ".join(xs[:-1]) + y + xs[-1] if len(xs) > 1 else "".join(xs)


INC_EN = {"cirujano": "surgeon", "instrumentador": "surgical tech", "quirofano": "operating room with anesthesia", "implantes": "implants",
          "brasier": "post-op bra", "faja": "compression garment", "poliza": "complications insurance", "bomba": "pain pump",
          "masajes": "post-op massages", "preconsulta": "pre-consultation"}

# ---------------------------------------------------------------- TEXTOS (cada idioma escrito en su idioma)
T = {
 "es": {
  "archivo": "vienes-en-diciembre", "otro": "holidays", "locale": "es_CO", "origen": "promo-diaspora-es",
  "msj": "Hola, vivo afuera y quiero adelantar mi preconsulta para la promo de fin de año",
  "titulo": "¿Vienes a Medellín en diciembre?",
  "desc": "Si vives fuera de Colombia: preconsulta por video y valor estimado por escrito antes de viajar, valoración presencial al llegar y tu cirugía en Medellín antes del 15 de enero de 2027.",
  "idioma_link": "English", "idioma_hreflang": "en", "agendar": "Escríbenos",
  "ceja": "Si vives afuera · Promos de fin de año",
  "h1": "¿Vienes a Medellín en diciembre?<br><span>Adelanta todo desde&nbsp;allá.</span>",
  "bajada": "Preconsulta por video y valor estimado por escrito antes de viajar. Al llegar, tu valoración presencial con el Dr. Fernando Ruiz.",
  "boton": "Quiero adelantar mi preconsulta",
  "ya": "Te respondemos en minutos por WhatsApp (hora de Colombia)",
  "doc_rol": "Cirujano plástico reconstructivo · ReTHUS",
  "nombres": {"mamoplastia-de-aumento": "Aumento de senos", "mastopexia-sin-implantes": "Mastopexia sin implantes",
              "mastopexia-con-implantes": "Mastopexia con implantes", "lipo": "Lipo y lipotransferencia"},
  "desde": "Desde", "incluye": "Todo incluido: %s.",
  "precios_ceja": "Precios de fin de año", "precios_h2": "Lo que cuesta,<br><span>antes de viajar.</span>",
  "precios_sub": "Para cirugías hechas antes del 15 de enero de 2027, con todo lo que dice cada una adentro.",
  "nota_pesos": "<b>Pagas en pesos colombianos;</b> tu banco lo convierte con la tasa del día.",
  "otra": "<b>¿Buscas otra cirugía?</b> Te damos un valor estimado por escrito en tu preconsulta.", "otra_link": "Pregúntanos por WhatsApp",
  "como_ceja": "Cómo funciona", "como_h2": "Así funciona,<br><span>de allá a Medellín.</span>",
  "aqui": "Desde allá", "alla": "En Medellín",
  "pasos": [
      ("Escríbenos", "Cuéntanos qué cirugía te interesa y en qué fechas vienes."),
      ("Preconsulta por video", "Con el equipo médico: le mandas tus fotos y resuelves tus dudas."),
      ("Tu valor estimado, por escrito", "Lo tienes antes de comprar el tiquete, y te ayudamos a organizar tus fechas para que todo quede en un solo viaje."),
      ("Valoración presencial con el Dr. Fernando Ruiz", "Cirujano plástico con registro en ReTHUS. Cuesta %s y confirma tu plan antes de la cirugía." % cop(VALORACION, "es")),
      ("Exámenes y fecha", "Te haces los exámenes y separas tu fecha con %s. El saldo, antes de tu cirugía." % cop(LP.ABONO, "es")),
      ("Tu cirugía y tus controles", "En quirófano, nunca en un consultorio. Haces tus controles aquí hasta que tu cirujano te autorice volar; en casa, seguimos por WhatsApp o videollamada."),
  ],
  "viaje_ceja": "Tu viaje", "viaje_h2": "Planea tu viaje<br><span>con tiempo.</span>",
  "recibo_h3": "Tu viaje, en un número",
  "formula": "Tu cirugía (valor por escrito) + tu valoración presencial + los días de recuperación que indique tu cirujano + traslados.",
  "ejemplo": "Ejemplo, si tu cirujano te indica %d días:" % CASA_DIAS,
  "fila_cx": "Aumento de senos", "fila_val": "Valoración presencial",
  "fila_casa": "%d días de casa de recuperación a %s" % (CASA_DIAS, cop(CASA_DIA, "es")),
  "total": "Total, en pesos", "sin": "Sin el vuelo, los traslados, los exámenes ni los medicamentos para la casa.",
  "fuente": "El precio por día es el que publica una casa de recuperación cerca de %s (<a href=\"%s\" target=\"_blank\" rel=\"noopener nofollow\">Recovery House</a>, consultado el 4 de noviembre de 2026). No es un servicio de noon." % (SEDE_QX, CASA_URL),
  "reserva_h3": "Reserva con tiempo",
  "reserva": "Diciembre y comienzos de enero son las semanas de más viajes a Colombia: los tiquetes suelen subir y las sillas se acaban. Las fechas de quirófano antes del 15 de enero también se acaban.",
  "dias": "Te quedas en Medellín los días que indique tu cirujano.", "guia": "Cuántos días quedarse en Colombia después de una cirugía",
  "vuelos_h3": "Vuelos sin escala a Medellín",
  "ciudades": ["Desde varias ciudades de Estados Unidos y de Europa", "Con escala, desde casi cualquier ciudad"],
  "vuelos_nota": "Llegas al aeropuerto internacional de Medellín (MDE), en Rionegro. Revisa horarios vigentes con tu aerolínea.",
  "no_h3": "Lo que no va en el precio:",
  "no": ["Vuelos", "Hospedaje", "Alimentación", "Traslados", "Exámenes antes de la cirugía", "Medicamentos para la casa", "Gastos de tu acompañante",
         "La valoración (%s)" % cop(VALORACION, "es")],
  "doc_ceja": "Quién te opera", "doc_h2": "Dr. Fernando Ruiz,<br><span>cirujano plástico reconstructivo.</span>",
  "razones": [("Cirujano plástico, estético y reconstructivo", "Con registro en ReTHUS, el registro oficial del Ministerio de Salud."),
              ("Siempre en quirófano", "Nunca en un consultorio: en las salas de cirugía habilitadas de %s, en Medellín." % SEDE_QX),
              ("Contigo antes, durante y después", "Te valora en persona, te opera y sigue tus controles.")],
  "rethus": "Cómo verificarlo en ReTHUS",
  "faq_ceja": "Preguntas", "faq_h2": "Lo que preguntan<br><span>las que vienen de afuera.</span>",
  "faq": [
      ("¿Necesito visa?", "Si tienes pasaporte de EE. UU., no necesitas visa de turismo y puedes quedarte hasta 90 días. Si también eres colombiana, entras y sales con tu pasaporte colombiano. Revisa los requisitos vigentes antes de viajar."),
      ("¿El valor estimado puede cambiar?", "Tu cirujano confirma el plan en la valoración presencial. Si ahí se define algo distinto o adicional, te damos la cotización por escrito antes de que decidas."),
      ("¿Cuántos días me quedo en Medellín?", "Los que indique tu cirujano. Como guía, entre una y dos semanas para cirugías de seno y entre dos y tres para lipo; el regreso lo autoriza tu cirujano en el control. Más detalle en la guía <a href=\"%s\">cuántos días quedarse en Colombia después de una cirugía</a>." % GUIA["es"]),
      ("¿Quién me ve cuando vuelva?", "Antes de volar haces tus controles en Medellín. Ya en casa, seguimos contigo por WhatsApp o videollamada. Si necesitas que te vean en persona, vas a un médico de tu ciudad y le avisas a tu cirujano; ante una urgencia, vas a urgencias donde estés."),
      ("¿Puedo viajar sola?", "Para una cirugía necesitas un adulto que te acompañe los primeros días. Sus gastos de viaje no van en el precio."),
      ("¿Puedo pagar desde allá?", "Escríbenos y te contamos los medios de pago. Pagas en pesos colombianos."),
      ("¿Y si mi vuelo cambia?", "Pides el cambio de fecha con anticipación, por WhatsApp. La nueva fecha depende del quirófano y, si tu cirugía es de promo, tiene que ser antes del 15 de enero. Compra tiquetes y hospedaje flexibles: si una cirugía se aplaza, los gastos de viaje no se reembolsan."),
      ("Si abono y cambio de opinión, ¿me devuelven?", "Sí. Si abonas %s y luego decides no operarte, te devolvemos %s. La valoración no se devuelve. Todo está en los <a href=\"/terminos-y-condiciones\">términos y condiciones</a>." % (cop(LP.ABONO, "es"), cop(LP.DEVUELVE, "es"))),
  ],
  "cierre_ceja": "Promos de fin de año", "cierre_h2": "¿Te ayudamos<br><span>a mirar fechas?</span>",
  "cierre_nota": "Precios para cirugías realizadas antes del 15 de enero de 2027. La valoración (%s) no se abona a la cirugía y su valor no se devuelve. <a href=\"/terminos-y-condiciones\">Términos y condiciones</a>" % cop(VALORACION, "es"),
  "pie_nav": [("/", "Conoce noon"), ("/especialistas", "Especialistas"), ("/terminos-y-condiciones", "Términos")],
  "legal": "La información de esta página es orientativa y no reemplaza una consulta médica. Toda cirugía tiene riesgos y los resultados varían de una persona a otra. © noon Clinic",
  "barra_n": "¿Vienes en diciembre?", "barra_p": "Adelanta tu preconsulta", "barra_btn": "Escríbenos",
 },
 "en": {
  "archivo": "holidays", "otro": "vienes-en-diciembre", "locale": "en_US", "origen": "promo-diaspora-en",
  "msj": "Hi, I live abroad and I'd like to start my pre-consultation for the year-end package",
  "titulo": "Coming to Medellín for the holidays?",
  "desc": "Live outside Colombia? A video pre-consultation and a written estimate before you fly, an in-person consultation when you arrive, and surgery in Medellín before January 15, 2027.",
  "idioma_link": "Español", "idioma_hreflang": "es", "agendar": "Message us",
  "ceja": "Living abroad · Year-end packages",
  "h1": "Coming to Medellín for the holidays?<br><span>Get everything ready from&nbsp;home.</span>",
  "bajada": "A video pre-consultation and a written estimate before you fly. Your in-person consultation with Dr. Fernando Ruiz when you arrive.",
  "boton": "Start my pre-consultation",
  "ya": "We reply on WhatsApp within minutes (Colombia time)",
  "doc_rol": "Plastic & reconstructive surgeon · ReTHUS",
  "nombres": {"mamoplastia-de-aumento": "Breast augmentation", "mastopexia-sin-implantes": "Breast lift without implants",
              "mastopexia-con-implantes": "Breast lift with implants", "lipo": "Liposuction with fat transfer"},
  "desde": "From", "incluye": "Includes: %s.",
  "precios_ceja": "Year-end prices", "precios_h2": "What it costs,<br><span>before you fly.</span>",
  "precios_sub": "For surgeries done before January 15, 2027. Everything listed on each one is included.",
  "nota_pesos": "<b>You pay in Colombian pesos (COP);</b> your bank converts at the day's rate.",
  "otra": "<b>Looking for a different surgery?</b> We'll give you a written estimate at your pre-consultation.", "otra_link": "Ask us on WhatsApp",
  "como_ceja": "How it works", "como_h2": "How it works,<br><span>from home to Medellín.</span>",
  "aqui": "From home", "alla": "In Medellín",
  "pasos": [
      ("Message us", "Tell us which surgery you're interested in and when you're coming."),
      ("Video pre-consultation", "With our medical team: you send your photos and ask your questions."),
      ("Your written estimate", "You have it before you buy your ticket, and we help you line up your dates so everything fits into one trip."),
      ("In-person consultation with Dr. Fernando Ruiz", "A plastic surgeon listed in ReTHUS, Colombia's official registry. It costs %s and confirms your plan before surgery." % cop(VALORACION, "en")),
      ("Tests and date", "You do your pre-op tests and book your date with a %s deposit. The balance is due before surgery." % cop(LP.ABONO, "en")),
      ("Your surgery and follow-ups", "In an operating room, never in a doctor's office. Follow-ups happen here until your surgeon clears you to fly; once you're home, we stay in touch by WhatsApp or video call."),
  ],
  "viaje_ceja": "Your trip", "viaje_h2": "Plan your trip<br><span>early.</span>",
  "recibo_h3": "Your trip, in one number",
  "formula": "Your surgery (written price) + your in-person consultation + the recovery days your surgeon recommends + local transport.",
  "ejemplo": "Example, if your surgeon recommends %d days:" % CASA_DIAS,
  "fila_cx": "Breast augmentation", "fila_val": "In-person consultation",
  "fila_casa": "%d days at a recovery house, %s a day" % (CASA_DIAS, cop(CASA_DIA, "en")),
  "total": "Total, in pesos", "sin": "Not counting flights, local transport, pre-op tests or take-home medication.",
  "fuente": "The daily rate is what a recovery house near %s publishes (<a href=\"%s\" target=\"_blank\" rel=\"noopener nofollow\">Recovery House</a>, checked November 4, 2026). It isn't a noon service." % (SEDE_QX, CASA_URL),
  "reserva_h3": "Book early",
  "reserva": "December and early January are the busiest weeks for travel to Colombia: fares tend to climb and seats sell out. Operating room dates before January 15 fill up too.",
  "dias": "You'll stay in Medellín as long as your surgeon recommends.", "guia": "How long to stay in Colombia after plastic surgery",
  "vuelos_h3": "Nonstop flights to Medellín",
  "ciudades": ["From several cities in the US and Europe", "With a connection, from almost anywhere"],
  "vuelos_nota": "You land at Medellín's international airport (MDE), in Rionegro. Check current schedules with your airline.",
  "no_h3": "Not included in the price:",
  "no": ["Flights", "Lodging", "Meals", "Local transport", "Pre-op tests", "Take-home medication", "Your companion's expenses",
         "The consultation (%s)" % cop(VALORACION, "en")],
  "doc_ceja": "Your surgeon", "doc_h2": "Dr. Fernando Ruiz,<br><span>plastic and reconstructive surgeon.</span>",
  "razones": [("Plastic, aesthetic and reconstructive surgeon", "Listed in ReTHUS, the Colombian Ministry of Health's official registry."),
              ("Always in an operating room", "Never in a doctor's office: licensed operating rooms at %s, in Medellín." % SEDE_QX),
              ("With you before, during and after", "He examines you in person, operates and follows your recovery.")],
  "rethus": "How to look him up in ReTHUS",
  "faq_ceja": "Questions", "faq_h2": "What people traveling<br><span>from abroad ask.</span>",
  "faq": [
      ("Do I need a visa?", "With a US passport, you don't need a tourist visa and can stay up to 90 days. If you're also Colombian, you must enter and leave Colombia on your Colombian passport. Please check current requirements before you travel."),
      ("Can the estimate change?", "Your surgeon confirms your plan at the in-person consultation. If something different or additional comes up there, you get the quote in writing before you decide."),
      ("How long will I stay in Medellín?", "As long as your surgeon recommends. As a guide, one to two weeks for breast surgery and two to three for liposuction; your surgeon clears you to fly at a follow-up visit. More in our guide <a href=\"%s\">how long to stay in Colombia after plastic surgery</a>." % GUIA["en"]),
      ("Who follows up with me once I'm home?", "Before you fly, you do your follow-ups in Medellín. Once you're home, we stay in touch by WhatsApp or video call. If you need to be seen in person, see a local doctor and let your surgeon know; for an emergency, go to the nearest ER."),
      ("Can I travel alone?", "For surgery, you'll need an adult with you during the first days. Their travel costs aren't included in the price."),
      ("Can I pay from abroad?", "Message us and we'll walk you through the payment options. You pay in Colombian pesos."),
      ("What if my flight changes?", "Ask to change your date in advance, on WhatsApp. The new date depends on operating room availability and, for a year-end package, it has to be before January 15. Buy flexible flights and lodging: if surgery is postponed, travel costs aren't refunded."),
      ("What if I pay the deposit and change my mind?", "If you pay the %s deposit and then decide not to have surgery, we refund %s. The consultation fee isn't refundable. Full details are in our <a href=\"/terminos-y-condiciones\" hreflang=\"es\">terms and conditions</a> (in Spanish)." % (cop(LP.ABONO, "en"), cop(LP.DEVUELVE, "en"))),
  ],
  "cierre_ceja": "Year-end packages", "cierre_h2": "Want help<br><span>picking your dates?</span>",
  "cierre_nota": "Prices for surgeries performed before January 15, 2027. The consultation fee (%s) isn't credited toward surgery and isn't refundable. <a href=\"/terminos-y-condiciones\" hreflang=\"es\">Terms and conditions</a> (in Spanish)" % cop(VALORACION, "en"),
  "pie_nav": [("/about-noon-clinic", "About noon"), ("/why-noon-clinic", "Why noon"), ("/terminos-y-condiciones", "Terms (Spanish)")],
  "legal": "The information on this page is for guidance only and does not replace a medical consultation. Every surgery carries risks and results vary from person to person. © noon Clinic",
  "barra_n": "Coming for the holidays?", "barra_p": "Start your pre-consultation", "barra_btn": "Message us",
 },
}

# ---------------------------------------------------------------- estilos propios (sobre promos.css)
CSS = """<style>
/* ¿Vienes en diciembre? (landing_afuera.py) · sobre promos.css, prefijo af- */
.af-der{display:flex;align-items:center;gap:4px}
.af-idioma{min-height:44px;display:inline-flex;align-items:center;padding:0 12px;border-radius:999px;font:500 14px/1 var(--display);color:var(--tenue);text-decoration:none;transition:color .3s}
.af-idioma:hover{color:var(--tinta)}
.pr-afuera .pr-portada h1{font-size:clamp(40px,4.9vw,66px)}
.pr-afuera .pr-portada .pr-inc{margin-top:22px;max-width:500px;font-size:17px;text-wrap:pretty}
.pr-afuera .pr-ya,.pr-afuera .pr-sub,.af-paso p,.af-bloque p{text-wrap:pretty}
.pr-afuera .pr-ya{text-wrap:balance}
.pr-afuera .pr-portada .pr-arco>img{object-position:center 30%}
.af-precios{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.af-precio{display:flex;flex-direction:column;padding:26px 26px 24px;border-radius:24px;background:#fff}
.af-precio h3{font-size:clamp(19px,1.7vw,22px);line-height:1.2;letter-spacing:-.015em;margin-bottom:14px}
.af-cop{display:flex;align-items:baseline;gap:8px;margin:0 0 14px}
.af-cop small{font:500 14px var(--display);color:var(--tenue)}
.af-cop b{font:600 clamp(28px,2.8vw,36px)/1 var(--display);letter-spacing:-.03em}
.af-precio .af-inc{margin:auto 0 0;font-size:15px;color:var(--tenue)}
.af-nota{display:flex;align-items:center;gap:10px;margin:18px 4px 0;font-size:15px;color:var(--tenue)}
.af-nota i{flex:none;width:8px;height:8px;border-radius:50%;background:var(--champan)}
.af-nota b{color:var(--tinta);font-weight:600}
.af-otra{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 22px;margin-top:20px;padding:18px 24px;border-radius:22px;background:#fff}
.af-otra p{margin:0;font-size:16px}
.af-pasos{list-style:none;margin:0 auto;padding:0;max-width:var(--max);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.af-paso{position:relative;padding:26px 24px 26px;border-radius:26px;background:var(--gris)}
.af-paso:nth-child(n+4){background:var(--marfil)}
.af-paso .pr-pn{width:46px;height:46px;margin:0 0 18px;background:#fff;box-shadow:none;font-size:18px}
.af-paso:last-child .pr-pn{background:var(--tinta);color:#fff}
.af-donde{position:absolute;top:36px;right:22px;padding:6px 11px;border-radius:999px;background:#fff;font:500 12.5px/1 var(--display);color:#7a6a55}
.af-paso h3{font-size:19px;line-height:1.25;letter-spacing:-.015em;margin-bottom:6px}
.af-paso p{margin:0;color:var(--tenue);font-size:15.5px}
.af-viaje{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:12px;max-width:var(--max);margin:0 auto}
.af-recibo{padding:clamp(26px,3.4vw,42px);border-radius:32px;background:var(--marfil)}
.af-recibo h3,.af-bloque h3{font-size:clamp(21px,2vw,24px);line-height:1.2;letter-spacing:-.02em;margin-bottom:10px}
.af-formula{margin:0 0 18px;color:var(--tenue);font-size:16px}
.af-ej{margin:0 0 4px;font:500 15px/1.3 var(--display)}
.af-filas{list-style:none;margin:0;padding:0}
.af-filas li{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:14px 0;border-bottom:1px solid #e3d8c8;font-size:16px}
.af-filas li b{font:600 17px/1.2 var(--display);white-space:nowrap}
.af-total{display:flex;justify-content:space-between;align-items:baseline;gap:6px 16px;padding:18px 0 0}
.af-total span{font:500 16px var(--display)}
.af-total b{font:600 clamp(30px,3.2vw,38px)/1 var(--display);letter-spacing:-.03em;white-space:nowrap}
.af-sin{margin:16px 0 0;font-size:15px;color:var(--tenue)}
.af-fuente{margin:14px 0 0;padding-top:14px;border-top:1px dashed #dccfbd;font-size:13.5px;color:var(--tenue)}
.af-fuente a,.af-bloque a,.pr-preg a,.pr-nota a{color:var(--tinta);text-decoration-color:var(--champan);text-underline-offset:3px}
.af-lado{display:grid;gap:12px}
.af-bloque{padding:clamp(24px,3vw,34px);border-radius:32px;background:var(--gris)}
.af-bloque p{margin:0 0 12px;color:var(--tenue);font-size:16px}
.af-bloque p:last-child{margin-bottom:0}
.af-ciudades{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:14px 0;padding:0}
.af-ciudades li{min-height:40px;display:inline-flex;align-items:center;padding:0 16px;border-radius:999px;background:#fff;font:500 15px/1.1 var(--display)}
.af-no{max-width:var(--max);margin:12px auto 0;padding:22px 28px;border-radius:28px;background:var(--marfil);display:flex;flex-wrap:wrap;align-items:center;gap:12px 26px}
.af-no h3{font-size:18px;letter-spacing:-.01em}
.af-no ul{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;flex:1}
.af-no li{padding:8px 14px;border-radius:999px;background:#fff;font:500 14.5px/1.2 var(--display);color:var(--tenue)}
.pr-medico .af-link{margin:0 0 26px}
@media (max-width:960px){.af-pasos{grid-template-columns:repeat(2,minmax(0,1fr))}.af-viaje{grid-template-columns:1fr}}
@media (max-width:760px){
 .af-idioma{padding:0 8px;font-size:13.5px}
 .pr-afuera .pr-portada h1{font-size:clamp(30px,8.6vw,36px)}
 .pr-afuera .pr-portada .pr-inc{margin-top:14px;font-size:16px}
 .af-precios{grid-template-columns:1fr;gap:8px}
 .af-precio{padding:22px 20px}
 .af-nota{align-items:flex-start}.af-nota i{margin-top:7px}
 .af-otra{padding:16px 18px}
 .af-otra .pr-link{min-height:44px}
 .af-pasos{grid-template-columns:1fr;gap:8px}
 .af-paso{display:grid;grid-template-columns:46px minmax(0,1fr);column-gap:16px;padding:20px 18px}
 .af-paso .pr-pn{grid-row:1/4;margin:0}
 .af-donde{position:static;justify-self:start;margin:0 0 8px}
 .af-recibo,.af-bloque{border-radius:28px;padding:26px 20px}
 .af-filas li{font-size:15px}
 .af-no{padding:20px;border-radius:24px}
 .pr-afuera .pr-ya{display:block;text-align:center}
 .pr-afuera .pr-ya i{display:inline-block;margin:0 8px 1px 0;vertical-align:middle}
 .pr-afuera .pr-cierre-in{padding-left:12px;padding-right:12px}
 .pr-afuera .pr-cierre .pr-btn{gap:8px;padding:18px 18px;font-size:16px;white-space:nowrap}
}
</style>"""


def _medicion(b, origen):
    """El encabezado de medición de toda la web, con el origen dentro del MISMO evento clic_whatsapp (sin duplicarlo)."""
    clave = 'event:"clic_whatsapp",'
    assert clave in b.HEAD_MEDICION, "Cambió HEAD_MEDICION en build.py: revisa cómo se agrega el origen aquí"
    return b.HEAD_MEDICION.replace(clave, clave + 'origen:"%s",' % origen, 1)


def _script(origen):
    """Cabecera, aparición suave, barra fija del celular y marcas de Clarity (lo mismo que promos.js, sin el selector de cirugías)."""
    return """<script>(function () {
  var quieto = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var captura = /[?&]captura/.test(location.search);
  if (captura) document.documentElement.classList.add("captura");
  function marcar(n, v) { if (!window.clarity) return; if (v === undefined) window.clarity("event", n); else window.clarity("set", n, v); }
  var cab = document.querySelector(".pr-cab"), barra = document.querySelector(".pr-barra"), portada = document.querySelector(".pr-portada"), cierre = document.querySelector(".pr-cierre"), cierreVisible = false;
  function alBajar() {
    var y = window.scrollY || window.pageYOffset, on = y > portada.offsetHeight * 0.8 && !cierreVisible;
    cab.classList.toggle("solida", y > 10); barra.classList.toggle("on", on); barra.setAttribute("aria-hidden", on ? "false" : "true");
  }
  if ("IntersectionObserver" in window && cierre) new IntersectionObserver(function (e) { cierreVisible = e[0].isIntersecting; alBajar(); }, { threshold: 0.1 }).observe(cierre);
  window.addEventListener("scroll", alBajar, { passive: true }); alBajar();
  var revs = Array.prototype.slice.call(document.querySelectorAll(".pr-rev"));
  if ("IntersectionObserver" in window && !quieto && !captura) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -6%% 0px", threshold: 0.06 });
    revs.forEach(function (el) { io.observe(el); });
  } else revs.forEach(function (el) { el.classList.add("on"); });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[data-wa]");
    if (a) { var s = a.closest("section,header,footer,.pr-barra"); marcar("origen", "%s"); marcar("boton_whatsapp", s ? (s.id || String(s.className).split(" ")[0]) : ""); marcar("clic_whatsapp"); }
  });
})();</script>""" % origen


def _pagina(b, lang):
    t = T[lang]
    wa = "https://wa.me/" + b.WHATSAPP + "?text=" + quote(t["msj"])
    flecha = LP.ico("flecha", "ico-f")
    doc = [e for e in b.ESPECIALISTAS if e["area"] == "cirugia"][0]
    doc_jpg = "/assets/equipo/" + doc["foto"]
    doc_web = doc_jpg.rsplit(".", 1)[0] + ".webp" if os.path.exists(os.path.join(b.AQUI, doc_jpg.lstrip("/").rsplit(".", 1)[0] + ".webp")) else doc_jpg
    foto, og = "/assets/clinica/vista.webp", "/assets/clinica/vista.jpg"  # Medellín desde lo alto, con las montañas

    def boton(texto, clase="pr-btn"):
        return '<a class="%s" href="%s" target="_blank" rel="noopener" data-wa>%s %s</a>' % (clase, wa, texto, flecha)

    # las 4 promos con precio (mismos precios y lo que incluyen de landing_promos.PROMOS), solo en pesos
    tarjetas = ""
    for s in ORDEN:
        p = LP.PROMOS[s]
        claves = [k for k in p["incluye"] if k != "instrumentador"]  # como en la portada de las promos: corto
        inc = _lista([LP.INC_CORTO[k] if lang == "es" else INC_EN[k] for k in claves], lang)
        tarjetas += ('<li class="af-precio pr-rev"><h3>%s</h3><p class="af-cop">%s<b>%s</b></p><p class="af-inc">%s</p></li>' % (
            escape(t["nombres"][s]), ("<small>%s</small>" % t["desde"]) if p["desde"] else "", cop(_precio_int(p["precio"]), lang),
            escape(t["incluye"] % inc)))
    pasos = ""
    for i, (h, d) in enumerate(t["pasos"], 1):
        donde = ('<span class="af-donde">%s</span>' % (t["aqui"] if i == 1 else t["alla"])) if i in (1, 4) else ""
        pasos += '<li class="af-paso pr-rev"><span class="pr-pn">%d</span>%s<h3>%s</h3><p>%s</p></li>' % (i, donde, escape(h), escape(d))
    cx = _precio_int(LP.PROMOS[EJEMPLO]["precio"])
    total = cx + VALORACION + CASA_DIA * CASA_DIAS
    ciudades = "".join("<li>%s</li>" % escape(c) for c in t["ciudades"])
    no = "".join("<li>%s</li>" % escape(x) for x in t["no"])
    razones = "".join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (LP.ico(i), escape(h), escape(d)) for i, (h, d) in zip(["medico", "cruz", "reloj"], t["razones"]))
    faq = "".join('<details class="pr-preg pr-rev"><summary>%s<span class="pr-mas" aria-hidden="true"></span></summary><p>%s</p></details>' % (escape(p), r) for p, r in t["faq"])
    pie = "".join('<a href="%s"%s>%s</a>' % (h, ' hreflang="es"' if (lang == "en" and h == "/terminos-y-condiciones") else "", escape(n)) for h, n in t["pie_nav"])
    clarity = ('<script>addEventListener("load",function(){setTimeout(function(){(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;'
               't.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");'
               'clarity("set","idioma","%s");clarity("set","pagina",%s);clarity("set","tipo","landing");},1200)});</script>') % (b.CLARITY_ID, lang, json.dumps(t["origen"]))

    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
%(medicion)s
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(titulo)s · noon Clinic</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:site_name" content="noon Clinic">
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(dominio)s%(og)s">
<meta property="og:locale" content="%(locale)s">
%(clarity)s
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/assets/favicon.png">
<script>document.documentElement.className="js"</script>
%(fuentes)s
<link rel="preload" as="image" href="%(foto)s" fetchpriority="high">
<link rel="stylesheet" href="/assets/promos.css?v=%(v)s">
%(css)s
</head>
<body class="pr pr-afuera" data-origen="%(origen)s">
<header class="pr-cab">
  <a class="pr-logo" href="/" aria-label="noon Clinic"><img src="/assets/logo-noon-s.webp" alt="noon Clinic" width="360" height="118"></a>
  <div class="af-der"><a class="af-idioma" href="/promos/%(otro)s" hreflang="%(idioma_hreflang)s" lang="%(idioma_hreflang)s">%(idioma_link)s</a><a class="pr-btn-borde" href="%(wa)s" target="_blank" rel="noopener" data-wa>%(agendar)s</a></div>
</header>
<main>

<!-- 1 · PORTADA -->
<section class="pr-portada">
  <div class="pr-portada-in">
    <div class="pr-portada-txt">
      <p class="pr-ceja"><i></i>%(ceja)s</p>
      <h1>%(h1)s</h1>
      <p class="pr-inc">%(bajada)s</p>
      %(cuenta)s
      %(boton_xl)s
      <p class="pr-ya"><i></i>%(ya)s</p>
    </div>
    <figure class="pr-arco">
      <img src="%(foto)s" alt="" width="900" height="1200" fetchpriority="high">
      <div class="pr-doc"><img src="%(doc_web)s" alt="" width="1120" height="1400"><div>%(doc)s<span>%(doc_rol)s</span></div></div>
    </figure>
  </div>
</section>

<!-- 2 · LAS 4 PROMOS CON PRECIO (en pesos colombianos) -->
<section class="pr-sec" id="precios">
  <div class="pr-panel pr-marfil">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>%(precios_ceja)s</p><h2>%(precios_h2)s</h2><p class="pr-sub" style="margin-left:0">%(precios_sub)s</p></header>
    <ul class="af-precios">%(tarjetas)s</ul>
    <p class="af-nota"><i aria-hidden="true"></i><span>%(nota_pesos)s</span></p>
    <div class="af-otra pr-rev"><p>%(otra)s</p><a class="pr-link" href="%(wa)s" target="_blank" rel="noopener" data-wa>%(otra_link)s %(flecha)s</a></div>
  </div>
</section>

<!-- 3 · ASÍ FUNCIONA: DESDE ALLÁ (preconsulta y valor estimado) Y EN MEDELLÍN (valoración presencial y cirugía) -->
<section class="pr-sec" id="como">
  <header class="pr-cabeza pr-centro pr-rev"><p class="pr-ceja"><i></i>%(como_ceja)s</p><h2>%(como_h2)s</h2></header>
  <ol class="af-pasos">%(pasos)s</ol>
</section>

<!-- 4 · TU VIAJE: EN UN NÚMERO, CON TIEMPO Y VUELOS -->
<section class="pr-sec" id="viaje">
  <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>%(viaje_ceja)s</p><h2>%(viaje_h2)s</h2></header>
  <div class="af-viaje">
    <div class="af-recibo pr-rev">
      <h3>%(recibo_h3)s</h3>
      <p class="af-formula">%(formula)s</p>
      <p class="af-ej">%(ejemplo)s</p>
      <ul class="af-filas"><li><span>%(fila_cx)s</span><b>%(cop_cx)s</b></li><li><span>%(fila_val)s</span><b>%(cop_val)s</b></li><li><span>%(fila_casa)s</span><b>%(cop_casa)s</b></li></ul>
      <div class="af-total"><span>%(total_txt)s</span><b>%(cop_total)s</b></div>
      <p class="af-sin">%(sin)s</p>
      <p class="af-fuente">%(fuente)s</p>
    </div>
    <div class="af-lado">
      <div class="af-bloque pr-rev">
        <h3>%(reserva_h3)s</h3>
        <p>%(reserva)s</p>
        <p>%(dias)s <a href="%(guia_url)s">%(guia)s</a></p>
      </div>
      <div class="af-bloque pr-rev">
        <h3>%(vuelos_h3)s</h3>
        <ul class="af-ciudades">%(ciudades)s</ul>
        <p>%(vuelos_nota)s</p>
      </div>
    </div>
  </div>
  <div class="af-no pr-rev"><h3>%(no_h3)s</h3><ul>%(no)s</ul></div>
</section>

<!-- 5 · TU CIRUJANO -->
<section class="pr-sec" id="cirujano">
  <div class="pr-panel pr-gris pr-medico">
    <figure class="pr-arco pr-arco-doc pr-rev"><img src="%(doc_web)s" alt="%(doc)s" width="1120" height="1400" loading="lazy"></figure>
    <div class="pr-rev">
      <p class="pr-ceja"><i></i>%(doc_ceja)s</p>
      <h2>%(doc_h2)s</h2>
      <ul class="pr-razones">%(razones)s</ul>
      <p class="af-link"><a class="pr-link" href="%(rethus_url)s" target="_blank" rel="noopener">%(ico_lupa)s %(rethus)s</a></p>
      %(boton)s
    </div>
  </div>
</section>

<!-- 6 · PREGUNTAS -->
<section class="pr-sec" id="preguntas">
  <div class="pr-faq-in">
    <header class="pr-cabeza pr-rev"><p class="pr-ceja"><i></i>%(faq_ceja)s</p><h2>%(faq_h2)s</h2></header>
    <div class="pr-faq">%(faq)s</div>
  </div>
</section>

<!-- 7 · CIERRE -->
<section class="pr-sec pr-cierre" id="agendar">
  <div class="pr-panel pr-marfil pr-cierre-in pr-rev">
    <p class="pr-ceja"><i></i>%(cierre_ceja)s</p>
    <h2>%(cierre_h2)s</h2>
    %(cuenta)s
    %(boton_xl)s
    <p class="pr-nota">%(cierre_nota)s</p>
  </div>
</section>

</main>
<footer class="pr-pie">
  <a class="pr-logo" href="/"><img src="/assets/logo-noon-s.webp" alt="noon Clinic" width="360" height="118" loading="lazy"></a>
  <nav>%(pie)s<a href="/promos/%(otro)s" hreflang="%(idioma_hreflang)s" lang="%(idioma_hreflang)s">%(idioma_link)s</a><a href="%(wa)s" target="_blank" rel="noopener" data-wa>WhatsApp %(tel)s</a></nav>
  <p class="pr-legal">%(legal)s</p>
</footer>
<div class="pr-barra" aria-hidden="true">
  <div class="pr-barra-txt"><b>%(barra_n)s</b><span>%(barra_p)s</span></div>
  <a class="pr-btn" href="%(wa)s" target="_blank" rel="noopener" data-wa>%(barra_btn)s</a>
</div>
%(script_cuenta)s
%(script)s
<script src="/assets/medicion-ads.js?v=%(v)s" defer></script>
</body>
</html>
""" % dict(t, lang=lang, medicion=_medicion(b, t["origen"]), titulo=escape(t["titulo"]), desc=escape(t["desc"]), dominio=b.DOMINIO, og=og,
           clarity=clarity, fuentes=b.FUENTES.replace("assets/fuentes/", "/assets/fuentes/"), foto=foto, v=b.V,
           css=cuenta_regresiva.CSS + CSS, wa=wa, flecha=flecha, cuenta=cuenta_regresiva.bloque("", lang),
           boton_xl=boton(t["boton"], "pr-btn pr-btn-xl"), boton=boton(t["boton"]), doc=escape(doc["nombre"]), doc_web=doc_web,
           tarjetas=tarjetas, pasos=pasos, cop_cx=cop(cx, lang), cop_val=cop(VALORACION, lang), cop_casa=cop(CASA_DIA * CASA_DIAS, lang),
           cop_total=cop(total, lang), total_txt=t["total"], guia_url=GUIA[lang], ciudades=ciudades, no=no, razones=razones,
           rethus_url=LP.RETHUS, ico_lupa=LP.ico("lupa"), faq=faq, pie=pie, tel=TEL, script_cuenta=cuenta_regresiva.script(),
           script=_script(t["origen"]))


def generar(b, carpeta):
    """Escribe promos/vienes-en-diciembre.html y promos/holidays.html. Devuelve cuántas páginas hizo."""
    for lang in ("es", "en"):
        with open(os.path.join(carpeta, T[lang]["archivo"] + ".html"), "w", encoding="utf-8") as f:
            f.write(_pagina(b, lang))
    return 2
