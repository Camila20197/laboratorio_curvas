
from modules.geometria import Punto, Curva
import unittest

class TestComposicionCurva(unittest.TestCase):
    def test_composicion_puntos(self):
        punto = Punto(2, 3)
        curva1 = Curva('curva 1')
        curva2 = Curva('curva 2')

        curva1.agregar_punto(punto)
        curva2.agregar_punto(punto)

        #las curvas tienen instancias independientes
        self.assertIsNot(curva1.puntos[0], curva2.puntos[0])

        #las coordenadas siguen siendo iguales
        self.assertEqual(curva1.puntos[0].x, curva2.puntos[0].x)
        self.assertEqual(curva1.puntos[0].y, curva2.puntos[0].y)

        #el punto original tampoco es compartido
        self.assertIsNot(curva1.puntos[0], punto)
        self.assertIsNot(curva2.puntos[0], punto)

if __name__ == '__main__':
    unittest.main()

