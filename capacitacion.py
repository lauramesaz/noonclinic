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

# ---------------------------------------------------------------- PRECIOS (solo los que conocemos; el resto se define en la valoración)
CX_INCLUYE = ["Fajas", "Bomba del dolor", "Quirófano", "Instrumentador", "Póliza"]
PRECIOS = {
    "mastopexia": {"items": [("Mastopexia con implantes", "Desde $17.900.000"), ("Mastopexia sin implantes", "Desde $15.900.000")],
                   "incluye": CX_INCLUYE + ["Implantes (en la mastopexia con implantes)"],
                   "msj": "La mastopexia sin implantes está desde $15.900.000 y con implantes desde $17.900.000. Incluye fajas, bomba del dolor, quirófano, instrumentador y póliza. ¿Te agendo tu valoración con el Dr. Fernando para confirmar tu plan?"},
    "lipotransferencia-glutea": {"items": [("Lipotransferencia", "Desde $18.900.000")],
                   "incluye": CX_INCLUYE + ["Implantes (si los necesita)"],
                   "msj": "La lipotransferencia está desde $18.900.000 e incluye fajas, bomba del dolor, quirófano, instrumentador y póliza. ¿Te agendo tu valoración con el Dr. Fernando para confirmar tu plan?"},
    "mamoplastia-de-aumento": {"items": [("Mamoplastia de aumento (paquete)", "$10.900.000")],
                   "incluye": ["Honorarios del cirujano", "Instrumentador", "Quirófano", "Implantes", "Brasier posquirúrgico", "Póliza", "Bomba del dolor", "Preconsulta"],
                   "msj": "La mamoplastia de aumento tiene un valor de $10.900.000 e incluye cirujano, quirófano, implantes, brasier, póliza y bomba del dolor. ¿Te agendo tu valoración con el Dr. Fernando esta semana?"},
    "bioestimuladores": {"items": [("Sculptra", "$1.830.000"), ("Radiesse", "$1.830.000")],
                   "msj": "Sculptra y Radiesse tienen un valor de $1.830.000 cada uno. ¿Te agendo con la Dra. Valeria para saber cuál es ideal para ti?"},
    "acido-hialuronico": {"items": [("Ácido hialurónico en labios", "$990.000")],
                   "msj": "El ácido hialurónico en labios tiene un valor de $990.000. Para otras zonas, el valor se define en tu valoración. ¿Te agendo con la Dra. Valeria esta semana?"},
    "toxina-botulinica": {"items": [("Toxina botulínica", "$999.000")],
                   "msj": "La toxina botulínica tiene un valor de $999.000. ¿Te agendo con la Dra. Valeria esta semana?"},
    "skinboosters": {"items": [("Mesoterapia facial NCTF", "$810.000"), ("Mesoterapia de ojeras NCTF", "$540.000")],
                   "msj": "La mesoterapia facial NCTF tiene un valor de $810.000 y la de ojeras $540.000. ¿Te agendo con la Dra. Valeria para ver cuál necesitas?"},
    "microagujas": {"items": [("Nanopore", "$490.000"), ("Nanopore con ADN de salmón", "$702.000")],
                   "msj": "El Nanopore tiene un valor de $490.000, y con ADN de salmón $702.000. ¿Te agendo con la Dra. Valeria esta semana?"},
    "peelings": {"items": [("Peeling Salipeel (poros abiertos)", "$430.000")],
                   "msj": "El peeling Salipeel para poros abiertos tiene un valor de $430.000. Otros peelings se definen en tu valoración. ¿Te agendo con la Dra. Valeria?"},
}
# Precios sin ficha propia en el catálogo (aparecen en la lista de precios)
OTROS_PRECIOS = [("Terapia capilar", "$540.000", "Medicina estética")]

PRECIO = "El valor se define en tu cita de valoración con {doc}, porque cada plan es personal. ¿Te agendo esta semana?"

CIERRES = ["¿Te agendo tu valoración?", "¿Te queda mejor esta semana o la próxima?", "¿Quieres que te reserve un espacio con {doc}?", "¿Qué día te queda fácil venir?"]


def _q(texto, i, doc):
    # toda respuesta termina en una pregunta que lleva a la valoración
    texto = texto.strip()
    return texto if texto.endswith("?") else texto + " " + CIERRES[i % len(CIERRES)].format(doc=doc)


def _precio_msj(slug, doc):
    return PRECIOS[slug]["msj"] if slug in PRECIOS else PRECIO.format(doc=doc)


def _faq_cx(c, doc):
    d = c["datos"]
    pares = ([(p, r) for p, r in c["faq"]]
             + [("¿Cuánto dura la cirugía?", "Más o menos %s." % d[0].lower()),
                ("¿Qué anestesia usan?", "%s. El cirujano lo confirma según tu caso." % d[1]),
                ("¿Cuántos días de incapacidad?", "Como guía, %s." % d[2].lower()),
                ("¿Cuándo veo el resultado final?", "Hacia %s." % d[3].lower()),
                ("¿Dónde me operan?", "En salas de cirugía habilitadas, nunca en un consultorio."),
                ("¿Necesito acompañante?", "Sí, un adulto el día de la cirugía y la primera noche.")])
    return [("¿Cuánto cuesta?", _precio_msj(c["slug"], doc))] + [(p, _q(r, i, doc)) for i, (p, r) in enumerate(pares)]


def _faq_me(t, doc):
    d = t["datos"]
    pares = ([(p, r) for p, r in t["faq"]]
             + [("¿Cuántas sesiones necesito?", "Como guía, %s." % d[0].lower()),
                ("¿Cuánto dura la sesión?", "Más o menos %s." % d[1].lower()),
                ("¿Puedo seguir con mi rutina?", "Recuperación: %s." % d[2].lower()),
                ("¿Cuándo se ve el resultado?", "%s." % d[3]),
                ("¿Lo puedo combinar con otro tratamiento?", "Sí, muchas veces combinar da mejores resultados.")])
    return [("¿Cuánto cuesta?", _precio_msj(t["slug"], doc))] + [(p, _q(r, i, doc)) for i, (p, r) in enumerate(pares)]


SEDAS = ["seda-clara", "seda-burdeos", "seda-cafe", "seda-champan", "seda-noche", "seda-horizonte"]


def _imagen(slug, i):
    # foto propia del procedimiento si existe (assets/capacitacion/<slug>.jpg); si no, una seda de la marca
    if os.path.exists(os.path.join(AQUI, "assets", "capacitacion", slug + ".jpg")):
        return "assets/capacitacion/%s.jpg" % slug
    return "assets/noon/%s.jpg" % SEDAS[i % len(SEDAS)]


def _proc(x, tipo, cats):
    doc = DOCTORES[0]["nombre"] if tipo == "cx" else DOCTORES[1]["nombre"]
    con = "el Dr. Fernando" if tipo == "cx" else "la Dra. Valeria"  # como se dice en un mensaje
    etiquetas = ("Duración", "Anestesia", "Incapacidad", "Resultado final") if tipo == "cx" else ("Sesiones", "Duración", "Recuperación", "Resultado")
    return {"slug": x["slug"], "tipo": tipo, "img": "", "cat": cats[x["cat"]], "nombre": x["nombre"], "corto": x["corto"],
            "que_es": x["que_es"], "datos": list(zip(etiquetas, x["datos"])), "ideal": x["ideal"],
            "recuperacion": x.get("recuperacion", []), "doc": doc,
            "faq": _faq_cx(x, con) if tipo == "cx" else _faq_me(x, con),
            "precios": PRECIOS.get(x["slug"], {}).get("items", []), "incluye": PRECIOS.get(x["slug"], {}).get("incluye", []),
            "precio_msj": _precio_msj(x["slug"], con),
            "cierre": "En tu valoración con %s sales con tu plan y tu valor exacto. ¿Te queda mejor el ___ o el ___?" % con}


OBJECIONES = [
    ("“Dame un precio aproximado”", "Cada caso es distinto y no quiero darte un número que después cambie. En tu valoración sales con tu valor exacto. ¿Te agendo esta semana?"),
    ("“¿Por qué cobran la valoración?”", "Porque es una consulta médica real: el especialista te examina y te entrega tu plan por escrito. ¿Te reservo un espacio?"),
    ("“En otro lugar me dieron precio por WhatsApp”", "Sin examinarte nadie sabe si eres candidata ni qué incluye. Aquí decides con información completa y segura. ¿Agendamos tu valoración?"),
    ("“Lo voy a pensar”", "¡Claro! La valoración es justo para decidir con toda la información, y no te compromete. ¿Te separo un espacio?"),
    ("“Vivo en otra ciudad”", "Te organizamos las fechas para que todo quede en un mismo viaje. ¿En qué fechas podrías venir?"),
    ("“¿Me puedo operar ya?”", "Primero va tu valoración y tus exámenes; desde ahí te damos la fecha más cercana. ¿Te agendo la valoración esta semana?"),
]

REGLAS = [
    ("Vende la valoración", "Tu meta es que el paciente agende su cita de valoración."),
    ("Precio solo si lo tenemos", "Si el procedimiento tiene precio, dalo. Si no, el valor se define en la valoración."),
    ("Mensajes cortos", "Dos o tres líneas máximo. Nada de párrafos largos."),
    ("Termina siempre en pregunta", "Ejemplo: “¿Te queda mejor el martes o el jueves?”."),
]

PASOS = [
    ("Saluda", "Pregunta su nombre y qué le gustaría mejorar."),
    ("Explica corto", "En dos líneas, qué es el procedimiento."),
    ("Responde", "Usa las respuestas de cada procedimiento."),
    ("Agenda", "Ofrece dos fechas de la pestaña Disponibilidad."),
]


def generar():
    procs = ([_proc(c, "cx", {k: n for k, n, d, f in CATEGORIAS_CX}) for c in CIRUGIAS_NOON]
             + [_proc(t, "me", {k: n for k, n, d, f in CATEGORIAS_ME}) for t in TRATAMIENTOS])
    for i, p in enumerate(procs):
        p["img"] = _imagen(p["slug"], i)
    datos = {"procs": procs, "cats_cx": [n for k, n, d, f in CATEGORIAS_CX], "cats_me": [n for k, n, d, f in CATEGORIAS_ME],
             "doctores": DOCTORES, "disp": DISPONIBILIDAD, "objeciones": OBJECIONES, "reglas": REGLAS, "pasos": PASOS,
             "precio": PRECIO, "lista_precios": [(p["nombre"], it, v, p["slug"], p["tipo"]) for p in procs for it, v in p["precios"]],
             "otros_precios": OTROS_PRECIOS}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.replace("%%DATOS%%", js).replace("%%HASH%%", hashlib.sha256(CODIGO.encode()).hexdigest())
    with open(os.path.join(AQUI, "capacitacion-comercial.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(procs)


with open(os.path.join(AQUI, "_capacitacion_plantilla.html"), encoding="utf-8") as _f:
    PLANTILLA = _f.read()

if __name__ == "__main__":
    print("Capacitación comercial: %d procedimientos." % generar())
