
from pathlib import Path
from modules.geometria.curva import Curva
from modules.geometria.punto import Punto
import json
import re

class RepositorioCurvas:
    def __init__(self, p_directorio: Path):
        self._directorio = Path(p_directorio)
        self._directorio.mkdir(parents=True, exist_ok=True)

    def guardar(self, p_curva: Curva, p_sobrescribir: bool = False) -> bool:
        if not isinstance(p_curva, Curva):
            raise TypeError('solo se pueden guardar objetos Curva')

        if not isinstance(p_sobrescribir, bool):
            raise TypeError('p_sobrescribir debe ser booleano')

        nombre_archivo = self._nombre_seguro(p_curva.nombre)
        ruta = self._directorio / f'{nombre_archivo}.json'

        #verificamos si ya existe una curva con ese nombre
        if ruta.exists() and not p_sobrescribir:
            raise FileExistsError(f'ya existe una curva guardada con el nombre '{p_curva.nombre}'")

        datos = {
           'nombre': p_curva.nombre,
           'puntos': [{'x': punto.x, 'y': punto.y} for punto in p_curva]
        }

        with ruta.open('w', encoding='utf-8') as archivo:
           json.dump(datos, archivo, indent=4, ensure_ascii=False)

        return True

    def cargar(self, p_nombre: str) -> Curva:
        nombre_archivo = self._nombre_seguro(p_nombre)
        ruta = self._directorio / f'{nombre_archivo}.json'

        if not ruta.is_file():
            raise FileNotFoundError(f"No existe una curva guardada con el nombre '{p_nombre}'")

        with ruta.open('r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            raise ValueError('el archivo no contiene una curva valida')

        if 'nombre' not in datos or 'puntos' not in datos:
            raise ValueError('el archivo no contiene los datos necesarios')

        if not isinstance(datos['nombre'], str) or not datos['nombre'].strip():
            raise ValueError('el nombre de la curva no es valido')

        if not isinstance(datos['puntos'], list):
            raise ValueError('la lista de puntos no es valida')

        curva = Curva(datos['nombre'])

        for coordenadas in datos['puntos']:
            if not isinstance(coordenadas, dict):
                raise ValueError('un punto almacenado no es valido')

            if 'x' not in coordenadas or 'y' not in coordenadas:
                raise ValueError('faltan coordenadas de un punto')

            punto = Punto(coordenadas['x'], coordenadas['y'])

            curva.agregar_punto(punto)

        return curva

    def listar(self) -> list:
        return sorted(ruta.stem for ruta in self._directorio.glob('*.json') if ruta.is_file())

    @staticmethod
    def _nombre_seguro(p_nombre: str) -> str:
        if not isinstance(p_nombre, str) or not p_nombre.strip():
            raise ValueError('el nombre no puede estar vacio')

        nombre = p_nombre.strip()

        if not re.fullmatch(r"[\w -]+", nombre):
            raise ValueError('el nombre contiene caracteres no permitidos')

        return nombre
