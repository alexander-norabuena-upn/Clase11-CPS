"""Pruebas de integración ligera de la API con el cliente de pruebas de Flask."""

import unittest

from app.api import crear_app


class TestApi(unittest.TestCase):
    def setUp(self):
        self.cliente = crear_app().test_client()

    def test_salud(self):
        respuesta = self.cliente.get("/salud")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json()["estado"], "ok")

    def test_cotizar_valido(self):
        respuesta = self.cliente.post(
            "/api/cotizar", json={"peso_kg": 5, "destino": "Tarma", "servicio": "estandar"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.get_json()["monto"], "23.13")

    def test_cotizar_sin_peso_devuelve_400(self):
        respuesta = self.cliente.post("/api/cotizar", json={"destino": "Lima"})
        self.assertEqual(respuesta.status_code, 400)


if __name__ == "__main__":
    unittest.main()
