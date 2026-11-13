"""Pruebas unitarias de modules/visualizacion/visualizador.py (casos V1 a V15).

Se usa el backend Agg y p_interactivo=False: ninguna prueba abre una ventana
(lo pide la consigna para los componentes que deben probarse sin gráficos).
"""
import math
import unittest

import matplotlib
matplotlib.use("Agg")                     # renderizador sin interfaz de usuario
import matplotlib.pyplot as plt          # noqa: E402

from modules.geometria import Curva, Punto              # noqa: E402
from modules.visualizacion import Visualizador          # noqa: E402


def crear_curva(p_nombre, p_coordenadas):
    curva = Curva(p_nombre)
    for x, y in p_coordenadas:
        curva.agregar_punto(Punto(x, y))
    return curva


def lineas_con_etiqueta(p_ejes):
    """Líneas dibujadas por el usuario (las auxiliares de matplotlib empiezan con '_')."""
    return [linea for linea in p_ejes.lines if not linea.get_label().startswith("_")]


class TestVisualizador(unittest.TestCase):

    def setUp(self):
        self.visualizador = Visualizador("Prueba", p_interactivo=False)
        self.curva = crear_curva("curva A", [(0, 0), (1, 1), (2, 4)])

    def tearDown(self):
        plt.close("all")

    # --- Casos habituales ---
    def test_v1_titulo(self):
        self.visualizador.poner_titulo("Bisección")
        self.assertEqual(self.visualizador.ejes.get_title(), "Bisección")

    def test_v2_limpiar_deja_ejes_cartesianos(self):
        ejes = self.visualizador.ejes
        self.assertEqual(ejes.get_xlabel(), "x")
        self.assertEqual(ejes.get_ylabel(), "y")
        self.assertEqual(lineas_con_etiqueta(ejes), [])

    def test_v3_dibujar_curva(self):
        self.visualizador.dibujar_curva(self.curva)
        lineas = lineas_con_etiqueta(self.visualizador.ejes)
        self.assertEqual(len(lineas), 1)
        self.assertEqual(lineas[0].get_label(), "curva A")
        self.assertEqual(list(lineas[0].get_xdata()), [0, 1, 2])
        self.assertEqual(list(lineas[0].get_ydata()), [0, 1, 4])

    def test_v4_marcar_raiz(self):
        self.visualizador.marcar_raiz(1.5)
        raiz = lineas_con_etiqueta(self.visualizador.ejes)[0]
        self.assertTrue(raiz.get_label().startswith("raíz"))
        self.assertEqual(list(raiz.get_xdata()), [1.5])
        self.assertEqual(list(raiz.get_ydata()), [0])

    def test_v5_marcar_intervalo(self):
        self.visualizador.marcar_intervalo(0, 2)
        lineas = lineas_con_etiqueta(self.visualizador.ejes)
        self.assertEqual(len(lineas), 2)
        self.assertEqual(lineas[0].get_xdata()[0], 0)
        self.assertEqual(lineas[1].get_xdata()[0], 2)

    def test_v6_ajustar_vista(self):
        self.visualizador.ajustar_vista(-1, 1, -2, 2)
        self.assertEqual(self.visualizador.ejes.get_xlim(), (-1, 1))
        self.assertEqual(self.visualizador.ejes.get_ylim(), (-2, 2))

    def test_v7_escala_igual(self):
        self.visualizador.ajustar_vista(-1, 1, -1, 1, p_escala_igual=True)
        self.assertEqual(self.visualizador.ejes.get_aspect(), 1.0)

    def test_v8_leyenda_con_las_curvas(self):
        self.visualizador.dibujar_curva(self.curva)
        self.visualizador.dibujar_curva(crear_curva("curva B", [(0, 1), (1, 2)]))
        self.visualizador.actualizar()
        textos = [t.get_text() for t in self.visualizador.ejes.get_legend().get_texts()]
        self.assertEqual(textos, ["curva A", "curva B"])

    def test_v9_limpiar_borra_lo_dibujado(self):
        self.visualizador.dibujar_curva(self.curva)
        self.visualizador.marcar_raiz(1)
        self.visualizador.limpiar()
        self.assertEqual(lineas_con_etiqueta(self.visualizador.ejes), [])

    def test_autoajustar_incluye_toda_la_curva(self):
        self.visualizador.ajustar_vista(-1, 0.5, -1, 0.5)
        self.visualizador.dibujar_curva(self.curva)
        self.visualizador.autoajustar()
        xmin, xmax = self.visualizador.ejes.get_xlim()
        ymin, ymax = self.visualizador.ejes.get_ylim()
        self.assertLessEqual(xmin, 0)
        self.assertGreaterEqual(xmax, 2)
        self.assertGreaterEqual(ymax, 4)

    # --- Entradas inválidas y casos límite ---
    def test_v10_titulo_vacio(self):
        with self.assertRaises(ValueError):
            Visualizador("   ", p_interactivo=False)

    def test_v11_dibujar_algo_que_no_es_curva(self):
        with self.assertRaises(TypeError):
            self.visualizador.dibujar_curva([(0, 0), (1, 1)])

    def test_v12_curva_sin_puntos(self):
        with self.assertRaises(ValueError):
            self.visualizador.dibujar_curva(Curva("vacía"))

    def test_v13_intervalo_invalido(self):
        with self.assertRaises(ValueError):
            self.visualizador.marcar_intervalo(2, 1)

    def test_v14_limites_invalidos(self):
        with self.assertRaises(ValueError):
            self.visualizador.ajustar_vista(1, 1, -1, 1)
        with self.assertRaises(ValueError):
            self.visualizador.ajustar_vista(-1, 1, 2, -2)

    def test_v15_raiz_no_finita(self):
        with self.assertRaises(ValueError):
            self.visualizador.marcar_raiz(math.inf)


if __name__ == "__main__":
    unittest.main()
