
from math import hypot, isfinite

class Punto:
    def __init__(self, p_x: float, p_y: float):
        if not isinstance(p_x, (int, float)) or not isfinite(p_x):
            raise ValueError('la coordenada x debe ser un numero real finito')

        if not isinstance(p_y, (int, float)) or not isfinite(p_y):
            raise ValueError('la coordenada y debe ser un numero real finito')

        self._x = float(p_x)
        self._y = float(p_y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def a_homogeneo(self) -> list:
        return [self._x, self._y, 1.0]

    @classmethod
    def desde_homogeneo(cls, p_vector: list) -> 'Punto':
        if len(p_vector) != 3:
            raise ValueError('el vector debe tener tres componentes')

        if any(not isinstance(v, (int, float)) or not isfinite(v) for v in p_vector):
            raise ValueError('las componentes deben ser reales finitas')

        x, y, w = p_vector

        if w == 0:
            raise ValueError('la coordenada homogenea w no puede ser cero')

        return cls(x / w, y / w)

    def distancia_a(self, p_otro: 'Punto') -> float:
        if not isinstance(p_otro, Punto):
            raise TypeError('el argumento debe ser un objeto Punto')

        return hypot(self._x - p_otro.x, self._y - p_otro.y)
