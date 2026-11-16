
#generador recursivo del copo de nieve de Koch

from modules.geometria import Curva, Punto
from .generador_koch import GeneradorKoch
import math

class GeneradorCopoNieve:
    """
    construye un copo de nieve a partir de tres lados de Koch, 
    el nivel permitido coincide con el de GeneradorKoch (0 a 6),
    la curva resultante es cerrada: el ultimo punto coincide con el primero
    """
    NIVEL_MAXIMO = GeneradorKoch.NIVEL_MAXIMO

    def __init__(self, p_nivel: int):
        if not isinstance(p_nivel, int) or isinstance(p_nivel, bool):
            raise ValueError('el nivel debe ser un numero entero')
        if p_nivel < 0 or p_nivel > self.NIVEL_MAXIMO:
            raise ValueError(f'el nivel debe estar entre 0 y {self.NIVEL_MAXIMO}')

        self._nivel = p_nivel
        self._generador_koch = GeneradorKoch(p_nivel)

    @property
    def nivel(self) -> int:
        return self._nivel

    def generar(self) -> Curva:
        """genera el contorno cerrado del copo de nieve"""
        altura = math.sqrt(3) / 2
        vertices = (Punto(0, 0), Punto(0.5, altura), Punto(1, 0),)
        puntos_copo = []
        for indice in range(3):
            inicio = vertices[indice]
            fin = vertices[(indice + 1) % 3]
            puntos_lado = self._generador_koch.koch(inicio, fin, self._nivel)
            puntos_copo.extend(puntos_lado[:-1])

        #cerrar el contorno repitiendo el primer punto al final
        puntos_copo.append(puntos_copo[0])
        curva = Curva(f'copo de nieve de Koch - nivel {self._nivel}')
        for punto in puntos_copo:
            curva.agregar_punto(punto)

        return curva

