"""Casos de uso en memoria para el incremento del Sprint 2."""

import hashlib
import secrets
from datetime import datetime

from ecologistica.reglas import (
    carga_prohibida,
    coordenada_valida,
    preparar_contador,
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
