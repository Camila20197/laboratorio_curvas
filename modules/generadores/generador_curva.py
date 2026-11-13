
from ..funciones import FuncionMatematica
from ..geometria import Punto, Curva
import math

class GeneradorCurva:
    def generar(
        self,
        p_funcion: FuncionMatematica,
        p_a: float,
        p_b: float,
        p_cantidad: int
    ) -> Curva:

        if not isinstance(p_funcion, FuncionMatematica):
            raise TypeError('se debe proporcionar una FuncionMatematica')

        if (not isinstance(p_a, (int, float)) or isinstance(p_a, bool) or not math.isfinite(p_a)):
            raise ValueError('el extremo a debe ser un numero finito')

        if (not isinstance(p_b, (int, float)) or isinstance(p_b, bool) or not math.isfinite(p_b)):
            raise ValueError('el extremo b debe ser un número finito')

        if p_a >= p_b:
            raise ValueError('el extremo a debe ser menor que b')

        if (not isinstance(p_cantidad, int) or isinstance(p_cantidad, bool) or p_cantidad < 2):
            raise ValueError('la cantidad de puntos debe ser un entero mayor o igual a 2')

        curva = Curva(f'curva de {p_funcion.descripcion()}')
        paso = (p_b - p_a) / (p_cantidad - 1)

        for i in range(p_cantidad):
            x = p_a + i * paso

            #garantizar que el ultimo punto sea exactamente b
            if i == p_cantidad - 1:
                x = float(p_b)

            y = p_funcion.evaluar(x)
            punto = Punto(x, y)
            curva.agregar_punto(punto)

        return curva

