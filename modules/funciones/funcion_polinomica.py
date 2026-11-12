
from collections.abc import Iterable
from math import isfinite
from modules.funciones.funcion_matematica import FuncionMatematica

class FuncionPolinomica(FuncionMatematica):
    def __init__(self, p_coeficientes: Iterable[float]):
        coeficientes = tuple(p_coeficientes)

        if not coeficientes:
            raise ValueError('el polinomio debe tener coeficientes')

        if any(not isinstance(c, (int, float)) or not isfinite(c) for c in coeficientes):
            raise ValueError('los coeficientes deben ser reales finitos')

        self._coeficientes = coeficientes

    @property
    def coeficientes(self):
        return self._coeficientes

    def evaluar(self, p_x: float) -> float:
        resultado = 0.0

        for coeficiente in self._coeficientes:
            resultado = resultado * p_x + coeficiente

        return resultado

    def descripcion(self) -> str:
        terminos = []
        grado = len(self._coeficientes) - 1

        for indice, coeficiente in enumerate(self._coeficientes):
            exponente = grado - indice

            if coeficiente == 0:
                continue

            if exponente == 0:
                termino = f'{coeficiente:g}'
            elif exponente == 1:
                termino = f'{coeficiente:g}x'
            else:
                termino = f'{coeficiente:g}x^{exponente}'

            terminos.append(termino)

        return ' + '.join(terminos).replace('+ -', '- ') or '0'
