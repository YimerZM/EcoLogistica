import unittest
from datetime import datetime, timedelta

from ecologistica.reglas import carga_prohibida, coordenada_valida, preparar_contador, registrar_fallo
from ecologistica.servicio import Servicio


class ReglasTest(unittest.TestCase):
    def test_el_contador_se_restablece_al_iniciar_si_el_bloqueo_vencio(self):
        ahora = datetime(2026, 10, 1, 12, 0, 0)
        usuario = {"intentos_fallidos": 3, "bloqueado_hasta": ahora - timedelta(minutes=1)}
        self.assertEqual(preparar_contador(usuario, ahora), "continuar")
        self.assertEqual(usuario["intentos_fallidos"], 0)
        self.assertIsNone(usuario["bloqueado_hasta"])

    def test_el_bloqueo_vigente_no_se_limpia_al_iniciar(self):
        ahora = datetime(2026, 10, 1, 12, 0, 0)
        usuario = {"intentos_fallidos": 3, "bloqueado_hasta": ahora + timedelta(minutes=10)}
        self.assertEqual(preparar_contador(usuario, ahora), "bloqueado")
        self.assertEqual(usuario["intentos_fallidos"], 3)

    def test_al_tercer_fallo_bloquea_quince_minutos(self):
        ahora = datetime(2026, 10, 1, 12, 0, 0)
        usuario = {"intentos_fallidos": 2, "bloqueado_hasta": None}
        registrar_fallo(usuario, ahora)
        self.assertEqual(usuario["bloqueado_hasta"], ahora + timedelta(minutes=15))

    def test_rechaza_carga_prohibida_y_acepta_general(self):
        self.assertTrue(carga_prohibida("explosivo"))
        self.assertFalse(carga_prohibida(" general "))

    def test_la_geolocalizacion_exige_los_tres_distritos(self):
        self.assertIsNone(coordenada_valida(-12.07, -75.21, "Huancayo"))
        self.assertIsNotNone(coordenada_valida(-12.07, -75.21, "Lima"))


class ServicioTest(unittest.TestCase):
    def test_login_valido_despues_de_un_fallo_no_deja_el_contador_como_condicion_de_acceso(self):
        reloj = {"ahora": datetime(2026, 10, 1, 8, 0, 0)}
        servicio = Servicio(ahora=lambda: reloj["ahora"])
        fallo = servicio.iniciar_sesion("operador@ecologistica.test", "mala")
        self.assertFalse(fallo["ok"])
        ok = servicio.iniciar_sesion("operador@ecologistica.test", "operador123")
        self.assertTrue(ok["ok"])
        self.assertEqual(ok["rol"], "Operador")

    def test_pedido_prohibido_no_se_guarda(self):
        servicio = Servicio()
        punto = servicio.crear_punto("Mercado", "Jr. Real", -12.07, -75.21, "Huancayo")
        with self.assertRaises(ValueError):
            servicio.crear_pedido(punto["punto_id"], 10, "residuo peligroso")
        self.assertEqual(servicio.pedidos, [])
        pedido = servicio.crear_pedido(punto["punto_id"], 10, "GENERAL")
        self.assertEqual(pedido["estado"], "PENDIENTE")


if __name__ == "__main__":
    unittest.main()
