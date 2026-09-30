"""
callejero.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GPxxx
Integrantes:
    - Pablo Tuñón Laguna
    - Jorge Vančo Sampedro

Descripción:
Librería con herramientas y clases auxiliares necesarias para la representación de un callejero en un grafo.

Complétese esta descripción según las funcionalidades agregadas por el grupo.
"""

from typing import List, Tuple, Dict, Type, Any

# Constantes con las velocidades máximas establecidas por el enunciado para cada tipo de vía.

VELOCIDADES_CALLES: Dict[str, int] = {
    "AUTOVIA": 100,
    "AVENIDA": 90,
    "CARRETERA": 70,
    "CALLEJON": 30,
    "CAMINO": 30,
    "ESTACION DE METRO": 20,
    "PASADIZO": 20,
    "PLAZUELA": 20,
    "COLONIA": 20,
}
VELOCIDAD_CALLES_ESTANDAR = 50


class Cruce:
    # Completar esta clase con los datos y métodos que se necesite asociar a cada cruce

    def __init__(
        self, coord_x: int, coord_y: int, location: list, points: list
    ) -> None:
        self.coord_x: int = coord_x
        self.coord_y: int = coord_y
        self.point = (coord_x, coord_y)
        self.location = location  # [latitud, longitud]
        self.points = points
        self.calles: list = []

    def add_calle(self, calle):
        self.calles.append(calle)

    def add_calles(self, calles):
        for calle in calles:
            self.add_calle(calle)

    def has_calle(self, calle):
        if isinstance(calle, int):
            index = 1
        else:
            index = 0

        return calle in list(zip(*self.calles))[index]

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return (self.coord_x == other.coord_x) and (self.coord_y == other.coord_y)
        else:
            return False

    def __le__(self, other) -> bool:
        return (self.coord_x, self.coord_y) <= (other.coord_x, other.coord_y)

    def __lt__(self, other) -> bool:
        return (self.coord_x, self.coord_y) < (other.coord_x, other.coord_y)

    def __hash__(self) -> int:
        return hash((self.coord_x, self.coord_y))

    def __repr__(self) -> str:
        return f"({self.coord_x}, {self.coord_y}) -> {self.calles}"


class Calle:
    # velocidad
    # clase de la vía
    # codigo de número
    # codigo de via
    # nombre de la via
    def __init__(self, codigo, clase, nombre) -> None:
        self.codigo = int(codigo)
        self.nombre = nombre  # nombre
        self.cruces: set = set()
        self.clase = clase
        self.velocidad = (
            VELOCIDADES_CALLES.get(clase, VELOCIDAD_CALLES_ESTANDAR) * 5000 / 3
        )  # pasarlo a cm/min

    def add_cruce(self, cruce) -> None:
        self.cruces.add(cruce)

    def toDict(self) -> Dict[str, Any]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "cruces": self.cruces,
        }
