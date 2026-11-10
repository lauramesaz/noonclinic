# -*- coding: utf-8 -*-
# noon Clinic · Test "¿Soy candidata?" de 1 minuto en fichas de medicina estética (ronda de ventas 2, 9-nov-2026).
# Molde: el test de /criolipolisis (landing_criolipolisis.py + assets/criolipolisis.js): misma mecánica (una pregunta a la vez,
# cada opción suma una "bandera", la bandera de mayor prioridad decide el resultado) y misma medición en Clarity
# (evento test_inicio, etiqueta test = resultado, evento test_resultado_<clave>).
# REGLAS:
#   · Cada pregunta y cada resultado sale SOLO de lo que la propia ficha ya dice (datos_noon.py: "ideal", "que_es", "datos",
#     "todo", "faq"). Si cambia la ficha, se revisa aquí.
#   · El resultado NUNCA diagnostica: orienta ("vale la pena que te valoremos" / "probablemente te sirva más X").
#   · Sin precios.
#   · "link" va sin .html (dirección limpia, como en el test de criolipólisis).
#   · El botón abre WhatsApp con la frase de la página y, detrás, las respuestas del test (para que la asesora no las vuelva a pedir).
# Formato de cada opción: [texto, bandera].  "prioridad": qué bandera manda si hay varias (la primera que aparezca).
# Resultado: "t" título, "d" texto, "link" opcional [archivo, texto del enlace].

_NOTA = "Es una orientación. La indicación final la da tu médica en la valoración."

TESTS = {
    # ------------------------------------------------------------ TOXINA BOTULÍNICA
    "toxina-botulinica": {
        "titulo": "¿Eres candidata a <em>toxina botulínica</em>?",
        "intro": "Cinco preguntas para orientarte antes de escribirnos.",
        "preguntas": [
            {"id": "busco", "c": "Busco mejorar", "p": "¿Qué te gustaría mejorar?", "o": [
                ["Líneas en frente, entrecejo o patas de gallo", "ok"],
                ["Bruxismo", "ok"],
                ["Sudoración excesiva en axilas o manos", "ok"],
                ["Surcos marcados, ojeras hundidas o falta de volumen", "volumen"],
                ["Piel que perdió firmeza o flacidez leve", "firmeza"],
                ["Piel que sobra en el párpado", "parpado"]]},
            {"id": "espero", "c": "Espero", "p": "¿Qué resultado esperas?", "o": [
                ["Verme descansada y conservar mi expresión", "ok"],
                ["Un cambio que me dure para siempre", "temporal"]]},
            {"id": "embarazo", "c": "Embarazo o lactancia", "p": "¿Estás embarazada, lactando o planeas un embarazo?", "o": [
                ["No", "ok"], ["Sí", "embarazo"]]},
            {"id": "salud", "c": "Salud", "p": "¿Alguna de estas te aplica?", "o": [
                ["Ninguna", "ok"],
                ["Tengo una enfermedad de nervios y músculos, o problemas para respirar, tragar o de sangrado", "medica"],
                ["Me operaron la cara o tengo un párpado caído", "medica"],
                ["Tengo menos de 18 años", "menor"]]},
            {"id": "antes", "c": "Toxina antes", "p": "¿Ya te habías aplicado toxina botulínica?", "o": [
                ["No, sería la primera vez", "ok"], ["Sí", "ok"]]},
        ],
        "prioridad": ["menor", "embarazo", "medica", "parpado", "volumen", "firmeza", "temporal"],
        "resultados": {
            "ok": {"t": "Vale la pena que te valoremos",
                   "d": "Por lo que cuentas, eso es lo que se trata con toxina botulínica. Si tu caso se trata con toxina, y cómo, lo define tu médica cuando te examina: revisa tus líneas de expresión y tu historia médica y arma contigo tu plan."},
            "temporal": {"t": "Vale la pena que te valoremos, con una claridad",
                         "d": "El efecto de la toxina es temporal: se ve en 3 a 7 días y dura de 4 a 6 meses. Cuando pasa, el músculo vuelve a moverse y las líneas se notan otra vez. Cuándo repetir lo defines con tu médica."},
            "volumen": {"t": "Probablemente te sirva más el ácido hialurónico",
                        "d": "La toxina trabaja sobre el músculo: sirve para las líneas que aparecen al gesticular. Si hay pérdida de volumen, surcos marcados u ojeras hundidas, se evalúa el ácido hialurónico. Si conviene uno, otro o una combinación, te lo decimos en la valoración.",
                        "link": ["acido-hialuronico", "Ver ácido hialurónico"]},
            "firmeza": {"t": "Probablemente te sirvan más los bioestimuladores",
                        "d": "La toxina trabaja sobre el músculo: sirve para las líneas que aparecen al gesticular. Si la piel perdió firmeza o hay flacidez leve, se miran los bioestimuladores o los hilos tensores. Si conviene uno, otro o una combinación, te lo decimos en la valoración.",
                        "link": ["bioestimuladores", "Ver bioestimuladores"]},
            "parpado": {"t": "Probablemente lo tuyo sea una blefaroplastia",
                        "d": "Si lo que pesa es la piel que sobra en el párpado, lo que se evalúa es la blefaroplastia, que ya es una cirugía. En la valoración te decimos qué tiene sentido para ti.",
                        "link": ["blefaroplastia", "Ver blefaroplastia"]},
            "embarazo": {"t": "Cuéntaselo primero a tu médica",
                         "d": "La guía para pacientes de Botox® aprobada por la FDA dice que no se sabe si puede afectar al bebé ni si pasa a la leche materna. Cuéntaselo a tu médica antes de cualquier aplicación: con esa información define contigo qué hacer."},
            "medica": {"t": "Hay algo que tu médica debe saber antes",
                       "d": "Lo que marcaste es justo lo que hay que contarle a tu médica antes de cualquier aplicación. En la valoración revisa tu historia médica y te dice si la toxina botulínica es para ti."},
            "menor": {"t": "Por ahora no es para ti",
                      "d": "Para uso estético, la toxina botulínica no se recomienda en menores de 18 años. Si tienes dudas, escríbenos."},
        },
    },
    # ------------------------------------------------------------ ÁCIDO HIALURÓNICO
    "acido-hialuronico": {
        "titulo": "¿Eres candidata a <em>ácido hialurónico</em>?",
        "intro": "Cinco preguntas para orientarte antes de escribirnos.",
        "preguntas": [
            {"id": "busco", "c": "Busco mejorar", "p": "¿Qué te gustaría mejorar?", "o": [
                ["Labios finos o poco definidos", "ok"],
                ["Ojeras hundidas o surcos marcados", "ok"],
                ["Pérdida de volumen en el rostro", "ok"],
                ["Perfilar nariz, mentón o mandíbula sin cirugía", "ok"],
                ["Líneas de expresión en frente, entrecejo o patas de gallo", "toxina"],
                ["Piel opaca o deshidratada", "piel"],
                ["Falta de firmeza o flacidez leve", "firmeza"]]},
            {"id": "cambio", "c": "Tipo de cambio", "p": "¿Qué tipo de cambio buscas?", "o": [
                ["Uno temporal, sin cirugía", "ok"],
                ["Uno permanente, o cambiar la estructura de la nariz o el mentón", "cirugia"]]},
            {"id": "embarazo", "c": "Embarazo o lactancia", "p": "¿Estás embarazada o lactando?", "o": [
                ["No", "ok"], ["Sí", "embarazo"]]},
            {"id": "salud", "c": "Salud", "p": "¿Alguna de estas te aplica?", "o": [
                ["Ninguna", "ok"],
                ["Tengo la piel de la zona inflamada o con una infección", "esperar"],
                ["Tengo un trastorno de la coagulación, alergias graves o alergia a la lidocaína", "medica"],
                ["Tiendo a hacer queloides o cicatrices gruesas", "medica"]]},
            {"id": "antes", "c": "Rellenos o toxina antes", "p": "¿Ya te has aplicado rellenos o toxina botulínica?", "o": [
                ["No, sería la primera vez", "ok"], ["Sí", "ok"]]},
        ],
        "prioridad": ["embarazo", "esperar", "medica", "cirugia", "toxina", "piel", "firmeza"],
        "resultados": {
            "ok": {"t": "Vale la pena que te valoremos",
                   "d": "Por lo que cuentas, eso es lo que se trata con ácido hialurónico. Qué zonas tratar, con qué producto y en qué cantidad lo define tu médica estética cuando examina tu rostro en la valoración presencial. El efecto se ve de inmediato y dura de 6 a 18 meses según la zona."},
            "cirugia": {"t": "Probablemente lo tuyo sea una cirugía",
                        "d": "El ácido hialurónico es un relleno temporal: el cuerpo lo va absorbiendo. Cambiar la estructura de la nariz o del mentón, o tratar una flacidez marcada, es tema de cirugía (rinoplastia, mentoplastia o lifting facial), con el cirujano plástico. En la valoración te decimos qué tiene sentido para ti.",
                        "link": ["cirugia-plastica", "Ver cirugías"]},
            "toxina": {"t": "Probablemente te sirva más la toxina botulínica",
                       "d": "El ácido hialurónico rellena. Las líneas de expresión de frente, entrecejo o patas de gallo se tratan con toxina botulínica, que relaja el músculo en lugar de rellenar. En la valoración te decimos qué tiene sentido para ti.",
                       "link": ["toxina-botulinica", "Ver toxina botulínica"]},
            "piel": {"t": "Probablemente te sirvan más los skinboosters",
                     "d": "Para la piel opaca o deshidratada están los skinboosters: también son ácido hialurónico, pero se aplican para hidratar y mejorar la textura de la piel, no para rellenar. En la valoración te decimos qué tiene sentido para ti.",
                     "link": ["skinboosters", "Ver skinboosters"]},
            "firmeza": {"t": "Probablemente te sirvan más los bioestimuladores",
                        "d": "El ácido hialurónico rellena. Para la falta de firmeza o la flacidez leve se miran los bioestimuladores o los hilos tensores. En la valoración te decimos qué tiene sentido para ti.",
                        "link": ["bioestimuladores", "Ver bioestimuladores"]},
            "embarazo": {"t": "Puede que convenga esperar",
                         "d": "Según la FDA, no se conoce la seguridad de los rellenos durante el embarazo ni la lactancia. Cuéntalo en la valoración y tu médica te dice si conviene esperar."},
            "esperar": {"t": "Primero, que la piel esté bien",
                        "d": "Si la piel de la zona está inflamada o con una infección, el relleno se aplaza hasta que esté controlada. Escríbenos y lo organizamos para ese momento."},
            "medica": {"t": "Hay algo que tu médica debe saber antes",
                       "d": "Lo que marcaste es justo lo que hay que avisarle a tu médica antes del tratamiento. Con esa información te dice si el ácido hialurónico es para ti o si conviene esperar."},
        },
    },
    # ------------------------------------------------------------ MANCHAS Y MELASMA
    "manchas-y-melasma": {
        "titulo": "¿Te sirve un plan para <em>tus manchas</em>?",
        "intro": "Cinco preguntas para orientarte antes de escribirnos.",
        "preguntas": [
            {"id": "mancha", "c": "Mis manchas", "p": "¿Cómo son las manchas que te molestan?", "o": [
                ["Café o grisáceas, en mejillas, frente, mentón o encima del labio", "ok"],
                ["Manchas por el sol", "ok"],
                ["Marcas que me dejó el acné", "ok"],
                ["No sé qué tipo de mancha es", "ok"]]},
            {"id": "acne", "c": "Acné activo", "p": "¿Tienes acné activo en este momento?", "o": [
                ["No", "ok"], ["Sí", "acne"]]},
            {"id": "espero", "c": "Espero", "p": "¿Qué resultado esperas?", "o": [
                ["Un cambio progresivo, con constancia", "ok"],
                ["Que desaparezcan de una vez", "constancia"]]},
            {"id": "embarazo", "c": "Embarazo o lactancia", "p": "¿Estás embarazada, lactando o buscando un embarazo?", "o": [
                ["No", "ok"], ["Sí", "embarazo"]]},
            {"id": "sol", "c": "Protector solar diario", "p": "¿Usas protector solar todos los días?", "o": [
                ["Sí", "ok"], ["No siempre", "sol"]]},
        ],
        "prioridad": ["embarazo", "acne", "constancia", "sol"],
        "resultados": {
            "ok": {"t": "Vale la pena que te valoremos",
                   "d": "Las manchas tienen causas distintas y no se tratan igual; por eso no se diagnostican por fotos ni por WhatsApp. En la valoración tu médica estética revisa tus manchas de cerca, te dice de qué tipo son y recibes tu plan por escrito, con los cuidados en casa incluidos."},
            "embarazo": {"t": "Vale la pena que te valoremos, y cuéntaselo a tu médica",
                         "d": "Si estás embarazada, lactando o buscando un embarazo, el plan cambia: la Academia Estadounidense de Dermatología (AAD) pide no usar en el embarazo retinoides ni hidroquinona. Cuéntaselo a tu médica antes de empezar y ella ajusta el plan o te dice si es mejor esperar."},
            "acne": {"t": "Primero, controlar el acné",
                     "d": "Cuando la mancha viene del acné, primero hay que controlar el acné: así lo explica la AAD. En la valoración tu médica revisa tu piel y define qué va primero y qué después."},
            "constancia": {"t": "Vale la pena que te valoremos, con una claridad",
                           "d": "El resultado es progresivo: el melasma se controla con constancia y, según la AAD, puede ser persistente aun siguiendo el plan. Como puede volver con el sol o con cambios hormonales, el plan sigue con mantenimiento."},
            "sol": {"t": "Vale la pena que te valoremos, y el protector cuenta",
                    "d": "Lo que más ayuda a prevenir el melasma es protegerse del sol, y lo que haces en casa también es parte del tratamiento: protector solar todos los días, aunque esté nublado. En la valoración tu médica arma tu plan con esos cuidados incluidos."},
        },
    },
}
for _t in TESTS.values():
    _t["nota"] = _NOTA
