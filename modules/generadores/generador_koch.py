
from ..geometria import Punto, Curva
import math

class GeneradorKoch:
    NIVEL_MAXIMO = 6

    def __init__(self, p_nivel: int):
        if (not isinstance(p_nivel, int) or isinstance(p_nivel, bool)):
            raise ValueError('el nivel debe ser un numero entero')

        if p_nivel < 0 or p_nivel > self.NIVEL_MAXIMO:
            raise ValueError(f'el nivel debe estar entre 0 y {self.NIVEL_MAXIMO}')

        self._nivel = p_nivel

    @property
    def nivel(self) -> int:
        return self._nivel

    def generar(self) -> Curva:
        p1 = Punto(0, 0)
        p2 = Punto(1, 0)

        puntos = self.koch(p1, p2, self._nivel)
        curva = Curva(f'curva de Koch - nivel {self._nivel}')

        for punto in puntos:
            curva.agregar_punto(punto)

        return curva

    def koch(self, p_p1: Punto, p_p2: Punto, p_nivel: int) -> list:
        if not isinstance(p_p1, Punto) or not isinstance(p_p2, Punto):
            raise TypeError('los extremos deben ser objetos Punto')

        if (not isinstance(p_nivel, int) or isinstance(p_nivel, bool) or p_nivel < 0 or p_nivel > self.NIVEL_MAXIMO):
            raise ValueError('el nivel de recursion no es valido')

        #caso base
        if p_nivel == 0:
            return [p_p1, p_p2]

        #vector del segmento
        dx = p_p2.x - p_p1.x
        dy = p_p2.y - p_p1.y

        #primer y segundo punto de division
        p_a = Punto(p_p1.x + dx / 3, p_p1.y + dy / 3)
        p_b = Punto(p_p1.x + 2 * dx / 3, p_p1.y + 2 * dy / 3)

        #vector del segundo tercio
        vx = p_b.x - p_a.x
        vy = p_b.y - p_a.y

        #rotacion de 60 grados para formar el pico
        angulo = math.pi / 3
        coseno = math.cos(angulo)
        seno = math.sin(angulo)
        p_c = Punto((p_a.x + (vx * coseno) - (vy * seno)), (p_a.y + (vx * seno) + (vy * coseno)))

        #cuatro llamadas recursivas
        tramo1 = self.koch(p_p1, p_a, p_nivel - 1)
        tramo2 = self.koch(p_a, p_c, p_nivel - 1)
        tramo3 = self.koch(p_c, p_b, p_nivel - 1)
        tramo4 = self.koch(p_b, p_p2, p_nivel - 1)

        #unir los tramos evitando repetir extremos
        return (tramo1[:-1] + tramo2[:-1] + tramo3[:-1] + tramo4)


