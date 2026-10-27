# -*- coding: utf-8 -*-
"""Lee Search Console con el "usuario robot" (cuenta de servicio, solo lectura) y saca la foto semanal en Markdown.

Lo usan las revisiones SEO de los lunes que corren en la nube, así que no hace falta el Chrome ni el computador de Laura.

Uso (desde la raíz del repositorio):
  python3 _agencia-seo/gsc.py PROPIEDAD [--paises] [--sin-indexacion] [--max-urls N]
  PROPIEDAD: "sc-domain:noon.clinic" (propiedad de dominio) o "https://www.clinicaseravena.com/" (prefijo de URL)

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
    return pedir(tok, ruta, cuerpo).get("rows", [])


def fila(r):
    return "%d | %d | %.1f%% | %.1f" % (r["clicks"], r["impressions"], 100 * r["ctr"], r["position"])


def urls_sitemap(prop):
    base = "https://" + prop.split(":", 1)[1] + "/" if prop.startswith("sc-domain:") else prop
    try:
        xml = urllib.request.urlopen(urllib.parse.urljoin(base, "sitemap.xml"), timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        return [], "no se pudo leer el sitemap (%s)" % e
    return re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml), ""


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
        for r in analitica(tok, prop, i, f, ["country"], 10):
            print(r["keys"][0].upper() + " | " + fila(r))
        print()

    print("## Búsquedas (top 15)\nbúsqueda | clics | impresiones | CTR | posición\n---|---|---|---|---")
    for r in analitica(tok, prop, i, f, ["query"], 15):
        print(r["keys"][0] + " | " + fila(r))
    print()

    paginas = analitica(tok, prop, i, f, ["page"], 250)
    print("## Páginas (top 15)\npágina | clics | impresiones | CTR | posición\n---|---|---|---|---")
    for r in paginas[:15]:
        print(r["keys"][0] + " | " + fila(r))
    print()

    cand = [r for r in paginas if r["position"] <= 20 and r["clicks"] <= 1 and r["impressions"] >= 10]
    print("## Salen pero casi nadie abre (posición ≤ 20, 0-1 clics, ≥ 10 impresiones)")
    print("\n".join("- " + r["keys"][0] + " · " + fila(r) for r in cand) or "- ninguna")
    print()

    if "--sin-indexacion" in a:
        return
    urls, error = urls_sitemap(prop)
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
