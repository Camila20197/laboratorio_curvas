
from math import isfinite
from typing import List

class Punto:
    """representa un punto en el plano cartesiano, cada punto posee dos coordenadas reales: x e y"""
    def __init__(self, p_x: float, p_y: float):
        """inicializa un punto verificando que sus coordenadas sean numeros reales finitos"""
        if (not isinstance(p_x, (int, float)) or isinstance(p_x, bool) or not isfinite(p_x)):
            raise ValueError('la coordenada x debe ser un numero real finito')

        if (not isinstance(p_y, (int, float)) or isinstance(p_y, bool) or not isfinite(p_y)):
            raise ValueError('la coordenada y debe ser un numero real finito')

        self._x = float(p_x)
        self._y = float(p_y)

    @property
    def x(self) -> float:
        """devuelve la coordenada x"""
        return self._x

    @property
    def y(self) -> float:
        """devuelve la coordenada y"""
        return self._y

    def a_homogeneo(self) -> List[float]:
        """convierte el punto a coordenadas homogeneas, retorna: [x, y, 1.0]"""
        return [self._x, self._y, 1.0]

    @classmethod
    def desde_homogeneo(cls, p_vector: List[float]) -> 'Punto':
        """
        construye un punto a partir de coordenadas homogeneas;
        si el vector es [x, y, w], las coordenadas cartesianas se obtienen dividiendo x e y por w
        """
        if not isinstance(p_vector, (list, tuple)) or len(p_vector) != 3:
            raise ValueError('el vector homogeneo debe tener tres componentes')

        if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not isfinite(v) for v in p_vector):
            raise ValueError('las componentes deben ser reales finitas')

        x, y, w = p_vector

        if w == 0:
            raise ValueError('la componente homogenea w no puede ser cero')

        return cls(x / w, y / w)

    def distancia_a(self, p_otro: "Punto") -> float:
        """calcula la distancia euclidiana entre dos puntos: d = sqrt((x2-x1)^2 + (y2-y1)^2)"""

        if not isinstance(p_otro, Punto):
            raise TypeError('el argumento debe ser una instancia de Punto')

        dx = p_otro.x - self._x
        dy = p_otro.y - self._y

        return (dx ** 2 + dy ** 2) ** 0.5

