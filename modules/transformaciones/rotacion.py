
from .transformacion import Transformacion
import numpy as np

class Rotacion(Transformacion):
    def __init__(self, p_angulo: float):
        if not isinstance(p_angulo, (int, float)) or isinstance(p_angulo, bool):
            raise ValueError('el angulo debe ser numerico')

        if not np.isfinite(p_angulo):
            raise ValueError('el angulo debe ser finito')

        self._angulo = float(p_angulo)

    @property
    def angulo(self) -> float:
        return self._angulo

    def matriz(self) -> np.ndarray:
        coseno = np.cos(self._angulo)
        seno = np.sin(self._angulo)

        return np.array([[coseno, -seno, 0], [seno, coseno, 0], [0, 0, 1]], dtype=float)

    def descripcion(self) -> str:
        return f'rotacion (angulo={self._angulo} rad)'

