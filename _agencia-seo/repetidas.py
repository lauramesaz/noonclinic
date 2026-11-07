# -*- coding: utf-8 -*-
"""¿La entrada de esta guía copia frases de otra guía? Lo corre el Policía humanizador (agente 3) ANTES de aprobar.

Uso (desde la raíz del repositorio):
  python3 _agencia-seo/repetidas.py                      # revisa todas las guías
  python3 _agencia-seo/repetidas.py <slug o archivo>     # revisa solo esa (o esas) guía(s)
  python3 _agencia-seo/repetidas.py <slug> --min 6       # umbral distinto (por defecto 8 palabras)

Qué mira: el primer párrafo (<p class="entrada">), el "intro" (texto de la tarjeta del blog) y la "descripcion"
(lo que sale en Google) de cada guía, y los compara con el texto completo de las DEMÁS guías del mismo idioma
(title, h1, intro, descripción y cuerpo). Su propio "par" en el otro idioma no cuenta.
Avisa cuando hay 8 o más palabras seguidas iguales (sin contar tildes, mayúsculas ni etiquetas HTML).
No cuenta como copia la palabra clave de la propia guía ni el texto de un enlace (<a>) de la otra guía: es normal que
otra guía enlace a esta con su keyword.

Termina con código 1 si encuentra alguna copia: la pieza no se aprueba hasta reescribir esa frase.
Regla de la agencia (INSTRUCCIONES.md §4 y agentes/3-humanizador.md, punto 8 de la prueba).
"""
import json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join(AQUI, "articulos")


def palabras(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", t)


def leer(ruta):
    texto = open(ruta, encoding="utf-8").read()
    m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->", texto, re.S)
    if not m:
        return None
    g = json.loads(m.group(1))
    cuerpo = texto[m.end():]
    e = re.search(r'<p class="entrada">(.*?)</p>', cuerpo, re.S)
    g["_entrada"] = e.group(1) if e else ""
    g["_todo"] = " ".join([g.get("title", ""), g.get("h1", ""), g.get("intro", ""), g.get("descripcion", ""), cuerpo])
    g["_archivo"] = os.path.basename(ruta)
    g["_anclas"] = [" ".join(palabras(a)) for a in re.findall(r"<a\b[^>]*>(.*?)</a>", cuerpo, re.S)]
    g["_propias"] = [" ".join(palabras(g.get(k, ""))) for k in ("keyword", "title", "h1")] + [g["slug"].replace("-", " ")]
    return g


def permitida(frase, g, otra):
    """La frase es la keyword/título de la guía revisada o el texto de un enlace de la otra guía."""
    f = " " + frase + " "
    return any(f in " " + t + " " for t in g["_propias"] + otra["_anclas"])


def tramos(lista, n):
    return {tuple(lista[i:i + n]): i for i in range(len(lista) - n + 1)}


def mas_largo(a, b, n):
    """Tramos de n o más palabras de 'a' que aparecen tal cual en 'b'. Devuelve [(largo, frase)], sin solapes."""
    vistos = tramos(b, n)
    out, i = [], 0
    while i <= len(a) - n:
        if tuple(a[i:i + n]) in vistos:
            j = i + n
            texto_b = " " + " ".join(b) + " "
            while j < len(a) and (" " + " ".join(a[i:j + 1]) + " ") in texto_b:
                j += 1
            out.append((j - i, " ".join(a[i:j])))
            i = j
        else:
            i += 1
    return out


def main():
    args = sys.argv[1:]
    n = 8
    if "--min" in args:
        k = args.index("--min")
        n = int(args[k + 1])
        del args[k:k + 2]
    guias = [g for g in (leer(os.path.join(CARPETA, f)) for f in sorted(os.listdir(CARPETA)) if f.endswith(".html")) if g]
    por_slug = {g["slug"]: g for g in guias}
    if args:
        revisar = []
        for a in args:
            slug = os.path.basename(a)[:-5] if a.endswith(".html") else a
            if slug not in por_slug:
                sys.exit("No encuentro la guía '%s' en _agencia-seo/articulos/." % a)
            revisar.append(por_slug[slug])
    else:
        revisar = guias
    texto_de = {g["slug"]: palabras(g["_todo"]) for g in guias}
    hallazgos = 0
    for g in revisar:
        lineas = []
        for campo, valor in (("entrada", g["_entrada"]), ("intro", g.get("intro", "")), ("descripcion", g.get("descripcion", ""))):
            a = palabras(valor)
            if len(a) < n:
                continue
            for otra in guias:
                if otra["slug"] == g["slug"] or otra.get("lang") != g.get("lang") or otra["slug"] == g.get("par"):
                    continue
                for largo, frase in mas_largo(a, texto_de[otra["slug"]], n):
                    if permitida(frase, g, otra):
                        continue
                    lineas.append("  - %s: %d palabras iguales a %s → \"%s\"" % (campo, largo, otra["slug"], frase))
        if lineas:
            hallazgos += 1
            print("COPIA en %s:" % g["slug"])
            print("\n".join(lineas))
    if not hallazgos:
        print("Sin frases copiadas de %d o más palabras (%d guía(s) revisada(s))." % (n, len(revisar)))
    else:
        print("\n%d guía(s) con frases copiadas de %d o más palabras. Reescribe esas frases antes de aprobar." % (hallazgos, n))
    sys.exit(1 if hallazgos else 0)


if __name__ == "__main__":
    main()
