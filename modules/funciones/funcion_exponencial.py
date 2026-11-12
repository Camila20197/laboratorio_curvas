
from math import exp, isfinite
from modules.funciones.funcion_matematica import FuncionMatematica

class FuncionExponencial(FuncionMatematica):
    def __init__(self, p_a, p_b, p_c):
        parametros = (p_a, p_b, p_c)

        if any(not isinstance(v, (int, float)) or not isfinite(v) for v in parametros):
            raise ValueError('los parametros deben ser reales finitos')

        self._a = float(p_a)
        self._b = float(p_b)
        self._c = float(p_c)

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    def evaluar(self, p_x: float) -> float:
        return self._a * exp(self._b * p_x) + self._c

    def descripcion(self) -> str:
        return (f'f(x) = {self._a:g} * e^({self._b:g}x) + {self._c:g}')
