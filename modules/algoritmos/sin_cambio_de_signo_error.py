"""Excepción propia del método de bisección (RF4)."""


class SinCambioDeSignoError(ValueError):
    """Excepción propia: la función no cambia de signo en los extremos del
    intervalo y ninguno de ellos es raíz (RF4: condición inicial de la bisección).

    Hereda de ValueError, así quien captura ValueError también la atrapa
    (respeta el contrato de AlgoritmoNumerico.calcular, principio de Liskov).
    """
