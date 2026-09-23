# -*- coding: utf-8 -*-
# Servidor local de vista previa: entiende direcciones limpias (sin .html), igual que GitHub Pages.
# Uso:  python3 _servidor.py 5540
import os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

AQUI = os.path.dirname(os.path.abspath(__file__))


class Limpio(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=AQUI, **k)

    def translate_path(self, path):
        ruta = super().translate_path(path)
        if not os.path.exists(ruta) and os.path.exists(ruta + ".html"):
            return ruta + ".html"
        return ruta


ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 5540), Limpio).serve_forever()
