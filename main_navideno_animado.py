
"""
demostracion navidena del copo de nieve de Koch,
ejecutar desde la raiz del proyecto: python main_navideno_animacion.py
"""

from modules.generadores import GeneradorCopoNieve
from modules.visualizacion import Visualizador
from pathlib import Path
from PIL import Image
import pygame

#rutas de los recursos
CARPETA_PROYECTO = Path(__file__).parent
RUTA_AUDIO = (CARPETA_PROYECTO / 'data' / 'audio' / 'mariah.mp3')
RUTA_GIF = (CARPETA_PROYECTO / 'data' / 'animaciones' / 'copito_navideno.gif')

#segundo desde el que comienza la cancion
SEGUNDO_INICIO = 59

#dimensiones de la ventana
ANCHO_VENTANA = 960
ALTO_VENTANA = 540

def solicitar_nivel():
    """solicita y valida el nivel de recursividad"""
    while True:
        try:
            nivel = int(input('Elige el nivel de Koch (0 a 6), el 6 trae sorpresa: '))

            if 0 <= nivel <= GeneradorCopoNieve.NIVEL_MAXIMO:
                return nivel

            print('El nivel debe estar entre 0 y 6')

        except ValueError:
            print('Ingresa un numero entero')

def cargar_gif(ruta_gif):
    """carga los cuadros y sus duraciones desde un GIF"""
    cuadros = []
    duraciones = []

    with Image.open(ruta_gif) as gif:
        for indice in range(gif.n_frames):
            gif.seek(indice)
            cuadro = gif.convert('RGBA')
            superficie = pygame.image.fromstring(cuadro.tobytes(), cuadro.size, 'RGBA').convert_alpha()

            cuadros.append(superficie)

            duracion = gif.info.get('duration', 100)
            duraciones.append(max(duracion, 20))

    return cuadros, duraciones

def ajustar_cuadro(cuadro):
    """adapta el GIF a la ventana sin deformarlo"""
    ancho_original, alto_original = cuadro.get_size()
    escala = min(ANCHO_VENTANA / ancho_original, ALTO_VENTANA / alto_original)
    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto = int(alto_original * escala)

    return pygame.transform.smoothscale(cuadro, (nuevo_ancho, nuevo_alto))

def reproducir_escena():
    """reproduce el GIF y la cancion simultaneamente"""
    if not RUTA_AUDIO.exists():
        print(f'No se encontro el audio: {RUTA_AUDIO}')
        return

    if not RUTA_GIF.exists():
        print(f'No se encontro la animacion: {RUTA_GIF}')
        return

    try:
        pygame.init()
        pygame.mixer.init()

        ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

        pygame.display.set_caption('Operacion Copito: Mariah has been unfrozen')

        #cargar todos los cuadros del GIF
        cuadros, duraciones = cargar_gif(RUTA_GIF)
        cuadros = [ajustar_cuadro(cuadro) for cuadro in cuadros]

        #cargar y comenzar la cancion
        pygame.mixer.music.load(str(RUTA_AUDIO))
        pygame.mixer.music.play(start=SEGUNDO_INICIO)

        print('\nMariah ha sido descongelada.')
        print('La animacion esta en marcha...')

        reloj = pygame.time.Clock()

        indice_cuadro = 0
        tiempo_acumulado = 0
        ejecutando = True

        while ejecutando:
            tiempo_transcurrido = reloj.tick(60)
            tiempo_acumulado += tiempo_transcurrido

            #atender eventos de la ventana
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

            #avanzar la animacion respetando la duracion individual de cada cuadro del GIF
            while tiempo_acumulado >= duraciones[indice_cuadro]:
                tiempo_acumulado -= duraciones[indice_cuadro]
                indice_cuadro = (indice_cuadro + 1) % len(cuadros)

            #dibujar el cuadro actual
            ventana.fill((15, 20, 35))
            cuadro_actual = cuadros[indice_cuadro]
            rectangulo = cuadro_actual.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

            ventana.blit(cuadro_actual, rectangulo)
            pygame.display.flip()

            #cuando termina la cancion, termina la escena
            if not pygame.mixer.music.get_busy():
                ejecutando = False

        pygame.mixer.music.stop()

    except (pygame.error, OSError) as error:
        print(f'No se pudo reproducir la escena: {error}')

    finally:
        pygame.quit()

    print('\nLa operacion Copito ha finalizado')

def main():
    """ejecuta la demostracion navidena"""

    print('=' * 55)
    print('PROYECTO ESPECIAL: OPERACION COPITO')
    print('Una demostracion fractal navidena')
    print('=' * 55)

    nivel = solicitar_nivel()

    #generar el copo de nieve
    generador = GeneradorCopoNieve(nivel)
    curva = generador.generar()

    #visualizar el resultado matematico
    visualizador = Visualizador('Especial navideno: copo de nieve de Koch')
    visualizador.poner_titulo(curva.nombre)
    visualizador.dibujar_curva(curva)
    visualizador.autoajustar()
    visualizador.actualizar()

    print('\nCopo generado correctamente.')
    print(f'Nivel de recursividad: {nivel}')
    print(f'Cantidad de puntos: {curva.cantidad_puntos()}')
    print(f'Longitud del contorno: {curva.longitud():.6f}')

    if nivel == 6:
        print('\n¡COPITO COMPLETADO!')
        print("It's tiiiiiime... Mariah Carey ha sido descongelada")

        reproducir_escena()

    else:
        print('\nMariah sigue en el congelador.')
        print('Alcanza el nivel 6 para liberarla.')
        input('\nPresiona Enter para terminar... ')


if __name__ == '__main__':
    main()
