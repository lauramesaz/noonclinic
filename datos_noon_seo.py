# -*- coding: utf-8 -*-
# Refuerzos SEO del 27-oct-2026 a fichas que YA salen en Google (Search Console, usuario robot): las preguntas que la gente
# escribe ("…precio", "…en Medellín", "nutrición personalizada…") respondidas sin precios de noon y sin promesas.
# datos_noon.py los suma al final de "faq_nuevas" y "todo" de cada ficha (salen también en el JSON-LD de preguntas).
_PRESUPUESTO = ("Depende de tu caso: qué tanto hay que tratar, si se combina con otra cirugía, la anestesia y el tiempo de quirófano. "
                "Por eso no publicamos un precio fijo: después de la valoración presencial en Medellín recibes un presupuesto por escrito "
                "con todo lo que incluye. Te explicamos de qué depende en "
                '<a href="de-que-depende-el-precio-de-una-cirugia-plastica-en-colombia.html">precio de la cirugía plástica en Colombia</a>.')


def _en_medellin(cirugia):
    return ("Tu %s en Medellín, paso a paso" % cirugia,
            "<p>Todo empieza con la valoración presencial con el Dr. Fernando Ruiz, cirujano plástico, en Medellín: te examina, te escucha "
            "y te dice si la cirugía tiene sentido para ti. Si sí, recibes el plan y el presupuesto por escrito, te haces los exámenes previos "
            "y separas tu fecha con un abono. La cirugía se hace en quirófano habilitado, nunca en consultorio, y los controles siguen hasta "
            'el alta (así es <a href="tu-proceso.html">tu proceso</a>). Si vives en otra ciudad, organizamos las fechas para que '
            '<a href="otra-ciudad.html">valoración, cirugía y controles te queden en un solo viaje</a>.</p>')


EXTRA = {
    "lipotransferencia-glutea": {
        "faq": [("¿Cuánto cuesta la lipotransferencia glútea en Medellín?", _PRESUPUESTO)],
        "todo": [_en_medellin("lipotransferencia glútea")],
    },
    "braquioplastia": {
        "faq": [("¿Cuánto cuesta la braquioplastia en Medellín?", _PRESUPUESTO)],
        "todo": [_en_medellin("braquioplastia")],
    },
    "ginecomastia": {
        "faq": [("¿Cuánto cuesta la cirugía de ginecomastia en Medellín?", _PRESUPUESTO)],
    },
    "mastopexia-sin-implantes": {
        "faq": [("¿Cuánto cuesta la mastopexia sin implantes en Medellín?", _PRESUPUESTO)],
    },
    "nutricion": {
        "faq": [("¿La nutrición personalizada sirve si no me voy a operar?",
                 "Sí. El plan también sirve para cambiar hábitos o mantener tu peso, sin ninguna cirugía de por medio. Lo que cambia es el "
                 "objetivo, y eso se define en la primera consulta con la Dra. Valeria Enciso, en Medellín.")],
        # el primer bloque de "Todo sobre…" empieza nombrando cómo lo busca la gente: se suma "nutrición personalizada"
        "reemplazar": [("Mucha gente lo busca como consulta de nutrición, dieta personalizada o plan de alimentación.",
                        "Mucha gente lo busca como nutrición personalizada, consulta de nutrición, dieta personalizada o plan de alimentación.")],
    },
}
