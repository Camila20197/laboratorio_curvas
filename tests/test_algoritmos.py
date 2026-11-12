"""Pruebas unitarias de modules/algoritmos.py."""
import math
import unittest

from modules.algoritmos import AlgoritmoNumerico, Biseccion, SinCambioDeSignoError
from modules.resultados import ResultadoBiseccion


class FuncionStub:
    """Doble de prueba (stub) que reemplaza a las clases FuncionMatematica del grupo.
    Por duck typing, alcanza con que tenga el método evaluar(x)."""

    def __init__(self, p_regla):
        self.__regla = p_regla

    def evaluar(self, p_x):
        return self.__regla(p_x)


class AlgoritmoDePrueba(AlgoritmoNumerico):
    """Doble de prueba: subclase mínima para poder probar el método concreto
    _validar_intervalo de la clase abstracta."""

    def calcular(self, p_funcion, p_a, p_b):
        self._validar_intervalo(p_a, p_b)
        return None


class TestAlgoritmoNumerico(unittest.TestCase):

    def test_no_se_puede_instanciar_la_clase_abstracta(self):
        with self.assertRaises(TypeError):
            AlgoritmoNumerico()

    def test_validar_intervalo_acepta_a_menor_que_b(self):
        AlgoritmoDePrueba().calcular(None, 0, 1)   # no debe lanzar excepción

    def test_validar_intervalo_rechaza_a_mayor_que_b(self):
        with self.assertRaises(ValueError):
            AlgoritmoDePrueba().calcular(None, 2, 1)

    def test_validar_intervalo_rechaza_a_igual_a_b(self):
        with self.assertRaises(ValueError):
            AlgoritmoDePrueba().calcular(None, 1, 1)


class TestSinCambioDeSignoError(unittest.TestCase):

    def test_hereda_de_value_error(self):
        self.assertTrue(issubclass(SinCambioDeSignoError, ValueError))

    def test_se_captura_como_value_error(self):
        with self.assertRaises(ValueError):
            raise SinCambioDeSignoError("f(a) y f(b) tienen el mismo signo")


class TestBiseccion(unittest.TestCase):

    def setUp(self):
        self.cuadratica = FuncionStub(lambda x: x ** 2 - 2)      # raíz: raíz cuadrada de 2

    # --- Casos habituales ---
    def test_b1_raiz_de_x2_menos_2(self):
        resultado = Biseccion(p_tolerancia=1e-6).calcular(self.cuadratica, 1, 2)
        self.assertIsInstance(resultado, ResultadoBiseccion)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), delta=1e-6)
        self.assertTrue(resultado.convergio)
        self.assertLessEqual(resultado.error_estimado, 1e-6)

    def test_b2_raiz_de_polinomio_cubico(self):
        cubica = FuncionStub(lambda x: x ** 3 - x - 2)            # raíz ≈ 1.5213797068
        resultado = Biseccion(p_tolerancia=1e-8).calcular(cubica, 1, 2)
        self.assertAlmostEqual(resultado.raiz, 1.5213797068, delta=1e-8)
        self.assertLessEqual(resultado.error_estimado, 1e-8)

    # --- Casos límite ---
    def test_b3_extremo_a_es_raiz(self):
        resultado = Biseccion().calcular(FuncionStub(lambda x: x - 1), 1, 3)
        self.assertEqual(resultado.raiz, 1)
        self.assertEqual(resultado.iteraciones, 0)
        self.assertTrue(resultado.convergio)

    def test_b4_extremo_b_es_raiz(self):
        resultado = Biseccion().calcular(FuncionStub(lambda x: x - 3), 1, 3)
        self.assertEqual(resultado.raiz, 3)
        self.assertEqual(resultado.iteraciones, 0)

    def test_b5_raiz_en_el_punto_medio(self):
        resultado = Biseccion().calcular(FuncionStub(lambda x: x), -1, 1)
        self.assertEqual(resultado.raiz, 0)
        self.assertEqual(resultado.iteraciones, 1)
        self.assertEqual(resultado.error_estimado, 0)

    # --- No alcanza el criterio de convergencia ---
    def test_b6_no_converge_por_maximo_de_iteraciones(self):
        resultado = Biseccion(1e-12, 3).calcular(self.cuadratica, 1, 2)
        self.assertFalse(resultado.convergio)
        self.assertEqual(resultado.iteraciones, 3)
        self.assertGreater(resultado.error_estimado, 1e-12)
        self.assertEqual(resultado.error_estimado, 1 / 16)   # (2 - 1) / 2^3 / 2

    # --- Entradas inválidas ---
    def test_b7_tolerancia_no_positiva(self):
        for tolerancia in (0, -1e-3):
            with self.assertRaises(ValueError):
                Biseccion(p_tolerancia=tolerancia)

    def test_b8_maximo_de_iteraciones_invalido(self):
        for maximo in (0, -5, 2.5):
            with self.assertRaises(ValueError):
                Biseccion(p_max_iteraciones=maximo)

    def test_b9_intervalo_invalido(self):
        with self.assertRaises(ValueError):
            Biseccion().calcular(self.cuadratica, 2, 1)

    def test_b10_sin_cambio_de_signo(self):
        with self.assertRaises(SinCambioDeSignoError):
            Biseccion().calcular(FuncionStub(lambda x: x ** 2 + 1), -1, 1)

    def test_b11_dos_raices_en_el_intervalo(self):
        with self.assertRaises(SinCambioDeSignoError):
            Biseccion().calcular(FuncionStub(lambda x: x ** 2 - 1), -2, 2)

    def test_b12_se_captura_como_value_error(self):
        with self.assertRaises(ValueError):
            Biseccion().calcular(FuncionStub(lambda x: x ** 2 + 1), -1, 1)

    # --- RF4: tolerancia "ó" número máximo de iteraciones ---
    def test_b13_solo_tolerancia(self):
        resultado = Biseccion(p_tolerancia=1e-3).calcular(self.cuadratica, 1, 2)
        self.assertTrue(resultado.convergio)
        self.assertLessEqual(resultado.error_estimado, 1e-3)

    def test_b14_solo_maximo_de_iteraciones(self):
        resultado = Biseccion(p_max_iteraciones=5).calcular(self.cuadratica, 1, 2)
        self.assertEqual(resultado.iteraciones, 5)
        self.assertFalse(resultado.convergio)   # tolerancia por defecto 1e-6 no se alcanza en 5

    def test_b15_tolerancia_y_maximo(self):
        resultado = Biseccion(1e-3, 50).calcular(self.cuadratica, 1, 2)
        self.assertTrue(resultado.convergio)
        self.assertLessEqual(resultado.iteraciones, 50)

    # --- Caso excepcional ---
    def test_b16_funcion_no_finita_en_un_extremo(self):
        with self.assertRaises(ValueError):
            Biseccion().calcular(FuncionStub(lambda x: math.inf if x == 1 else x), 1, 2)


if __name__ == "__main__":
    unittest.main()
