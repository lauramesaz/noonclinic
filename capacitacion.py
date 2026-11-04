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
    ("Valoración presencial", "Se hace en persona al llegar a Medellín. Antes de viajar se adelanta una preconsulta por video con sus fotos para darle un valor estimado por escrito; el especialista lo confirma en la valoración presencial."),
    ("Nunca des fecha para volar", "El regreso lo autoriza el especialista en el control. Recomienda tiquete flexible."),
    ("Acompañante", "Si es cirugía, debe venir con un adulto que la acompañe los primeros días."),
    ("Precios en pesos", "Se dan en pesos colombianos (COP). No los conviertas a dólares."),
    ("Seguimiento al volver", "Al volver a EE. UU. seguimos con ella por WhatsApp o videollamada. No reemplaza los controles en Medellín ni urgencias."),
]
INTERNACIONAL = [  # (tema, mensaje en español, mensaje en inglés)
    ("Saludo", "¡Hola! Gracias por escribir a noon Clinic en Medellín. ¿Desde qué ciudad nos escribes y para cuándo piensas viajar?",
     "Hi! Thank you for reaching out to noon Clinic in Medellín. Which city are you writing from, and when are you thinking of traveling?"),
    ("¿Cuánto cuesta?", "Con una preconsulta por video y tus fotos te damos un valor estimado por escrito antes de viajar. El valor final lo confirma el especialista en tu valoración presencial, porque cada plan es personal. ¿Adelantamos tu preconsulta?",
     "With a video pre-consultation and your photos, we send you an estimated price in writing before you travel. The specialist confirms the final price at your in-person consultation, because every plan is personal. Shall we start your pre-consultation?"),
    ("¿Cuántos días me quedo?", "Como guía: rostro y senos entre 1 y 2 semanas; contorno corporal y combinadas entre 2 y 3 semanas. El regreso lo autoriza tu especialista. ¿Qué fechas tienes en mente?",
     "As a guide: face and breast procedures 1 to 2 weeks; body contouring and combined procedures 2 to 3 weeks. Your specialist confirms when you can fly home. What dates do you have in mind?"),
    ("¿Hacen valoración virtual?", "La valoración es presencial en Medellín, para que el especialista te examine. Antes de viajar sí hacemos una preconsulta por video con tus fotos y te damos un valor estimado por escrito. ¿Qué día llegas?",
     "Your consultation is in person in Medellín, so the specialist can examine you. Before you travel, we do a video pre-consultation with your photos and send you an estimated price in writing. What day do you arrive?"),
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


# ---------------------------------------------------------------- SEGUIMIENTO DESPUÉS DE LA VALORACIÓN (de la cita al abono)
# 3-nov-2026: en octubre hubo 54 citas de cirugía pagadas y 6 abonos → el seguimiento es donde más ventas se ganan.
# Solo reglas que ya existen: abono $1.000.000 → empieza el montaje; la cita de $200.000 no se abona; las promos con precio
# exigen operarse antes de FECHA_LIMITE; lo adicional se paga aparte. Nada de cupos, descuentos ni plazos inventados.
from datos import FECHA_LIMITE
SEGUIMIENTO_REGLAS = [
    ("Cada paciente tiene dueña", "Quien la atendió le hace el seguimiento hasta que abone o diga que no."),
    ("Anota cada mensaje", "Fecha, qué le escribiste y qué respondió. Así nadie le escribe dos veces lo mismo."),
    ("Busca la duda real", "Casi siempre es una de cuatro: el valor, el miedo, la pareja o las fechas. Pregunta cuál es."),
    ("Nada de presión falsa", "No inventes cupos, descuentos ni fechas que no existen. La confianza vende más."),
    ("Tres sin respuesta, pausa", "Si no contesta tres mensajes seguidos, deja de escribir y vuelve a intentarlo en dos meses."),
    ("Termina en pregunta", "Igual que en el primer chat: un mensaje corto y una pregunta al final."),
]
SEGUIMIENTO = [  # (cuándo, para qué, mensaje)
    ("El mismo día de la consulta", "Que se sienta acompañada.",
     "¡Hola, {nombre}! ¿Cómo te sentiste en tu valoración? Si te quedó alguna duda, aquí estoy para ayudarte 🤍"),
    ("Día 1 · Cuando le llega la cotización", "Confirmar que la recibió y la entiende.",
     "¿Te llegó bien tu cotización? Si quieres, te explico qué incluye punto por punto. ¿Tienes alguna pregunta?"),
    ("Día 3", "Encontrar la duda real.",
     "¿Ya pudiste revisar tu cotización con calma? Cuéntame qué es lo que más te hace dudar y lo resolvemos juntas."),
    ("Día 7", "Pasar de la duda a las fechas.",
     "Te escribo porque las fechas de cirugía se organizan desde el abono. ¿Quieres que miremos qué fechas te quedarían bien?"),
    ("Día 15 · Solo si su cotización es de promo", "Recordar la vigencia real de la promo.",
     "Te recuerdo que el valor de tu cotización es de la promo de fin de año: la cirugía debe hacerse antes del " + FECHA_LIMITE + ". ¿Te ayudo a mirar fechas?"),
    ("Día 30", "Reactivar sin presión.",
     "Hola, {nombre}. Solo quería saber cómo vas con tu decisión. Si no es el momento, está bien; cuando quieras retomarlo, aquí estamos 🤍"),
]
SEGUIMIENTO_SIN_CITA = [  # (cuándo, para qué, mensaje) · escribió por WhatsApp, preguntó y no pagó la cita de valoración
    ("Al día siguiente", "Retomar la conversación donde quedó.",
     "¡Hola, {nombre}! Ayer hablamos de tu {procedimiento}. ¿Te quedó alguna duda que te pueda resolver? 🤍"),
    ("Día 3", "Pasar de la información a la cita.",
     "Te escribo para ayudarte a dar el primer paso: en tu valoración el especialista te examina y sales con tu plan y tu valor exacto. ¿Te queda mejor esta semana o la próxima?"),
    ("Día 7", "Último intento, sin presión.",
     "Hola, {nombre}. No quiero llenarte de mensajes 🤍 Si más adelante quieres retomar lo de tu {procedimiento}, aquí estamos. ¿Te escribo en unas semanas?"),
]
SEGUIMIENTO_ESTETICA = [  # (cuándo, mensaje) · pacientes de estética que ya vinieron: volver por su retoque o su siguiente sesión
    ("Bótox · desde 4 meses después de la aplicación",
     "Hola, {nombre} 🤍 Te escribimos de noon Clinic. Ya van unos meses desde tu bótox con la Dra. Valeria y por esta época es cuando suele tocar el retoque. ¿Quieres que te revisemos un espacio en su agenda?"),
    ("Terapia capilar · va por sesiones",
     "Hola, {nombre} 🤍 Te escribimos de noon Clinic. ¿Cómo vas con tu terapia capilar? Cuéntanos en qué sesión vas y te ayudamos a agendar la siguiente con la Dra. Valeria. ¿Te parece?"),
    ("Bioestimuladores · si su plan tiene más sesiones",
     "Hola, {nombre} 🤍 Te escribimos de noon Clinic. ¿Cómo te has sentido después de tu sesión? Si tu plan con la Dra. Valeria tiene más sesiones, te ayudamos a agendar la siguiente. ¿Te revisamos un espacio?"),
    ("No sabes qué se hizo · primero revisa en Saneo",
     "Hola, {nombre} 🤍 Te escribimos de noon Clinic para saber cómo te fue con tu tratamiento con la Dra. Valeria. ¿Te gustaría que te ayudemos a agendar tu próxima cita?"),
]
SEGUIMIENTO_OBJ = [  # objeciones que aparecen DESPUÉS de la cotización
    ("“Lo voy a pensar”", "¡Claro que sí! Es una decisión importante. ¿Qué es lo que más te hace dudar: el valor, la recuperación o las fechas? Así te ayudo con eso puntual."),
    ("“Está muy caro”", "Te entiendo. Cuando compares, revisa si la otra cotización incluye quirófano, instrumentador, póliza y bomba de dolor, y si el cirujano es plástico con registro en ReTHUS. ¿Quieres que revisemos la tuya punto por punto?"),
    ("“Lo tengo que hablar con mi pareja”", "Me parece muy bien. Si quieres, te mando un resumen corto de tu plan para que se lo muestres. ¿Te sirve?"),
    ("“No tengo todo el dinero ahora”", "Te entiendo. Con el abono de $1.000.000 empezamos a organizar tu cirugía. ¿Quieres que te expliquemos cómo funcionan los pagos?"),
    ("“Me da miedo”", "Es normal sentirlo. Te puedo contar cómo es la recuperación día a día y qué cuidados tenemos, y la Dra. Valeria te resuelve las dudas médicas. ¿Te gustaría?"),
    ("“Quiero comparar con otros lugares”", "¡Hazlo! Compara con información completa: que el cirujano sea plástico con registro en ReTHUS, qué incluye el valor y dónde se opera. ¿Te paso el enlace para verificar a tu cirujano en el ReTHUS?"),
]


# ---------------------------------------------------------------- EL CAMINO DEL PACIENTE (proceso comercial, de que escribe a que abona)
# Cada paso: quién, qué, cómo, alerta (opcional), chat de ejemplo [(lado, quien, texto)] lado = "pac" | "noon" | "int" (interno)
TERMINOS_URL = "https://noon.clinic/terminos-y-condiciones#t2"
CIUDADES = ["Medellín", "Bogotá", "Pereira"]
CAMINO = [
    {"ico": "chat", "corto": "Escribe", "quien": "Paciente → Comercial", "foto": "",
     "que": "El paciente escribe y tú lo atiendes.",
     "como": "Resuelves sus dudas y haces las 3 preguntas clave: ciudad, qué se quiere hacer y si la cita es presencial o virtual.",
     "ojo": "Siempre pregunta si la cita es presencial o virtual y en qué ciudad está.",
     "chat": [("pac", "Paciente", "Hola, quiero info de la lipo 🙌"),
              ("noon", "Comercial", "¡Hola! Qué bueno que nos escribes. ¿Desde qué ciudad nos escribes: Medellín, Bogotá o Pereira?")]},
    {"ico": "precio", "corto": "Paga", "quien": "Paciente", "foto": "",
     "que": "Paga la cita de valoración: $200.000.",
     "como": "Sin pago no hay cita. Así de simple.",
     "ojo": "Los $200.000 son de la promoción y NO se abonan a la cirugía.",
     "chat": [("noon", "Comercial", "Para reservar tu valoración el valor es $200.000. ¿Te paso los datos para el pago?"),
              ("pac", "Paciente", "Listo, ya te mando el comprobante ✅")]},
    {"ico": "cal", "corto": "Agenda", "quien": "Comercial", "foto": "",
     "que": "Agendas la cita y avisas a todos.",
     "como": "1) Montas la cita en Saneo, en la agenda y la ciudad correctas. 2) Mandas el comprobante al grupo de WhatsApp con el formato de siempre. 3) Le envías al paciente el mensaje de confirmación.",
     "ojo": "Cirugía plástica y medicina estética son agendas distintas. Si dudas, pregunta.",
     "chat": [("int", "Grupo de WhatsApp", "📎 Comprobante · Nombre · Cédula · Ciudad · Fecha y hora · Doctor"),
              ("noon", "Comercial", "¡Tu cita quedó agendada! Te envío la confirmación con todos los detalles 💌")]},
    {"ico": "check", "corto": "Verifica", "quien": "Administración", "foto": "",
     "que": "Administración revisa que el pago sí entró.",
     "como": "Lo hace con el comprobante que mandaste al grupo. Por eso el formato es tan importante.",
     "ojo": "",
     "chat": [("int", "Administración", "Pago confirmado ✔️")]},
    {"ico": "gota", "corto": "Preconsulta", "quien": "Dra. Valeria · médica general", "foto": "valeria",
     "que": "La Dra. Valeria hace la preconsulta.",
     "como": "Le escribe al paciente desde su número para conocer su caso antes de la cita.",
     "ojo": "Si la cita es virtual, la Dra. Valeria le pide las fotos. Siempre.",
     "chat": [("noon", "Dra. Valeria", "Hola, soy la Dra. Valeria de noon. Para preparar tu cita virtual, ¿me compartes unas fotos de la zona a tratar?")]},
    {"ico": "bisturi", "corto": "Consulta", "quien": "Dr. Fer · cirujano plástico", "foto": "fernando",
     "que": "Consulta con el cirujano plástico.",
     "como": "El Dr. Fer valora al paciente y define el plan.",
     "ojo": "Cada ciudad tiene su médico: el paciente lo atiende el médico de SU ciudad.",
     "chat": []},
    {"ico": "lista", "corto": "Cotización", "quien": "Dra. Valeria · médica general", "foto": "valeria",
     "que": "La Dra. Valeria saca la cotización y se la manda.",
     "como": "La hace en el cotizador de la página web, con lo que definió el doctor.",
     "ojo": "Si se suma un procedimiento adicional, ese se paga aparte.",
     "chat": [("noon", "Dra. Valeria", "Te comparto tu cotización 📄 Cualquier duda me cuentas.")]},
    {"ico": "chat", "corto": "Seguimiento", "quien": "Equipo comercial", "foto": "",
     "que": "Le haces seguimiento hasta que decida.",
     "como": "Lo acompañas con el plan de mensajes de la sección Seguimiento (día 0, 1, 3, 7, 15 y 30) hasta que decida.",
     "ojo": "",
     "chat": [("noon", "Comercial", "¿Cómo te fue con la cotización? ¿Te ayudo a escoger la fecha de tu cirugía?")]},
    {"ico": "check", "corto": "¡Abona!", "quien": "Paciente → Equipo de cirugía", "foto": "",
     "que": "El paciente abona su cirugía: $1.000.000.",
     "como": "¡Lo lograste! Aquí empieza otro proceso: el montaje de la cirugía (qué quiere el paciente, quirófano, fechas).",
     "ojo": "",
     "chat": [("pac", "Paciente", "¡Ya hice el abono! 🎉"), ("noon", "Comercial", "¡Qué emoción! Ya empezamos a organizar tu cirugía.")]},
]
CONFIRMACION = ("✨ *CONFIRMACIÓN DE CITA* ✨\n"
                "━━━━━━━━━━━━━━\n\n"
                "🤍 *Nombre:* \n"
                "🗓️ *Fecha:* \n"
                "🕰️ *Hora:* \n"
                "📲 *Tipo de cita:* Presencial / Virtual\n"
                "🩺 *Especialidad:* \n"
                "👩🏻‍⚕️ *Especialista:* \n"
                "📍 *Consultorio:* \n\n"
                "━━━━━━━━━━━━━━\n"
                "🌿 *Ten en cuenta*\n\n"
                "▫️ Si necesitas reprogramar, avísanos con mínimo *24 horas* de anticipación.\n"
                "▫️ Si no asistes y pides la devolución del valor de la cita, se hace entre *30 y 90 días hábiles*, con un cargo del *20%* por proceso administrativo.\n"
                "▫️ El valor de la cita no se abona a la cirugía.\n"
                "▫️ Si se suma un procedimiento adicional, se paga aparte.\n\n"
                "📜 Términos y condiciones: " + TERMINOS_URL + "\n\n"
                "Antes de tu cita te escribirá la Dra. Valeria, nuestra médica general.\n"
                "Gracias por confiar en *noon Clinic* 🤍")
REGLAS_ORO = [
    ("🙋", "Si dudas, pregunta.", "Nunca asumas. Preguntar es de pros."),
    ("📍", "Ciudad clara, siempre.", "Medellín, Bogotá o Pereira. Cada una tiene su médico."),
    ("🗓️", "Agenda correcta.", "Cirugía plástica y medicina estética no van juntas."),
    ("💸", "Los $200.000 no se abonan.", "Son de la promoción. Lo adicional se paga aparte."),
    ("📜", "Términos en cada cita.", "Van en el mensaje de confirmación."),
    ("📲", "Docs y redes del Dr. Fer.", "A todos los pacientes, sin excepción."),
]
QUIZ = [  # (situación, [opciones], índice correcto, explicación)
    ("Una paciente te escribe desde Pereira y quiere su valoración.",
     ["La agendo con el Dr. Fer en Medellín", "La agendo con el médico de Pereira", "La agendo donde haya espacio"], 1,
     "Cada ciudad tiene su médico. Paciente de Pereira = médico de Pereira."),
    ("Te dice: “Te pago mañana, ¿me apartas la cita?”",
     ["Sí, se la aparto de una", "La cita queda agendada cuando llega el pago"], 1,
     "Sin pago no hay cita. Lo dices con cariño, pero lo dices."),
    ("Te pregunta: “¿Los 200 mil se me abonan a la cirugía?”",
     ["Sí, claro", "No, son de la promoción y no se abonan", "Depende del doctor"], 1,
     "Los $200.000 no se abonan. Y está en los términos que le mandas."),
    ("La cita es virtual. ¿Quién le pide las fotos?",
     ["Yo, la comercial", "La Dra. Valeria, desde su número", "Nadie, no hacen falta"], 1,
     "Las fotos las pide la Dra. Valeria. Y siempre se piden."),
    ("No estás segura si va en la agenda de cirugía o en la de estética.",
     ["La pongo en la que creo", "Pregunto antes de agendar"], 1,
     "Si dudas, pregunta. Una pregunta ahorra un problemón."),
    ("En la valoración quiere sumar otro procedimiento a su cirugía.",
     ["Va incluido en el precio", "El procedimiento adicional se paga aparte"], 1,
     "Lo adicional se paga aparte, y queda en su cotización."),
]


# Conversación de WhatsApp de ejemplo (UNA sola, crece paso a paso). Vista desde el WhatsApp de noon:
# "noon" = mensajes del equipo (derecha, verde), "pac" = paciente (izquierda, blanco), "sys" = nota interna (centro).
# Texto que empieza por [img] = foto/comprobante, [pdf] = documento, [conf] = mensaje de confirmación lleno.
CONF_EJEMPLO = {"Nombre": "Ana Gómez", "Fecha": "Jueves 23 de octubre", "Hora": "10:00 a. m.", "Tipo de cita": "Presencial",
                "Especialidad": "Cirugía plástica", "Especialista": "Dr. Fernando Ruiz", "Consultorio": "noon Clinic · Medellín"}
CHAT_WA = [
    [("pac", "", "Hola, buenas tardes 👋 Quiero información de la lipo", "2:14 p. m."),
     ("noon", "Comercial", "¡Hola, Ana! Qué gusto saludarte, te habla Sofía de noon Clinic 🤍 ¿Desde qué ciudad nos escribes?", "2:15 p. m."),
     ("pac", "", "Desde Medellín", "2:15 p. m."),
     ("noon", "Comercial", "¡Perfecto! ¿Prefieres tu cita de valoración presencial o virtual?", "2:16 p. m."),
     ("pac", "", "Presencial, por favor", "2:16 p. m.")],
    [("noon", "Comercial", "Listo 😊 Para reservar tu cita de valoración el valor es de $200.000. ¿Te comparto los datos para el pago?", "2:17 p. m."),
     ("pac", "", "Sí, por favor", "2:18 p. m."),
     ("pac", "", "[img]Comprobante de pago", "2:31 p. m."),
     ("pac", "", "Listo, ya pagué ✨", "2:31 p. m.")],
    [("sys", "", "Interno: comprobante enviado al grupo de WhatsApp y cita montada en Saneo", ""),
     ("noon", "Comercial", "[conf]", "2:40 p. m."),
     ("pac", "", "¡Mil gracias! 🙌", "2:42 p. m.")],
    [("sys", "", "Interno: administración confirmó que el pago entró ✔️", "")],
    [("noon", "Dra. Valeria", "Hola, Ana. Soy la Dra. Valeria, médica general de noon 🤍 Te escribo para preparar tu cita con el Dr. Fernando. ¿Me cuentas qué te gustaría mejorar?", "Mar 9:05 a. m."),
     ("pac", "", "Hola, doctora. El abdomen y la cintura 😊", "Mar 9:20 a. m."),
     ("noon", "Dra. Valeria", "Perfecto, quedó anotado. ¡Nos vemos el jueves!", "Mar 9:22 a. m.")],
    [("sys", "", "Cita de valoración con el Dr. Fernando · en persona 🩺", ""),
     ("pac", "", "¡Me encantó el doctor! Me explicó todo 😍", "Jue 12:10 p. m.")],
    [("noon", "Dra. Valeria", "Ana, te comparto tu cotización 📄", "Jue 3:30 p. m."),
     ("noon", "Dra. Valeria", "[pdf]Cotización Ana Gómez.pdf", "Jue 3:30 p. m."),
     ("noon", "Dra. Valeria", "Cualquier duda me cuentas.", "Jue 3:31 p. m.")],
    [("noon", "Comercial", "Hola, Ana 🤍 ¿Cómo te fue con la cotización? ¿Te ayudo a escoger la fecha de tu cirugía?", "Sáb 11:00 a. m."),
     ("pac", "", "Sí, estoy pensando en diciembre", "Sáb 11:24 a. m."),
     ("noon", "Comercial", "¡Me encanta! Con el abono reservamos tu fecha. ¿Te paso los datos?", "Sáb 11:25 a. m.")],
    [("pac", "", "[img]Comprobante del abono", "Sáb 4:02 p. m."),
     ("pac", "", "¡Listo, ya hice el abono! 🎉", "Sáb 4:02 p. m."),
     ("noon", "Comercial", "¡Qué emoción, Ana! Tu fecha queda reservada. Ahora empezamos a organizar tu cirugía 🤍", "Sáb 4:05 p. m.")],
]


# ---------------------------------------------------------------- SIMULADOR (sin IA, con guion)
# Cada caso: nodos. Nodo = mensajes del paciente + opciones [(texto que envía la comercial, bien?, por qué, reacción del paciente [])]
SIMULADOR = [
    {"nombre": "Ana Gómez", "nivel": "Fácil", "resumen": "Quiere lipo. Escribe desde Medellín y pregunta el precio de una.", "nodos": [
        {"pac": ["Hola 👋 quiero información de la lipo, ¿cuánto vale?"], "op": [
            ("¡Hola, Ana! Qué gusto saludarte, te habla Sofía de noon Clinic 🤍 El valor de la lipo se define en tu valoración, porque cada plan es personal. ¿Desde qué ciudad nos escribes?", True, "Saludas con calidez, no inventas precios y terminas con la pregunta de la ciudad.", []),
            ("La lipo cuesta más o menos 12 millones.", False, "Nunca des precios que no están en la lista. El valor de la lipo se define en la valoración.", ["Ah ok… ¿y eso incluye todo?"]),
            ("Hola, ¿qué te quieres hacer exactamente?", False, "Ya te dijo que quiere lipo, y no respondiste su pregunta. Lee bien antes de responder.", ["La lipo 😅"])]},
        {"pac": ["Soy de Medellín. ¿Cómo hago para tener la cita?"], "op": [
            ("¡Perfecto! ¿Prefieres tu cita de valoración presencial o virtual?", True, "Siempre pregunta si la cita es presencial o virtual.", []),
            ("Te agendo para el jueves a las 10 con el Dr. Fernando.", False, "Te saltaste dos cosas: presencial o virtual, y el pago. Sin pago no hay cita.", ["Ah bueno… ¿pero es presencial?"])]},
        {"pac": ["Presencial. ¿Y cuánto vale la cita?"], "op": [
            ("La cita de valoración tiene un valor de $200.000 y con eso reservamos tu espacio. ¿Te comparto los datos para el pago?", True, "Precio claro, explicas para qué es y cierras con una pregunta.", []),
            ("Es gratis si te operas con nosotros.", False, "La cita vale $200.000 y no se abona a la cirugía. No prometas cosas que no son.", ["¿Gratis? Ah, qué bien 😊"])]},
        {"pac": ["Listo. ¿Esos 200 mil se me abonan a la cirugía?"], "op": [
            ("Sí, claro, se descuentan de la cirugía.", False, "Los $200.000 NO se abonan. Es uno de los errores que más problemas trae después.", ["¡Súper!"]),
            ("No, el valor de la cita no se abona a la cirugía: es la consulta con el especialista. ¿Te paso los datos para que reserves?", True, "Lo dices claro y con amabilidad, sin rodeos.", [])]},
        {"pac": ["[img]Comprobante de pago", "Ya pagué ✨"], "op": [
            ("¡Gracias, Ana! Ya mismo monto tu cita y te envío la confirmación con todos los detalles 💌", True, "Ahora te toca: comprobante al grupo, cita en Saneo y mensaje de confirmación.", []),
            ("Gracias, después te digo la hora.", False, "Confirma de una: monta la cita en Saneo y envía el mensaje de confirmación.", ["Ok… quedo pendiente 😕"])]},
    ]},
    {"nombre": "Camila Restrepo", "nivel": "Media", "resumen": "Quiere aumento de senos. Vive en Pereira y prefiere cita virtual.", "nodos": [
        {"pac": ["Buenas, vi su página. Quiero hacerme el aumento de senos"], "op": [
            ("¡Hola, Camila! Qué bueno que nos escribes 🤍 ¿Desde qué ciudad nos escribes?", True, "Antes de cualquier cosa: la ciudad.", []),
            ("¡Hola! Te agendo con el Dr. Fernando en Medellín, ¿qué día te sirve?", False, "No sabes de qué ciudad es. Cada ciudad tiene su médico.", ["Uy, pero yo vivo en Pereira 😕"])]},
        {"pac": ["Estoy en Pereira"], "op": [
            ("¡Perfecto! Te agendamos con el especialista de Pereira. ¿Prefieres la cita presencial o virtual?", True, "Paciente de Pereira = médico de Pereira. Y preguntaste la modalidad.", []),
            ("No hay problema, igual el Dr. Fernando te atiende.", False, "Paciente de Pereira = médico de Pereira.", ["Ah, ¿tengo que viajar a Medellín?"])]},
        {"pac": ["Virtual mejor, trabajo todo el día"], "op": [
            ("¡Listo! La cita de valoración tiene un valor de $200.000. Antes de la cita, la Dra. Valeria te escribirá para pedirte unas fotos. ¿Te comparto los datos para el pago?", True, "Precio claro y le avisas que las fotos las pide la Dra. Valeria.", []),
            ("Listo. Mándame unas fotos por aquí y te digo.", False, "Las fotos las pide la Dra. Valeria desde su número, no la comercial.", ["Ehh… ¿a ti? Me da un poco de pena 😳"])]},
        {"pac": ["¿Y cuánto vale la cirugía?"], "op": [
            ("El valor final te lo da la cotización después de tu valoración, porque cada plan es personal. ¿Te comparto los datos para reservar tu cita?", True, "No inventas y llevas la conversación de vuelta a reservar.", []),
            ("Unos 8 millones, más o menos.", False, "Nunca inventes precios. El valor sale de la cotización.", ["¿8? Listo, eso me sirve"])]},
        {"pac": ["Ok, ya te pago", "[img]Comprobante de pago"], "op": [
            ("¡Gracias, Camila! Monto tu cita y te envío la confirmación. La Dra. Valeria te escribirá antes para las fotos 💌", True, "Confirmas, le dices qué sigue y envías la confirmación.", []),
            ("Listo, gracias.", False, "Muy seco. Confirma, cuéntale qué sigue y envía la confirmación.", ["¿Y ya quedó? 🤔"])]},
    ]},
    {"nombre": "Daniela Ochoa", "nivel": "Difícil", "resumen": "Quiere rinoplastia. Pide apartar sin pagar, pregunta por devoluciones y quiere sumar otro procedimiento.", "nodos": [
        {"pac": ["Hola, quiero rinoplastia. Soy de Medellín y quiero cita presencial 🙏"], "op": [
            ("¡Hola, Daniela! Qué gusto 🤍 Para reservar tu valoración presencial el valor es de $200.000. ¿Te comparto los datos para el pago?", True, "Ya te dio ciudad y modalidad: no repreguntes, avanza.", []),
            ("¡Hola! ¿Desde qué ciudad nos escribes?", False, "Ya te lo dijo. Lee bien antes de responder.", ["Te acabo de decir, Medellín 😅"])]},
        {"pac": ["Te pago mañana, ¿me apartas la cita para el jueves?"], "op": [
            ("Sí, claro, te la dejo apartada.", False, "Sin pago no hay cita. Si no paga, le quitas el espacio a otra paciente.", ["¡Gracias, eres un amor!"]),
            ("¡Claro que sí! La cita queda reservada apenas recibamos el pago. Si pagas hoy te guardo el jueves. ¿Te paso los datos?", True, "Amable pero firme: sin pago no hay cita.", [])]},
        {"pac": ["Y si no puedo ir, ¿me devuelven la plata?"], "op": [
            ("Si necesitas cambiarla, avísanos con mínimo 24 horas y la reprogramamos. Todo está en nuestros términos y condiciones, que te llegan con la confirmación. ¿Te parece?", True, "Explicas la regla de las 24 horas y la remites a los términos.", []),
            ("Sí, tranquila, te devolvemos todo.", False, "No prometas devoluciones. Explica la reprogramación con 24 horas y los términos.", ["Ah bueno, entonces no me preocupo"])]},
        {"pac": ["[img]Comprobante de pago", "Listo, pagué. Ah, y de una vez quiero que me hagan la bichectomía"], "op": [
            ("¡Gracias, Daniela! El Dr. Fernando lo revisa contigo en la valoración. Si se suma un procedimiento adicional, ese se paga aparte. ¿Te parece?", True, "Lo adicional se paga aparte, y lo dejas claro desde ya.", []),
            ("¡Listo! Te la incluimos en el mismo precio.", False, "Lo adicional se paga aparte. Nunca lo regales.", ["¡Wow, qué buena promo! 😍"])]},
        {"pac": ["Perfecto, gracias 😊"], "op": [
            ("¡A ti! Ya te envío la confirmación con todos los detalles 💌", True, "Cierre perfecto. Ahora: Saneo, comprobante al grupo y confirmación.", []),
            ("👍", False, "Un pulgar no es un cierre. Confirma y envía el mensaje de confirmación.", ["…"])]},
    ]},
]


def _cirugias():
    # en la capacitación la mastopexia va dividida: con implantes y sin implantes
    out = []
    for c in CIRUGIAS_NOON:
        if c.get("nueva"):
            continue  # las fichas nuevas de la web (variantes y combinaciones) no cambian la capacitación
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


# ---------------------------------------------------------------- SI COMPARAN PRECIOS (investigación 3-nov-2026, ~/Documents/noon ventas/precios-competencia-nov-2026.md)
# Precios PUBLICADOS en internet 2025-2026 (orientativos, casi todos "desde"). Son para la asesora: nunca nombrar otras clínicas.
COMPARAR = [  # (cirugía, precio noon, lo típico publicado, cómo estamos, frase para la paciente)
    ("Aumento de senos", "$10.900.000", "14 a 17 millones", "Por debajo: de lo más bajo con todo incluido",
     "¡Qué bueno que compares! Pide que te pongan por escrito si ese precio ya trae los implantes, la póliza de complicaciones, la bomba de dolor y el brasier. Aquí los $10.900.000 ya traen todo eso."),
    ("Mastopexia con implantes", "Desde $17.900.000", "19 a 22 millones", "Por debajo de lo típico",
     "Revisa si ese precio incluye los implantes; muchas veces la mastopexia se cotiza sin ellos y se suman aparte. Aquí, desde $17.900.000, ya van los implantes, la póliza y la bomba de dolor."),
    ("Mastopexia sin implantes", "Desde $15.900.000", "12 a 16 millones", "En el medio, tirando a arriba",
     "Es normal ver precios más bajos; la pregunta es qué traen. El nuestro ya trae cirujano plástico, instrumentador, quirófano, póliza de complicaciones y bomba de dolor. Compáralos con todo sumado y por escrito."),
    ("Lipo y lipotransferencia", "Desde $18.900.000", "18 a 25 millones", "En el medio, tirando a abajo",
     "Fíjate si te cotizaron solo la lipo o también la lipotransferencia, y si trae faja y masajes: en muchos lugares los masajes de la recuperación se pagan aparte. Aquí van la faja, los masajes, la póliza y la bomba de dolor."),
    ("Abdominoplastia", "Se cotiza", "13,5 a 16 millones", "Depende de cada cotización · el dato es de la abdominoplastia sola",
     "Tu cotización es por escrito, en quirófano y con póliza de complicaciones. Así puedes comparar punto por punto: pregunta en el otro lugar si su precio trae quirófano con anestesia, póliza, bomba de dolor y faja."),
    ("Criolipólisis", "$800.000 por zona", "699.000 a 912.500 por zona o copa", "En el medio (por debajo si el abdomen completo cuenta como una zona)",
     "¡Es normal comparar! Pregunta si ese precio es por zona o por copa: a veces una zona necesita 2 copas o más. En noon el precio es por sesión por zona, y siempre empieza con una valoración médica para saber si es para ti."),
    ("Rinoplastia", "Se cotiza", "11 a 14 millones", "Depende de cada cotización",
     "Te la cotizamos por escrito en tu valoración, en quirófano y con póliza de complicaciones. Así puedes comparar punto por punto."),
]
TRAMPAS = [
    ("“Desde” = el caso más sencillo", "Casi ningún precio publicado es cerrado: sube en la valoración."),
    ("Implantes por fuera", "En mastopexia muchas veces no van incluidos. Solo los implantes valen de 3,5 a 5,5 millones."),
    ("Póliza por fuera", "Algunos lo dicen claro (“no incluye póliza”) y la mayoría ni la menciona."),
    ("Faja, brasier y masajes por fuera", "Los masajes de la recuperación pueden sumar de 0,8 a 2,3 millones más."),
    ("“Solo honorarios”", "Muchos precios son solo del cirujano, sin quirófano ni anestesia."),
    ("Precio de la consulta", "Los “desde $140.000” que salen en internet son la consulta, no la cirugía."),
]
NO_PROMETER = [  # solo lo que va escrito en la cotización está incluido
    ("Exámenes antes de la cirugía", "Solo van si aparecen escritos en la cotización."),
    ("Medicamentos para la casa", "Solo van si aparecen escritos en la cotización (el quirófano trae los básicos del procedimiento)."),
    ("Cualquier cosa que no esté escrita", "Si no está en la cotización, no lo prometas: pregunta primero."),
]


# ---------------------------------------------------------------- CIERRE DE FIN DE AÑO (plan del Comercializador Digital, 4-nov-2026)
# Hasta el 15 de enero, para las pacientes que YA tienen cotización. No reemplaza Seguimiento: es su versión de cierre.
# Cada dato sale de los términos (puntos 2 a 6), de /promos, de /formas-de-pago y del cotizador:
#   el abono de $1.000.000 separa la fecha · el saldo se paga "según tu plan por escrito", completo antes de la cirugía (punto 3)
#   si desiste, se retiene RETENCION de TODO lo pagado (punto 4.2): de $1.000.000 se devuelven $800.000
#   la valoración ($200.000) no se abona ni se devuelve · la cotización vence a los VIGENCIA_MESES meses (cotizador)
#   el 15 de enero solo se nombra en las 4 promos con precio (aumento, las dos mastopexias, lipo y lipotransferencia).
# Welli: hoy NO está activa, así que no se ofrece; cuando se active, va siempre con su aviso legal.
# Sin porcentajes, sin "últimos cupos" inventados, sin resultados y sin "el mejor".
from datos import VALORACION, RETENCION
from cotizador import VIGENCIA_MESES

TU_COTIZACION = "https://noon.clinic/tu-cotizacion"
VIENES_DICIEMBRE = "https://noon.clinic/promos/vienes-en-diciembre"
ABONO = 1000000  # separa la fecha de la cirugía (parada "¡Abona!" del camino del paciente)
CIERRE_FIN = "2027-01-15"  # = FECHA_LIMITE; la página calcula sola cuántas semanas faltan
WELLI_AVISO = "Financiación con Welli. noon no presta dinero. Sujeto a estudio y aprobación de la entidad."


def _pesos(n):
    return "$" + format(int(round(n)), ",").replace(",", ".")


_DEVUELVE = 1 - int(RETENCION.rstrip("%")) / 100  # lo que se devuelve de cada peso pagado si desiste (términos 4.2)
_AB = _pesos(ABONO)
_EJ_TOTAL = 26800000  # ejemplo de plan de pagos: la cotización del medio (plan comercial, jugada 4)
_EJ_PARTE = (_EJ_TOTAL - ABONO) // 2
_EJ_PAGADO = ABONO + _EJ_PARTE  # ya abonó y pagó la primera parte

CIERRE = {
    "fin": CIERRE_FIN,
    "secuencia": [  # (cuándo · qué, qué haces)
        ("Día 1 · Llega la cotización", "Le mandas la página de su cotización y le ofreces explicársela en 5 minutos."),
        ("Día 3 · La duda", "Le preguntas qué la frena: el valor, la recuperación o la fecha."),
        ("Día 7 · La plata y la llamada", "Le cuentas que el saldo se puede pagar por partes. Si no ha respondido nada, ese día la llama la Dra. Valeria."),
        ("Día 15 · Comparar", "Le ofreces revisar la otra cotización, punto por punto."),
        ("Última semana", "Promo: las últimas fechas antes del 15 de enero. Las demás: 7 días antes de que se venza su cotización."),
    ],
    "reglas": [
        ("Fechas reales, siempre", "Las fechas de quirófano te las da la Dra. Valeria. Nunca ofrezcas una que ella no te dio."),
        ("El 15 de enero, solo en promo", "Solo va en las 4 promos con precio: aumento de senos, las dos mastopexias y la lipo con lipotransferencia. "
         "A las demás les dices “tu cotización vence el …” (vence a los %d meses de hecha)." % VIGENCIA_MESES),
        ("Tres sin respuesta, espera", "Si no contestó el día 1, ni el 3, ni el 7, no le escribas más hasta el mensaje de la última semana. Y ese es el último."),
        ("Antes de enviar, mira su cotización", "Si es de Bogotá, quita “con anestesia” (allá la consulta preanestésica va aparte). Si no trae bomba de dolor, quítala de la frase."),
    ],
    "mensajes": [  # (título, [(etiqueta, texto)], mensaje, ojo, enlace interno)
        ("Día 1 · Llega la cotización",
         [("Para qué", "Que tenga a la mano qué paga y cómo separar su fecha. Sirve también para retomar a las que ya tienen cotización.")],
         "¡Hola, {nombre}! Te habla {asesora}, de noon Clinic 🤍 Para que lo tengas todo a la mano, te dejo en una sola página lo que ya va en tu cotización de {cirugía} y cómo separar tu fecha: " + TU_COTIZACION + "\n"
         "Tu precio ya trae el cirujano, el quirófano con anestesia, la póliza de complicaciones y la bomba de dolor. Si quieres, te la explico en una llamada de 5 minutos. ¿Te queda mejor hoy o mañana?",
         "Si es de Bogotá, quita “con anestesia”. Si su cotización no trae bomba de dolor, quítala de la frase.", None),
        ("Día 3 · La duda",
         [("Para qué", "Encontrar qué la frena.")],
         "Hola, {nombre}, ¿cómo vas? Cuéntame qué es lo que más te hace dudar: el valor, la recuperación o la fecha. Me dices cuál y te mando justo eso. "
         "Y si es la fecha, te consigo dos opciones de quirófano para que las mires con calma. ¿Te parece?", "", None),
        ("Día 7 · La plata (y la llamada)",
         [("Para qué", "Que vea que no necesita tener toda la plata hoy.")],
         "{nombre}, te cuento cómo funciona el pago, por si te sirve: separas tu fecha con " + _AB + " y el resto lo puedes pagar por partes, con un plan por escrito. "
         "Lo único es que tiene que quedar completo antes de tu cirugía. Y desde el día que abonas, tu precio se respeta. ¿Te armo un plan de pagos con una fecha tentativa?",
         "Si no ha respondido nada desde el día 1, avísale hoy a la Dra. Valeria para la llamada de 5 minutos. En las promos, el precio se respeta si la cirugía es antes del 15 de enero.", None),
        ("Día 15 · Comparar",
         [("Para qué", "Que compare con todo sumado y por escrito.")],
         "{nombre}, si estás comparando con otra cotización, me parece muy bien: es lo que haría yo. Mándamela (tapa tu nombre y tu cédula) y te digo punto por punto qué trae cada una: "
         "quirófano con anestesia, póliza, bomba de dolor, prenda y si el cirujano es plástico con registro en ReTHUS. ¿Te la reviso hoy?",
         "", ("#comparar", "Antes de responder, mira Si comparan precios")),
        ("Última semana · Cirugías de promo",
         [("Cuándo", "Apenas la Dra. Valeria te diga que para su cirugía ya quedan las últimas fechas antes del 15 de enero (a más tardar, la semana del 28 de diciembre).")],
         "Hola, {nombre}. Te escribo porque el precio de fin de año es para cirugías hechas antes del 15 de enero, y para la tuya ya solo me quedan estas fechas de quirófano: "
         "el {fecha 1} y el {fecha 2}. Con " + _AB + " separas la que prefieras. ¿Te reservo una?",
         "Solo si de verdad son las últimas. Si no, no lo mandes.", None),
        ("Última semana · Las demás cirugías",
         [("Cuándo", "7 días antes de que se venza su cotización (vence a los %d meses de hecha)." % VIGENCIA_MESES)],
         "Hola, {nombre}. Te aviso con tiempo: tu cotización vence el {fecha}. Después toca hacerla de nuevo y el valor puede cambiar. "
         "Si separas antes con " + _AB + ", tu precio se respeta. ¿Te ayudo a separar esta semana?", "", None),
    ],
    "llamada": {
        "quien": "La hace la Dra. Valeria, el día 7, a la que no ha respondido. Una llamada de la médica pesa más que otro mensaje.",
        "pasos": [  # (lo que dice, nota para ella)
            ("Hola, {nombre}, habla la Dra. Valeria Enciso, de noon. ¿Tienes 5 minuticos? Te llamo por tu cotización de {cirugía}.", ""),
            ("¿Te quedó alguna duda médica de lo que te explicó el doctor en la valoración?", ""),
            ("Y cuéntame, ¿qué es lo que más te hace dudar: el valor, la recuperación o la fecha?",
             "Escucha. Si es la plata: el saldo por partes. Si es la recuperación: cómo son los primeros días y, si su cotización la trae, la bomba de dolor. Si es la fecha: dos fechas."),
            ("Tengo libres el {fecha 1} y el {fecha 2}. ¿Cuál te queda mejor?", ""),
            ("Si quieres, te aparto una por 48 horas mientras lo hablas en tu casa. ¿Te la aparto?",
             "Apartar sin abono solo lo hace la Dra. Valeria. Si a las 48 horas no ha abonado, la fecha se libera."),
        ],
        "si_no": "“Tranquila, ¿te parece si te escribo en un mes?”",
        "regla": "Nunca resultados, nunca presión.",
    },
    "fechas": {
        "msj": "{nombre}, para tu {cirugía} tengo libres el {fecha 1} y el {fecha 2}. ¿Cuál te queda mejor?",
        "nota": "Dos fechas concretas, no “¿cuándo puedes?”: así es más fácil decidir. Solo fechas reales que te dé la Dra. Valeria.",
    },
    "dudas": [  # (lo que dice la paciente, respuesta para copiar, [lo que tú debes saber], enlace interno)
        ("“No tengo toda la plata”",
         "Te entiendo, {nombre}, es mucha plata para pagarla de una. Por eso separas tu fecha con " + _AB + " y el resto lo vas pagando por partes, con un plan por escrito, "
         "hasta completarlo antes de tu cirugía. Si cuentas con tu prima de diciembre, puede ser una de las partes. ¿Te armo el plan con tu fecha?",
         ["Así se ve un plan: cirugía de %s el 12 de enero → %s hoy · %s el 18 de diciembre · %s el 4 de enero." % (_pesos(_EJ_TOTAL), _AB, _pesos(_EJ_PARTE), _pesos(_EJ_PARTE)),
          "La fecha límite del saldo la indica noon al reservar. Sin el pago completo no hay cirugía.",
          "La prima se paga a más tardar el 20 de diciembre. Este año el 20 cae domingo: muchas empresas la pagan el viernes 18.",
          "Si se arrepiente: de %s abonado se le devuelven %s. Si ya pagó partes, la retención es sobre todo lo pagado: de %s se le devuelven %s. La valoración (%s) no se devuelve."
          % (_AB, _pesos(ABONO * _DEVUELVE), _pesos(_EJ_PAGADO), _pesos(_EJ_PAGADO * _DEVUELVE), VALORACION),
          "Financiación con Welli: todavía no está activa, así que no la ofrezcas. Cuando lo esté, siempre va con su aviso: “" + WELLI_AVISO + "”"],
         None),
        ("“Lo voy a pensar con mi pareja”",
         "¡Claro que sí! Me parece muy bien que lo hablen juntos. Te dejo esta página para que la vean con calma: " + TU_COTIZACION + "\n"
         "Ahí está qué trae tu precio y cómo se separa la fecha. Si les queda alguna duda, me escriben y se la resuelvo. ¿Te parece?",
         [], None),
        ("“En otro lado me sale más barato”",
         "Te entiendo, y qué bueno que compares. Mándame la otra cotización (tapa tu nombre y tu cédula) y te digo punto por punto qué trae cada una, "
         "porque muchas veces la diferencia está en lo que no sale en el precio. ¿Te la reviso?",
         ["Nunca nombres ni critiques a otra clínica."],
         ("#comparar", "Mira Si comparan precios: lo típico afuera, por cirugía, y qué responder")),
        ("“Vivo afuera” o “vengo en diciembre”",
         "¡Qué bueno que nos escribas desde allá! Puedes hacerte la valoración virtual antes de viajar y, si el cirujano te la indica, operarte cuando llegues. "
         "Aquí te explico cómo funciona: " + VIENES_DICIEMBRE + "\n¿En qué fechas vienes a Medellín?",
         ["Lo primero es saber en qué fechas llega: con eso se arma todo.", "Si la valoración es virtual, la Dra. Valeria le pide las fotos.",
          "Si su cirugía es de promo, tiene que hacerse antes del 15 de enero."],
         None),
    ],
    "no_decir": [  # (lo que no se dice, qué decir en cambio)
        ("“Últimos cupos” o “quedan pocas fechas”", "Solo si la Dra. Valeria te lo confirmó. Si no, di las fechas que hay: “tengo libres el … y el …”."),
        ("Resultados: “vas a quedar…”, “garantizado”, “sin riesgo”", "Mejor: “el doctor te explica qué se puede lograr en tu caso”. Toda cirugía tiene riesgos."),
        ("“El mejor cirujano” o “los mejores quirófanos”", "Mejor lo que se puede comprobar: cirujano plástico con registro en ReTHUS y quirófano habilitado, nunca un consultorio."),
        ("Descuentos que no existen", "Ni de Black Friday ni “solo por hoy”. Los precios son los de la lista, y por escrito."),
        ("Cuotas, crédito o “ya te aprobaron”", "Lo que hay hoy es el saldo por partes, con un plan por escrito. Welli todavía no está activa."),
    ],
    "rapidas_nota": "Guárdalas una vez en WhatsApp Business (Herramientas para la empresa › Respuestas rápidas). En el atajo escribes la palabra, por ejemplo tucotizacion. "
                    "Después, en cualquier chat escribes / y eliges. Antes de enviar, cambia lo que va entre llaves.",
    "rapidas": [  # (atajo, cuándo, mensaje)
        ("/tucotizacion", "Cuando le llega la cotización o la retomas",
         "Te dejo en una sola página lo que ya va en tu cotización y cómo separar tu fecha: " + TU_COTIZACION + "\n¿Te la explico en una llamada de 5 minutos?"),
        ("/fechas", "Cuando ya está mirando fechas",
         "Para tu cirugía tengo libres el {fecha 1} y el {fecha 2}. ¿Cuál te queda mejor?"),
        ("/partes", "Cuando dice que no le alcanza",
         "Separas tu fecha con " + _AB + " y el resto lo vas pagando por partes, con un plan por escrito, hasta completarlo antes de tu cirugía. ¿Te armo el plan con tu fecha?"),
        ("/comparartuya", "Cuando está comparando",
         "Mándame la otra cotización (tapa tu nombre y tu cédula) y te digo punto por punto qué trae cada una. ¿Te la reviso?"),
        ("/vence", "Cirugías que no son de promo, 7 días antes de que venza",
         "Te cuento que tu cotización vence el {fecha}. Si separas antes con " + _AB + ", tu precio se respeta. ¿Te ayudo a separar esta semana?"),
        ("/diciembre", "Vive afuera o viene en diciembre",
         "Si vienes a Medellín en diciembre, tu valoración puede ser virtual desde allá y, si el cirujano te la indica, la cirugía cuando llegues: " + VIENES_DICIEMBRE + "\n¿En qué fechas llegas?"),
    ],
}


def generar():
    procs = ([_proc(c, "cx", {k: n for k, n, d, f in CATEGORIAS_CX}) for c in _cirugias()]
             + [_proc(t, "me", {k: n for k, n, d, f in CATEGORIAS_ME}) for t in TRATAMIENTOS if not t.get("nueva")])
    for i, p in enumerate(procs):
        p["img"] = _imagen(p["slug"], i)
    datos = {"procs": procs, "cats_cx": [n for k, n, d, f in CATEGORIAS_CX], "cats_me": [n for k, n, d, f in CATEGORIAS_ME],
             "doctores": DOCTORES, "disp": DISPONIBILIDAD, "objeciones": OBJECIONES, "reglas": REGLAS, "pasos": PASOS,
             "precio": PRECIO, "lista_precios": [(p["nombre"], it, v, p["slug"], p["tipo"]) for p in procs for it, v in p["precios"]],
             "otros_precios": OTROS_PRECIOS, "video": VIDEO,
             "inter_reglas": INTERNACIONAL_REGLAS, "inter": INTERNACIONAL,
             "camino": CAMINO, "sim": SIMULADOR, "wa": CHAT_WA, "conf_ej": CONF_EJEMPLO, "confirmacion": CONFIRMACION, "reglas_oro": REGLAS_ORO, "quiz": QUIZ, "ciudades": CIUDADES,
             "seg_reglas": SEGUIMIENTO_REGLAS, "seg": SEGUIMIENTO, "seg_obj": SEGUIMIENTO_OBJ, "seg_me": SEGUIMIENTO_ESTETICA, "seg_sin": SEGUIMIENTO_SIN_CITA,
             "comparar": COMPARAR, "trampas": TRAMPAS, "no_prometer": NO_PROMETER, "cierre": CIERRE}
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.replace("%%DATOS%%", js).replace("%%HASH%%", hashlib.sha256(CODIGO.encode()).hexdigest())
    with open(os.path.join(AQUI, "capacitacion-comercial.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(procs)


with open(os.path.join(AQUI, "_capacitacion_plantilla.html"), encoding="utf-8") as _f:
    PLANTILLA = _f.read()

if __name__ == "__main__":
    print("Capacitación comercial: %d procedimientos." % generar())
