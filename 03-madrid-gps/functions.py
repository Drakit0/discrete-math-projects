import numpy as np
import folium
from typing import List, Tuple


def get_vector(cruce1, cruce2) -> Tuple:
    return (cruce2.coord_x - cruce1.coord_x, cruce2.coord_y - cruce1.coord_y)


def get_tercera_coordenada_producto_vectorial(v1, v2) -> float:
    """
    Calcula el valor de la tercera coordenada del producto vectorial
    """
    x1, y1 = v1
    x2, y2 = v2
    return x1 * y2 - y1 * x2


def get_giro(v1, v2) -> str:
    """
    Decide hacia donde hay que girar
    """
    if get_tercera_coordenada_producto_vectorial(v1, v2) > 0:
        return "izquierda"
    else:
        return "derecha"


def dot_product_vector(v1, v2) -> float:
    """
    Producto escalar de dos vectores
    """
    return v1[0] * v2[0] + v2[1] * v1[1]


def vector_norm(v) -> float:
    """
    Norma del vector
    """
    return np.sqrt(np.square(v[0]) + np.square(v[1]))


def cos_angle(v1, v2) -> float:
    """
    Coseno del ángulo que forman dos vectores
    """
    return dot_product_vector(v1, v2) / (vector_norm(v1) * vector_norm(v2))


def get_caracter_ordinal(num) -> str:
    """
    Encuentra el caracter ordinal para un número
    """
    caracteres_ordinales = {1: "er", 3: "er"}
    resto = num % 10
    return caracteres_ordinales.get(resto, "º")


def get_direcciones(camino_minimo, grafo) -> List[str]:
    """
    Obtiene las direcciones para un camino
    """

    direcciones = []

    cruce_inicial = camino_minimo[0]

    if len(camino_minimo) < 2:
        return ["No se ha encontrado el camino seleccionado"]

    arista1, _ = grafo.obtener_arista(cruce_inicial, camino_minimo[1])
    longitud1 = arista1.data["longitud"]

    longitud_total_trayecto = longitud1

    tiempo_total = arista1.data["tiempo"]

    cruces_pasados = 0
    for i, cruce in enumerate(camino_minimo[2:], 1):
        arista2, _ = grafo.obtener_arista(camino_minimo[i], cruce)

        vector1 = get_vector(camino_minimo[i - 1], camino_minimo[i])
        calle1 = arista1.data["calle"]

        vector2 = get_vector(camino_minimo[i], cruce)
        longitud2 = arista2.data["longitud"]
        calle2 = arista2.data["calle"]

        if calle1 == calle2:
            longitud1 += longitud2
            cruces_pasados += 1

            if i == len(camino_minimo) - 2:
                caracter_ordinal = get_caracter_ordinal(cruces_pasados + 1)
                direcciones.append(
                    f"Continúe por <strong>{calle1}</strong> {(longitud1 + longitud2)/100:0.0f} metros, en el {cruces_pasados + 1}{caracter_ordinal} cruce está su destino."
                )
        else:
            # Se comprueba el ángulo por si el giro es demasiado pequeño como para decir girar
            if cos_angle(vector1, vector2) < 0.9:
                giro = get_giro(vector1, vector2)
                if (
                    cruces_pasados > 0
                ):  # Significa que hemos seguido recto por la calle:
                    caracter_ordinal = get_caracter_ordinal(cruces_pasados + 1)
                    if i == len(camino_minimo) - 2:
                        direcciones.append(
                            f"En {longitud1/100:0.0f} metros <strong>gire a la {giro}</strong> en el {cruces_pasados + 1}{caracter_ordinal} cruce por <strong>{calle2}</strong>. En {longitud2/100:0.0f} metros habrá llegado a su destino."
                        )
                    else:
                        direcciones.append(
                            f"Continúe recto por {calle1} {longitud1/100:0.0f} metros, <strong>gire a la {giro}</strong> en el {cruces_pasados + 1}{caracter_ordinal} cruce por <strong>{calle2}</strong>."
                        )
                else:
                    if i == len(camino_minimo) - 2:
                        direcciones.append(
                            f"En {longitud1/100:0.0f} metros <strong>gire a la {giro}</strong> por <strong>{calle2}</strong>. En {longitud2/100:0.0f} metros habrá llegado a su destino."
                        )
                    else:
                        direcciones.append(
                            f"En {longitud1/100:0.0f} metros <strong>gire a la {giro}</strong> por <strong>{calle2}</strong>."
                        )

            else:
                if i == len(camino_minimo) - 2:
                    direcciones.append(
                        f"En {longitud1/100:0.0f} metros, <strong>continúe</strong> recto por <strong>{calle2}</strong>. En {longitud2/100:0.0f} metros habrá llegado a su destino."
                    )
                else:
                    direcciones.append(
                        f"En {longitud1/100:0.0f} metros, <strong>continúe</strong> recto por <strong>{calle2}</strong>."
                    )

            longitud1 = longitud2
            cruces_pasados = 0

        longitud_total_trayecto += longitud2
        tiempo_total += arista2.data["tiempo"]
        arista1 = arista2

    direcciones.insert(0, f"Tiempo estimado: {tiempo_total:0.0f} min.")
    direcciones.insert(
        0,
        f"La longitud del total del trayecto es {longitud_total_trayecto/100000:0.02f} km.",
    )

    return direcciones


def get_caminos_minimos(
    cruce_salida, cruce_llegada, grafo_distancias, grafo_velocidades
):
    """
    Encuentra los caminos mínimos y las direcciones de las dos rutas.
    """
    camino_minimo_distancias = grafo_distancias.camino_minimo(
        cruce_salida, cruce_llegada
    )
    camino_minimo_velocidad = grafo_velocidades.camino_minimo(
        cruce_salida, cruce_llegada
    )

    direcciones_d = get_direcciones(camino_minimo_distancias, grafo_distancias)
    direcciones_v = get_direcciones(camino_minimo_velocidad, grafo_velocidades)

    loc_d = [node.location for node in camino_minimo_distancias]
    loc_v = [node.location for node in camino_minimo_velocidad]
    return loc_d, direcciones_d, loc_v, direcciones_v


def create_map(
    cruce_salida=None, cruce_llegada=None, loc_d=None, loc_v=None
) -> folium.Map:
    """
    Crea el mapa de folium
    """
    m = folium.Map(
        location=[40.416775, -3.45],  # -3.703790],
        zoom_start=11,
        zoom_control=False,
    )

    # Añadir salida
    if cruce_salida is not None:
        folium.Marker(
            location=cruce_salida.location,
            icon=folium.Icon(color="green", icon="star"),
        ).add_to(m)

    # Añadir destino
    if cruce_llegada is not None:
        folium.Marker(
            location=cruce_llegada.location,
            icon=folium.Icon(color="blue", icon="fa-flag-checkered", prefix="fa"),
        ).add_to(m)

    # Añadir caminos
    if loc_d:
        folium.PolyLine(loc_d, color="green", weight=3, opacity=0.8).add_to(m)
    if loc_v:
        folium.PolyLine(loc_v, color="blue", weight=3, opacity=0.8).add_to(m)

    return m


def get_calles_cortan_calle(calle, nombre_calle) -> List:
    """
    Consigue el nombre de las calles que cortan a dicha calle
    """
    new_calles = set()
    for cruce in calle.cruces:
        new_calles = new_calles | set(list(zip(*cruce.calles))[0])
    new_calles -= {nombre_calle}
    return list(new_calles)


def get_numeros_portales_calle(nombre_calle, direcciones_df) -> None:
    """
    Consigue los números de portales de una calle
    """
    k = direcciones_df[direcciones_df["Nombre completo de la via"] == nombre_calle][
        ["Coordenada X (Guia Urbana) cm", "Coordenada Y (Guia Urbana) cm", "Numero"]
    ].apply(
        lambda r: (
            (r["Coordenada X (Guia Urbana) cm"], r["Coordenada Y (Guia Urbana) cm"]),
            r["Numero"],
        ),
        axis=1,
    )
    diccionario_codigos = {}

    for coord, num in k:
        diccionario_codigos[num] = coord
    return diccionario_codigos


def distance_points(p, q) -> float:
    """
    Calcula la distancia entre dos puntos
    """
    return np.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def find_cruce(calle, calle_seleccionada, numeros_portales):
    """
    Encuentra el cruce elegido para una calle a partir del número de portal o el nombre de la calle que la cruza
    """
    # Si es un número se encuentra el cruce más cercano al portal
    if calle_seleccionada.isnumeric():
        numero_portal = int(calle_seleccionada)
        coord_numero_portal = numeros_portales.get(numero_portal, None)
        if coord_numero_portal is None:
            return

        min_node = None
        min_distance = None
        # Se busca el cruce más cercano
        for nodo in calle.cruces:
            d = distance_points(coord_numero_portal, nodo.point)
            if min_node is None or d < min_distance:
                min_node = nodo
                min_distance = d
        return min_node

    else:
        # Se busca el cruce con la calle elegida
        for nodo in calle.cruces:
            if nodo.has_calle(calle_seleccionada):
                return nodo