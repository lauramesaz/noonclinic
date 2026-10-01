# -*- coding: utf-8 -*-
# noon Clinic · página INTERNA "Capacitación comercial" (con código de acceso, no indexada, sin enlace desde la web).
# Se genera sola al correr build.py. Toma los procedimientos de datos_noon.py.
import os, json, hashlib
from datos_noon import CIRUGIAS_NOON, TRATAMIENTOS, CATEGORIAS_CX, CATEGORIAS_ME

AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGO = "0000"  # código de acceso para el equipo comercial

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


SEDAS = ["seda-clara", "seda-burdeos", "seda-cafe", "seda-champan", "seda-noche", "seda-horizonte"]


def _imagen(slug, i):
    # foto propia del procedimiento si existe (assets/capacitacion/<slug>.jpg); si no, una seda de la marca
    if os.path.exists(os.path.join(AQUI, "assets", "capacitacion", slug + ".jpg")):
        return "assets/capacitacion/%s.jpg" % slug
    return "assets/noon/%s.jpg" % SEDAS[i % len(SEDAS)]


def _proc(x, tipo, cats):
    doc = DOCTORES[0]["nombre"] if tipo == "cx" else DOCTORES[1]["nombre"]
    etiquetas = ("Duración", "Anestesia", "Incapacidad", "Resultado final") if tipo == "cx" else ("Sesiones", "Duración", "Recuperación", "Resultado")
    return {"slug": x["slug"], "tipo": tipo, "img": "", "cat": cats[x["cat"]], "nombre": x["nombre"], "corto": x["corto"],
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
    for i, p in enumerate(procs):
        p["img"] = _imagen(p["slug"], i)
    datos = {"procs": procs, "cats_cx": [n for k, n, d, f in CATEGORIAS_CX], "cats_me": [n for k, n, d, f in CATEGORIAS_ME],
             "doctores": DOCTORES, "disp": DISPONIBILIDAD, "objeciones": OBJECIONES, "reglas": REGLAS, "pasos": PASOS,
             "precio": PRECIO}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.replace("%%DATOS%%", js).replace("%%HASH%%", hashlib.sha256(CODIGO.encode()).hexdigest())
    with open(os.path.join(AQUI, "capacitacion-comercial.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(procs)


with open(os.path.join(AQUI, "_capacitacion_plantilla.html"), encoding="utf-8") as _f:
    PLANTILLA = _f.read()

if __name__ == "__main__":
    print("Capacitación comercial: %d procedimientos." % generar())
