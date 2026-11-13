"""Clase Biseccion: método de bisección para aproximar una raíz (RF4)."""
import math

from modules.algoritmos.algoritmo_numerico import AlgoritmoNumerico
from modules.algoritmos.sin_cambio_de_signo_error import SinCambioDeSignoError
from modules.funciones import FuncionMatematica
from modules.resultados import ResultadoBiseccion


class Biseccion(AlgoritmoNumerico):
    """Método de bisección para aproximar una raíz de f en [a, b] (RF4).

    En cada iteración el intervalo que contiene a la raíz se divide a la mitad.
    La aproximación es el punto medio del intervalo y el error de estimación es
    la mitad de su ancho (la raíz está dentro del intervalo).

    INV: tolerancia > 0 y max_iteraciones >= 1 (no cambian durante la vida del objeto).
    """

    TOLERANCIA_POR_DEFECTO = 1e-6
    MAX_ITERACIONES_POR_DEFECTO = 100

    def __init__(self, p_tolerancia: float = TOLERANCIA_POR_DEFECTO,
                 p_max_iteraciones: int = MAX_ITERACIONES_POR_DEFECTO):
        """El usuario puede establecer la tolerancia, el máximo de iteraciones o
        ambos (RF4); el que no indique toma su valor por defecto.
        PRE: p_tolerancia > 0  y  p_max_iteraciones es un entero >= 1;
        si no, lanza ValueError."""
        if not p_tolerancia > 0:
            raise ValueError(f"La tolerancia debe ser mayor que 0 (se recibió {p_tolerancia}).")
        if not isinstance(p_max_iteraciones, int) or p_max_iteraciones < 1:
            raise ValueError("El número máximo de iteraciones debe ser un entero mayor o igual a 1 "
                             f"(se recibió {p_max_iteraciones}).")
        self.__tolerancia = p_tolerancia
        self.__max_iteraciones = p_max_iteraciones

    def calcular(self, p_funcion: FuncionMatematica, p_a: float, p_b: float) -> ResultadoBiseccion:
        """PRE: p_a < p_b (si no, ValueError).
        PRE: f(a) y f(b) tienen distinto signo, salvo que alguno ya sea raíz
             (si no, SinCambioDeSignoError).
        PRE: f da valores finitos en los puntos evaluados (si no, ValueError).
        POST: ResultadoBiseccion con la raíz aproximada (dentro de [a, b]), la
              cantidad de iteraciones (<= max_iteraciones), si se alcanzó el criterio
              de convergencia (error <= tolerancia) y el error de estimación."""
        self._validar_intervalo(p_a, p_b)
        f_a = self._evaluar(p_funcion, p_a)
        f_b = self._evaluar(p_funcion, p_b)

        # Caso especial: alguno de los extremos ya es raíz (0 iteraciones).
        if f_a == 0:
            return ResultadoBiseccion(p_a, p_b, p_a, 0, True, 0.0)
        if f_b == 0:
            return ResultadoBiseccion(p_a, p_b, p_b, 0, True, 0.0)

        # Condición inicial del método: distinto signo en los extremos.
        if self.__mismo_signo(f_a, f_b):
            raise SinCambioDeSignoError(
                f"f(a) = {f_a} y f(b) = {f_b} tienen el mismo signo: no se puede garantizar "
                f"una raíz en [{p_a}, {p_b}] con el método de bisección.")

        izquierda, derecha, f_izquierda = p_a, p_b, f_a
        medio = (izquierda + derecha) / 2
        error = (derecha - izquierda) / 2
        iteraciones = 0

        while error > self.__tolerancia and iteraciones < self.__max_iteraciones:
            iteraciones += 1
            f_medio = self._evaluar(p_funcion, medio)
            if f_medio == 0:                       # el punto medio es la raíz exacta
                return ResultadoBiseccion(p_a, p_b, medio, iteraciones, True, 0.0)
            if self.__mismo_signo(f_izquierda, f_medio):
                izquierda, f_izquierda = medio, f_medio   # la raíz está en [medio, derecha]
            else:
                derecha = medio                           # la raíz está en [izquierda, medio]
            medio = (izquierda + derecha) / 2
            error = (derecha - izquierda) / 2

        convergio = error <= self.__tolerancia
        return ResultadoBiseccion(p_a, p_b, medio, iteraciones, convergio, error)

    @staticmethod
    def __mismo_signo(p_valor_1: float, p_valor_2: float) -> bool:
        """True si ambos valores (distintos de 0) tienen el mismo signo (privado).
        Se comparan signos en lugar de multiplicar para evitar desbordes numéricos."""
        return (p_valor_1 < 0) == (p_valor_2 < 0)


if __name__ == "__main__":
    # Prueba rápida con las funciones del grupo (modules/funciones).
    from modules.funciones import FuncionExponencial, FuncionPolinomica, FuncionSeno

    print("=== 1) Polinómica: f(x) = x^2 - 2 en [1, 2], tolerancia 1e-6 ===")
    polinomica = FuncionPolinomica([1, 0, -2])      # coeficientes de mayor a menor grado
    print(polinomica.descripcion())
    print(Biseccion(p_tolerancia=1e-6).calcular(polinomica, 1, 2).resumen())

    print("\n=== 2) Seno: f(x) = sen(x) en [3, 4], solo 5 iteraciones (no converge) ===")
    seno = FuncionSeno(1, 1, 0)
    print(seno.descripcion())
    print(Biseccion(p_max_iteraciones=5).calcular(seno, 3, 4).resumen())

    print("\n=== 3) Exponencial: f(x) = e^x - 2 en [0, 1] (raíz exacta: ln 2) ===")
    exponencial = FuncionExponencial(1, 1, -2)
    print(exponencial.descripcion())
    resultado = Biseccion().calcular(exponencial, 0, 1)
    print(resultado.resumen())
    print(f"  Valor exacto ln(2): {math.log(2)}")

    print("\n=== 4) Entrada inválida: f(x) = x^2 + 1 en [-1, 1] (sin cambio de signo) ===")
    try:
        Biseccion().calcular(FuncionPolinomica([1, 0, 1]), -1, 1)
    except SinCambioDeSignoError as error:
        print(f"  SinCambioDeSignoError: {error}")
