"""Clase abstracta AlgoritmoNumerico (RF4 y RF5).

Los algoritmos numéricos están separados de la interfaz y de la representación
gráfica (RF5): no usan matplotlib ni la consola, así se prueban sin abrir ventanas.
"""
from abc import ABC, abstractmethod

from modules.funciones import FuncionMatematica
from modules.resultados import Resultado


class AlgoritmoNumerico(ABC):
    """Clase abstracta: procedimiento de cálculo numérico sobre una función en [a, b].

    Patrón Estrategia: los algoritmos concretos son intercambiables detrás de calcular().
    Principio Abierto/Cerrado: un algoritmo nuevo se agrega como subclase.
    """

    @abstractmethod
    def calcular(self, p_funcion: FuncionMatematica, p_a: float, p_b: float) -> Resultado:
        """PRE: p_a < p_b.
        POST: devuelve un objeto Resultado.
        Lanza ValueError si el intervalo es inválido o si el método no puede
        aplicarse a esa función en ese intervalo."""

    def _validar_intervalo(self, p_a: float, p_b: float) -> None:
        """Método protegido, común a todas las subclases (evita duplicar código).
        PRE: ninguna.
        POST: no hace nada si p_a < p_b; en caso contrario lanza ValueError."""
        if not p_a < p_b:
            raise ValueError(f"Intervalo inválido: se requiere a < b (a={p_a}, b={p_b}).")
