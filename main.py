
from apps.menu_consola import MenuConsola
from modules.persistencia import RepositorioCurvas
from modules.visualizacion import Visualizador
from pathlib import Path

def main():
    directorio_datos = Path(__file__).resolve().parent / 'data' / 'curvas'
    repositorio = RepositorioCurvas(directorio_datos)
    visualizador = Visualizador('laboratorio de curvas')
    menu = MenuConsola(repositorio, visualizador)
    menu.ejecutar()

if __name__ == '__main__':
    main()

