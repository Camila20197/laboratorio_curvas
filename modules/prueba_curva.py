
from pathlib import Path
from modules.geometria import Punto, Curva
from modules.persistencia import RepositorioCurvas

#1 crear puntos
p1 = Punto(0, 0)
p2 = Punto(3, 0)
p3 = Punto(3, 4)

#2 comprobar coordenadas homogeneas
print('coordenadas homogeneas:', p1.a_homogeneo())

#3 reconstruccion de punto
p4 = Punto.desde_homogeneo([6, 8, 2])
print('ounto reconstruido:', p4.x, p4.y)

#4 crear curva y agregar puntos
curva = Curva('curva de prueba')

curva.agregar_punto(p1)
curva.agregar_punto(p2)
curva.agregar_punto(p3)

print('nombre:', curva.nombre)
print('cantidad de puntos:', curva.cantidad_puntos())
print('coordenadas X:', curva.coordenadas_x())
print('coordenadas Y:', curva.coordenadas_y())
print('longitud:', curva.longitud())

#5 crear repositorio
repositorio = RepositorioCurvas(Path('data/curvas'))

#6 guardar curva
repositorio.guardar(curva)

#7 listar curvas almacenadas
print('curvas guardadas:', repositorio.listar())

#8 recuperar curva
curva_recuperada = repositorio.cargar('curva de prueba')

print('curva recuperada:', curva_recuperada.nombre)
print('puntos recuperados:', curva_recuperada.cantidad_puntos())
print('longitud recuperada:', curva_recuperada.longitud())
