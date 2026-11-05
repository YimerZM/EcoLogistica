"""Casos de uso en memoria del incremento."""

import hashlib
import secrets
from datetime import datetime

from ecologistica.reglas import (
    carga_prohibida,
    coordenada_valida,
    datos_usuario_validos,
    preparar_contador,
    propuesta_de_ruta,
    registrar_fallo,
)


def _hash(clave: str) -> str:
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


class Servicio:
    def __init__(self, ahora=None):
        self._ahora = ahora or datetime.now
        self.usuarios = {}
        self.sesiones = {}
        self.vehiculos = []
        self.puntos = []
        self.pedidos = []
        self.rutas = []
        self._sec = 0
        self._cargar_demo()

    def _id(self) -> int:
        self._sec += 1
        return self._sec

    def _cargar_demo(self) -> None:
        self.usuarios["operador@ecologistica.test"] = {
            "email": "operador@ecologistica.test",
            "nombre": "Operador logístico",
            "rol": "Operador",
            "password_hash": _hash("operador123"),
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "estado": "ACTIVO",
        }
        self.usuarios["administrador@ecologistica.test"] = {
            "email": "administrador@ecologistica.test",
            "nombre": "Administrador",
            "rol": "Administrador",
            "password_hash": _hash("admin123"),
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "estado": "ACTIVO",
        }

    def iniciar_sesion(self, email: str, password: str) -> dict:
        ahora = self._ahora()
        usuario = self.usuarios.get(email.strip().lower())
        if usuario is None or usuario["estado"] != "ACTIVO":
            return {"ok": False, "mensaje": "Credenciales no válidas."}

        # El contador se evalúa al comenzar, no después de conceder el acceso.
        estado = preparar_contador(usuario, ahora)
        if estado == "bloqueado":
            return {
                "ok": False,
                "mensaje": "Usuario bloqueado. El contador se restablece al iniciar una sesión cuando venzan los 15 minutos.",
            }

        if usuario["password_hash"] != _hash(password):
            registrar_fallo(usuario, ahora)
            return {"ok": False, "mensaje": "Credenciales no válidas."}

        token = secrets.token_hex(16)
        self.sesiones[token] = usuario["email"]
        return {
            "ok": True,
            "token": token,
            "nombre": usuario["nombre"],
            "rol": usuario["rol"],
            "intentos_fallidos": usuario["intentos_fallidos"],
        }

    def usuario_de(self, token: str) -> dict | None:
        email = self.sesiones.get(token or "")
        if not email:
            return None
        return self.usuarios.get(email)

    def listar_usuarios(self) -> list:
        return [self._publico(usuario) for usuario in self.usuarios.values()]

    def crear_usuario(self, email: str, nombre: str, rol: str, password: str) -> dict:
        email = email.strip().lower()
        error = datos_usuario_validos(email, nombre, rol)
        if error:
            raise ValueError(error)
        if len(password) < 8:
            raise ValueError("La clave debe tener al menos 8 caracteres.")
        if email in self.usuarios:
            raise ValueError("El correo ya está registrado.")
        usuario = {
            "email": email,
            "nombre": nombre.strip(),
            "rol": rol,
            "password_hash": _hash(password),
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "estado": "ACTIVO",
        }
        self.usuarios[email] = usuario
        return self._publico(usuario)

    def modificar_usuario(self, email: str, nombre: str, estado: str) -> dict:
        email = email.strip().lower()
        usuario = self.usuarios.get(email)
        if usuario is None:
            raise ValueError("El usuario no existe.")
        if not nombre.strip():
            raise ValueError("El nombre es obligatorio.")
        if estado not in ("ACTIVO", "INACTIVO"):
            raise ValueError("El estado debe ser ACTIVO o INACTIVO.")
        if usuario["rol"] == "Administrador" and estado == "INACTIVO":
            activos = [
                otro
                for otro in self.usuarios.values()
                if otro["rol"] == "Administrador" and otro["estado"] == "ACTIVO" and otro["email"] != email
            ]
            if not activos:
                raise ValueError("Debe quedar al menos un administrador activo.")
        usuario["nombre"] = nombre.strip()
        usuario["estado"] = estado
        return self._publico(usuario)

    def generar_ruta(self) -> dict:
        resultado = propuesta_de_ruta(self.pedidos, self.vehiculos, self.puntos)
        if not resultado["ok"]:
            return resultado
        for ruta in resultado["rutas"]:
            ruta["ruta_id"] = self._id()
            self.rutas.append(ruta)
            vehiculo = next(v for v in self.vehiculos if v["vehiculo_id"] == ruta["vehiculo_id"])
            vehiculo["estado"] = "EN_RUTA"
            for parada in ruta["paradas"]:
                pedido = next(p for p in self.pedidos if p["pedido_id"] == parada["pedido_id"])
                pedido["estado"] = "EN_RUTA"
        return resultado

    def _publico(self, usuario: dict) -> dict:
        return {
            "email": usuario["email"],
            "nombre": usuario["nombre"],
            "rol": usuario["rol"],
            "estado": usuario["estado"],
        }

    def crear_vehiculo(self, placa: str, capacidad_kg: float) -> dict:
        placa = placa.strip().upper()
        if not placa:
            raise ValueError("La placa es obligatoria.")
        if capacidad_kg <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")
        if any(v["placa"] == placa for v in self.vehiculos):
            raise ValueError("La placa ya está registrada.")
        vehiculo = {
            "vehiculo_id": self._id(),
            "placa": placa,
            "capacidad_kg": capacidad_kg,
            "estado": "DISPONIBLE",
        }
        self.vehiculos.append(vehiculo)
        return vehiculo

    def crear_punto(self, nombre: str, direccion: str, latitud: float, longitud: float, distrito: str) -> dict:
        if not nombre.strip() or not direccion.strip():
            raise ValueError("Nombre y dirección son obligatorios.")
        error = coordenada_valida(latitud, longitud, distrito)
        if error:
            raise ValueError(error)
        punto = {
            "punto_id": self._id(),
            "nombre": nombre.strip(),
            "direccion": direccion.strip(),
            "latitud": latitud,
            "longitud": longitud,
            "distrito": distrito,
            "metodo_geolocalizacion": "WGS84",
        }
        self.puntos.append(punto)
        return punto

    def crear_pedido(self, punto_id: int, peso_kg: float, tipo_carga: str) -> dict:
        if carga_prohibida(tipo_carga):
            raise ValueError(
                "RN-016: no se planifica el transporte de productos peligrosos o prohibidos."
            )
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor que cero.")
        punto = next((p for p in self.puntos if p["punto_id"] == punto_id), None)
        if punto is None:
            raise ValueError("El punto de entrega no existe.")
        pedido = {
            "pedido_id": self._id(),
            "punto_id": punto_id,
            "distrito": punto["distrito"],
            "peso_kg": peso_kg,
            "tipo_carga": "GENERAL",
            "estado": "PENDIENTE",
        }
        self.pedidos.append(pedido)
        return pedido
