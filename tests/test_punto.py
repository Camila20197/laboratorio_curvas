
from modules.geometria import Punto
import unittest

class TestPunto(unittest.TestCase):
    def test_crear_punto(self):
        punto = Punto(2, 3)

        self.assertEqual(punto.x, 2.0)
        self.assertEqual(punto.y, 3.0)

    def test_coordenadas_booleanas_invalidas(self):
        with self.assertRaises(ValueError):
            Punto(True, 2)

        with self.assertRaises(ValueError):
            Punto(2, False)

    def test_coordenadas_no_numericas(self):
        with self.assertRaises(ValueError):
            Punto('2', 3)

    def test_coordenadas_no_finitas(self):
        with self.assertRaises(ValueError):
            Punto(float('inf'), 2)

        with self.assertRaises(ValueError):
            Punto(2, float('nan'))

    def test_vector_homogeneo(self):
        punto = Punto(2, 4)
        self.assertEqual(punto.a_homogeneo(), [2.0, 4.0, 1.0])

    def test_desde_homogeneo(self):
        punto = Punto.desde_homogeneo([4, 8, 2])

        self.assertEqual(punto.x, 2.0)
        self.assertEqual(punto.y, 4.0)

    def test_vector_homogeneo_invalido(self):
        with self.assertRaises(ValueError):
            Punto.desde_homogeneo([1, 2])

        with self.assertRaises(ValueError):
            Punto.desde_homogeneo([1, 2, 0])

        with self.assertRaises(ValueError):
            Punto.desde_homogeneo([True, 2, 1])

    def test_distancia_entre_puntos(self):
        punto1 = Punto(0, 0)
        punto2 = Punto(3, 4)

        self.assertEqual(punto1.distancia_a(punto2), 5.0)

    def test_distancia_con_argumento_invalido(self):
        punto = Punto(0, 0)

        with self.assertRaises(TypeError):
            punto.distancia_a((3, 4))

if __name__ == '__main__':
    unittest.main()

