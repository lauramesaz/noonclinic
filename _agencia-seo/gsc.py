# -*- coding: utf-8 -*-
"""Lee Search Console con el "usuario robot" (cuenta de servicio, solo lectura) y saca la foto semanal en Markdown.

Lo usan las revisiones SEO de los lunes que corren en la nube, así que no hace falta el Chrome ni el computador de Laura.

Uso (desde la raíz del repositorio):
  python3 _agencia-seo/gsc.py PROPIEDAD [--paises] [--sin-indexacion] [--max-urls N] [--sitemap URL]
                              [--paginas N] [--marca [palabras]] [--cruce] [--seguimiento [ARCHIVO]]
  PROPIEDAD: "sc-domain:noon.clinic" (propiedad de dominio) o "https://www.clinicaseravena.com/" (prefijo de URL)

  --paginas N        cuántas páginas mostrar en la tabla de páginas (por defecto 15).
  --marca [p1,p2]    separa las búsquedas de la marca (las que contienen esas palabras; por defecto la primera
                     parte del dominio, "noon" en noon.clinic) de las demás: clics, impresiones y búsquedas sin
                     la marca en primera página (posición media 10 o mejor y 3 o más impresiones).
  --cruce            búsqueda × página: marca "compiten" cuando 2 o más páginas salen para la misma búsqueda y
                     suman 3 o más impresiones, y compara las dos últimas quincenas para ver si una búsqueda ya
                     cambió de página. También dice qué páginas están cerca de la primera página SIN la marca.
  --seguimiento [ARCHIVO]  escribe una fila semanal (posición · impresiones) en ARCHIVO para las páginas listadas
                     en su línea "<!-- paginas: slug1, slug2, ... -->" (por defecto _agencia-seo/seguimiento-fichas.md).
                     Si ya hay una fila con el mismo período, la reemplaza.

Llave del robot: variable de entorno GSC_ROBOT_B64 (el JSON de la cuenta de servicio en base64, puesta en el entorno de la
nube) o, en el Mac, el archivo ~/.gsc-robot/llave.json. Nunca imprime la llave.
"""
from concurrent.futures import ThreadPoolExecutor
import base64, datetime, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.parse, urllib.request

ALCANCE = "https://www.googleapis.com/auth/webmasters.readonly"
API = "https://searchconsole.googleapis.com"


def llave():
    b64 = os.environ.get("GSC_ROBOT_B64", "").strip()
    if b64:
        return json.loads(base64.b64decode(b64))
    ruta = os.path.expanduser("~/.gsc-robot/llave.json")
    if os.path.exists(ruta):
        return json.load(open(ruta))
    sys.exit("FALTA LA LLAVE DEL ROBOT: no está la variable GSC_ROBOT_B64 en el entorno de la nube.")


def b64url(datos):
    return base64.urlsafe_b64encode(datos).rstrip(b"=")


def token(k):
    ahora = int(time.time())
    cabeza = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    cuerpo = b64url(json.dumps({"iss": k["client_email"], "scope": ALCANCE, "aud": k["token_uri"],
                                "iat": ahora, "exp": ahora + 3600}).encode())
    firmar = cabeza + b"." + cuerpo
    with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
        f.write(k["private_key"])
        pem = f.name
    try:
        os.chmod(pem, 0o600)
        firma = subprocess.run(["openssl", "dgst", "-sha256", "-sign", pem], input=firmar,
                               capture_output=True, check=True).stdout
    finally:
        os.remove(pem)
    jwt = firmar + b"." + b64url(firma)
    datos = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                    "assertion": jwt.decode()}).encode()
    r = urllib.request.urlopen(urllib.request.Request(k["token_uri"], data=datos), timeout=30)
    return json.loads(r.read())["access_token"]


def pedir(tok, ruta, cuerpo):
    req = urllib.request.Request(API + ruta, data=json.dumps(cuerpo).encode(),
                                 headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        detalle = e.read().decode()[:300]
        if e.code == 403:
            sys.exit("SIN PERMISO (403): agrega al robot como usuario 'Restringido' en esta propiedad de Search Console. " + detalle)
        raise SystemExit("ERROR %d de Search Console: %s" % (e.code, detalle))


def analitica(tok, prop, inicio, fin, dims, filas=25):
    ruta = "/webmasters/v3/sites/%s/searchAnalytics/query" % urllib.parse.quote(prop, safe="")
    cuerpo = {"startDate": inicio, "endDate": fin, "rowLimit": filas, "dataState": "all"}
    if dims:
        cuerpo["dimensions"] = dims
    filas_api = pedir(tok, ruta, cuerpo).get("rows", [])
    # Google ordena solo por clics; con pocos clics el top queda alfabético. Mejor: clics y luego impresiones.
    return sorted(filas_api, key=lambda r: (-r["clicks"], -r["impressions"]))


def fila(r):
    return "%d | %d | %.1f%% | %.1f" % (r["clicks"], r["impressions"], 100 * r["ctr"], r["position"])


def base_url(prop):
    return "https://" + prop.split(":", 1)[1] + "/" if prop.startswith("sc-domain:") else prop


def urls_sitemap(prop, sitemap=None):
    base = sitemap or base_url(prop)
    try:
        xml = urllib.request.urlopen(base if base.endswith(".xml") else urllib.parse.urljoin(base, "sitemap.xml"),
                                     timeout=30).read().decode("utf-8", "ignore")
        if "<sitemapindex" in xml:  # índice de sitemaps (noon desde el 27-oct-2026): se leen sus partes
            xml = "".join(urllib.request.urlopen(u, timeout=30).read().decode("utf-8", "ignore")
                          for u in re.findall(r"<sitemap>.*?<loc>\s*([^<]+?)\s*</loc>", xml, re.S))
    except Exception as e:
        return [], "no se pudo leer el sitemap (%s)" % e
    return re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml), ""


def opcion(a, nombre, defecto=None):
    """Valor que sigue a una opción, si lo hay (si lo siguiente empieza por --, no hay valor)."""
    if nombre not in a:
        return None
    k = a.index(nombre)
    return a[k + 1] if k + 1 < len(a) and not a[k + 1].startswith("--") else defecto


def terminos_marca(a, prop):
    v = opcion(a, "--marca", "")
    if v:
        return [w.strip().lower() for w in v.split(",") if w.strip()]
    dom = (prop.split(":", 1)[1] if prop.startswith("sc-domain:") else urllib.parse.urlparse(prop).netloc).lower()
    return [dom[4:].split(".")[0] if dom.startswith("www.") else dom.split(".")[0]]


def es_marca(q, terminos):
    return any(t in q.lower() for t in terminos)


def ruta(url):
    """https://noon.clinic/mentoplastia -> /mentoplastia (para leer más fácil)."""
    u = urllib.parse.urlparse(url)
    return (u.path or "/") + ("?" + u.query if u.query else "")


def suma(filas):
    c = sum(r["clicks"] for r in filas)
    im = sum(r["impressions"] for r in filas)
    pos = sum(r["position"] * r["impressions"] for r in filas) / im if im else 0
    return c, im, pos


def seccion_marca(tok, prop, i, f, t, consultas, terminos):
    marca = [r for r in consultas if es_marca(r["keys"][0], terminos)]
    otras = [r for r in consultas if not es_marca(r["keys"][0], terminos)]
    cm, im_m, _ = suma(marca)
    co, im_o, pos_o = suma(otras)
    ocultos = t["clicks"] - sum(r["clicks"] for r in consultas)
    print("## Sin la marca (búsquedas que no dicen %s)" % " / ".join('"%s"' % x for x in terminos))
    print("- Búsquedas de la marca: %d clics · %d impresiones (%s)."
          % (cm, im_m, ", ".join('"%s" %d/%d' % (r["keys"][0], r["clicks"], r["impressions"]) for r in marca[:5]) or "ninguna"))
    print("- **Sin la marca: %d clics · %d impresiones** en %d búsquedas distintas · posición media %.1f."
          % (co, im_o, len(otras), pos_o))
    if ocultos > 0:
        print("- Clics sin búsqueda visible (Google no muestra la consulta): %d." % ocultos)
    por_pais = {}
    for r in analitica(tok, prop, i, f, ["query", "country"], 5000):
        if not es_marca(r["keys"][0], terminos):
            c = por_pais.setdefault(r["keys"][1].upper(), [0, 0])
            c[0] += r["clicks"]
            c[1] += r["impressions"]
    if por_pais:
        print("- Sin la marca por país (clics/impresiones): " + " · ".join(
            "%s %d/%d" % (k, v[0], v[1]) for k, v in sorted(por_pais.items(), key=lambda x: (-x[1][0], -x[1][1]))[:5]) + ".")
    primera = [r for r in otras if r["position"] <= 10 and r["impressions"] >= 3]
    print("- Sin la marca en primera página (posición media ≤ 10 y ≥ 3 impresiones): %d%s"
          % (len(primera), (": " + ", ".join('"%s" (%.1f)' % (r["keys"][0], r["position"]) for r in primera)) if primera else "."))
    print("\nbúsqueda sin la marca (top 10) | clics | impresiones | CTR | posición\n---|---|---|---|---")
    for r in otras[:10]:
        print(r["keys"][0] + " | " + fila(r))
    print()


def seccion_cruce(tok, prop, inicio, fin, paginas, terminos):
    i, f = inicio.isoformat(), fin.isoformat()
    qp = analitica(tok, prop, i, f, ["query", "page"], 5000)
    por_q = {}
    for r in qp:
        por_q.setdefault(r["keys"][0], []).append(r)
    print("## Búsqueda × página")
    print("### Compiten (2 o más páginas para la misma búsqueda, 3 o más impresiones en total)")
    compiten, de_marca = [], []
    for q, filas in sorted(por_q.items(), key=lambda x: -sum(r["impressions"] for r in x[1])):
        if len(filas) >= 2 and sum(r["impressions"] for r in filas) >= 3:
            linea = '- "%s" · %d impr. → %s' % (q, sum(r["impressions"] for r in filas), " · ".join(
                "%s %d (pos. %.0f)" % (ruta(r["keys"][1]), r["impressions"], r["position"])
                for r in sorted(filas, key=lambda r: -r["impressions"])))
            (de_marca if es_marca(q, terminos) else compiten).append(linea)
    print("\n".join(compiten) or "- ninguna")
    print("- **%d búsquedas sin la marca repartidas entre 2 o más páginas.**" % len(compiten))
    if de_marca:
        print("- De la marca (es normal que salgan varias páginas, no cuenta): " + "; ".join(l[2:] for l in de_marca))

    mitad = inicio + datetime.timedelta(days=13)
    q1 = analitica(tok, prop, i, mitad.isoformat(), ["query", "page"], 5000)
    q2 = analitica(tok, prop, (mitad + datetime.timedelta(days=1)).isoformat(), f, ["query", "page"], 5000)
    def arriba(filas):
        d = {}
        for r in filas:
            d.setdefault(r["keys"][0], []).append(r)
        return {q: sorted(v, key=lambda r: -r["impressions"]) for q, v in d.items()}
    a1, a2 = arriba(q1), arriba(q2)
    print("\n### Cambió de página entre quincenas (%s a %s → %s a %s)"
          % (i, mitad.isoformat(), (mitad + datetime.timedelta(days=1)).isoformat(), f))
    cambios = []
    for q in a1:
        if q in a2 and not es_marca(q, terminos):
            antes, ahora = a1[q][0], a2[q][0]
            total = sum(r["impressions"] for r in a1[q] + a2[q])
            if total >= 3 and antes["keys"][1] != ahora["keys"][1]:
                cambios.append('- "%s": %s (%d impr.) → %s (%d de %d impr.)' % (
                    q, ruta(antes["keys"][1]), antes["impressions"], ruta(ahora["keys"][1]), ahora["impressions"],
                    sum(r["impressions"] for r in a2[q])))
    print("\n".join(cambios) or "- ninguna")

    print("\n### Cerca de la primera página (página en posición ≤ 20 con 3 o más impresiones, sin contar el inicio)")
    lineas = []
    for r in paginas:
        if r["position"] > 20 or r["impressions"] < 3 or ruta(r["keys"][0]) == "/":
            continue
        de_p = [x for x in qp if x["keys"][1] == r["keys"][0]]
        m = sum(x["impressions"] for x in de_p if es_marca(x["keys"][0], terminos))
        o = [x for x in de_p if not es_marca(x["keys"][0], terminos)]
        if o:
            nota = "sin la marca: " + ", ".join('"%s" pos. %.0f' % (x["keys"][0], x["position"]) for x in o[:3])
        elif m:
            nota = "solo por la marca (%d impr.): no cuenta como casi en primera página" % m
        else:
            nota = "búsquedas que Google no muestra"
        lineas.append("- %s · pos. %.1f · %d impr. → %s" % (ruta(r["keys"][0]), r["position"], r["impressions"], nota))
    print("\n".join(lineas) or "- ninguna")
    print()


def seccion_seguimiento(paginas, inicio, fin, archivo):
    print("## Seguimiento de fichas (%s)" % archivo)
    if not os.path.exists(archivo):
        print("- No existe %s: no se escribe la fila." % archivo)
        print()
        return
    texto = open(archivo, encoding="utf-8").read()
    m = re.search(r"<!--\s*paginas:\s*(.*?)-->", texto, re.S)
    if not m:
        print("- %s no tiene la línea <!-- paginas: slug1, slug2, ... -->: no se escribe la fila." % archivo)
        print()
        return
    slugs = [x.strip().strip("/") for x in m.group(1).split(",") if x.strip()]
    datos = {}
    for r in paginas:
        p = ruta(r["keys"][0]).strip("/")
        p = p[:-5] if p.endswith(".html") else p
        datos[p] = r
    periodo = "%s a %s" % (inicio.isoformat(), fin.isoformat())
    celdas = []
    for sl in slugs:
        r = datos.get(sl)
        celdas.append("%.0f · %d" % (r["position"], r["impressions"]) if r else "—")
    nueva = "| " + periodo + " | " + " | ".join(celdas) + " |"
    cabeza = "| Período (28 días) | " + " | ".join(slugs) + " |"
    lineas = texto.rstrip("\n").split("\n")
    if cabeza not in lineas:
        lineas += ["", cabeza, "|" + "---|" * (len(slugs) + 1)]
    desde = lineas.index(cabeza) + 2
    filas_tabla = []
    for k in range(desde, len(lineas)):
        if not lineas[k].startswith("| 20"):
            break
        filas_tabla.append(k)
    previa = None
    reemplazo = [k for k in filas_tabla if lineas[k].startswith("| " + periodo + " |")]
    if reemplazo:
        k = reemplazo[0]
        previa = lineas[filas_tabla[filas_tabla.index(k) - 1]] if filas_tabla.index(k) > 0 else None
        lineas[k] = nueva
    else:
        previa = lineas[filas_tabla[-1]] if filas_tabla else None
        lineas.insert(filas_tabla[-1] + 1 if filas_tabla else desde, nueva)
    open(archivo, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
    print("- Fila escrita: " + nueva)
    if previa:
        antes = [c.strip() for c in previa.strip("|").split("|")][1:]
        mejoras = []
        for sl, a_, b_ in zip(slugs, antes, celdas):
            if a_ != "—" and b_ != "—":
                pa, pb = float(a_.split("·")[0]), float(b_.split("·")[0])
                mejoras.append((pa - pb, sl, pa, pb))
        if mejoras:
            d, sl, pa, pb = max(mejoras)
            print("- La que más subió frente a la fila anterior: %s (puesto %.0f → %.0f)." % (sl, pa, pb) if d > 0
                  else "- Ninguna ficha subió frente a la fila anterior.")
    else:
        print("- Primera fila: todavía no hay con qué comparar.")
    print("- Fichas en el puesto 40 o mejor: %d de %d." % (
        sum(1 for c in celdas if c != "—" and float(c.split("·")[0]) <= 40), len(slugs)))
    print()


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    prop = a[0]
    max_urls = int(a[a.index("--max-urls") + 1]) if "--max-urls" in a else 400
    tok = token(llave())
    fin = datetime.date.today() - datetime.timedelta(days=2)
    inicio = fin - datetime.timedelta(days=27)
    i, f = inicio.isoformat(), fin.isoformat()
    print("# Search Console · %s · %s a %s (28 días)\n" % (prop, i, f))

    tot = analitica(tok, prop, i, f, None, 1)
    t = tot[0] if tot else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}
    print("**Totales:** %d clics · %d impresiones · CTR %.1f%% · posición media %.1f\n"
          % (t["clicks"], t["impressions"], 100 * t["ctr"], t["position"]))

    if "--paises" in a:
        print("## Países (top 10)\npaís | clics | impresiones | CTR | posición\n---|---|---|---|---")
        for r in analitica(tok, prop, i, f, ["country"], 250)[:10]:
            print(r["keys"][0].upper() + " | " + fila(r))
        print()

    consultas = analitica(tok, prop, i, f, ["query"], 5000)
    print("## Búsquedas (top 15)\nbúsqueda | clics | impresiones | CTR | posición\n---|---|---|---|---")
    for r in consultas[:15]:
        print(r["keys"][0] + " | " + fila(r))
    print()

    n_pag = int(opcion(a, "--paginas", "15") or 15)
    paginas = analitica(tok, prop, i, f, ["page"], 5000)
    print("## Páginas (top %d)\npágina | clics | impresiones | CTR | posición\n---|---|---|---|---" % n_pag)
    for r in paginas[:n_pag]:
        print(r["keys"][0] + " | " + fila(r))
    print()

    terminos = terminos_marca(a, prop)
    if "--marca" in a:
        seccion_marca(tok, prop, i, f, t, consultas, terminos)
    if "--cruce" in a:
        seccion_cruce(tok, prop, inicio, fin, paginas, terminos)
    if "--seguimiento" in a:
        seccion_seguimiento(paginas, inicio, fin, opcion(a, "--seguimiento", os.path.join("_agencia-seo", "seguimiento-fichas.md")))

    cand = [r for r in paginas if r["position"] <= 20 and r["clicks"] <= 1 and r["impressions"] >= 10]
    print("## Salen pero casi nadie abre (posición ≤ 20, 0-1 clics, ≥ 10 impresiones)")
    print("\n".join("- " + r["keys"][0] + " · " + fila(r) for r in cand) or "- ninguna")
    print()

    if "--sin-indexacion" in a:
        return
    urls, error = urls_sitemap(prop, a[a.index("--sitemap") + 1] if "--sitemap" in a else None)
    print("## Indexación (inspección de las páginas del sitemap)")
    if error:
        print("- " + error)
        return
    def inspeccionar(u):
        res = pedir(tok, "/v1/urlInspection/index:inspect", {"inspectionUrl": u, "siteUrl": prop, "languageCode": "es"})
        return u, res.get("inspectionResult", {}).get("indexStatusResult", {})

    estados, fuera = {}, []
    with ThreadPoolExecutor(max_workers=6) as grupo:  # varias a la vez: una por una tarda ~5 s por página
        for u, st in grupo.map(inspeccionar, urls[:max_urls]):
            estado = st.get("coverageState", "sin dato")
            estados[estado] = estados.get(estado, 0) + 1
            if st.get("verdict") != "PASS":
                fuera.append((u, estado))
    en_google = len(urls[:max_urls]) - len(fuera)
    print("- %d páginas en el sitemap, revisadas %d: **%d en Google**, %d todavía no."
          % (len(urls), len(urls[:max_urls]), en_google, len(fuera)))
    for estado, n in sorted(estados.items(), key=lambda x: -x[1]):
        print("  - %s: %d" % (estado, n))
    if fuera:
        print("- Páginas que aún no están en Google:")
        for u, estado in fuera[:40]:
            print("  - %s (%s)" % (u, estado))


if __name__ == "__main__":
    main()
