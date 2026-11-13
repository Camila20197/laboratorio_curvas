
from .transformacion import Transformacion
import numpy as np

class Escalado(Transformacion):
    def __init__(self, p_sx: float, p_sy: float):
        if not isinstance(p_sx, (int, float)) or isinstance(p_sx, bool):
            raise ValueError('el factor sx debe ser numerico')

        if not isinstance(p_sy, (int, float)) or isinstance(p_sy, bool):
            raise ValueError('el factor sy debe ser numerico')

        if not np.isfinite(p_sx) or not np.isfinite(p_sy):
            raise ValueError('los factores deben ser finitos')

        self._sx = float(p_sx)
        self._sy = float(p_sy)

    @property
    def sx(self) -> float:
        return self._sx

    @property
    def sy(self) -> float:
        return self._sy

    def matriz(self) -> np.ndarray:
        return np.array([[self._sx, 0, 0], [0, self._sy, 0], [0, 0, 1]], dtype=float)

    def descripcion(self) -> str:
        return f'escalado (sx={self._sx}, sy={self._sy})'


