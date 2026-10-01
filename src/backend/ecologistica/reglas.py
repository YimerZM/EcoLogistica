"""Reglas de negocio puras del incremento del Sprint 2."""

from datetime import datetime, timedelta

BLOQUEO_MINUTOS = 15
MAX_INTENTOS = 3
DISTRITOS = ("El Tambo", "Huancayo", "Chilca")
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


def coordenada_valida(latitud: float, longitud: float, distrito: str) -> str | None:
    if distrito not in DISTRITOS:
        return "El distrito debe ser El Tambo, Huancayo o Chilca."
    if not (LAT_MIN <= latitud <= LAT_MAX and LON_MIN <= longitud <= LON_MAX):
        return "La coordenada WGS84 queda fuera de El Tambo, Huancayo y Chilca."
    return None
