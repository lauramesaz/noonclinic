# -*- coding: utf-8 -*-
"""Revisa con el "usuario robot" de Search Console (solo lectura) cuáles páginas del sitemap ya están en Google y cuáles no.

Escribe dos archivos en _agencia-seo/:
  indexacion.json  → {url: {"en_google": bool, "estado": "...", "rastreo": "AAAA-MM-DD", "grupo": "..."}}
                     build.py lo lee para darles más enlaces internos a las páginas que Google todavía no tiene.
  indexacion.md    → resumen por grupo (cirugías y tratamientos, guías, inglés) para la agencia y para Laura.

Lo corre cada mañana la rutina de la agencia en la nube (llave en GSC_ROBOT_B64) o el Mac (~/.gsc-robot/llave.json).
Uso (desde la raíz del repositorio): python3 _agencia-seo/indexacion.py
"""
from concurrent.futures import ThreadPoolExecutor
import datetime, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import gsc  # noqa: E402

PROP = "sc-domain:noon.clinic"
GRUPOS = {"paginas": "Cirugías, tratamientos y páginas de la clínica", "guias": "Guías del blog (español)", "en": "Páginas en inglés"}
SITEMAPS = {"sitemap-paginas.xml": "paginas", "sitemap-guias.xml": "guias", "sitemap-en.xml": "en"}


def urls_por_grupo():
    """Lee los sitemaps del repositorio (el índice y sus 3 hijos; si aún es uno solo, lo clasifica por idioma)."""
    out = {}
    for nombre, grupo in SITEMAPS.items():
        ruta = os.path.join(RAIZ, nombre)
        if os.path.exists(ruta):
            for u in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", open(ruta, encoding="utf-8").read()):
                out[u] = grupo
    if out:
        return out
    guias = {f[:-5] for f in os.listdir(os.path.join(AQUI, "articulos")) if f.endswith(".html")}
    for u in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", open(os.path.join(RAIZ, "sitemap.xml"), encoding="utf-8").read()):
        slug = u.rstrip("/").rsplit("/", 1)[-1] if u.rstrip("/") != "https://noon.clinic" else "index"
        archivo = os.path.join(RAIZ, slug + ".html")
        en = os.path.exists(archivo) and '<html lang="en">' in open(archivo, encoding="utf-8").read(300)
        out[u] = "en" if en else ("guias" if slug in guias else "paginas")
    return out


def main():
    urls = urls_por_grupo()
    tok = gsc.token(gsc.llave())

    def inspeccionar(u):
        res = gsc.pedir(tok, "/v1/urlInspection/index:inspect", {"inspectionUrl": u, "siteUrl": PROP, "languageCode": "es"})
        r = res.get("inspectionResult", {}).get("indexStatusResult", {})
        return u, {"en_google": r.get("verdict") == "PASS", "estado": r.get("coverageState", "sin dato"),
                   "rastreo": (r.get("lastCrawlTime") or "")[:10], "grupo": urls[u]}

    with ThreadPoolExecutor(max_workers=6) as ex:  # límite de Google: 600 por minuto y 2.000 por día
        datos = dict(ex.map(inspeccionar, sorted(urls)))
    hoy = datetime.date.today().isoformat()
    with open(os.path.join(AQUI, "indexacion.json"), "w", encoding="utf-8") as f:
        json.dump({"fecha": hoy, "urls": datos}, f, ensure_ascii=False, indent=1, sort_keys=True)

    lineas = ["# Qué páginas de noon.clinic ya están en Google", "",
              "Lo actualiza cada mañana la agencia con el usuario robot de Search Console (solo lectura). "
              "build.py usa indexacion.json para darles más enlaces internos a las que Google todavía no tiene.", "",
              "## Revisión del %s" % hoy, ""]
    total_si = sum(d["en_google"] for d in datos.values())
    lineas.append("**Total:** %d de %d páginas en Google.\n" % (total_si, len(datos)))
    for g, nombre in GRUPOS.items():
        del_grupo = {u: d for u, d in datos.items() if d["grupo"] == g}
        si = sum(d["en_google"] for d in del_grupo.values())
        lineas.append("- %s: **%d de %d** en Google." % (nombre, si, len(del_grupo)))
    lineas += ["", "## Por qué no están las demás", ""]
    estados = {}
    for d in datos.values():
        if not d["en_google"]:
            estados[d["estado"]] = estados.get(d["estado"], 0) + 1
    lineas += ["- %s: %d" % (e, n) for e, n in sorted(estados.items(), key=lambda x: -x[1])]
    for g, nombre in GRUPOS.items():
        faltan = sorted(u.replace("https://noon.clinic", "") or "/" for u, d in datos.items() if d["grupo"] == g and not d["en_google"])
        if faltan:
            lineas += ["", "### Faltan · %s (%d)" % (nombre, len(faltan)), "", ", ".join(faltan)]
    with open(os.path.join(AQUI, "indexacion.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print("Indexación: %d de %d páginas en Google." % (total_si, len(datos)))


if __name__ == "__main__":
    main()
