
from modules.geometria import Punto, Curva
from modules.persistencia import RepositorioCurvas
from pathlib import Path
import unittest
import tempfile

class TestRepositorioCurvas(unittest.TestCase):

    def test_no_sobrescribir_curva_existente(self):
        with tempfile.TemporaryDirectory() as directorio:
            repositorio = RepositorioCurvas(Path(directorio))

            curva1 = Curva('mi curva')
            curva1.agregar_punto(Punto(1, 2))

            curva2 = Curva('mi curva')
            curva2.agregar_punto(Punto(5, 6))

            repositorio.guardar(curva1)

            #no debe permitir sobrescribir sin autorizacion
            with self.assertRaises(FileExistsError):
                repositorio.guardar(curva2)

            #el contenido original debe conservarse
            recuperada = repositorio.cargar('mi curva')
            self.assertEqual(recuperada.puntos[0].x, 1)
            self.assertEqual(recuperada.puntos[0].y, 2)

            #ahora si se autoriza la sobrescritura
            repositorio.guardar(curva2, p_sobrescribir=True)
            recuperada = repositorio.cargar('mi curva')

            self.assertEqual(recuperada.puntos[0].x, 5)
            self.assertEqual(recuperada.puntos[0].y, 6)

if __name__ == '__main__':
    unittest.main()



