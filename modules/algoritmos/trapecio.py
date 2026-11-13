"""Clase Trapecio: método de los trapecios para aproximar una integral definida (RF5)."""
from modules.algoritmos.algoritmo_numerico import AlgoritmoNumerico
from modules.funciones import FuncionMatematica
from modules.resultados import ResultadoIntegracion


class Trapecio(AlgoritmoNumerico):
    """Regla del trapecio compuesta (Newton-Cotes de orden 1).

    Divide [a, b] en n subintervalos de ancho h = (b - a) / n y aproxima el área
    bajo la curva sumando el área de los n trapecios:

        I ≈ h/2 · [f(x0) + 2·f(x1) + ... + 2·f(x_(n-1)) + f(xn)]

    Error de aproximación: E = -(b - a)/12 · h² · f''(ξ), con ξ en (a, b).

    INV: subintervalos es un entero >= 1 (no cambia durante la vida del objeto).
    """

    def __init__(self, p_subintervalos: int):
        """El usuario establece la cantidad de subintervalos (RF5).
        PRE: p_subintervalos es un entero >= 1; si no, lanza ValueError."""
        if not isinstance(p_subintervalos, int) or p_subintervalos < 1:
            raise ValueError("La cantidad de subintervalos debe ser un entero mayor o igual a 1 "
                             f"(se recibió {p_subintervalos}).")
        self.__subintervalos = p_subintervalos

    def calcular(self, p_funcion: FuncionMatematica, p_a: float, p_b: float) -> ResultadoIntegracion:
        """PRE: p_a < p_b (si no, ValueError).
        PRE: f da valores finitos en los puntos evaluados (si no, ValueError).
        POST: ResultadoIntegracion con la aproximación de la integral de f en [a, b]
              y los parámetros utilizados (a, b, subintervalos).
        Siempre termina: evalúa la función exactamente n + 1 veces."""
        self._validar_intervalo(p_a, p_b)
        n = self.__subintervalos
        h = (p_b - p_a) / n

        # Los extremos se cuentan una vez; los puntos interiores, dos veces
        # (cada uno es lado de dos trapecios vecinos).
        suma = (self._evaluar(p_funcion, p_a) + self._evaluar(p_funcion, p_b)) / 2
        for i in range(1, n):
            suma += self._evaluar(p_funcion, p_a + i * h)

        return ResultadoIntegracion(p_a, p_b, h * suma, n)


if __name__ == "__main__":
    # Prueba rápida con las funciones del grupo (modules/funciones).
    import math

    from modules.funciones import FuncionExponencial, FuncionPolinomica, FuncionSeno

    print("=== 1) Polinómica: integral de x^2 en [0, 1] (exacta: 1/3) ===")
    cuadrado = FuncionPolinomica([1, 0, 0])          # coeficientes de mayor a menor grado
    print(cuadrado.descripcion())
    for n in (1, 2, 4, 8):
        resultado = Trapecio(n).calcular(cuadrado, 0, 1)
        print(f"  n = {n}: {resultado.valor:.6f}   error = {resultado.valor - 1 / 3:.6f}")
    print("  -> al duplicar n, el error se divide aproximadamente por 4 (error proporcional a h²)")

    print("\n=== 2) Seno: integral de sen(x) en [0, pi] (exacta: 2) ===")
    print(Trapecio(100).calcular(FuncionSeno(1, 1, 0), 0, math.pi).resumen())

    print("\n=== 3) Exponencial: integral de e^x en [0, 1] (exacta: e - 1) ===")
    print(Trapecio(50).calcular(FuncionExponencial(1, 1, 0), 0, 1).resumen())
    print(f"  Valor exacto e - 1: {math.e - 1}")

    print("\n=== 4) Entrada inválida: 0 subintervalos ===")
    try:
        Trapecio(0)
    except ValueError as error:
        print(f"  ValueError: {error}")
