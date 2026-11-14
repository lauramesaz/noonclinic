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
            "<p>Todo empieza con la valoración presencial con el Dr. Fernando Ruiz, cirujano plástico, en Medellín (Torre Médica El Tesoro 2, "
            "en El Poblado): te examina, te escucha "
            "y te dice si la cirugía tiene sentido para ti. Si sí, recibes el plan y el presupuesto por escrito, te haces los exámenes previos "
            "y separas tu fecha con un abono. La cirugía se hace en quirófano habilitado, nunca en consultorio, y los controles siguen hasta "
            'el alta (así es <a href="tu-proceso.html">tu proceso</a>). Si vives en otra ciudad, organizamos las fechas para que '
            '<a href="otra-ciudad.html">valoración, cirugía y controles te queden en un solo viaje</a>.</p>')


# Plan orgánico del 13-nov-2026 (Search Console 11-oct a 7-nov + lo que hacen los que salen arriba en Google): cada búsqueda con
# UNA página dueña y las 10 fichas en seguimiento con las preguntas que la competencia sí responde (duración y anestesia, cicatriz,
# incapacidad, precio). Todo sale de datos ya publicados en la ficha (datos, recuperación, "Todo sobre…") o de hechos.md. Sin precios.
# Detalle y "no tocar antes del 4-dic-2026": _agencia-seo/search-console.md, sección "Plan orgánico 13-nov-2026".
# Claves: "faq" y "todo" se suman al final · "ver_tambien" se suma a las líneas "ver también" · "campos" pisa campos de la ficha
# ("h1" = título grande de la página; "ancla" = texto del enlace que las guías le ponen a su ficha dueña).
_Q2 = "Siempre en salas de cirugía habilitadas (Q2), nunca en un consultorio."
_MASTOPEXIA_GENERAL = ("¿Quieres saber de qué depende el precio de una mastopexia en Colombia, o vienes de Bogotá u otra ciudad?",
                       "mastopexia.html", "Mastopexia en Medellín: precio y viaje")

EXTRA = {
    "mentoplastia": {
        "faq": [("¿Cuánto dura una mentoplastia y qué anestesia se usa?",
                 "Dura de 1 a 2 horas y se hace con anestesia general o con anestesia local y sedación, según tu caso. " + _Q2),
                ("¿La mentoplastia deja cicatriz visible?",
                 'Depende de por dónde entre el cirujano. Según el <a href="https://www.plasticsurgery.org/news/blog/plastic-surgery-options-for-patients-with-a-small-or-recessed-chin">'
                 "blog de la ASPS</a>, el implante puede colocarse por una incisión dentro de la boca o por una debajo del mentón. Cuál se usa en "
                 "tu caso te lo explica tu cirujano cuando te examina."),
                ("¿Cuándo se ve el resultado de una mentoplastia?",
                 "La primera semana hay inflamación y llevas un vendaje de soporte. En la segunda se suele volver a la rutina, y el resultado "
                 "termina de asentarse hacia los 3 meses.")],
        "todo": [_en_medellin("mentoplastia")],
    },
    "rinoplastia-y-mentoplastia": {
        "faq": [("¿La mentoplastia y la rinoplastia se pueden hacer al mismo tiempo?",
                 "Sí. Mentoplastia y rinoplastia pueden ir en un mismo tiempo quirúrgico, con anestesia general, cuando tu perfil necesita las dos "
                 "y tu salud lo permite. Si van juntas o en dos tiempos lo decide tu cirujano en la valoración presencial."),
                ("¿Cuánto dura la recuperación de la rinoplastia con mentoplastia?",
                 "Para la incapacidad calcula los 10 a 15 días de la rinoplastia; tu cirujano confirma si el mentón suma días. La primera semana "
                 "llevas férula nasal y vendaje de soporte en el mentón, y en la segunda vuelves a actividades suaves.")],
        "todo": [_en_medellin("rinoplastia y mentoplastia")],
        # el título grande decía "…y mentoplastia en Medellín" y Google la mostraba por "mentoplastia en medellín", que es de /mentoplastia
        "campos": {"h1": "Rinoplastia y mentoplastia juntas en <em>Medellín</em>"},
    },
    "lipotransferencia-glutea": {
        "faq": [("¿Cuánto cuesta la lipotransferencia glútea en Medellín?", _PRESUPUESTO),
                # las dos siguientes vienen de la guía /lipotransferencia-glutea-en-medellin, fusionada aquí el 13-nov-2026
                ("¿Qué pasa si no tengo suficiente grasa para transferir?",
                 "La indicación cambia: con poca grasa en otras zonas puede no alcanzar para la transferencia. Eso se evalúa examinándote en la "
                 "valoración presencial, con tus exámenes en la mano."),
                ("¿Cuánto dura la lipotransferencia glútea y qué anestesia se usa?",
                 "Dura entre 3 y 5 horas, con anestesia general. " + _Q2),
                ("¿Puedo hacerme la lipotransferencia glútea en Medellín si vivo en otra ciudad o fuera del país?",
                 "Sí. La valoración es presencial y, como guía, para una cirugía de contorno corporal se calculan de 2 a 3 semanas en Medellín; el "
                 'regreso lo autoriza tu cirujano en el control. Lo explicamos en <a href="otra-ciudad.html">operarte en Medellín si vienes de otra '
                 'ciudad</a> y, si vives en Estados Unidos, en <a href="cuantos-dias-quedarse-en-colombia-despues-de-una-cirugia-plastica.html">'
                 "cuántos días quedarse en Colombia después de una cirugía</a>.")],
        "todo": [_en_medellin("lipotransferencia glútea")],
    },
    "braquioplastia": {
        "faq": [("¿Cuánto cuesta la braquioplastia en Medellín?", _PRESUPUESTO),
                ("¿Cuántos días de incapacidad necesito para una braquioplastia?",
                 "Aproximadamente 2 semanas. Las semanas 1 y 2 llevas prenda de compresión en los brazos, entre la 3 y la 6 vuelves poco a poco "
                 "al ejercicio y el resultado final se ve hacia los 6 meses. Tu cirujano te da los tiempos exactos."),
                ("¿Cuánto dura la braquioplastia y qué anestesia se usa?",
                 "Dura de 2 a 3 horas, con anestesia general. " + _Q2)],
        "todo": [_en_medellin("braquioplastia")],
    },
    "ginecomastia": {
        "faq": [("¿Cuánto cuesta la cirugía de ginecomastia en Medellín?", _PRESUPUESTO)],
    },
    # 9-nov-2026: "mastopexia precio colombia" y "mastopexia bogota" se repartían entre con/sin implantes; la dueña es la general
    "mastopexia": {
        "faq": [("¿Cuánto cuesta una mastopexia en Colombia?", _PRESUPUESTO),
                ("¿Puedo operarme la mastopexia en Medellín si vivo en Bogotá?",
                 "Sí. La valoración es presencial en Medellín y, si la cirugía tiene sentido para ti, organizamos las fechas para que "
                 "valoración, cirugía y controles te queden en un solo viaje. Para una mastopexia calcula quedarte de 1 a 2 semanas; tu "
                 'cirujano te confirma el tiempo. Lo explicamos en <a href="operarte-en-medellin-desde-bogota-cali-o-barranquilla.html">'
                 "operarte en Medellín desde Bogotá, Cali o Barranquilla</a>.")],
        "todo": [_en_medellin("mastopexia")],
    },
    "mastopexia-con-implantes": {
        "ver_tambien": [_MASTOPEXIA_GENERAL],
    },
    "mastopexia-sin-implantes": {
        "faq": [("¿Cuánto cuesta la mastopexia sin implantes en Medellín?", _PRESUPUESTO),
                ("¿Cuántos días de incapacidad necesito para una mastopexia sin implantes?",
                 "Cuenta con una incapacidad aproximada de 2 a 3 semanas. La primera semana es de reposo relativo y cuidado de heridas; entre "
                 "la segunda y la cuarta vuelves poco a poco a tu rutina, sin esfuerzos.")],
        "todo": [_en_medellin("mastopexia sin implantes")],
        "ver_tambien": [_MASTOPEXIA_GENERAL],
    },
    "otoplastia": {
        "faq": [("¿Cuánto dura la otoplastia y qué anestesia se usa?",
                 "Dura de 1 a 2 horas y se hace con anestesia local y sedación o con anestesia general, según el caso. " + _Q2),
                ("¿Cuánto tiempo hay que usar la banda después de la otoplastia?",
                 "La primera semana llevas un vendaje en la cabeza, que no se retira por cuenta propia. De la semana 2 a la 6 usas una banda "
                 "para dormir. Tu cirujano te confirma los tiempos en los controles.")],
        "todo": [_en_medellin("otoplastia")],
    },
    "liposuccion": {
        "faq": [("¿Qué zonas se pueden tratar con una liposucción?",
                 "Abdomen, cintura, espalda, brazos, muslos y otras zonas con grasa localizada que no cede con dieta ni ejercicio. Cuando se "
                 'trabajan abdomen, cintura y espalda en la misma cirugía se habla de <a href="lipo-360.html">lipo 360</a>. Qué zonas van en tu '
                 "caso lo define tu cirujano en la valoración."),
                ("¿Cuánto dura una liposucción y qué anestesia se usa?",
                 "Entre 2 y 5 horas, según las zonas tratadas, con anestesia general o raquídea. " + _Q2)],
        "todo": [_en_medellin("liposucción")],
        # "liposucción medellín" se repartía entre 4 páginas: la dueña es esta ficha
        "campos": {"h1": "Liposucción en <em>Medellín</em>", "ancla": "Liposucción en Medellín"},
    },
    "abdominoplastia": {
        "faq": [("¿Dónde queda la cicatriz de la abdominoplastia?",
                 "Queda baja, cubierta por la ropa interior. Según la ASPS, es una incisión horizontal entre el vello púbico y el ombligo, y su "
                 "largo depende de cuánta piel sobra. La cicatriz madura a lo largo del primer año."),
                ("¿Cuántos días de incapacidad necesito para una abdominoplastia?",
                 "Aproximadamente de 2 a 3 semanas. La primera semana caminas ligeramente inclinada, con faja y reposo relativo; entre la "
                 "segunda y la cuarta vuelves poco a poco a tus actividades, y el ejercicio regresa entre el mes 1 y el 3, con autorización "
                 "de tu cirujano."),
                ("¿Qué diferencia hay entre abdominoplastia y lipoabdominoplastia?",
                 "La abdominoplastia retira la piel y la grasa que sobran en el abdomen y repara la diástasis cuando hace falta. Cuando se "
                 "combina con liposucción para definir la cintura, muchos la llaman lipoabdominoplastia. Si en tu caso van juntas lo decide tu "
                 "cirujano en la valoración presencial."),
                ("¿Cuánto cuesta una abdominoplastia en Medellín?",
                 _PRESUPUESTO + ' Lo que conviene revisar en una cotización está en <a href="abdominoplastia-en-medellin-que-debe-incluir-el-precio.html">'
                 "qué debe incluir el precio de una abdominoplastia</a>.")],
        "todo": [_en_medellin("abdominoplastia")],
    },
    "mamoplastia-de-aumento": {
        "faq": [("¿Cuánto dura la mamoplastia de aumento y qué anestesia se usa?",
                 "Dura entre 1,5 y 2 horas, con anestesia general, en salas de cirugía habilitadas (Q2), nunca en un consultorio. Sales con "
                 "brasier posquirúrgico y necesitas un acompañante adulto."),
                ("¿Cómo son las primeras semanas después del aumento de senos?",
                 "La primera semana es de reposo relativo, con tu primer control. Entre la segunda y la cuarta vuelves poco a poco a tu rutina, "
                 'y los implantes toman su forma entre el mes 3 y el 6. Lo contamos paso a paso en <a href="recuperacion-del-aumento-de-senos-que-esperar-las-primeras-semanas.html">'
                 "recuperación del aumento de senos: qué esperar las primeras semanas</a>."),
                ("¿Cuánto cuesta una mamoplastia de aumento en Medellín?",
                 _PRESUPUESTO + ' Lo que conviene preguntar antes de decidir está en <a href="aumento-de-senos-que-incluye-el-precio-y-que-preguntar.html">'
                 "aumento de senos: qué incluye el precio y qué preguntar</a>.")],
        "todo": [_en_medellin("mamoplastia de aumento")],
    },
    "nutricion": {
        "faq": [("¿La nutrición personalizada sirve si no me voy a operar?",
                 "Sí. El plan también sirve para cambiar hábitos o mantener tu peso, sin ninguna cirugía de por medio. Lo que cambia es el "
                 "objetivo, y eso se define en la primera consulta con la Dra. Valeria Enciso, en Medellín."),
                ("¿Cómo es un plan de alimentación personalizado en noon?",
                 "Es un plan hecho para ti, con un objetivo claro: mejorar tu salud, prepararte para una cirugía o mantener tus resultados. La "
                 "valoración y el plan los hace la Dra. Valeria Enciso en Medellín, en consultas de 45 minutos y con las sesiones que pida tu plan.")],
        # el primer bloque de "Todo sobre…" empieza nombrando cómo lo busca la gente: se suma "nutrición personalizada"
        "reemplazar": [("Mucha gente lo busca como consulta de nutrición, dieta personalizada o plan de alimentación.",
                        "Mucha gente lo busca como nutrición personalizada, consulta de nutrición, dieta personalizada o plan de alimentación.")],
        # la gente la busca como "nutrición personalizada medellín": el título grande ahora lo dice igual que el título de Google
        "campos": {"h1": "Nutrición personalizada en <em>Medellín</em>"},
    },
}
