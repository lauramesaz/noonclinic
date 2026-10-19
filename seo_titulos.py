# -*- coding: utf-8 -*-
# Títulos y descripciones para Google (lo que sale en azul y en gris en los resultados). Escritos el 19-oct-2026 con las
# búsquedas reales de Search Console y revisados (largo, sin precios, sin promesas, cifras solo de la ficha).
# build.py los usa en lugar del nombre y la frase corta de cada página. El título de cada página (menos el inicio)
# termina solo en " · noon Clinic": aquí máximo 47 caracteres; descripción de 135 a 158.
# Archivo: (título, descripción)  ·  la búsqueda que debe ganar va en el comentario.
SEO = {
    # clínica de cirugía plástica y medicina estética en Medellín
    'index.html': ('Cirugía plástica y medicina estética en Medellín · noon Clinic',
                    'Clínica de cirugía plástica y medicina estética en Medellín: rostro, senos, contorno corporal, inyectables y piel. Valoración presencial con el especialista.'),
    # cirugía plástica en Medellín
    'cirugia-plastica.html': ('Cirugía plástica en Medellín: rostro y cuerpo',
                               'Cirugía plástica en Medellín de rostro, senos y contorno corporal: rinoplastia, mamoplastia, lipo, abdominoplastia y más, siempre en quirófano habilitado.'),
    # medicina estética en Medellín
    'medicina-estetica.html': ('Medicina estética en Medellín, sin cirugía',
                                'Bótox, ácido hialurónico, bioestimuladores, láser, HIFU, peelings y sueroterapia en Medellín. Cada plan parte de una valoración con la médica estética.'),
    # cirujano plástico en Medellín
    'especialistas.html': ('Cirujano plástico y médica estética en Medellín',
                            'Conoce al Dr. Fernando Ruiz, cirujano plástico, y a la Dra. Valeria Enciso, médica estética, del equipo noon Clinic en Medellín. La valoración es presencial.'),
    # seguridad en cirugía plástica
    'seguridad.html': ('Seguridad en cirugía plástica en Medellín',
                        'En Medellín operamos solo en salas de cirugía habilitadas, nunca en consultorio, con valoración presencial, exámenes previos y consentimiento informado.'),
    # proceso de una cirugía plástica
    'tu-proceso.html': ('Proceso de una cirugía plástica en Medellín',
                         'Así es el proceso en noon Clinic: valoración presencial en Medellín, plan y presupuesto por escrito, exámenes, abono para tu fecha y controles hasta el alta.'),
    # preguntas frecuentes sobre cirugía plástica
    'preguntas-frecuentes.html': ('Preguntas frecuentes sobre cirugía plástica',
                                   'Lo que más nos preguntan antes de una cirugía plástica o un tratamiento estético en Medellín: valoración, exámenes, recuperación, requisitos y pagos.'),
    # formas de pago cirugía plástica
    'formas-de-pago.html': ('Formas de pago de tu cirugía plástica',
                             'Después de la valoración en Medellín recibes un presupuesto por escrito. Separas la fecha de tu cirugía con un abono y pagas el saldo antes de operarte.'),
    # operarse en Medellín desde otra ciudad
    'otra-ciudad.html': ('Operarte en Medellín si vienes de otra ciudad',
                          '¿Vives en otra ciudad o en el exterior? Organizamos valoración, procedimiento y controles en un solo viaje a Medellín. Si es cirugía, calcula 1 a 3 semanas.'),
    # blefaroplastia en Medellín
    'blefaroplastia.html': ('Blefaroplastia en Medellín: cirugía de párpados',
                             'Cirugía de párpados superiores, inferiores o ambos para piel sobrante y bolsas, con incisiones en los pliegues del párpado. Valoración presencial en Medellín.'),
    # rinoplastia en Medellín
    'rinoplastia.html': ('Rinoplastia en Medellín: cirugía de nariz',
                          'Cambia la forma, el tamaño o la proporción de la nariz y, si el tabique te dificulta respirar, puede sumar septoplastia. Te valora el cirujano en Medellín.'),
    # lifting facial en Medellín
    'lifting-facial.html': ('Lifting facial en Medellín: rostro y cuello',
                             'Cirugía para la flacidez de mejillas, mandíbula y cuello: reposiciona las capas profundas y retira la piel sobrante. Valoración presencial en Medellín.'),
    # bichectomía en Medellín
    'bichectomia.html': ('Bichectomía en Medellín: afinar las mejillas',
                          'Retira parte de las bolsas de Bichat para afinar las mejillas, por dentro de la boca y sin cicatriz visible. No es para todos: se valora en Medellín.'),
    # mentoplastia en Medellín
    'mentoplastia.html': ('Mentoplastia en Medellín: cirugía de mentón',
                           'Cirugía del mentón para proyectarlo o reducirlo, con implante o remodelando el hueso. Suele combinarse con rinoplastia. Valoración presencial en Medellín.'),
    # otoplastia en Medellín
    'otoplastia.html': ('Otoplastia en Medellín: cirugía de orejas',
                         'Acerca las orejas a la cabeza o corrige su forma, con la cicatriz detrás de la oreja. Para adultos y niños desde unos 6 años. Primero, valoración en Medellín.'),
    # lipopapada en Medellín
    'lipopapada.html': ('Lipopapada en Medellín: liposucción de papada',
                         'Liposucción de la papada por incisiones mínimas bajo el mentón y detrás de las orejas, para definir el cuello si la piel es elástica. Se valora en Medellín.'),
    # aumento de senos en Medellín
    'mamoplastia-de-aumento.html': ('Aumento de senos en Medellín: mamoplastia',
                                     'Mamoplastia de aumento con implantes para dar volumen y mejorar la forma. Tamaño, perfil y ubicación del implante los decides con el cirujano en Medellín.'),
    # mastopexia en Medellín
    'mastopexia.html': ('Mastopexia en Medellín: levantamiento de senos',
                         'Levanta el seno caído: retira piel sobrante, da nueva forma al tejido y sube areola y pezón, con o sin implantes. Valoración con el cirujano en Medellín.'),
    # reducción de senos en Medellín
    'mamoplastia-de-reduccion.html': ('Reducción de senos en Medellín: mamoplastia',
                                       'Mamoplastia de reducción: retira tejido, grasa y piel para un busto más liviano; suele aliviar el dolor de espalda y cuello. Agenda tu valoración en Medellín.'),
    # recambio de implantes en Medellín
    'recambio-de-implantes.html': ('Recambio o retiro de implantes en Medellín',
                                    'Cambia tus implantes, ajusta su tamaño o retíralos (explantación), con o sin levantamiento; la contractura capsular puede tratarse ahí mismo. En Medellín.'),
    # ginecomastia en Medellín
    'ginecomastia.html': ('Ginecomastia en Medellín: pecho masculino',
                           'Cirugía para hombres que retira el exceso de tejido mamario y grasa del pecho, con liposucción, resección de la glándula o ambas. Te valoramos en Medellín.'),
    # lipo en Medellín
    'liposuccion.html': ('Lipo en Medellín: liposucción y lipoescultura',
                          'Retira la grasa localizada de abdomen, cintura, espalda, brazos o muslos para definir el contorno. Moldea; no es para bajar de peso. Valoración en Medellín.'),
    # lipotransferencia glútea en Medellín
    'lipotransferencia-glutea.html': ('Lipotransferencia glútea en Medellín (BBL)',
                                       'Transferencia de grasa a glúteos: se toma grasa de abdomen o espalda con lipo y, purificada, se pasa a los glúteos para dar volumen. Te valoramos en Medellín.'),
    # abdominoplastia en Medellín
    'abdominoplastia.html': ('Abdominoplastia en Medellín, sola o con lipo',
                              'Retira piel y grasa sobrante del abdomen y repara la diástasis si hace falta. Suele hacerse con lipo (lipoabdominoplastia). Lo define el cirujano en Medellín.'),
    # mini abdominoplastia en Medellín
    'mini-abdominoplastia.html': ('Mini abdominoplastia en Medellín: abdomen bajo',
                                   'Versión corta de la abdominoplastia para piel y grasa sobrante solo bajo el ombligo, con una cicatriz más pequeña. Mini o completa: se define en Medellín.'),
    # braquioplastia en Medellín
    'braquioplastia.html': ('Braquioplastia en Medellín: cirugía de brazos',
                             'Retira la piel y la grasa sobrante de la cara interna del brazo, donde queda la cicatriz. Es frecuente tras bajar mucho de peso. Valoración en Medellín.'),
    # lifting de muslos en Medellín
    'lifting-de-muslos.html': ('Lifting de muslos en Medellín: piel sobrante',
                                'Retira la piel y la grasa sobrante de la cara interna de los muslos y levanta los tejidos, sobre todo tras bajar mucho de peso. Te valoramos en Medellín.'),
    # cirugía post bariátrica en Medellín
    'cirugia-post-bariatrica.html': ('Cirugía post bariátrica en Medellín: body lift',
                                      'Body lift y cirugías para retirar la piel que sobra tras una bariátrica o una gran pérdida de peso, por etapas según tu salud. Valoración en Medellín.'),
    # mommy makeover en Medellín
    'mommy-makeover.html': ('Mommy makeover en Medellín: senos y abdomen',
                             'Combina mastopexia o aumento de senos con abdominoplastia y lipo tras los embarazos, todo junto solo si tu salud lo permite. Se planea contigo en Medellín.'),
    # labioplastia en Medellín
    'labioplastia.html': ('Labioplastia en Medellín: cirugía íntima',
                           'Cirugía íntima que reduce o remodela los labios menores cuando causan roce, irritación o incomodidad. Es corta y discreta. Valoración presencial en Medellín.'),
    # bótox en Medellín
    'toxina-botulinica.html': ('Bótox en Medellín: toxina botulínica',
                                'Toxina botulínica para líneas de frente, entrecejo y patas de gallo, y para el bruxismo. Hace efecto en 3 a 7 días y dura 4 a 6 meses. Valoración en Medellín.'),
    # ácido hialurónico en Medellín
    'acido-hialuronico.html': ('Ácido hialurónico en Medellín: rellenos',
                                'Rellenos de ácido hialurónico en labios, ojeras, surcos, mentón y rinomodelación. Dura de 6 a 18 meses según la zona. Valoración médica en Medellín.'),
    # bioestimuladores de colágeno en Medellín
    'bioestimuladores.html': ('Bioestimuladores de colágeno en Medellín',
                               'Hidroxiapatita de calcio o ácido poli-L-láctico que estimulan tu colágeno y mejoran la firmeza de rostro y cuerpo de forma progresiva. Se valora en Medellín.'),
    # hilos tensores en Medellín
    'hilos-tensores.html': ('Hilos tensores en Medellín para la flacidez',
                             'Hilos reabsorbibles que reposicionan tejidos en mejillas, mandíbula y cuello. Para flacidez leve a moderada; no reemplazan un lifting. Se valora en Medellín.'),
    # skinboosters en Medellín
    'skinboosters.html': ('Skinboosters en Medellín: hidratación profunda',
                           'Microinyecciones de ácido hialurónico no reticulado que hidratan y mejoran textura y brillo en rostro, cuello, escote y manos. No dan volumen. En Medellín.'),
    # plasma rico en plaquetas en Medellín
    'plasma-rico-en-plaquetas.html': ('Plasma rico en plaquetas en Medellín (PRP)',
                                       'PRP de una pequeña muestra de tu sangre para mejorar textura y luminosidad de la piel y ayudar en algunos tipos de caída del cabello. Valoración en Medellín.'),
    # peeling químico en Medellín
    'peelings.html': ('Peeling químico en Medellín: manchas y acné',
                       'Peelings con ácidos de concentración médica para manchas, acné y sus marcas, poros y textura. Tipo y profundidad según tu piel. Te valoramos en Medellín.'),
    # microagujas en Medellín
    'microagujas.html': ('Microagujas en Medellín: cicatrices y poros',
                          'Microagujas o microneedling: microperforaciones controladas que estimulan colágeno para cicatrices de acné, poros dilatados y textura. Valoración en Medellín.'),
    # limpieza facial profunda en Medellín
    'limpieza-facial-medica.html': ('Limpieza facial profunda en Medellín',
                                     'Limpieza facial profunda con protocolo médico en Medellín: extracción, exfoliación y activos según tu piel, cada mes o antes de otro tratamiento.'),
    # tratamiento de manchas y melasma en Medellín
    'manchas-y-melasma.html': ('Tratamiento de manchas y melasma en Medellín',
                                'Primero se diagnostica la causa de tus manchas y luego se combinan despigmentantes, peelings, tecnologías y cuidado en casa. Valoración en Medellín.'),
    # láser facial en Medellín
    'laser.html': ('Láser facial en Medellín: manchas y textura',
                    'Láser en Medellín para manchas, daño solar, textura, poros, arrugas finas y pequeñas lesiones vasculares. El tipo y la intensidad dependen de tu piel.'),
    # depilación láser en Medellín
    'depilacion-laser.html': ('Depilación láser en Medellín: rostro y cuerpo',
                               'Reduce el vello de forma progresiva y duradera en rostro y cuerpo; útil con foliculitis o vellos encarnados. De 6 a 8 sesiones o más. Valoración en Medellín.'),
    # HIFU facial en Medellín
    'hifu.html': ('HIFU facial en Medellín: ultrasonido focalizado',
                   'Ultrasonido focalizado que estimula colágeno en capas profundas de la piel para un efecto tensor en rostro y cuello, sin agujas ni incisiones. En Medellín.'),
    # radiofrecuencia en Medellín
    'radiofrecuencia.html': ('Radiofrecuencia en Medellín: firmeza de la piel',
                              'Calor controlado en la dermis que estimula colágeno y mejora la firmeza de rostro y cuerpo, también tras el parto o una lipo si está indicada. En Medellín.'),
    # tratamientos corporales en Medellín
    'tratamientos-corporales.html': ('Tratamientos corporales en Medellín: celulitis',
                                      'Tecnologías, mesoterapia y drenajes para celulitis, flacidez y grasa localizada leve. No reemplazan una cirugía. Te valora la médica estética en Medellín.'),
    # sueroterapia en Medellín
    'sueroterapia.html': ('Sueroterapia en Medellín: sueros con vitaminas',
                           'Vitaminas, minerales y antioxidantes por vía intravenosa, en sueros que formula un médico según lo que necesitas. Con valoración médica previa en Medellín.'),
    # programa médico para bajar de peso en Medellín
    'manejo-medico-del-peso.html': ('Programa médico para bajar de peso en Medellín',
                                     'Programa para bajar de peso con valoración médica, exámenes, plan nutricional y medicamentos solo si el médico los indica. Seguimiento cercano en Medellín.'),
    # nutrición en Medellín
    'nutricion.html': ('Nutrición en Medellín: plan de alimentación',
                        'Plan de alimentación personalizado para cuidar tu salud, prepararte para una cirugía o mantener tus resultados. Acompañamiento nutricional en Medellín.'),
}
