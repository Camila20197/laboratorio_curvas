"""Clase ResultadoIntegracion: resultado del método de los trapecios (RF5)."""
import math

from modules.resultados.resultado import Resultado


class ResultadoIntegracion(Resultado):
    """Resultado del método de los trapecios (RF5).

    Muestra la aproximación calculada y los parámetros utilizados (a, b, subintervalos).

    INV: valor es un número finito;  subintervalos >= 1.
    """

    def __init__(self, p_a: float, p_b: float, p_valor: float, p_subintervalos: int):
        """PRE: se cumplen los invariantes de la clase; si no, lanza ValueError."""
        super().__init__(p_a, p_b)
        if not math.isfinite(p_valor):
            raise ValueError(f"El valor de la integral debe ser finito (se obtuvo {p_valor}).")
        if p_subintervalos < 1:
            raise ValueError("La cantidad de subintervalos debe ser al menos 1.")
        self.__valor = p_valor
        self.__subintervalos = p_subintervalos

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def subintervalos(self) -> int:
        return self.__subintervalos

    def resumen(self) -> str:
        return (f"Método de los trapecios en [{self.a}, {self.b}]\n"
                f"  Subintervalos: {self.__subintervalos}\n"
                f"  Integral aproximada: {self.__valor}")
