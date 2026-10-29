"""Pruebas unitarias del cotizador (escritas con unittest; pytest también las ejecuta)."""

import unittest
from decimal import Decimal

from app.cotizador import CotizacionInvalida, cotizar, tarifa_base


class TestTramosDePeso(unittest.TestCase):
    """Valores límite de los tramos de peso (técnica de análisis de valores límite)."""

    def test_peso_minimo_aceptado(self):
        self.assertEqual(tarifa_base(0.1), Decimal("12.00"))

    def test_debajo_del_minimo_es_rechazado(self):
        with self.assertRaises(CotizacionInvalida):
            tarifa_base(0.09)

    def test_limite_superior_primer_tramo(self):
        self.assertEqual(tarifa_base(1), Decimal("12.00"))

    def test_justo_encima_de_1_kg(self):
        self.assertEqual(tarifa_base(1.01), Decimal("18.50"))

    def test_limite_superior_segundo_tramo_5_kg(self):
        # Requisito HU-01: un envío de exactamente 5 kg pertenece al segundo tramo.
        self.assertEqual(tarifa_base(5), Decimal("18.50"))

    def test_justo_encima_de_5_kg(self):
        self.assertEqual(tarifa_base(5.01), Decimal("29.00"))

    def test_peso_maximo_aceptado(self):
        self.assertEqual(tarifa_base(20), Decimal("29.00"))

    def test_encima_del_maximo_es_rechazado(self):
        with self.assertRaises(CotizacionInvalida):
            tarifa_base(20.01)


class TestCotizacion(unittest.TestCase):
    """Reglas de recargos y destinos."""

    def test_estandar_huancayo(self):
        self.assertEqual(cotizar(3, "Huancayo"), Decimal("18.50"))

    def test_express_aplica_35_por_ciento(self):
        self.assertEqual(cotizar(3, "Huancayo", servicio="express"), Decimal("24.98"))

    def test_fragil_suma_recargo_fijo(self):
        self.assertEqual(cotizar(0.5, "Jauja", fragil=True), Decimal("17.20"))

    def test_selva_central_con_mayusculas(self):
        # El destino debe reconocerse sin importar mayúsculas ni espacios.
        self.assertEqual(cotizar(2, "  Satipo "), Decimal("35.60"))

    def test_destino_con_tilde(self):
        self.assertEqual(cotizar(1, "Concepción"), Decimal("13.20"))

    def test_destino_sin_cobertura(self):
        with self.assertRaises(CotizacionInvalida):
            cotizar(2, "Iquitos")

    def test_servicio_desconocido(self):
        with self.assertRaises(CotizacionInvalida):
            cotizar(2, "Lima", servicio="nocturno")


if __name__ == "__main__":
    unittest.main()
