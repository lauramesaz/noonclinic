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

# Video central del inicio (Google Drive compartido con enlace; el archivo pesa 1 GB, por eso no va en la web)
VIDEO = {"titulo": "Estructura para un chat de ventas", "duracion": "34 min", "drive": "1QN8iaPSyiQWAjHC6tb_EdtH2HhW8rU16",
         "portada": "assets/capacitacion/video-portada.jpg"}

# ---------------------------------------------------------------- PRECIOS (solo los que conocemos; el resto se define en la valoración)
CX_INCLUYE = ["Fajas", "Bomba del dolor", "Quirófano", "Instrumentador", "Póliza"]
PRECIOS = {
    "mastopexia-con-implantes": {"items": [("Mastopexia con implantes", "Desde $17.900.000")],
                   "incluye": CX_INCLUYE + ["Implantes"],
                   "msj": "La mastopexia con implantes está desde $17.900.000 e incluye implantes, fajas, bomba del dolor, quirófano, instrumentador y póliza. ¿Te agendo tu valoración con el Dr. Fernando?"},
    "mastopexia-sin-implantes": {"items": [("Mastopexia sin implantes", "Desde $15.900.000")],
                   "incluye": CX_INCLUYE,
                   "msj": "La mastopexia sin implantes está desde $15.900.000 e incluye fajas, bomba del dolor, quirófano, instrumentador y póliza. ¿Te agendo tu valoración con el Dr. Fernando?"},
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


# ---------------------------------------------------------------- PACIENTES DEL EXTERIOR (EE. UU.) · guiones ES + EN
# Solo datos verificados (_agencia-seo/hechos.md). Precios siempre en pesos colombianos (COP), nunca convertidos a dólares.
INTERNACIONAL_REGLAS = [
    ("Pregunta ciudad y fechas", "Desde qué ciudad escribe y cuándo podría viajar. Con eso se arma todo."),
    ("Valoración presencial", "Se hace en persona al llegar a Medellín. Por WhatsApp solo se adelanta información y se agenda."),
    ("Nunca des fecha para volar", "El regreso lo autoriza el especialista en el control. Recomienda tiquete flexible."),
    ("Acompañante", "Si es cirugía, debe venir con un adulto que la acompañe los primeros días."),
    ("Precios en pesos", "Se dan en pesos colombianos (COP). No los conviertas a dólares."),
    ("Seguimiento al volver", "Al volver a EE. UU. seguimos con ella por WhatsApp o videollamada. No reemplaza los controles en Medellín ni urgencias."),
]
INTERNACIONAL = [  # (tema, mensaje en español, mensaje en inglés)
    ("Saludo", "¡Hola! Gracias por escribir a noon Clinic en Medellín. ¿Desde qué ciudad nos escribes y para cuándo piensas viajar?",
     "Hi! Thank you for reaching out to noon Clinic in Medellín. Which city are you writing from, and when are you thinking of traveling?"),
    ("¿Cuánto cuesta?", "El valor se define en tu valoración presencial con el especialista, porque cada plan es personal. ¿Te la agendo para el día que llegues?",
     "The cost is defined at your in-person consultation with our specialist, because every plan is personal. Would you like us to book it for the day you arrive?"),
    ("¿Cuántos días me quedo?", "Como guía: rostro y senos entre 1 y 2 semanas; contorno corporal y combinadas entre 2 y 3 semanas. El regreso lo autoriza tu especialista. ¿Qué fechas tienes en mente?",
     "As a guide: face and breast procedures 1 to 2 weeks; body contouring and combined procedures 2 to 3 weeks. Your specialist confirms when you can fly home. What dates do you have in mind?"),
    ("¿Hacen valoración virtual?", "La valoración es presencial en Medellín, para que el especialista te examine. Antes de viajar adelantamos tu información por aquí. ¿Qué día llegas?",
     "Your consultation is in person in Medellín, so the specialist can examine you. Before you travel, we can get your details ready here on WhatsApp. What day do you arrive?"),
    ("¿Es seguro?", "Las cirugías se hacen en salas de cirugía habilitadas en Q2, nunca en un consultorio, y con exámenes previos obligatorios. ¿Te agendo tu valoración?",
     "Surgeries are performed in licensed operating rooms at Q2, never in a doctor's office, and pre-op tests are required. Would you like to book your consultation?"),
    ("¿Y cuando vuelva a casa?", "Seguimos contigo por WhatsApp o videollamada. No reemplaza tus controles en Medellín antes de volar, y ante una urgencia vas a urgencias donde estés. ¿Miramos fechas?",
     "Once you're home, we stay in touch by WhatsApp or video call. It doesn't replace your follow-ups in Medellín before flying, and for any emergency please go to a local ER. Shall we look at dates?"),
    ("¿Necesito visa?", "Si tienes pasaporte de EE. UU., no necesitas visa de turismo para Colombia. Si también eres colombiana, entras y sales con tu pasaporte colombiano. Revisa los requisitos vigentes antes de viajar. ¿Para cuándo piensas venir?",
     "US citizens don't need a tourist visa for Colombia. If you're also Colombian, you must enter and leave with your Colombian passport. Please check current requirements before you travel. When are you planning to come?"),
    ("Acompañante", "Para una cirugía necesitas un adulto que te acompañe los primeros días. ¿Vienes con alguien?",
     "For surgery, you'll need an adult with you during the first days. Will someone be traveling with you?"),
    ("¿A qué aeropuerto llego?", "El aeropuerto internacional de Medellín (MDE) queda en Rionegro, fuera de la ciudad. ¿Desde qué ciudad vuelas?",
     "Medellín's international airport (MDE) is in Rionegro, just outside the city. Which city are you flying from?"),
    ("Precio con valor conocido", "La mamoplastia de aumento tiene un valor de $10.900.000 pesos colombianos e incluye cirujano, quirófano, implantes, brasier, póliza y bomba del dolor. ¿Te agendo tu valoración con el Dr. Fernando?",
     "Breast augmentation is COP 10,900,000 (Colombian pesos) and includes the surgeon, operating room, implants, post-op bra, complications insurance and pain pump. Would you like to book your consultation with Dr. Fernando?"),
]


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


def _cirugias():
    # en la capacitación la mastopexia va dividida: con implantes y sin implantes
    out = []
    for c in CIRUGIAS_NOON:
        if c["slug"] != "mastopexia":
            out.append(c); continue
        out.append(dict(c, slug="mastopexia-con-implantes", nombre="Mastopexia con implantes",
                        corto="Levanta el seno y le da volumen con implantes.",
                        que_es=["Cirugía que levanta el seno caído y, además, le pone implantes para dar volumen, sobre todo en la parte de arriba.",
                                "Retira el exceso de piel, da nueva forma al seno y sube la areola y el pezón."],
                        ideal=["Senos caídos y con poco volumen", "Sensación de seno 'vacío' arriba", "Cambios tras embarazos, lactancia o baja de peso"],
                        faq=[f for f in c["faq"] if not f[0].startswith("¿Con o sin")] + [("¿Cuál es la diferencia con la mastopexia sin implantes?", "La sin implantes solo levanta con tu propio tejido; la con implantes además da volumen.")]))
        out.append(dict(c, slug="mastopexia-sin-implantes", nombre="Mastopexia sin implantes",
                        corto="Levanta y reafirma el seno con tu propio tejido.",
                        que_es=["Cirugía que levanta el seno caído usando solo tu propio tejido, sin implantes.",
                                "Retira el exceso de piel, da nueva forma al seno y sube la areola y el pezón. Es ideal si te gusta tu volumen."],
                        ideal=["Senos caídos pero con buen volumen", "Areola y pezón que apuntan hacia abajo", "Cambios tras embarazos, lactancia o baja de peso"],
                        faq=[f for f in c["faq"] if not f[0].startswith("¿Con o sin")] + [("¿Cuál es la diferencia con la mastopexia con implantes?", "Esta solo levanta con tu propio tejido; la con implantes además da volumen.")]))
    return out


def generar():
    procs = ([_proc(c, "cx", {k: n for k, n, d, f in CATEGORIAS_CX}) for c in _cirugias()]
             + [_proc(t, "me", {k: n for k, n, d, f in CATEGORIAS_ME}) for t in TRATAMIENTOS])
    for i, p in enumerate(procs):
        p["img"] = _imagen(p["slug"], i)
    datos = {"procs": procs, "cats_cx": [n for k, n, d, f in CATEGORIAS_CX], "cats_me": [n for k, n, d, f in CATEGORIAS_ME],
             "doctores": DOCTORES, "disp": DISPONIBILIDAD, "objeciones": OBJECIONES, "reglas": REGLAS, "pasos": PASOS,
             "precio": PRECIO, "lista_precios": [(p["nombre"], it, v, p["slug"], p["tipo"]) for p in procs for it, v in p["precios"]],
             "otros_precios": OTROS_PRECIOS, "video": VIDEO,
             "inter_reglas": INTERNACIONAL_REGLAS, "inter": INTERNACIONAL}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.replace("%%DATOS%%", js).replace("%%HASH%%", hashlib.sha256(CODIGO.encode()).hexdigest())
    with open(os.path.join(AQUI, "capacitacion-comercial.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(procs)


with open(os.path.join(AQUI, "_capacitacion_plantilla.html"), encoding="utf-8") as _f:
    PLANTILLA = _f.read()

if __name__ == "__main__":
    print("Capacitación comercial: %d procedimientos." % generar())
