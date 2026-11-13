#se prueba comportamiento matematico y diseño orientado a objetos

from modules.geometria import Punto, Curva
from modules.transformaciones import Transformacion, Escalado, Rotacion, Traslacion
import unittest
import numpy as np

class TestTransformacion(unittest.TestCase):
    def test_clase_abstracta(self):
        #no debe ser posible instanciar una clase abstracta
        with self.assertRaises(TypeError):
            Transformacion()

    def test_escalado_es_transformacion(self):
        escalado = Escalado(2, 3)
        self.assertIsInstance(escalado, Transformacion)

    def test_aplicar_punto(self):
        escalado = Escalado(2, 3)
        punto = Punto(2, 4)
        resultado = escalado.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 4)
        self.assertAlmostEqual(resultado.y, 12)

    def test_matriz_escalado(self):
        escalado = Escalado(2, 3)
        matriz_esperada = np.array([[2, 0, 0], [0, 3, 0], [0, 0, 1]])
        np.testing.assert_array_equal(escalado.matriz(), matriz_esperada)

    def test_escalado_uniforme(self):
        escalado = Escalado(2, 2)
        punto = Punto(3, 5)
        resultado = escalado.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 6)
        self.assertAlmostEqual(resultado.y, 10)

    def test_escalado_con_factor_cero(self):
        escalado = Escalado(0, 2)
        punto = Punto(3, 4)
        resultado = escalado.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 0)
        self.assertAlmostEqual(resultado.y, 8)

    def test_escalado_con_factor_negativo(self):
        escalado = Escalado(-1, 2)
        punto = Punto(3, 4)
        resultado = escalado.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, -3)
        self.assertAlmostEqual(resultado.y, 8)

    def test_aplicar_curva(self):
        escalado = Escalado(2, 3)
        curva = Curva('curva original')
        curva.agregar_punto(Punto(1, 2))
        curva.agregar_punto(Punto(3, 4))
        resultado = escalado.aplicar_curva(curva)

        self.assertEqual(resultado.cantidad_puntos(), 2)
        self.assertAlmostEqual(resultado.puntos[0].x, 2)
        self.assertAlmostEqual(resultado.puntos[0].y, 6)
        self.assertAlmostEqual(resultado.puntos[1].x, 6)
        self.assertAlmostEqual(resultado.puntos[1].y, 12)

    def test_curva_original_no_se_modifica(self):
        escalado = Escalado(2, 2)
        curva = Curva('original')
        curva.agregar_punto(Punto(2, 3))
        resultado = escalado.aplicar_curva(curva)

        self.assertEqual(curva.puntos[0].x, 2)
        self.assertEqual(curva.puntos[0].y, 3)
        self.assertEqual(resultado.puntos[0].x, 4)
        self.assertEqual(resultado.puntos[0].y, 6)

    def test_aplicar_punto_tipo_invalido(self):
        escalado = Escalado(2, 2)
        with self.assertRaises(TypeError):
            escalado.aplicar_punto((2, 3))

    def test_aplicar_curva_tipo_invalido(self):
        escalado = Escalado(2, 2)
        with self.assertRaises(TypeError):
            escalado.aplicar_curva([Punto(1, 2)])

    def test_factores_no_numericos(self):
        with self.assertRaises(ValueError):
            Escalado('dos', 3)

        with self.assertRaises(ValueError):
            Escalado(2, 'tres')

    def test_factores_no_finitos(self):
        with self.assertRaises(ValueError):
            Escalado(float('inf'), 2)

        with self.assertRaises(ValueError):
            Escalado(2, float('nan'))

    def test_descripcion(self):
        escalado = Escalado(2, 3)
        self.assertEqual(escalado.descripcion(), 'escalado (sx=2.0, sy=3.0)')

    def test_rotacion_90_grados(self):
        rotacion = Rotacion(np.pi / 2)
        punto = Punto(1, 0)
        resultado = rotacion.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 0, places=7)
        self.assertAlmostEqual(resultado.y, 1, places=7)

    def test_rotacion_180_grados(self):
        rotacion = Rotacion(np.pi)
        punto = Punto(2, 3)
        resultado = rotacion.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, -2)
        self.assertAlmostEqual(resultado.y, -3)

    def test_rotacion_360_grados(self):
        rotacion = Rotacion(2 * np.pi)
        punto = Punto(2, 3)
        resultado = rotacion.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 2)
        self.assertAlmostEqual(resultado.y, 3)

    def test_matriz_rotacion(self):
        rotacion = Rotacion(0)
        matriz_esperada = np.eye(3)

        np.testing.assert_allclose(rotacion.matriz(), matriz_esperada, atol=1e-10)

    def test_rotacion_angulo_invalido(self):
        with self.assertRaises(ValueError):
            Rotacion('90')

        with self.assertRaises(ValueError):
            Rotacion(float('inf'))

    def test_traslacion(self):
        traslacion = Traslacion(4, -1)
        punto = Punto(2, 3)
        resultado = traslacion.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 6)
        self.assertAlmostEqual(resultado.y, 2)

    def test_matriz_traslacion(self):
        traslacion = Traslacion(4, -1)
        matriz_esperada = np.array([[1, 0, 4], [0, 1, -1], [0, 0, 1]])
        np.testing.assert_array_equal(traslacion.matriz(), matriz_esperada)

    def test_traslacion_nula(self):
        traslacion = Traslacion(0, 0)
        punto = Punto(2, 3)
        resultado = traslacion.aplicar_punto(punto)

        self.assertAlmostEqual(resultado.x, 2)
        self.assertAlmostEqual(resultado.y, 3)

    def test_traslacion_parametros_invalidos(self):
        with self.assertRaises(ValueError):
            Traslacion('cuatro', 2)

        with self.assertRaises(ValueError):
            Traslacion(2, float('nan'))

    def test_transformaciones_encadenadas(self):
        punto = Punto(1, 0)
        rotacion = Rotacion(np.pi / 2)
        traslacion = Traslacion(2, 3)
        resultado = rotacion.aplicar_punto(punto)
        resultado = traslacion.aplicar_punto(resultado)

        self.assertAlmostEqual(resultado.x, 2)
        self.assertAlmostEqual(resultado.y, 4)

if __name__ == '__main__':
    unittest.main()

