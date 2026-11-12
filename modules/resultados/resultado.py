"""Clase abstracta Resultado: resultado de un algoritmo numérico (RF4 y RF5).

Responsabilidad: CONOCER los valores obtenidos por un algoritmo y saber
mostrarse como texto. No calcula, no imprime ni dibuja.
"""
from abc import ABC, abstractmethod


class Resultado(ABC):
    """Clase abstracta: resultado de un algoritmo numérico sobre [a, b].

    INV: a < b.
    INV: es inmutable (solo tiene getters, no setters).
    """

    def __init__(self, p_a: float, p_b: float):
        """PRE: p_a < p_b; si no, lanza ValueError.
        POST: el resultado queda asociado al intervalo [p_a, p_b]."""
        if not p_a < p_b:
            raise ValueError(f"Intervalo inválido: se requiere a < b (a={p_a}, b={p_b}).")
        self.__a = p_a
        self.__b = p_b

    @property
    def a(self) -> float:
        """Extremo izquierdo del intervalo utilizado."""
        return self.__a

    @property
    def b(self) -> float:
        """Extremo derecho del intervalo utilizado."""
        return self.__b

    @abstractmethod
    def resumen(self) -> str:
        """POST: devuelve un texto con el resultado y los parámetros utilizados."""
