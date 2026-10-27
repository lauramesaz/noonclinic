# -*- coding: utf-8 -*-
# Avisa por IndexNow a Bing (y a quienes lo usan: Copilot, DuckDuckGo, Yahoo, búsquedas de ChatGPT) de las
# páginas nuevas o cambiadas del sitemap. Lo corre cada mañana una rutina en la nube (no necesita el computador).
# Compara el sitemap.xml de hoy con el de hace ~26 horas (según git); si no hay historial, manda lo de los últimos 2 días.
# Uso: python3 _agencia-seo/indexnow.py HOST LLAVE      (desde la raíz del repositorio)
import datetime, json, re, subprocess, sys, urllib.error, urllib.request


def leer(xml):
    urls = {}
    for bloque in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*([^<]+?)\s*</loc>", bloque)
        mod = re.search(r"<lastmod>\s*([^<]+?)\s*</lastmod>", bloque)
        if loc:
            urls[loc.group(1)] = mod.group(1) if mod else ""
    return urls


def sitemap_de_ayer():
    sha = subprocess.run(["git", "rev-list", "-1", "--before=26 hours ago", "HEAD"], capture_output=True, text=True).stdout.strip()
    if not sha:
        return None
    r = subprocess.run(["git", "show", sha + ":sitemap.xml"], capture_output=True, text=True)
    return leer(r.stdout) if r.returncode == 0 else None


def main(host, llave):
    subprocess.run(["git", "pull", "-q", "--ff-only"], capture_output=True)
    actual = leer(open("sitemap.xml", encoding="utf-8").read())
    previo = sitemap_de_ayer()
    if previo is None:
        desde = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
        nuevas = [u for u, f in actual.items() if f[:10] >= desde]
    else:
        nuevas = [u for u, f in actual.items() if previo.get(u) != f]
    if not nuevas:
        print("%s: nada nuevo que avisar (%d páginas en el sitemap)." % (host, len(actual)))
        return 0
    cuerpo = json.dumps({"host": host, "key": llave, "keyLocation": "https://%s/%s.txt" % (host, llave),
                         "urlList": nuevas[:10000]}).encode("utf-8")
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=cuerpo,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        codigo = urllib.request.urlopen(req, timeout=30).status
    except urllib.error.HTTPError as e:
        codigo = e.code
    except urllib.error.URLError as e:
        print("%s: no se pudo llegar a IndexNow (%s). Si dice 403, la red de la nube sigue cerrada." % (host, e.reason))
        return 1
    print("%s: %d páginas avisadas, Bing respondió %d" % (host, len(nuevas), codigo))
    for u in nuevas:
        print("  " + u)
    return 0 if codigo in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
