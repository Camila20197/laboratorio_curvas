
from modules.algoritmos import Biseccion, SinCambioDeSignoError, Trapecio
from modules.funciones import FuncionExponencial, FuncionPolinomica, FuncionSeno
from modules.generadores import GeneradorCurva, GeneradorKoch, GeneradorCopoNieve
from modules.transformaciones import Escalado, Rotacion, Traslacion
import math

class MenuConsola:
    'coordina las operaciones del laboratorio de curvas desde la terminal'
    def __init__(self, p_repositorio, p_visualizador):
        self._repositorio = p_repositorio
        self._visualizador = p_visualizador
        self._generador = GeneradorCurva()
        self._curvas = []

    def ejecutar(self):
        'inicia el ciclo principal de la aplicacion'
        while True:
            self._mostrar_menu()
            opcion = input('seleccione una opcion: ').strip()

            try:
                if opcion == '1':
                    self._generar_curva()

                elif opcion == '2':
                    self._generar_koch()

                elif opcion == '3':
                    self._generar_copo_nieve()

                elif opcion == '4':
                    self._transformar_curva()

                elif opcion == '5':
                    self._analisis_numerico()

                elif opcion == '6':
                    self._gestionar_curvas()

                elif opcion == '7':
                    self._visualizar_curvas()

                elif opcion == '0':
                    print('\ngracias por utilizar el laboratorio de curvas')
                    break

                else:
                    print('\nopcion invalida, seleccione una opcion del menu')

            except (ValueError, TypeError, FileNotFoundError, FileExistsError, SinCambioDeSignoError) as error:
                print(f'\nno se pudo completar la operacion: {error}')

            except KeyboardInterrupt:
                print('\n\noperacion interrumpida por el usuario')

    #MENU PRINCIPAL
    @staticmethod
    def _mostrar_menu():
        print('=' * 55)
        print('LABORATORIO DE CURVAS')
        print('explorador grafico de curvas y algoritmos')
        print('=' * 55)
        print('1. Generar curva matematica')
        print('2. Generar curva de Koch')
        print('3. Generar copo de nieve de Koch')
        print('4. Transformar una curva')
        print('5. Analisis numerico')
        print('6. Gestionar curvas guardadas')
        print('7. Visualizar curvas de la sesion')
        print('0. Salir')
        print('-' * 55)

    #METODOS AUXILIARES PARA INGRESAR DATOS
    @staticmethod
    def _leer_float(p_mensaje):
        'solicita un numero real al usuario'
        while True:
            entrada = input(p_mensaje).strip().replace(',', '.')
            try:
                return float(entrada)
            except ValueError:
                print('entrada invalida, ingrese un numero real')

    @staticmethod
    def _leer_entero(p_mensaje, p_minimo=None, p_maximo=None):
        'solicita un numero entero dentro de un rango opcional'
        while True:
            entrada = input(p_mensaje).strip()
            try:
                valor = int(entrada)

                if p_minimo is not None and valor < p_minimo:
                    print(f'el valor debe ser mayor o igual a {p_minimo}')
                    continue

                if p_maximo is not None and valor > p_maximo:
                    print(f'el valor debe ser menor o igual a {p_maximo}')
                    continue

                return valor

            except ValueError:
                print('entrada invalida, ingrese un numero entero')

    @staticmethod
    def _leer_confirmacion(p_mensaje):
        'solicita una respuesta afirmativa o negativa'
        while True:
            respuesta = input(p_mensaje).strip().lower()

            if respuesta in ('s', 'si', 'sí', 'y'):
                return True

            if respuesta in ('n', 'no'):
                return False

            print("ingrese 's' para sí o 'n' para no")

    def _seleccionar_curva(self):
        'permite seleccionar una curva de la sesion'
        if not self._curvas:
            print('\nno hay curvas disponibles en la sesion')
            return None

        print('\ncurvas disponibles:')

        for indice, curva in enumerate(self._curvas, start=1):
            print(f'{indice}. {curva.nombre} ({curva.cantidad_puntos()} puntos)')

        opcion = self._leer_entero('\nseleccione el numero de curva: ', 1, len(self._curvas))

        return self._curvas[opcion - 1]

    def _registrar_curva(self, p_curva):
        'agrega una curva a la coleccion de la sesion'
        self._curvas.append(p_curva)

        print(f'\ncurva agregada: {p_curva.nombre}')
        print(f'cantidad de puntos: {p_curva.cantidad_puntos()}')
        print(f'longitud aproximada: {p_curva.longitud():.6f}')

    def _mostrar_curvas(self, p_curvas, p_titulo):
        'dibuja una o varias curvas utilizando el visualizador'
        self._visualizador.limpiar()
        self._visualizador.poner_titulo(p_titulo)

        for curva in p_curvas:
            self._visualizador.dibujar_curva(curva)

        self._visualizador.autoajustar()
        self._visualizador.actualizar()

        print('\ngrafico actualizado, la ventana permanece abierta')

    #1 GENERACION DE CURVAS MATEMATICAS
    def _crear_funcion(self):
        'permite seleccionar y construir una funcion matematica'

        print('\n--- seleccion de funcion matematica ---')
        print("1. Funcion polinomica")
        print("2. Funcion seno")
        print("3. Funcion exponencial")

        opcion = self._leer_entero('seleccione el tipo de funcion: ', 1, 3)

        if opcion == 1:
            print('\npolinomio: los coeficientes se ingresan desde el mayor grado hasta el termino independiente')
            print('ejemplo: 2;0;-3 representa 2x**2 - 3')

            while True:
                entrada = input('ingrese los coeficientes separados por punto y coma: ')
                try:
                    coeficientes = [float(valor.strip().replace(',', '.')) for valor in entrada.split(';')]
                    return FuncionPolinomica(coeficientes)

                except ValueError:
                    print('entrada invalida, use punto y coma para separar coeficientes. ejemplo: 2;0;-3')

        if opcion == 2:
            print('\nfuncion seno: f(x) = A · sen(ωx + φ)')

            amplitud = self._leer_float('amplitud A: ')
            frecuencia = self._leer_float('frecuencia ω: ')
            fase = self._leer_float('fase φ (en radianes): ')

            return FuncionSeno(amplitud, frecuencia, fase)

        print('\nfuncion exponencial: f(x) = a · e^(bx) + c')

        a = self._leer_float('parametro a: ')
        b = self._leer_float('parametro b: ')
        c = self._leer_float('parametro c: ')

        return FuncionExponencial(a, b, c)

    def _generar_curva(self):
        print('\n--- generacion de curva matematica ---')

        funcion = self._crear_funcion()

        print(f'\nfuncion seleccionada: {funcion.descripcion()}')

        a = self._leer_float('extremo inicial del intervalo: ')
        b = self._leer_float('extremo final del intervalo: ')

        cantidad = self._leer_entero('cantidad de puntos (minimo 2): ', 2)
        curva = self._generador.generar(funcion, a, b, cantidad)

        self._registrar_curva(curva)
        self._mostrar_curvas([curva], funcion.descripcion())

    #2 GENERACION DE CURVA DE KOCH
    def _generar_koch(self):
        print('\n--- generacion de curva de koch ---')
        print('el nivel de recursividad permitido es de 0 a 6')

        nivel = self._leer_entero('ingrese el nivel: ', 0, 6)
        generador = GeneradorKoch(nivel)
        curva = generador.generar()

        self._registrar_curva(curva)
        self._mostrar_curvas([curva], f'curva de koch - nivel {nivel}')

    #3 GENERACION DEL COPO DE NIEVE DE KOCH
    def _generar_copo_nieve(self):
        print('\n--- generacion del copo de nieve de koch ---')
        print('el nivel de recursividad permitido es de 0 a 6')

        nivel = self._leer_entero('ingrese el nivel: ', 0, 6)
        generador = GeneradorCopoNieve(nivel)
        curva = generador.generar()

        self._registrar_curva(curva)
        self._mostrar_curvas([curva], f'copo de nieve de koch - nivel {nivel}')

    #3 TRANSFORMACIONES GEOMETRICAS
    def _transformar_curva(self):
        print('\n--- transformaciones geometricas ---')

        curva = self._seleccionar_curva()

        if curva is None:
            return

        print('\nseleccione la transformacion:')
        print("1. Escalado")
        print("2. Rotacion")
        print("3. Traslacion")

        opcion = self._leer_entero('opcion: ', 1, 3)

        if opcion == 1:
            sx = self._leer_float('factor de escala en x: ')
            sy = self._leer_float('factor de escala en y: ')
            transformacion = Escalado(sx, sy)

        elif opcion == 2:
            grados = self._leer_float('angulo de rotacion en grados: ')
            angulo = math.radians(grados)
            transformacion = Rotacion(angulo)

        else:
            dx = self._leer_float('desplazamiento horizontal dx: ')
            dy = self._leer_float('desplazamiento vertical dy: ')
            transformacion = Traslacion(dx, dy)

        nueva_curva = transformacion.aplicar_curva(curva)

        self._registrar_curva(nueva_curva)

        print(f'transformacion aplicada: {transformacion.descripcion()}')

        self._mostrar_curvas([curva, nueva_curva], 'comparacion entre curva original y transformada')

    #4 ANALISIS NUMERICO
    def _analisis_numerico(self):
        print('\n--- analisis numerico ---')
        print("1. Busqueda de raices (metodo de biseccion)")
        print("2. Integracion numerica (metodo de los trapecios)")

        opcion = self._leer_entero('seleccione el algoritmo: ', 1, 2)
        funcion = self._crear_funcion()

        print(f'\nfuncion seleccionada: {funcion.descripcion()}')

        a = self._leer_float('extremo inicial del intervalo: ')
        b = self._leer_float('extremo final del intervalo: ')

        if opcion == 1:
            self._ejecutar_biseccion(funcion, a, b)

        else:
            self._ejecutar_trapecio(funcion, a, b)

    def _ejecutar_biseccion(self, p_funcion, p_a, p_b):
        print('\n--- metodo de biseccion ---')

        print('deje vacio para utilizar la tolerancia predeterminada.')
        entrada = input('tolerancia: ').strip()

        if entrada:
            tolerancia = float(entrada.replace(',', '.'))
        else:
            tolerancia = Biseccion.TOLERANCIA_POR_DEFECTO

        max_iteraciones = self._leer_entero('maximo de iteraciones: ', 1)
        algoritmo = Biseccion(tolerancia, max_iteraciones)
        resultado = algoritmo.calcular(p_funcion, p_a, p_b)

        print('\n' + resultado.resumen())

        curva = self._generador.generar(p_funcion, p_a, p_b, 300)

        self._mostrar_curvas([curva], f'biseccion: {p_funcion.descripcion()}')
        self._visualizador.marcar_raiz(resultado.raiz)
        self._visualizador.actualizar()

    def _ejecutar_trapecio(self, p_funcion, p_a, p_b):
        print('\n--- metodo de los trapecios ---')

        cantidad = self._leer_entero('cantidad de subintervalos: ', 1)
        algoritmo = Trapecio(cantidad)
        resultado = algoritmo.calcular(p_funcion, p_a, p_b)

        print('\n' + resultado.resumen())

        curva = self._generador.generar(p_funcion, p_a, p_b, 300)

        self._mostrar_curvas([curva], f'integracion numerica: {p_funcion.descripcion()}')
        self._visualizador.marcar_intervalo(resultado.a, resultado.b)
        self._visualizador.actualizar()

    #5 GESTION DE CURVAS Y PERSISTENCIA
    def _gestionar_curvas(self):
        print('\n--- gestion de curvas guardadas ---')
        print("1. Listar curvas guardadas")
        print("2. Guardar curva de la sesion")
        print("3. Cargar curva guardada")

        opcion = self._leer_entero('seleccione una operacion: ', 1, 3)

        if opcion == 1:
            self._listar_curvas_guardadas()

        elif opcion == 2:
            self._guardar_curva()

        else:
            self._cargar_curva()

    def _listar_curvas_guardadas(self):
        nombres = self._repositorio.listar()
        if not nombres:
            print('\nno hay curvas guardadas')
            return

        print('\ncurvas guardadas:')

        for indice, nombre in enumerate(nombres, start=1):
            print(f'{indice}. {nombre}')

    def _guardar_curva(self):
        curva = self._seleccionar_curva()
        if curva is None:
            return

        sobrescribir = False

        if self._leer_confirmacion('¿desea permitir sobrescribir una curva con el mismo nombre? (s/n): '):
            sobrescribir = True

        self._repositorio.guardar(curva, sobrescribir)

        print(f"\ncurva '{curva.nombre}' guardada correctamente")

    def _cargar_curva(self):
        nombres = self._repositorio.listar()
        if not nombres:
            print('\nno hay curvas guardadas')
            return

        print('\ncurvas disponibles:')

        for indice, nombre in enumerate(nombres, start=1):
            print(f'{indice}. {nombre}')

        opcion = self._leer_entero('seleccione la curva que desea cargar: ', 1, len(nombres))
        curva = self._repositorio.cargar(nombres[opcion - 1])

        self._registrar_curva(curva)

    #6 VISUALIZACION DE CURVAS
    def _visualizar_curvas(self):
        print('\n--- visualizacion de curvas de la sesion ---')

        if not self._curvas:
            print('no hay curvas generadas o cargadas en esta sesion')
            return

        print('\ncurvas disponibles:')

        for indice, curva in enumerate(self._curvas, start=1):
            print(f'{indice}. {curva.nombre}')

        print("0. Mostrar todas")

        opcion = self._leer_entero('\nseleccione una curva o 0 para mostrar todas: ', 0, len(self._curvas))

        if opcion == 0:
            curvas = self._curvas
            titulo = 'todas las curvas de la sesion'

        else:
            curvas = [self._curvas[opcion - 1]]
            titulo = curvas[0].nombre

        self._mostrar_curvas(curvas, titulo)

