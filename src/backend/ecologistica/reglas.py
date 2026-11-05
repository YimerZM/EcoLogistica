"""Reglas de negocio puras del incremento."""

from datetime import datetime, timedelta

BLOQUEO_MINUTOS = 15
MAX_INTENTOS = 3
DISTRITOS = ("El Tambo", "Huancayo", "Chilca")
ROLES = (
    "Administrador",
    "Operador",
    "Planificador",
    "Conductor",
    "Responsable",
    "Auditor",
    "Contratante",
)
# Caja aproximada de la provincia de Huancayo donde están los tres distritos.
LAT_MIN, LAT_MAX = -12.20, -11.90
LON_MIN, LON_MAX = -75.40, -75.00


def carga_prohibida(tipo_carga: str) -> bool:
    """RN-016: solo se acepta carga general."""
    return tipo_carga.strip().lower() != "general"


def preparar_contador(usuario: dict, ahora: datetime) -> str:
    """Se ejecuta al iniciar el inicio de sesión, antes de validar la credencial.

    Si el bloqueo ya venció, el contador vuelve a cero en este momento.
    """
    hasta = usuario.get("bloqueado_hasta")
    if hasta is not None and hasta <= ahora:
        usuario["intentos_fallidos"] = 0
        usuario["bloqueado_hasta"] = None
    hasta = usuario.get("bloqueado_hasta")
    if hasta is not None and hasta > ahora:
        return "bloqueado"
    return "continuar"


def registrar_fallo(usuario: dict, ahora: datetime) -> None:
    usuario["intentos_fallidos"] = int(usuario.get("intentos_fallidos", 0)) + 1
    if usuario["intentos_fallidos"] >= MAX_INTENTOS:
        usuario["bloqueado_hasta"] = ahora + timedelta(minutes=BLOQUEO_MINUTOS)


def datos_usuario_validos(email: str, nombre: str, rol: str) -> str | None:
    if "@" not in email or not nombre.strip():
        return "Correo y nombre son obligatorios."
    if rol not in ROLES:
        return "El rol no corresponde a un perfil del sistema."
    return None


def propuesta_de_ruta(pedidos: list, vehiculos: list, puntos: list) -> dict:
    """US-006. Arma una propuesta por capacidad y ordena las paradas de norte a sur.

    No dibuja el mapa. Esa vista es US-007.
    """
    disponibles = [v for v in vehiculos if v.get("estado") == "DISPONIBLE"]
    pendientes = [p for p in pedidos if p.get("estado") == "PENDIENTE"]
    if not disponibles:
        return {"ok": False, "mensaje": "No es posible generar la ruta: no hay vehículos disponibles."}
    if not pendientes:
        return {"ok": False, "mensaje": "No hay pedidos pendientes para planificar."}

    por_punto = {p["punto_id"]: p for p in puntos}
    ordenados = sorted(
        pendientes,
        key=lambda pedido: (
            -por_punto[pedido["punto_id"]]["latitud"],
            por_punto[pedido["punto_id"]]["longitud"],
            pedido["pedido_id"],
        ),
    )
    cupo = {v["vehiculo_id"]: float(v["capacidad_kg"]) for v in disponibles}
    asignado = {v["vehiculo_id"]: [] for v in disponibles}
    sin_cupo = []
    for pedido in ordenados:
        elegido = next(
            (v for v in disponibles if cupo[v["vehiculo_id"]] >= float(pedido["peso_kg"])),
            None,
        )
        if elegido is None:
            sin_cupo.append(pedido["pedido_id"])
            continue
        cupo[elegido["vehiculo_id"]] -= float(pedido["peso_kg"])
        punto = por_punto[pedido["punto_id"]]
        paradas = asignado[elegido["vehiculo_id"]]
        paradas.append(
            {
                "orden": len(paradas) + 1,
                "pedido_id": pedido["pedido_id"],
                "punto_id": pedido["punto_id"],
                "nombre": punto["nombre"],
                "distrito": punto["distrito"],
                "latitud": punto["latitud"],
                "longitud": punto["longitud"],
                "peso_kg": pedido["peso_kg"],
            }
        )

    rutas = []
    for vehiculo in disponibles:
        paradas = asignado[vehiculo["vehiculo_id"]]
        if not paradas:
            continue
        rutas.append(
            {
                "placa": vehiculo["placa"],
                "vehiculo_id": vehiculo["vehiculo_id"],
                "capacidad_kg": vehiculo["capacidad_kg"],
                "peso_kg": round(sum(p["peso_kg"] for p in paradas), 3),
                "paradas": paradas,
            }
        )
    if not rutas:
        return {
            "ok": False,
            "mensaje": "Ningún vehículo tiene capacidad para los pedidos pendientes.",
            "sin_cupo": sin_cupo,
        }
    mensaje = "Propuesta de ruta generada."
    if sin_cupo:
        mensaje = "Propuesta generada. No hubo capacidad para todos los pedidos."
    return {"ok": True, "rutas": rutas, "sin_cupo": sin_cupo, "mensaje": mensaje}


def coordenada_valida(latitud: float, longitud: float, distrito: str) -> str | None:
    if distrito not in DISTRITOS:
        return "El distrito debe ser El Tambo, Huancayo o Chilca."
    if not (LAT_MIN <= latitud <= LAT_MAX and LON_MIN <= longitud <= LON_MAX):
        return "La coordenada WGS84 queda fuera de El Tambo, Huancayo y Chilca."
    return None
