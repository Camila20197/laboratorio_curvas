
from ..geometria import Punto, Curva
from abc import ABC, abstractmethod
import numpy as np

class Transformacion(ABC):

    @abstractmethod
    def matriz(self) -> np.ndarray:
        """devuelve la matriz de transformacion"""
        pass

    @abstractmethod
    def descripcion(self) -> str:
        """devuelve una descripcion de la transformacion"""
        pass

    def aplicar_punto(self, p_punto: Punto) -> Punto:
        if not isinstance(p_punto, Punto):
            raise TypeError('se debe proporcionar un objeto Punto')

        vector = np.array(p_punto.a_homogeneo(), dtype=float)
        resultado = self.matriz() @ vector     #@ multiplicador matricial

        return Punto.desde_homogeneo(resultado.tolist())

    def aplicar_curva(self, p_curva: Curva) -> Curva:
        if not isinstance(p_curva, Curva):
            raise TypeError('se debe proporcionar un objeto Curva')

        nueva_curva = Curva(f'{p_curva.nombre} - {self.descripcion()}')

        for punto in p_curva:
            nuevo_punto = self.aplicar_punto(punto)
            nueva_curva.agregar_punto(nuevo_punto)

        return nueva_curva
