# -*- coding: utf-8 -*-
"""¿Esta búsqueda ya tiene página en noon.clinic? Lo corre la agencia ANTES de escribir (agente 1) y el juez SEO (agente 5).

Uso (desde la raíz del repositorio):
  python3 _agencia-seo/dueno.py "lipotransferencia glútea recuperación"

Muestra las páginas más parecidas (fichas de procedimientos, guías del blog y páginas en inglés) y avisa si una FICHA
es la dueña de esa búsqueda. Regla (INSTRUCCIONES.md §3): una búsqueda = una página. Si hay dueña, la guía nueva
necesita otro ángulo (viaje, recuperación, comparación, costo…), su title no puede ser el de la ficha y enlaza a la
ficha en el primer tercio del texto. Si una GUÍA ya cubre el mismo tema, no se escribe otra: se mejora esa.
"""
import json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)

VACIAS = set("""de del la las el los en y o a para por con sin que como cual cuanto cuantos cuantas tras desde
un una unos unas al mi tu su se es mas the of in for to from and or a an how what is my your with after
medellin colombia noon clinic""".split())


def normal(t):
    t = unicodedata.normalize("NFD", re.sub("<[^>]+>", " ", t.lower()))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return [w[:-1] if len(w) > 4 and w.endswith("s") else w for w in re.findall(r"[a-z0-9]+", t) if w not in VACIAS]


def paginas():
    from datos_noon import CIRUGIAS_NOON, TRATAMIENTOS
    import fichas_en as FE
    out = []
    for p in CIRUGIAS_NOON + TRATAMIENTOS:
        out.append(("FICHA", p["slug"], p["nombre"] + " " + p["slug"].replace("-", " ")))
        en = FE.en_de(p["slug"])
        if en:
            out.append(("FICHA EN", en[:-5], FE.FICHAS_EN[p["slug"]]["nombre"] + " " + en[:-5].replace("-", " ")))
    out.append(("FICHA", "criolipolisis", "criolipolisis criolipólisis grasa sin cirugía frío"))
    carpeta = os.path.join(AQUI, "articulos")
    for f in sorted(os.listdir(carpeta)):
        if f.endswith(".html"):
            m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->", open(os.path.join(carpeta, f), encoding="utf-8").read(), re.S)
            if m:
                g = json.loads(m.group(1))
                out.append(("GUÍA" + (" EN" if g.get("lang") == "en" else ""), g["slug"], " ".join([g.get("title", ""), g.get("h1", ""), g["slug"].replace("-", " "), g.get("keyword", "")])))
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    q = set(normal(" ".join(sys.argv[1:])))
    if not q:
        sys.exit("Escribe la búsqueda con palabras de contenido (no solo 'en Medellín').")
    filas = []
    for tipo, slug, texto in paginas():
        w = set(normal(texto))
        comun = q & w
        if comun:
            filas.append((len(comun) / len(q), len(comun) / len(w | q), tipo, slug))
    filas.sort(reverse=True)
    print('Búsqueda: "%s"\n' % " ".join(sys.argv[1:]))
    for cubre, parecido, tipo, slug in filas[:8]:
        print("  %3d%%  %-9s https://noon.clinic/%s" % (round(100 * cubre), tipo, slug))
    duena = next((f for f in filas if f[2].startswith("FICHA") and f[0] >= 0.99), None)
    gemela = next((f for f in filas if f[2].startswith("GUÍA") and f[0] >= 0.99 and f[1] >= 0.3), None)
    print()
    if duena:
        print("DUEÑA: https://noon.clinic/%s es la página de esa búsqueda. La guía necesita otro ángulo, un title distinto"
              " y un enlace a esa ficha en el primer tercio." % duena[3])
    if gemela:
        print("OJO: la guía https://noon.clinic/%s ya cubre casi lo mismo. No escribas otra: mejora esa." % gemela[3])
    if not duena and not gemela:
        print("Libre: ninguna página cubre del todo esa búsqueda.")


if __name__ == "__main__":
    main()
