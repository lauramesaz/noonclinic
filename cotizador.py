# -*- coding: utf-8 -*-
# noon Clinic · página INTERNA "Cotizador de cirugía" (código de acceso, no indexada, sin enlace desde la web).
# Se genera sola al correr build.py. Tarifas de quirófano en _cotizador/tarifas-q2-2026.json (sacadas del PDF de Q2 Sur).
import os, json

AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGO = "111"
CORREO = "lauramesazuluaga@gmail.com"  # aquí llega cada cotización con todo discriminado (vía FormSubmit)

INSTRUMENTADOR_HORA = 200000
HOSPITALIZACION_NOCHE = 1380000  # habitación individual, tarifa Q2 2026
VIGENCIA_MESES = 3

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
PAGOS = [
    ("Abono para tu fecha", "Con un abono reservas la fecha de tu cirugía."),
    ("Saldo", "Se paga completo antes del procedimiento."),
]
TERMINOS = "https://noon.clinic/terminos-y-condiciones#t4"


def generar():
    tarifas = json.load(open(os.path.join(AQUI, "_cotizador", "tarifas-q2-2026.json"), encoding="utf-8"))
    config = {
        "codigo": CODIGO, "correo": CORREO, "instrumentador": INSTRUMENTADOR_HORA,
        "hospitalizacion": HOSPITALIZACION_NOCHE, "vigencia": VIGENCIA_MESES, "doctores": DOCTORES,
        "tarifas": tarifas, "mamarios": IMPLANTES_MAMARIOS, "incluye": QUIROFANO_INCLUYE,
        "pagos": PAGOS, "terminos": TERMINOS,
    }
    plantilla = open(os.path.join(AQUI, "_cotizador", "plantilla.html"), encoding="utf-8").read()
    html = plantilla.replace("/*CONFIG*/{}", json.dumps(config, ensure_ascii=False))
    with open(os.path.join(AQUI, "cotizador.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return len(tarifas)


if __name__ == "__main__":
    print("Cotizador: %d procedimientos." % generar())
