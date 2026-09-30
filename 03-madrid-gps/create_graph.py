import time
from callejero import Cruce, Calle
from clean_dgt import process_data
from functions import dot_product_vector, get_vector
from grafo import Grafo
from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import copy
import numpy as np


columna_x = "Coordenada X (Guia Urbana) cm (cruce)"
columna_y = "Coordenada Y (Guia Urbana) cm (cruce)"

nombre_calle = "Nombre completo de la via que cruza"
codigo_calle = "Codigo de via que cruza o enlaza"

group_id: int = 1


def compare_y(row, y, R) -> bool:
    y2 = row[columna_y]
    return y2 <= y + R and y2 >= y - R


def set_groups(cruces, cruce, row, y, R) -> None:
    global group_id
    cruce_id = row["group_id"]

    if compare_y(cruce, y, R):
        new_id = cruce["group_id"]
        if cruce_id is None:
            if new_id is not None:
                cruce_id = new_id
            else:
                cruce_id = group_id
                group_id += 1
                cruces.loc[cruce.name, "group_id"] = cruce_id
            cruces.loc[row.name, "group_id"] = cruce_id
        else:
            if new_id is not None:
                if new_id != cruce_id:
                    cruces.loc[cruces["group_id"] == new_id, "group_id"] = cruce_id
            else:
                cruces.loc[cruce.name, "group_id"] = cruce_id


def definir_grupo(cruces, row, R) -> None:
    global group_id

    low_boundary = row.name + 1
    x = row[columna_x]
    y = row[columna_y]

    cruces[(cruces[columna_x] >= x) & (cruces[columna_x] <= x + R)].loc[
        low_boundary:
    ].apply(lambda r: set_groups(cruces, r, row, y, R), axis=1)


def agrupar_puntos(cruces, R) -> None:
    cruces.apply(lambda row: definir_grupo(cruces, row, R), axis=1)


def crear_cruces(cruces, calles, grafo_distancias) -> None:
    for _, df in cruces.groupby("group_id"):
        coord_x, coord_y, lat, lon = (
            df[[columna_x, columna_y, "latitud", "longitud"]].mean().tolist()
        )
        c = Cruce(coord_x, coord_y, [lat, lon], None)
        grafo_distancias.agregar_vertice(c)
        c.calles = list(
            df[[nombre_calle, codigo_calle]]
            .drop_duplicates(codigo_calle)
            .itertuples(index=False, name=None)
        )
        for calle in c.calles:
            calles[calle[1]].add_cruce(c)


def sort_cruces_calle(cruces) -> List:
    return sorted(list(cruces))


def distance(cruce1, cruce2) -> float:
    return np.sqrt(
        (cruce1.coord_x - cruce2.coord_x) ** 2 + (cruce1.coord_y - cruce2.coord_y) ** 2
    )


def get_aristas(cruces) -> List:
    if len(cruces) < 3:
        if len(cruces) < 2:
            return []
        return [(*cruces, distance(cruces[0], cruces[1]))]

    distancias = []
    cruce2 = cruces[0]

    for cruce in cruces[1:]:
        d = distance(cruce2, cruce)
        distancias.append((d, cruce))

    distancias.sort()

    cruce1 = distancias[0][1]
    aristas = [(cruce2, cruce1, distancias[0][0])]

    v = get_vector(cruce2, cruce1)

    for d, cruce in distancias[1:]:
        producto_escalar = dot_product_vector(v, get_vector(cruce1, cruce))

        if producto_escalar >= 0:
            aristas.append((cruce1, cruce, distance(cruce1, cruce)))
            cruce1 = cruce
            v = get_vector(cruces[0], cruce)
        else:
            aristas.append((cruce2, cruce, distance(cruce2, cruce)))
            cruce2 = cruce
    return aristas


def unir_cruces(calles, grafo_distancias, grafo_velocidades) -> None:
    for calle in calles:
        cruces_list = list(calles[calle].cruces)
        if len(cruces_list) > 0:
            aristas = get_aristas(cruces_list)
            for a in aristas:
                if len(a) > 1:
                    distancia_arista = a[2]
                    tiempo = distancia_arista / calles[calle].velocidad

                    data = {
                        "longitud": distancia_arista,
                        "tiempo": tiempo,
                        "calle": calles[calle].nombre,
                        "vector": get_vector(a[0], a[1]),
                    }

                    grafo_distancias.agregar_arista(
                        a[0], a[1], weight=distancia_arista, data=data
                    )
                    grafo_velocidades.agregar_arista(
                        a[0], a[1], weight=tiempo, data=data
                    )


def create_graphs(
    path_cruces: str, path_direcciones: str, R: int
) -> Tuple[Grafo, Grafo]:
    cruces, direcciones = process_data(path_cruces, path_direcciones)

    t0 = time.time()

    cruces = cruces.sort_values(columna_x).reset_index(drop=True)
    cruces["group_id"] = None

    codigos_unicos = (
        set(
            cruces[
                [
                    "Codigo de vía tratado",
                    "Clase de la via tratado",
                    "Nombre completo de la via tratado",
                ]
            ]
            .drop_duplicates(subset="Codigo de vía tratado")
            .itertuples(index=False, name=None)
        )
        | set(
            cruces[
                [
                    "Codigo de via que cruza o enlaza",
                    "Clase de la via que cruza",
                    "Nombre completo de la via que cruza",
                ]
            ]
            .drop_duplicates(subset="Codigo de via que cruza o enlaza")
            .itertuples(index=False, name=None)
        )
        | set(
            direcciones[
                ["Codigo de via", "Clase de la via", "Nombre completo de la via"]
            ]
            .drop_duplicates(subset="Codigo de via")
            .itertuples(index=False, name=None)
        )
    )
    calles = {
        codigo: Calle(codigo, clase_de_via, nombre)
        for codigo, clase_de_via, nombre in codigos_unicos
    }

    nombre_calles = {nombre: codigo for codigo, _, nombre in codigos_unicos}

    agrupar_puntos(cruces, R)

    grafo_distancias = Grafo()

    crear_cruces(cruces, calles, grafo_distancias)

    grafo_velocidades = copy.deepcopy(grafo_distancias)

    unir_cruces(calles, grafo_distancias, grafo_velocidades)

    t1 = time.time()

    print(f"Ha tardado {t1 - t0}s")

    return (
        grafo_distancias,
        grafo_velocidades,
        calles,
        nombre_calles,
        cruces,
        direcciones,
    )
    
if __name__ == "__main__":
    path_cruces = "cruces.csv"
    path_direcciones = "direcciones.csv"
    R: int = 2000  # cm
    grafo_distancias, grafo_velocidades, calles, nombre_calles, cruces, direcciones = create_graphs(
        path_cruces, path_direcciones, R
    )

    nx_graph = grafo_distancias.convertir_a_NetworkX()
    nx.draw_networkx(
        nx_graph,
        with_labels=False,
        pos={node: (node.coord_x, node.coord_y) for node in nx_graph.nodes},
        node_size=0.3,
    )

    plt.show()
