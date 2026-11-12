
from math import isfinite, sin
from modules.funciones.funcion_matematica import FuncionMatematica

class FuncionSeno(FuncionMatematica):
    def __init__(self, p_amplitud, p_frecuencia, p_fase):
        parametros = (p_amplitud, p_frecuencia, p_fase)

        if any(not isinstance(v, (int, float)) or not isfinite(v) for v in parametros):
            raise ValueError('los parametros deben ser reales finitos')

        self._amplitud = float(p_amplitud)
        self._frecuencia = float(p_frecuencia)
        self._fase = float(p_fase)

    @property
    def amplitud(self):
        return self._amplitud

    @property
    def frecuencia(self):
        return self._frecuencia

    @property
    def fase(self):
        return self._fase

    def evaluar(self, p_x: float) -> float:
        return self._amplitud * sin(self._frecuencia * p_x + self._fase)

    def descripcion(self) -> str:
        return (f'f(x) = {self._amplitud:g} * sen({self._frecuencia:g}x + {self._fase:g})')
