"""API y estáticos del incremento. Solo biblioteca estándar."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from ecologistica.servicio import Servicio

RAIZ_FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
SERVICIO = Servicio()


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, formato, *args):
        return

    def _json(self, codigo: int, cuerpo: dict) -> None:
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def _leer(self) -> dict:
        longitud = int(self.headers.get("Content-Length", "0"))
        if longitud == 0:
            return {}
        return json.loads(self.rfile.read(longitud).decode("utf-8"))

    def _token(self) -> str:
        encabezado = self.headers.get("Authorization", "")
        if encabezado.startswith("Bearer "):
            return encabezado[7:]
        return ""

    def _exigir_sesion(self) -> bool:
        if SERVICIO.usuario_de(self._token()) is None:
            self._json(401, {"ok": False, "mensaje": "Debe iniciar sesión."})
            return False
        return True

    def do_GET(self):
        ruta = urlparse(self.path).path
        if ruta == "/api/vehiculos":
            if self._exigir_sesion():
                self._json(200, {"ok": True, "vehiculos": SERVICIO.vehiculos})
            return
        if ruta == "/api/puntos":
            if self._exigir_sesion():
                self._json(200, {"ok": True, "puntos": SERVICIO.puntos})
            return
        if ruta == "/api/pedidos":
            if self._exigir_sesion():
                self._json(200, {"ok": True, "pedidos": SERVICIO.pedidos})
            return
        self._estatico(ruta)

    def do_POST(self):
        ruta = urlparse(self.path).path
        try:
            cuerpo = self._leer()
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "mensaje": "El cuerpo no es JSON válido."})
            return
        try:
            if ruta == "/api/sesion":
                self._json(200, SERVICIO.iniciar_sesion(cuerpo.get("email", ""), cuerpo.get("password", "")))
                return
            if not self._exigir_sesion():
                return
            if ruta == "/api/vehiculos":
                creado = SERVICIO.crear_vehiculo(cuerpo.get("placa", ""), float(cuerpo.get("capacidad_kg", 0)))
                self._json(201, {"ok": True, "vehiculo": creado})
                return
            if ruta == "/api/puntos":
                creado = SERVICIO.crear_punto(
                    cuerpo.get("nombre", ""),
                    cuerpo.get("direccion", ""),
                    float(cuerpo.get("latitud", 0)),
                    float(cuerpo.get("longitud", 0)),
                    cuerpo.get("distrito", ""),
                )
                self._json(201, {"ok": True, "punto": creado})
                return
            if ruta == "/api/pedidos":
                creado = SERVICIO.crear_pedido(
                    int(cuerpo.get("punto_id", 0)),
                    float(cuerpo.get("peso_kg", 0)),
                    cuerpo.get("tipo_carga", ""),
                )
                self._json(201, {"ok": True, "pedido": creado})
                return
        except (TypeError, ValueError) as exc:
            self._json(400, {"ok": False, "mensaje": str(exc)})
            return
        self._json(404, {"ok": False, "mensaje": "Ruta no encontrada."})

    def _estatico(self, ruta: str) -> None:
        relativo = "index.html" if ruta in ("", "/") else ruta.lstrip("/")
        archivo = (RAIZ_FRONTEND / relativo).resolve()
        if not str(archivo).startswith(str(RAIZ_FRONTEND.resolve())) or not archivo.is_file():
            self._json(404, {"ok": False, "mensaje": "No encontrado."})
            return
        tipos = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}
        datos = archivo.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", tipos.get(archivo.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


def main() -> None:
    servidor = ThreadingHTTPServer(("127.0.0.1", 8765), Manejador)
    print("EcoLogística en http://127.0.0.1:8765")
    servidor.serve_forever()


if __name__ == "__main__":
    main()
