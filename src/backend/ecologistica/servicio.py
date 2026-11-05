"""Casos de uso en memoria del incremento."""

import hashlib
import math
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


def _distancia_km(origen: tuple, destino: tuple) -> float:
    radio = 6371.0
    lat1, lon1 = math.radians(origen[0]), math.radians(origen[1])
    lat2, lon2 = math.radians(destino[0]), math.radians(destino[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * radio * math.asin(math.sqrt(a))


class Servicio:
    def __init__(self, ahora=None):
        self._ahora = ahora or datetime.now
        self.usuarios = {}
        self.sesiones = {}
        self.vehiculos = []
        self.puntos = []
        self.pedidos = []
        self.rutas = []
        self.auditoria = []
        self.cambio_operativo = False
        self.parametros = {
            "factor_emision_kg_por_km": 0.21,
            "velocidad_kmh": 28,
        }
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
        self._cuenta("planificador@ecologistica.test", "Planificador de rutas", "Planificador", "plan12345")
        self._cuenta("conductor@ecologistica.test", "Conductor de ruta", "Conductor", "conductor1")
        self._cuenta("responsable@ecologistica.test", "Responsable de operaciones", "Responsable", "responsable1")
        self._cuenta("auditor@ecologistica.test", "Auditor", "Auditor", "auditor123")

    def _cuenta(self, email: str, nombre: str, rol: str, clave: str) -> None:
        self.usuarios[email] = {
            "email": email,
            "nombre": nombre,
            "rol": rol,
            "password_hash": _hash(clave),
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "estado": "ACTIVO",
        }

    def iniciar_sesion(self, email: str, password: str) -> dict:
        ahora = self._ahora()
        usuario = self.usuarios.get(email.strip().lower())
        if usuario is None or usuario["estado"] != "ACTIVO":
            self._auditar(email.strip().lower(), "Iniciar sesión", "RECHAZADO", "Credenciales no válidas.")
            return {"ok": False, "mensaje": "Credenciales no válidas."}

        # El contador se evalúa al comenzar, no después de conceder el acceso.
        estado = preparar_contador(usuario, ahora)
        if estado == "bloqueado":
            self._auditar(usuario["email"], "Iniciar sesión", "RECHAZADO", "Bloqueo de 15 minutos vigente.")
            return {
                "ok": False,
                "mensaje": "Usuario bloqueado. El contador se restablece al iniciar una sesión cuando venzan los 15 minutos.",
            }

        if usuario["password_hash"] != _hash(password):
            registrar_fallo(usuario, ahora)
            self._auditar(usuario["email"], "Iniciar sesión", "RECHAZADO", "Credenciales no válidas.")
            return {"ok": False, "mensaje": "Credenciales no válidas."}

        token = secrets.token_hex(16)
        self.sesiones[token] = usuario["email"]
        self._auditar(usuario["email"], "Iniciar sesión", "OK", usuario["rol"])
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
        self._auditar(email, "Registrar usuario", "OK", rol)
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
        self._auditar(email, "Modificar usuario", "OK", estado)
        return self._publico(usuario)

    def generar_ruta(self) -> dict:
        resultado = propuesta_de_ruta(self.pedidos, self.vehiculos, self.puntos)
        if not resultado["ok"]:
            return resultado
        for ruta in resultado["rutas"]:
            ruta["ruta_id"] = self._id()
            ruta["estado"] = "ACTIVA"
            ruta["fecha"] = self._ahora().isoformat(timespec="minutes")
            ruta["km"] = self._km(ruta["paradas"])
            self.rutas.append(ruta)
            vehiculo = next(v for v in self.vehiculos if v["vehiculo_id"] == ruta["vehiculo_id"])
            vehiculo["estado"] = "EN_RUTA"
            ruta["conductor_email"] = vehiculo.get("conductor_email", "")
            for parada in ruta["paradas"]:
                pedido = next(p for p in self.pedidos if p["pedido_id"] == parada["pedido_id"])
                pedido["estado"] = "EN_RUTA"
                pedido["ruta_id"] = ruta["ruta_id"]
        self._auditar("sistema", "Generar ruta", "OK", f"{len(resultado['rutas'])} ruta(s)")
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
            "conductor_email": "",
        }
        self.vehiculos.append(vehiculo)
        self._auditar("sistema", "Registrar vehículo", "OK", placa)
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
        self._auditar("sistema", "Registrar punto", "OK", punto["nombre"])
        return punto

    def crear_pedido(self, punto_id: int, peso_kg: float, tipo_carga: str, contratante_email: str = "") -> dict:
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
            "contratante_email": contratante_email.strip().lower(),
            "fecha": self._ahora().isoformat(timespec="minutes"),
            "ruta_id": None,
            "incidencia": "",
        }
        self.pedidos.append(pedido)
        if self.rutas:
            self.cambio_operativo = True
        self._auditar("sistema", "Registrar pedido", "OK", f"Pedido {pedido['pedido_id']}")
        return pedido

    def modificar_vehiculo(self, vehiculo_id: int, capacidad_kg: float, estado: str, conductor_email: str) -> dict:
        vehiculo = next((v for v in self.vehiculos if v["vehiculo_id"] == vehiculo_id), None)
        if vehiculo is None:
            raise ValueError("El vehículo no existe.")
        if capacidad_kg <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")
        if estado not in ("DISPONIBLE", "NO_DISPONIBLE", "EN_RUTA"):
            raise ValueError("El estado del vehículo no es válido.")
        vehiculo["capacidad_kg"] = capacidad_kg
        vehiculo["estado"] = estado
        vehiculo["conductor_email"] = conductor_email.strip().lower()
        self._auditar("sistema", "Modificar vehículo", "OK", vehiculo["placa"])
        return vehiculo

    def modificar_punto(self, punto_id: int, nombre: str, direccion: str, latitud: float, longitud: float, distrito: str) -> dict:
        punto = next((p for p in self.puntos if p["punto_id"] == punto_id), None)
        if punto is None:
            raise ValueError("El punto de entrega no existe.")
        if not nombre.strip() or not direccion.strip():
            raise ValueError("Nombre y dirección son obligatorios.")
        error = coordenada_valida(latitud, longitud, distrito)
        if error:
            raise ValueError(error)
        punto.update(
            {
                "nombre": nombre.strip(),
                "direccion": direccion.strip(),
                "latitud": latitud,
                "longitud": longitud,
                "distrito": distrito,
            }
        )
        self.cambio_operativo = True
        self._auditar("sistema", "Modificar punto", "OK", punto["nombre"])
        return punto

    def modificar_pedido(self, pedido_id: int, punto_id: int, peso_kg: float) -> dict:
        pedido = next((p for p in self.pedidos if p["pedido_id"] == pedido_id), None)
        if pedido is None:
            raise ValueError("No existe información disponible para ese pedido.")
        if pedido["estado"] != "PENDIENTE":
            raise ValueError("Solo se modifica un pedido antes de planificarlo.")
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor que cero.")
        punto = next((p for p in self.puntos if p["punto_id"] == punto_id), None)
        if punto is None:
            raise ValueError("El punto de entrega no existe.")
        pedido["punto_id"] = punto_id
        pedido["distrito"] = punto["distrito"]
        pedido["peso_kg"] = peso_kg
        self.cambio_operativo = True
        self._auditar("sistema", "Modificar pedido", "OK", f"Pedido {pedido_id}")
        return pedido

    def registrar_entrega(self, pedido_id: int, resultado: str, motivo: str) -> dict:
        pedido = next((p for p in self.pedidos if p["pedido_id"] == pedido_id), None)
        if pedido is None:
            raise ValueError("No existe información disponible para ese pedido.")
        if pedido["estado"] != "EN_RUTA":
            raise ValueError("El pedido no está asignado a una ruta. No se puede registrar la entrega.")
        if resultado == "ENTREGADO":
            pedido["estado"] = "ENTREGADO"
            pedido["incidencia"] = ""
        elif resultado == "INCIDENCIA":
            if not motivo.strip():
                raise ValueError("Registre la incidencia antes de cerrar la entrega.")
            pedido["estado"] = "INCIDENCIA"
            pedido["incidencia"] = motivo.strip()
        else:
            raise ValueError("El resultado debe ser ENTREGADO o INCIDENCIA.")
        self.cambio_operativo = True
        self._auditar("sistema", "Registrar entrega", "OK", f"Pedido {pedido_id} {pedido['estado']}")
        return pedido

    def reoptimizar(self) -> dict:
        if not any(r.get("estado") == "ACTIVA" for r in self.rutas):
            return {"ok": False, "mensaje": "No hay una ruta activa para reoptimizar."}
        if not self.cambio_operativo:
            return {"ok": False, "mensaje": "No hay un cambio operativo registrado. La reoptimización no se ejecutó."}
        for pedido in self.pedidos:
            if pedido["estado"] == "EN_RUTA":
                pedido["estado"] = "PENDIENTE"
                pedido["ruta_id"] = None
        for vehiculo in self.vehiculos:
            if vehiculo["estado"] == "EN_RUTA":
                vehiculo["estado"] = "DISPONIBLE"
        for ruta in self.rutas:
            if ruta.get("estado") == "ACTIVA":
                ruta["estado"] = "REEMPLAZADA"
        self.cambio_operativo = False
        resultado = self.generar_ruta()
        if resultado["ok"]:
            resultado["mensaje"] = "Ruta reoptimizada con la información actual."
            self._auditar("sistema", "Reoptimizar ruta", "OK", resultado["mensaje"])
        return resultado

    def ruta_por_id(self, ruta_id: int) -> dict:
        ruta = next((r for r in self.rutas if r["ruta_id"] == ruta_id), None)
        if ruta is None:
            return {"ok": False, "mensaje": "La ruta no está disponible."}
        return {"ok": True, "ruta": ruta}

    def indicadores(self, periodo: str, rol: str, email: str) -> dict:
        if periodo == "vacio":
            return {"ok": False, "mensaje": "No existen datos para realizar el cálculo."}
        pedidos = list(self.pedidos)
        rutas = [r for r in self.rutas if r.get("estado") == "ACTIVA" and "km" in r]
        if rol == "Contratante":
            pedidos = [p for p in pedidos if p.get("contratante_email") == email]
            rutas = []
        if periodo == "hoy":
            hoy = self._ahora().date().isoformat()
            pedidos = [p for p in pedidos if str(p.get("fecha", "")).startswith(hoy)]
            rutas = [r for r in rutas if str(r.get("fecha", "")).startswith(hoy)]
        if not pedidos and not rutas:
            return {"ok": False, "mensaje": "No existen datos para realizar el cálculo.", "periodo": periodo}
        km = round(sum(float(r.get("km", 0)) for r in rutas), 2)
        return {
            "ok": True,
            "periodo": "Hoy" if periodo == "hoy" else "Todo el registro",
            "pendientes": sum(1 for p in pedidos if p["estado"] == "PENDIENTE"),
            "en_ruta": sum(1 for p in pedidos if p["estado"] == "EN_RUTA"),
            "entregados": sum(1 for p in pedidos if p["estado"] == "ENTREGADO"),
            "incidencias": sum(1 for p in pedidos if p["estado"] == "INCIDENCIA"),
            "kg": round(sum(float(p["peso_kg"]) for p in pedidos), 2),
            "km": km,
            "co2_kg": round(km * float(self.parametros["factor_emision_kg_por_km"]), 2),
            "factor": self.parametros["factor_emision_kg_por_km"],
        }

    def actualizar_parametros(self, factor: float, velocidad: float) -> dict:
        if factor <= 0 or velocidad <= 0:
            raise ValueError("El factor de emisión y la velocidad deben ser mayores que cero.")
        self.parametros["factor_emision_kg_por_km"] = factor
        self.parametros["velocidad_kmh"] = velocidad
        self._auditar("sistema", "Modificar parámetro", "OK", f"{factor} kg/km")
        return self.parametros

    def cargar_ejemplo(self) -> dict:
        if any(v["placa"] == "ECO-101" for v in self.vehiculos):
            return {"ok": False, "mensaje": "El recorrido de demostración ya está cargado."}
        self.crear_vehiculo("ECO-101", 800)
        self.crear_vehiculo("ECO-202", 450)
        next(v for v in self.vehiculos if v["placa"] == "ECO-101")["conductor_email"] = "conductor@ecologistica.test"
        tambo = self.crear_punto("Parque Constitución", "El Tambo", -12.05, -75.23, "El Tambo")
        centro = self.crear_punto("Mercado Modelo", "Jr. Real", -12.07, -75.21, "Huancayo")
        chilca = self.crear_punto("Plaza de Chilca", "Av. Mariscal Castilla", -12.12, -75.20, "Chilca")
        self.crear_pedido(tambo["punto_id"], 18, "GENERAL", "cliente@ecologistica.test")
        self.crear_pedido(centro["punto_id"], 12, "GENERAL", "cliente@ecologistica.test")
        self.crear_pedido(chilca["punto_id"], 22, "GENERAL")
        return {"ok": True, "mensaje": "Recorrido de demostración listo en los tres distritos."}

    def _km(self, paradas: list) -> float:
        base = (-12.068, -75.210)
        puntos = [base] + [(p["latitud"], p["longitud"]) for p in paradas]
        total = 0.0
        for origen, destino in zip(puntos, puntos[1:]):
            total += _distancia_km(origen, destino)
        return round(total, 2)

    def _auditar(self, email: str, operacion: str, resultado: str, detalle: str) -> None:
        self.auditoria.append(
            {
                "auditoria_id": len(self.auditoria) + 1,
                "email": email or "sistema",
                "operacion": operacion,
                "fecha": self._ahora().isoformat(timespec="seconds"),
                "resultado": resultado,
                "detalle": detalle,
            }
        )
