"""Pruebas unitarias de modules/resultados.py (casos R1 a R4 + invariantes)."""
import unittest

from modules.resultados import Resultado, ResultadoBiseccion, ResultadoIntegracion


class TestResultado(unittest.TestCase):

    def test_r1_no_se_puede_instanciar_la_clase_abstracta(self):
        with self.assertRaises(TypeError):
            Resultado(0, 1)


class TestResultadoBiseccion(unittest.TestCase):

    def setUp(self):
        self.resultado = ResultadoBiseccion(1.0, 2.0, 1.4142, 20, True, 1e-6)

    def test_r2_getters_devuelven_los_valores_dados(self):
        self.assertEqual(self.resultado.a, 1.0)
        self.assertEqual(self.resultado.b, 2.0)
        self.assertEqual(self.resultado.raiz, 1.4142)
        self.assertEqual(self.resultado.iteraciones, 20)
        self.assertTrue(self.resultado.convergio)
        self.assertEqual(self.resultado.error_estimado, 1e-6)

    def test_r3_es_inmutable(self):
        with self.assertRaises(AttributeError):
            self.resultado.raiz = 5

    def test_r4_resumen_es_texto_con_los_datos_pedidos(self):
        texto = self.resultado.resumen()
        self.assertIsInstance(texto, str)
        self.assertIn("1.4142", texto)
        self.assertIn("20", texto)
        self.assertIn("alcanzado", texto)

    def test_resumen_indica_cuando_no_converge(self):
        resultado = ResultadoBiseccion(1.0, 2.0, 1.5, 3, False, 0.06)
        self.assertIn("NO alcanzado", resultado.resumen())

    def test_invariante_intervalo_invalido(self):
        with self.assertRaises(ValueError):
            ResultadoBiseccion(2.0, 1.0, 1.5, 1, True, 0.1)

    def test_invariante_raiz_fuera_del_intervalo(self):
        with self.assertRaises(ValueError):
            ResultadoBiseccion(1.0, 2.0, 3.0, 1, True, 0.1)

    def test_invariante_iteraciones_negativas(self):
        with self.assertRaises(ValueError):
            ResultadoBiseccion(1.0, 2.0, 1.5, -1, True, 0.1)

    def test_invariante_error_negativo(self):
        with self.assertRaises(ValueError):
            ResultadoBiseccion(1.0, 2.0, 1.5, 1, True, -0.1)


class TestResultadoIntegracion(unittest.TestCase):

    def test_r2_getters_devuelven_los_valores_dados(self):
        resultado = ResultadoIntegracion(0.0, 2.0, 2.6875, 4)
        self.assertEqual(resultado.a, 0.0)
        self.assertEqual(resultado.b, 2.0)
        self.assertEqual(resultado.valor, 2.6875)
        self.assertEqual(resultado.subintervalos, 4)

    def test_r3_es_inmutable(self):
        resultado = ResultadoIntegracion(0.0, 2.0, 2.6875, 4)
        with self.assertRaises(AttributeError):
            resultado.valor = 0

    def test_r4_resumen_es_texto_con_los_datos_pedidos(self):
        texto = ResultadoIntegracion(0.0, 2.0, 2.6875, 4).resumen()
        self.assertIsInstance(texto, str)
        self.assertIn("2.6875", texto)
        self.assertIn("4", texto)

    def test_invariante_valor_no_finito(self):
        with self.assertRaises(ValueError):
            ResultadoIntegracion(0.0, 1.0, float("inf"), 4)

    def test_invariante_subintervalos_menor_a_uno(self):
        with self.assertRaises(ValueError):
            ResultadoIntegracion(0.0, 1.0, 1.0, 0)


if __name__ == "__main__":
    unittest.main()
