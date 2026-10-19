# -*- coding: utf-8 -*-
# noon Clinic · página INTERNA "Cotizador de cirugía" (código de acceso, no indexada, sin enlace desde la web).
# Se genera sola al correr build.py. Tarifas de quirófano en _cotizador/tarifas-q2-2026.json (sacadas del PDF de Q2 Sur).
import os, json

AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGO = "111"
CORREO = "lauramesazuluaga@gmail.com"  # aquí llega cada cotización con todo discriminado y el PDF adjunto
ENVIO = "https://noon-cotizador-correo.vercel.app/api/enviar"  # proyecto ~/noon-cotizador-correo (Vercel personal + Resend)

INSTRUMENTADOR_HORA = 200000
HOSPITALIZACION_NOCHE = 1380000  # habitación individual, tarifa Q2 2026
VIGENCIA_MESES = 3
POLIZA = 600000  # va siempre, en todas las cotizaciones
RAPIDOS = [  # botones de "Otros elementos" en todas las sedes
    ["Bomba del dolor (3 días)", 550000],
]
FAJAS_RECARGO = 0.30  # sobre el precio de la tienda, redondeado al mil
FAJAS = [  # (nombre que ve la paciente, precio tienda, modelo de referencia — NO sale en el PDF)
    ("Faja todo el cuerpo · compresión alta", 260900, "Ana"),
    ("Faja todo el cuerpo · compresión media alta", 268900, "Ada"),
    ("Faja todo el cuerpo · compresión media", 221900, "Agatha C"),
    ("Faja todo el cuerpo · compresión baja", 135900, "Aurora"),
    ("Faja todo el cuerpo con mangas", 266900, "África / Calixta"),
    ("Faja solo senos", 105900, "Amara / Luna"),
    ("Faja senos con mangas", 116900, "Lyra"),
]

DOCTORES = ["Dr. Fernando Ruiz"]

# Implantes mamarios: precio por PAR, el que va con descuento (17%)
IMPLANTES_MAMARIOS = [
    {"modelo": "Standard redondo liso", "codigo": "10521", "precio": 1689166},
    {"modelo": "Soft Plus redondo (liso, opaco)", "codigo": "22622", "precio": 1838367},
    {"modelo": "Biodesign redondo texturizado", "codigo": "20622", "precio": 1838367},
    {"modelo": "Biodesign anatómico (texturizado)", "codigo": "20637 · 20674 · 20646", "precio": 2751334},
    {"modelo": "Biodesign redondo poliuretano", "codigo": "30622", "precio": 2129664},
]

QUIROFANO_INCLUYE = [
    "Derechos de sala por el tiempo programado",
    "Consulta preanestésica y honorarios de anestesia",
    "Materiales y medicamentos básicos para el procedimiento",
    "Equipos básicos de quirófano",
]
# Bogotá (Cirulaser 2026): el tarifario no dice qué incluye; la tarifa es por horas según el tipo de anestesia
QUIROFANO_INCLUYE_BOGOTA = [
    "Derechos de sala por el tiempo programado",
    "Anestesia según el tipo indicado",
]
BOGOTA_RAPIDOS = [  # cobros aparte del tarifario Cirulaser
    ["Consulta preanestésica", 175000],
    ["VASER", 633000],
    ["Recuperación posquirúrgica prolongada (1 hora)", 70000],
    ["Patología pequeña", 290000],
    ["Patología grande", 447000],
]
PAGOS = [
    ("Abono para tu fecha", "Con un abono reservas la fecha de tu cirugía."),
    ("Saldo", "Se paga completo antes del procedimiento."),
]
TERMINOS = "https://noon.clinic/terminos-y-condiciones#t4"


def _json(nombre):
    return json.load(open(os.path.join(AQUI, "_cotizador", nombre), encoding="utf-8"))


def generar():
    # Medellín (Q2 Sur): {proc: {anestesia, tiempos: [[h, v]]}} → {proc: [[h, anestesia, v]]}
    q2 = {p: [[h, d["anestesia"], v] for h, v in d["tiempos"]] for p, d in _json("tarifas-q2-2026.json").items()}
    sedes = {
        "medellin": {"nombre": "Medellín", "quirofano": "Quirófanos 2 Sur", "tarifas": q2, "incluye": QUIROFANO_INCLUYE,
                     "rapidos": [["Noche de hospitalización (habitación individual)", HOSPITALIZACION_NOCHE]]},
        # Bogotá (Cirulaser): {proc: [[h | None, anestesia, v]]}; None = precio fijo sin horas
        "bogota": {"nombre": "Bogotá", "quirofano": "Cirulaser", "tarifas": _json("tarifas-bogota-2026.json"), "incluye": QUIROFANO_INCLUYE_BOGOTA,
                   "rapidos": BOGOTA_RAPIDOS},
        # Pereira: mientras llega su tarifario, precios de quirófano iguales a Medellín (decisión de Laura, 19-oct-2026)
        "pereira": {"nombre": "Pereira", "quirofano": "Pereira", "tarifas": q2, "incluye": QUIROFANO_INCLUYE,
                    "rapidos": [["Noche de hospitalización (habitación individual)", HOSPITALIZACION_NOCHE]],
                    "nota": "Precios de quirófano iguales a Medellín (Quirófanos 2 Sur) mientras llega el tarifario de Pereira."},
    }
    config = {
        "codigo": CODIGO, "correo": CORREO, "envio": ENVIO, "instrumentador": INSTRUMENTADOR_HORA,
        "vigencia": VIGENCIA_MESES, "poliza": POLIZA, "rapidos": RAPIDOS,
        "fajas": [[n, int(round(v * (1 + FAJAS_RECARGO), -3))] for n, v, _ in FAJAS], "doctores": DOCTORES, "sedes": sedes,
        "mamarios": IMPLANTES_MAMARIOS, "pagos": PAGOS, "terminos": TERMINOS,
    }
    plantilla = open(os.path.join(AQUI, "_cotizador", "plantilla.html"), encoding="utf-8").read()
    html = plantilla.replace("/*CONFIG*/{}", json.dumps(config, ensure_ascii=False))
    with open(os.path.join(AQUI, "cotizador.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(q2) + len(sedes["bogota"]["tarifas"])


if __name__ == "__main__":
    print("Cotizador: %d procedimientos." % generar())
