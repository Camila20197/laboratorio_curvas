"""Clase ResultadoBiseccion: resultado del método de bisección (RF4)."""
from modules.resultados.resultado import Resultado


class ResultadoBiseccion(Resultado):
    """Resultado del método de bisección (RF4).

    Informa lo que pide la consigna: la aproximación obtenida, la cantidad de
    iteraciones, si se alcanzó el criterio de convergencia y el error de estimación.

    INV: a <= raiz <= b;  iteraciones >= 0;  error_estimado >= 0.
    """

    def __init__(self, p_a: float, p_b: float, p_raiz: float, p_iteraciones: int,
                 p_convergio: bool, p_error_estimado: float):
        """PRE: se cumplen los invariantes de la clase; si no, lanza ValueError."""
        super().__init__(p_a, p_b)
        if not p_a <= p_raiz <= p_b:
            raise ValueError(f"La raíz {p_raiz} no pertenece al intervalo [{p_a}, {p_b}].")
        if p_iteraciones < 0:
            raise ValueError("La cantidad de iteraciones no puede ser negativa.")
        if p_error_estimado < 0:
            raise ValueError("El error estimado no puede ser negativo.")
        self.__raiz = p_raiz
        self.__iteraciones = p_iteraciones
        self.__convergio = p_convergio
        self.__error_estimado = p_error_estimado

    @property
    def raiz(self) -> float:
        return self.__raiz

    @property
    def iteraciones(self) -> int:
        return self.__iteraciones

    @property
    def convergio(self) -> bool:
        return self.__convergio

    @property
    def error_estimado(self) -> float:
        return self.__error_estimado

    def resumen(self) -> str:
        estado = "alcanzado" if self.__convergio else "NO alcanzado"
        return (f"Método de bisección en [{self.a}, {self.b}]\n"
                f"  Raíz aproximada: {self.__raiz}\n"
                f"  Iteraciones: {self.__iteraciones}\n"
                f"  Criterio de convergencia: {estado}\n"
                f"  Error de estimación: {self.__error_estimado}")
