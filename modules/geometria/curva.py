
from modules.geometria.punto import Punto

class Curva:
    def __init__(self, p_nombre: str):
        if not isinstance(p_nombre, str) or not p_nombre.strip():
            raise ValueError('el nombre de la curva no puede estar vacio')

        self._nombre = p_nombre.strip()
        self._puntos = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def puntos(self) -> tuple:
        return tuple(self._puntos)

    def agregar_punto(self, p_punto: Punto) -> None:
        if not isinstance(p_punto, Punto):
            raise TypeError("Solo se pueden agregar objetos Punto.")

        #crear instancia propia del punto
        nuevo_punto = Punto(p_punto.x, p_punto.y)

        self._puntos.append(nuevo_punto)

    def cantidad_puntos(self) -> int:
        return len(self._puntos)

    def __iter__(self):
        return iter(self._puntos)

    def coordenadas_x(self) -> list:
        return [punto.x for punto in self._puntos]

    def coordenadas_y(self) -> list:
        return [punto.y for punto in self._puntos]

    def longitud(self) -> float:
        longitud_total = 0.0

        for indice in range(len(self._puntos) - 1):
            longitud_total += self._puntos[indice].distancia_a(self._puntos[indice + 1])

        return longitud_total
