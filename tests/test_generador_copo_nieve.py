
from modules.generadores import GeneradorCopoNieve
import math
import unittest

class TestGeneradorCopoNieve(unittest.TestCase):
    def test_cantidad_de_puntos_por_nivel(self):
        for nivel in range(7):
            with self.subTest(nivel=nivel):
                curva = GeneradorCopoNieve(nivel).generar()
                self.assertEqual(curva.cantidad_puntos(), 3 * (4 ** nivel) + 1)

    def test_curva_cerrada(self):
        curva = GeneradorCopoNieve(2).generar()
        primero = curva.puntos[0]
        ultimo = curva.puntos[-1]
        self.assertAlmostEqual(primero.x, ultimo.x)
        self.assertAlmostEqual(primero.y, ultimo.y)

    def test_nivel_cero_es_triangulo_equilatero_cerrado(self):
        curva = GeneradorCopoNieve(0).generar()
        self.assertEqual(curva.cantidad_puntos(), 4)
        lados = [curva.puntos[i].distancia_a(curva.puntos[i + 1]) for i in range(3)]
        for lado in lados:
            self.assertAlmostEqual(lado, 1.0)

    def test_nivel_invalido(self):
        for nivel in (-1, 7, 1.5, True):
            with self.subTest(nivel=nivel):
                with self.assertRaises(ValueError):
                    GeneradorCopoNieve(nivel)

if __name__ == '__main__':
    unittest.main()

