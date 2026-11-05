"""Recorrido de extremo a extremo contra la misma API que usa la página."""

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from ecologistica.servidor import Manejador


class ExtremoAExtremoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = ThreadingHTTPServer(("127.0.0.1", 0), Manejador)
        cls.hilo = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.hilo.start()
        cls.base = f"http://127.0.0.1:{cls.servidor.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.hilo.join(timeout=3)

    def llamar(self, ruta, cuerpo=None, token=None):
        datos = None if cuerpo is None else json.dumps(cuerpo).encode("utf-8")
        encabezados = {}
        if cuerpo is not None:
            encabezados["Content-Type"] = "application/json"
        if token:
            encabezados["Authorization"] = f"Bearer {token}"
        peticion = urllib.request.Request(self.base + ruta, data=datos, headers=encabezados)
        try:
            with urllib.request.urlopen(peticion) as respuesta:
                return respuesta.status, json.loads(respuesta.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            cuerpo = json.loads(error.read().decode("utf-8"))
            error.close()
            return error.code, cuerpo

    def test_recorrido_del_nucleo_operativo(self):
        codigo, malo = self.llamar(
            "/api/sesion",
            {"email": "operador@ecologistica.test", "password": "mala"},
        )
        self.assertEqual(codigo, 200)
        self.assertFalse(malo["ok"])

        codigo, sesion = self.llamar(
            "/api/sesion",
            {"email": "operador@ecologistica.test", "password": "operador123"},
        )
        self.assertTrue(sesion["ok"])
        token = sesion["token"]

        codigo, vehiculo = self.llamar(
            "/api/vehiculos",
            {"placa": "ABC-123", "capacidad_kg": 800},
            token,
        )
        self.assertEqual(codigo, 201)
        self.assertEqual(vehiculo["vehiculo"]["estado"], "DISPONIBLE")

        codigo, lima = self.llamar(
            "/api/puntos",
            {
                "nombre": "Fuera",
                "direccion": "Centro",
                "latitud": -12.04,
                "longitud": -77.03,
                "distrito": "Lima",
            },
            token,
        )
        self.assertEqual(codigo, 400)

        codigo, punto = self.llamar(
            "/api/puntos",
            {
                "nombre": "Mercado",
                "direccion": "Jr. Real",
                "latitud": -12.07,
                "longitud": -75.21,
                "distrito": "Huancayo",
            },
            token,
        )
        self.assertEqual(codigo, 201)
        self.assertEqual(punto["punto"]["metodo_geolocalizacion"], "WGS84")

        codigo, prohibido = self.llamar(
            "/api/pedidos",
            {"punto_id": punto["punto"]["punto_id"], "peso_kg": 10, "tipo_carga": "explosivo"},
            token,
        )
        self.assertEqual(codigo, 400)

        codigo, pedido = self.llamar(
            "/api/pedidos",
            {"punto_id": punto["punto"]["punto_id"], "peso_kg": 10, "tipo_carga": "GENERAL"},
            token,
        )
        self.assertEqual(codigo, 201)
        self.assertEqual(pedido["pedido"]["estado"], "PENDIENTE")

        codigo, lista = self.llamar("/api/pedidos", token=token)
        self.assertEqual(codigo, 200)
        self.assertEqual(len(lista["pedidos"]), 1)


if __name__ == "__main__":
    unittest.main()
