
from .transformacion import Transformacion
import numpy as np

class Traslacion(Transformacion):
    def __init__(self, p_dx: float, p_dy: float):
        if not isinstance(p_dx, (int, float)) or isinstance(p_dx, bool):
            raise ValueError('el desplazamiento dx debe ser numerico')

        if not isinstance(p_dy, (int, float)) or isinstance(p_dy, bool):
            raise ValueError('el desplazamiento dy debe ser numerico')

        if not np.isfinite(p_dx) or not np.isfinite(p_dy):
            raise ValueError('los desplazamientos deben ser finitos')

        self._dx = float(p_dx)
        self._dy = float(p_dy)

    @property
    def dx(self) -> float:
        return self._dx

    @property
    def dy(self) -> float:
        return self._dy

    def matriz(self) -> np.ndarray:
        return np.array([[1, 0, self._dx], [0, 1, self._dy], [0, 0, 1]], dtype=float)

    def descripcion(self) -> str:
        return f'traslacion (dx={self._dx}, dy={self._dy})'

