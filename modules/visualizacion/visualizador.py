"""Clase Visualizador: representación gráfica de las curvas con matplotlib (RF2).

Es el ÚNICO módulo del proyecto que usa matplotlib (Responsabilidad Única).
Usa la API orientada a objetos (fig, ax) vista en Graficación II
("explicit is better than implicit").

Funcionamiento junto a la terminal:
- p_interactivo=True (uso normal): activa el modo interactivo (plt.ion()), así la
  ventana queda abierta y se redibuja con actualizar() sin bloquear el menú.
- p_interactivo=False (pruebas): no abre ninguna ventana; las pruebas usan el
  backend Agg (renderizador sin interfaz de usuario).
"""
import math

import matplotlib.pyplot as plt

from modules.geometria import Curva


class Visualizador:
    """Se encarga de representar gráficamente curvas y marcas (raíz, intervalo).

    No decide QUÉ se dibuja: eso lo decide quien lo usa (el menú). Las marcas
    reciben números, así el Visualizador solo depende de Curva.

    INV: la figura y los ejes existen durante toda la vida del objeto.
    INV: el título general no cambia.
    """

    def __init__(self, p_titulo: str, p_interactivo: bool = True):
        """PRE: p_titulo es un texto no vacío; si no, lanza ValueError.
        POST: figura y ejes creados y limpios. Si p_interactivo es True, la
        ventana se muestra sin bloquear la terminal; si no, no se abre ventana."""
        if not isinstance(p_titulo, str) or not p_titulo.strip():
            raise ValueError("El título del visualizador no puede estar vacío.")
        self.__titulo = p_titulo.strip()
        self.__interactivo = bool(p_interactivo)

        if self.__interactivo:
            plt.ion()
        self.__figura, self.__ejes = plt.subplots(figsize=(8, 6))
        self.__figura.suptitle(self.__titulo, fontweight="bold")
        if self.__figura.canvas.manager is not None:
            self.__figura.canvas.manager.set_window_title(self.__titulo)
        self.limpiar()

        if self.__interactivo:
            self.__figura.show()
            plt.pause(0.001)

    @property
    def ejes(self):
        """Ejes de matplotlib, solo para lectura (los usan las pruebas)."""
        return self.__ejes

    def poner_titulo(self, p_texto: str) -> None:
        """PRE: p_texto es un texto; si no, lanza TypeError.
        POST: el gráfico muestra el título general y el subtítulo p_texto."""
        if not isinstance(p_texto, str):
            raise TypeError("El subtítulo debe ser un texto.")
        self.__ejes.set_title(p_texto)

    def limpiar(self) -> None:
        """POST: sin curvas ni marcas; ejes cartesianos con etiquetas, marcas y grilla."""
        self.__ejes.clear()
        self.__ejes.set_xlabel("x")
        self.__ejes.set_ylabel("y")
        self.__ejes.grid(True, linestyle=":", alpha=0.6)
        self.__ejes.axhline(0, color="black", linewidth=0.8, zorder=1)   # eje x
        self.__ejes.axvline(0, color="black", linewidth=0.8, zorder=1)   # eje y
        self.__ejes.set_aspect("auto")
        self.__ejes.set_autoscale_on(True)

    def dibujar_curva(self, p_curva: Curva) -> None:
        """PRE: p_curva es una Curva (si no, TypeError) con al menos un punto
        (si no, ValueError).
        POST: hay una línea más, con el nombre de la curva como etiqueta."""
        if not isinstance(p_curva, Curva):
            raise TypeError("Solo se pueden dibujar objetos Curva.")
        if p_curva.cantidad_puntos() == 0:
            raise ValueError(f"La curva '{p_curva.nombre}' no tiene puntos para dibujar.")
        marcador = "o" if p_curva.cantidad_puntos() == 1 else None
        self.__ejes.plot(p_curva.coordenadas_x(), p_curva.coordenadas_y(),
                         marker=marcador, linewidth=1.5, zorder=2, label=p_curva.nombre)

    def marcar_raiz(self, p_x: float) -> None:
        """PRE: p_x es un número finito; si no, lanza ValueError.
        POST: hay un punto destacado en (p_x, 0) con la etiqueta 'raíz ≈ p_x'."""
        self.__validar_numero(p_x, "La raíz")
        self.__ejes.plot([p_x], [0], linestyle="none", marker="o", markersize=9,
                         color="red", zorder=5, label=f"raíz ≈ {p_x:.6g}")

    def marcar_intervalo(self, p_a: float, p_b: float) -> None:
        """PRE: p_a y p_b son números finitos y p_a < p_b; si no, lanza ValueError.
        POST: hay dos líneas verticales en x = p_a y x = p_b con su valor como etiqueta."""
        self.__validar_numero(p_a, "El extremo a")
        self.__validar_numero(p_b, "El extremo b")
        if not p_a < p_b:
            raise ValueError(f"Intervalo inválido: se requiere a < b (a={p_a}, b={p_b}).")
        self.__ejes.axvline(p_a, color="green", linestyle="--", zorder=3, label=f"a = {p_a:g}")
        self.__ejes.axvline(p_b, color="purple", linestyle="--", zorder=3, label=f"b = {p_b:g}")

    def ajustar_vista(self, p_xmin: float, p_xmax: float, p_ymin: float, p_ymax: float,
                      p_escala_igual: bool = False) -> None:
        """PRE: límites finitos, p_xmin < p_xmax y p_ymin < p_ymax; si no, ValueError.
        POST: los ejes muestran exactamente ese rango; si p_escala_igual es True,
        una unidad mide lo mismo en x que en y."""
        for valor, nombre in ((p_xmin, "xmin"), (p_xmax, "xmax"), (p_ymin, "ymin"), (p_ymax, "ymax")):
            self.__validar_numero(valor, nombre)
        if not p_xmin < p_xmax:
            raise ValueError(f"Se requiere xmin < xmax (xmin={p_xmin}, xmax={p_xmax}).")
        if not p_ymin < p_ymax:
            raise ValueError(f"Se requiere ymin < ymax (ymin={p_ymin}, ymax={p_ymax}).")
        self.__ejes.set_xlim(p_xmin, p_xmax)
        self.__ejes.set_ylim(p_ymin, p_ymax)
        self.__ejes.set_aspect("equal" if p_escala_igual else "auto", adjustable="box")

    def autoajustar(self) -> None:
        """POST: los límites se recalculan para que entre todo lo dibujado."""
        self.__ejes.set_autoscale_on(True)
        self.__ejes.relim()
        self.__ejes.autoscale_view()

    def actualizar(self) -> None:
        """POST: la leyenda muestra los elementos con etiqueta; si es interactivo,
        la ventana se redibuja sin bloquear el menú."""
        manejadores, etiquetas = self.__ejes.get_legend_handles_labels()
        if manejadores:
            self.__ejes.legend(manejadores, etiquetas, loc="best")
        elif self.__ejes.get_legend() is not None:
            self.__ejes.get_legend().remove()

        if self.__interactivo:
            self.__figura.canvas.draw_idle()
            plt.pause(0.001)
        else:
            self.__figura.canvas.draw()

    @staticmethod
    def __validar_numero(p_valor, p_nombre: str) -> None:
        """Verifica que p_valor sea un número real finito (privado)."""
        if (not isinstance(p_valor, (int, float)) or isinstance(p_valor, bool)
                or not math.isfinite(p_valor)):
            raise ValueError(f"{p_nombre} debe ser un número finito (se recibió {p_valor}).")


if __name__ == "__main__":
    # Prueba rápida: abre la ventana y la va actualizando SIN bloquear la terminal.
    from modules.algoritmos import Biseccion, Trapecio
    from modules.funciones import FuncionPolinomica, FuncionSeno
    from modules.generadores import GeneradorCurva, GeneradorKoch
    from modules.transformaciones import Rotacion

    visualizador = Visualizador("Explorador de curvas - prueba del Visualizador")
    generador = GeneradorCurva()

    # 1) Curva + raíz (bisección)
    polinomica = FuncionPolinomica([1, 0, -2])
    curva = generador.generar(polinomica, -2, 2, 100)
    resultado = Biseccion().calcular(polinomica, 1, 2)
    visualizador.limpiar()
    visualizador.poner_titulo(f"Bisección sobre {polinomica.descripcion()}")
    visualizador.dibujar_curva(curva)
    visualizador.marcar_raiz(resultado.raiz)
    visualizador.actualizar()
    input("1) Curva y raíz dibujadas. Presione Enter para continuar...")

    # 2) Curva + intervalo de integración (trapecio)
    seno = FuncionSeno(1, 1, 0)
    curva = generador.generar(seno, -1, 4, 200)
    resultado = Trapecio(50).calcular(seno, 0, 3.14159)
    visualizador.limpiar()
    visualizador.poner_titulo(f"Integral ≈ {resultado.valor:.6f}")
    visualizador.dibujar_curva(curva)
    visualizador.marcar_intervalo(resultado.a, resultado.b)
    visualizador.actualizar()
    input("2) Intervalo de integración marcado. Presione Enter para continuar...")

    # 3) Curva de Koch y su rotación, con escala igual en ambos ejes
    koch = GeneradorKoch(4).generar()
    rotada = Rotacion(0.5).aplicar_curva(koch)          # ángulo en radianes
    visualizador.limpiar()
    visualizador.poner_titulo("Curva de Koch (nivel 4) y su rotación de 0.5 rad")
    visualizador.dibujar_curva(koch)
    visualizador.dibujar_curva(rotada)
    visualizador.ajustar_vista(-0.2, 1.2, -0.2, 1.0, p_escala_igual=True)
    visualizador.actualizar()
    input("3) Koch con escala igual. Presione Enter para cerrar...")
    plt.close("all")
