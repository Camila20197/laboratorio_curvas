
from abc import ABC, abstractmethod

class FuncionMatematica(ABC):

    @abstractmethod
    def evaluar(self, p_x: float) -> float:
        """calcula el valor de la funcion para x"""
        raise NotImplementedError

    @abstractmethod
    def descripcion(self) -> str:
        """devuelve una descripcion de la funcion"""
        raise NotImplementedError
