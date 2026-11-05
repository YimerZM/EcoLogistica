"""API y estáticos del incremento. Solo biblioteca estándar."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ecologistica.servicio import Servicio

RAIZ_FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
SERVICIO = Servicio()
OPERAR = ("Administrador", "Operador")
PLAN = ("Administrador", "Operador", "Planificador")
ENTREGA = ("Administrador", "Operador", "Conductor")
PEDIDO = ("Administrador", "Operador", "Contratante")
EXPORTAR = ("Administrador", "Operador", "Planificador", "Responsable", "Auditor")
AUDITORIA = ("Administrador", "Auditor")
LECTURA = (
    "Administrador",
    "Operador",
    "Planificador",
    "Conductor",
    "Responsable",
    "Auditor",
    "Contratante",
)


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

    def _exigir_rol(self, roles: tuple):
        usuario = SERVICIO.usuario_de(self._token())
        if usuario is None:
            self._json(401, {"ok": False, "mensaje": "Debe iniciar sesión."})
            return None
        if usuario["rol"] not in roles:
            self._json(403, {"ok": False, "mensaje": "No tiene autorización para esta operación."})
            return None
        return usuario

    def do_GET(self):
        analizador = urlparse(self.path)
        ruta = analizador.path
        consulta = parse_qs(analizador.query)
        if ruta == "/api/vehiculos":
            if self._exigir_rol(LECTURA):
                self._json(200, {"ok": True, "vehiculos": SERVICIO.vehiculos})
            return
        if ruta == "/api/puntos":
            if self._exigir_rol(LECTURA):
                self._json(200, {"ok": True, "puntos": SERVICIO.puntos})
            return
        if ruta == "/api/pedidos":
            usuario = self._exigir_rol(LECTURA)
            if not usuario:
                return
            pedidos = SERVICIO.pedidos
            if usuario["rol"] == "Contratante":
                pedidos = [p for p in pedidos if p.get("contratante_email") == usuario["email"]]
            estado = consulta.get("estado", [""])[0]
            if estado:
                pedidos = [p for p in pedidos if p["estado"] == estado]
            self._json(200, {"ok": True, "pedidos": pedidos})
            return
        if ruta == "/api/usuarios":
            if self._exigir_rol(("Administrador", "Auditor")):
                self._json(200, {"ok": True, "usuarios": SERVICIO.listar_usuarios()})
            return
        if ruta == "/api/rutas":
            usuario = self._exigir_rol(LECTURA)
            if not usuario:
                return
            if "ruta_id" in consulta:
                try:
                    encontrada = SERVICIO.ruta_por_id(int(consulta["ruta_id"][0]))
                except ValueError:
                    encontrada = {"ok": False, "mensaje": "La ruta no está disponible."}
                self._json(200 if encontrada["ok"] else 404, encontrada)
                return
            rutas = SERVICIO.rutas
            if usuario["rol"] == "Conductor":
                rutas = [r for r in rutas if r.get("conductor_email") == usuario["email"]]
            self._json(200, {"ok": True, "rutas": rutas})
            return
        if ruta == "/api/indicadores":
            usuario = self._exigir_rol(LECTURA)
            if not usuario:
                return
            periodo = consulta.get("periodo", ["todo"])[0]
            self._json(200, SERVICIO.indicadores(periodo, usuario["rol"], usuario["email"]))
            return
        if ruta == "/api/auditoria":
            if self._exigir_rol(AUDITORIA):
                self._json(200, {"ok": True, "eventos": SERVICIO.auditoria})
            return
        if ruta == "/api/parametros":
            if self._exigir_rol(LECTURA):
                self._json(200, {"ok": True, "parametros": SERVICIO.parametros})
            return
        if ruta == "/api/exportar/pedidos":
            usuario = self._exigir_rol(EXPORTAR)
            if not usuario:
                return
            lineas = ["pedido_id,distrito,peso_kg,estado,contratante"]
            for pedido in SERVICIO.pedidos:
                lineas.append(
                    f"{pedido['pedido_id']},{pedido['distrito']},{pedido['peso_kg']},{pedido['estado']},{pedido.get('contratante_email', '')}"
                )
            self._json(200, {"ok": True, "archivo": "pedidos.csv", "contenido": "\n".join(lineas)})
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
            if ruta == "/api/vehiculos":
                if not self._exigir_rol(OPERAR):
                    return
                creado = SERVICIO.crear_vehiculo(cuerpo.get("placa", ""), float(cuerpo.get("capacidad_kg", 0)))
                self._json(201, {"ok": True, "vehiculo": creado})
                return
            if ruta == "/api/puntos":
                if not self._exigir_rol(OPERAR):
                    return
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
                usuario = self._exigir_rol(PEDIDO)
                if not usuario:
                    return
                contratante = cuerpo.get("contratante_email", "")
                if usuario["rol"] == "Contratante":
                    contratante = usuario["email"]
                creado = SERVICIO.crear_pedido(
                    int(cuerpo.get("punto_id", 0)),
                    float(cuerpo.get("peso_kg", 0)),
                    cuerpo.get("tipo_carga", ""),
                    contratante,
                )
                self._json(201, {"ok": True, "pedido": creado})
                return
            if ruta == "/api/usuarios":
                if not self._exigir_rol(("Administrador",)):
                    return
                creado = SERVICIO.crear_usuario(
                    cuerpo.get("email", ""),
                    cuerpo.get("nombre", ""),
                    cuerpo.get("rol", ""),
                    cuerpo.get("password", ""),
                )
                self._json(201, {"ok": True, "usuario": creado})
                return
            if ruta == "/api/rutas":
                if not self._exigir_rol(PLAN):
                    return
                resultado = SERVICIO.generar_ruta()
                self._json(201 if resultado["ok"] else 400, resultado)
                return
            if ruta == "/api/rutas/reoptimizar":
                if not self._exigir_rol(PLAN):
                    return
                resultado = SERVICIO.reoptimizar()
                self._json(201 if resultado["ok"] else 400, resultado)
                return
            if ruta == "/api/entregas":
                if not self._exigir_rol(ENTREGA):
                    return
                pedido = SERVICIO.registrar_entrega(
                    int(cuerpo.get("pedido_id", 0)),
                    cuerpo.get("resultado", ""),
                    cuerpo.get("motivo", ""),
                )
                self._json(200, {"ok": True, "pedido": pedido})
                return
            if ruta == "/api/ejemplo":
                if not self._exigir_rol(OPERAR):
                    return
                self._json(200, SERVICIO.cargar_ejemplo())
                return
        except (TypeError, ValueError) as exc:
            self._json(400, {"ok": False, "mensaje": str(exc)})
            return
        self._json(404, {"ok": False, "mensaje": "Ruta no encontrada."})

    def do_PUT(self):
        ruta = urlparse(self.path).path
        try:
            cuerpo = self._leer()
        except json.JSONDecodeError:
            self._json(400, {"ok": False, "mensaje": "El cuerpo no es JSON válido."})
            return
        try:
            if ruta == "/api/usuarios":
                if not self._exigir_rol(("Administrador",)):
                    return
                actualizado = SERVICIO.modificar_usuario(
                    cuerpo.get("email", ""),
                    cuerpo.get("nombre", ""),
                    cuerpo.get("estado", ""),
                )
                self._json(200, {"ok": True, "usuario": actualizado})
                return
            if ruta == "/api/vehiculos":
                if not self._exigir_rol(OPERAR):
                    return
                actualizado = SERVICIO.modificar_vehiculo(
                    int(cuerpo.get("vehiculo_id", 0)),
                    float(cuerpo.get("capacidad_kg", 0)),
                    cuerpo.get("estado", ""),
                    cuerpo.get("conductor_email", ""),
                )
                self._json(200, {"ok": True, "vehiculo": actualizado})
                return
            if ruta == "/api/puntos":
                if not self._exigir_rol(OPERAR):
                    return
                actualizado = SERVICIO.modificar_punto(
                    int(cuerpo.get("punto_id", 0)),
                    cuerpo.get("nombre", ""),
                    cuerpo.get("direccion", ""),
                    float(cuerpo.get("latitud", 0)),
                    float(cuerpo.get("longitud", 0)),
                    cuerpo.get("distrito", ""),
                )
                self._json(200, {"ok": True, "punto": actualizado})
                return
            if ruta == "/api/pedidos":
                if not self._exigir_rol(OPERAR):
                    return
                actualizado = SERVICIO.modificar_pedido(
                    int(cuerpo.get("pedido_id", 0)),
                    int(cuerpo.get("punto_id", 0)),
                    float(cuerpo.get("peso_kg", 0)),
                )
                self._json(200, {"ok": True, "pedido": actualizado})
                return
            if ruta == "/api/parametros":
                if not self._exigir_rol(("Administrador",)):
                    return
                actualizado = SERVICIO.actualizar_parametros(
                    float(cuerpo.get("factor_emision_kg_por_km", 0)),
                    float(cuerpo.get("velocidad_kmh", 0)),
                )
                self._json(200, {"ok": True, "parametros": actualizado})
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
        tipos = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "text/javascript; charset=utf-8",
            ".svg": "image/svg+xml",
        }
        datos = archivo.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", tipos.get(archivo.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)


def main() -> None:
    servidor = ThreadingHTTPServer(("127.0.0.1", 8765), Manejador)
    print("EcoLogística en http://127.0.0.1:8765", flush=True)
    servidor.serve_forever()


if __name__ == "__main__":
    main()
