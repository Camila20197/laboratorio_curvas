
from modules.funciones import FuncionPolinomica, FuncionSeno, FuncionExponencial
from modules.geometria import Punto, Curva
from modules.generadores import GeneradorCurva, GeneradorKoch
import unittest

class TestGeneradorCurva(unittest.TestCase):
    def setUp(self):
        self.generador = GeneradorCurva()

    def test_generar_polinomica(self):
        funcion = FuncionPolinomica([1, 0, 0])
        curva = self.generador.generar(funcion, 0, 4, 5)

        self.assertIsInstance(curva, Curva)
        self.assertEqual(curva.cantidad_puntos(), 5)
        self.assertAlmostEqual(curva.puntos[0].y, 0)
        self.assertAlmostEqual(curva.puntos[1].y, 1)
        self.assertAlmostEqual(curva.puntos[2].y, 4)
        self.assertAlmostEqual(curva.puntos[3].y, 9)
        self.assertAlmostEqual(curva.puntos[4].y, 16)

    def test_generar_seno(self):
        funcion = FuncionSeno(1, 1, 0)
        curva = self.generador.generar(funcion, 0, 1, 3)

        self.assertEqual(curva.cantidad_puntos(), 3)
        self.assertAlmostEqual(curva.puntos[0].y, 0)
        self.assertAlmostEqual(curva.puntos[1].y, 0.4794255386)
        self.assertAlmostEqual(curva.puntos[2].y, 0.8414709848)

    def test_generar_exponencial(self):
        funcion = FuncionExponencial(1, 1, 0)
        curva = self.generador.generar(funcion, 0, 2, 3)

        self.assertEqual(curva.cantidad_puntos(), 3)
        self.assertAlmostEqual(curva.puntos[0].y, 1)
        self.assertAlmostEqual(curva.puntos[1].y, 2.718281828)
        self.assertAlmostEqual(curva.puntos[2].y, 7.389056099)

    def test_extremos_intervalo(self):
        funcion = FuncionPolinomica([1, 0])
        curva = self.generador.generar(funcion, -2, 2, 5)

        self.assertAlmostEqual(curva.puntos[0].x, -2)
        self.assertAlmostEqual(curva.puntos[-1].x, 2)

    def test_cantidad_minima_puntos(self):
        funcion = FuncionPolinomica([1, 0])
        curva = self.generador.generar(funcion, 0, 2, 2)
        self.assertEqual(curva.cantidad_puntos(), 2)

    def test_cantidad_invalida(self):
        funcion = FuncionPolinomica([1, 0])
        for cantidad in (0, 1, -2, 2.5, True):
            with self.subTest(cantidad=cantidad):
                with self.assertRaises(ValueError):
                    self.generador.generar(funcion, 0, 2, cantidad)

    def test_intervalo_invalido(self):
        funcion = FuncionPolinomica([1, 0])

        with self.assertRaises(ValueError):
            self.generador.generar(funcion, 2, 2, 5)

        with self.assertRaises(ValueError):
            self.generador.generar(funcion, 3, 1, 5)

    def test_funcion_invalida(self):
        with self.assertRaises(TypeError):
            self.generador.generar(lambda x: x**2, 0, 2, 5)

    def test_extremos_no_finitos(self):
        funcion = FuncionPolinomica([1, 0])

        with self.assertRaises(ValueError):
            self.generador.generar(funcion, float('-inf'), 2, 5)

class TestGeneradorKoch(unittest.TestCase):
    def test_nivel_cero(self):
        generador = GeneradorKoch(0)
        curva = generador.generar()

        self.assertEqual(curva.cantidad_puntos(), 2)
        self.assertAlmostEqual(curva.puntos[0].x, 0)
        self.assertAlmostEqual(curva.puntos[0].y, 0)
        self.assertAlmostEqual(curva.puntos[1].x, 1)
        self.assertAlmostEqual(curva.puntos[1].y, 0)

    def test_nivel_uno(self):
        generador = GeneradorKoch(1)
        curva = generador.generar()
        self.assertEqual(curva.cantidad_puntos(), 5)

    def test_cantidad_puntos_por_nivel(self):
        for nivel in range(GeneradorKoch.NIVEL_MAXIMO + 1):
            with self.subTest(nivel=nivel):
                generador = GeneradorKoch(nivel)
                curva = generador.generar()

                self.assertEqual(curva.cantidad_puntos(), (4**nivel + 1))

    def test_pico_primer_nivel(self):
        generador = GeneradorKoch(1)
        curva = generador.generar()

        #el pico debe quedar por encima del segmento inicial
        self.assertAlmostEqual(curva.puntos[2].x, 0.5)
        self.assertAlmostEqual(curva.puntos[2].y, ((3**0.5) / 6))

    def test_extremos_se_conservan(self):
        generador = GeneradorKoch(3)
        curva = generador.generar()

        self.assertAlmostEqual(curva.puntos[0].x, 0)
        self.assertAlmostEqual(curva.puntos[0].y, 0)
        self.assertAlmostEqual(curva.puntos[-1].x, 1)
        self.assertAlmostEqual(curva.puntos[-1].y, 0)

    def test_nivel_negativo(self):
        with self.assertRaises(ValueError):
            GeneradorKoch(-1)

    def test_nivel_superior_al_maximo(self):
        with self.assertRaises(ValueError):
            GeneradorKoch(GeneradorKoch.NIVEL_MAXIMO + 1)

    def test_nivel_no_entero(self):
        with self.assertRaises(ValueError):
            GeneradorKoch(2.5)

    def test_koch_con_puntos_invalidos(self):
        generador = GeneradorKoch(1)

        with self.assertRaises(TypeError):
            generador.koch((0, 0), Punto(1, 0), 1)

    def test_koch_nivel_invalido(self):
        generador = GeneradorKoch(1)
        p1 = Punto(0, 0)
        p2 = Punto(1, 0)

        with self.assertRaises(ValueError):
            generador.koch(p1, p2, -1)

if __name__ == '__main__':
    unittest.main()

