from flask import Flask, render_template_string, request, Blueprint, current_app
from typing import Tuple
from html_text import html_text
from functions import (
    get_calles_cortan_calle,
    get_numeros_portales_calle,
    find_cruce,
    create_map,
    get_caminos_minimos,
)


app_route_blueprint = Blueprint("app_route_blueprint", __name__)


def create_app(
    nombre_calles,
    calles,
    direcciones_df,
    calles_names,
    grafo_distancias,
    grafo_velocidades,
) -> Flask:
    """
    Crea la app de flask usando las variables creadas del dataset y los grafos
    """
    app = Flask(__name__)
    app.config["nombre_calles"] = nombre_calles
    app.config["calles"] = calles
    app.config["direcciones_df"] = direcciones_df
    app.config["calles_names"] = calles_names
    app.config["grafo_distancias"] = grafo_distancias
    app.config["grafo_velocidades"] = grafo_velocidades
    return app


def create_cruce_alert_message(calle_cruza, calle) -> str:
    """
    Crea el mensaje de alerta de las calles que cruzan
    """
    if calle_cruza.isnumeric():
        return f"No se ha encontrado el código postal {calle_cruza} en {calle}. "
    return f"{calle_cruza} no se ha encontrado cruzando a {calle}. "


def create_selected_alert_message(calle) -> str:
    """
    Crea el mensaje de alerta de la primera calle seleccionada
    """
    return f"{calle} no se encuentra en el Dataset. "


def get_form(request) -> Tuple:
    """
    Gets all variable from the form in the web page
    """
    selected_calle_salida = request.args.get("calles_salida_input")
    selected_calle_llegada = request.args.get("calles_llegada_input")
    selected_calle_cruza_salida = request.args.get("calle_cruza_salida")
    selected_calle_cruza_llegada = request.args.get("calle_cruza_llegada")
    return (
        selected_calle_salida,
        selected_calle_llegada,
        selected_calle_cruza_salida,
        selected_calle_cruza_llegada,
    )


def get_cruces_from(calle_selected, selected_calle_cruza_seleccionada, alert_message):
    """
    Consigue los cruces de la calle, los códigos postales, cambia las variables a sus valores por defecto si hay algún problema
    """
    codigo_calle_seleccionada = current_app.config["nombre_calles"].get(
        calle_selected, None
    )
    calle_seleccionada_names = []
    calle_seleccionada = None
    numeros_portales_seleccionada = None
    if codigo_calle_seleccionada is not None:
        calle_seleccionada = current_app.config["calles"][codigo_calle_seleccionada]

        if len(calle_seleccionada.cruces) == 0:
            alert_message += f"No hay cruces en {calle_selected}. "
            calle_selected = None
            calle_seleccionada = None
            selected_calle_cruza_seleccionada = None

        else:
            calle_seleccionada_names = get_calles_cortan_calle(
                calle_seleccionada,
                calle_selected,
            )
            numeros_portales_seleccionada = get_numeros_portales_calle(
                calle_selected, current_app.config["direcciones_df"]
            )
            calle_seleccionada_names = (
                list(numeros_portales_seleccionada.keys()) + calle_seleccionada_names
            )

    else:
        alert_message += create_selected_alert_message(calle_selected)
        selected_calle_cruza_seleccionada = None
        calle_selected = None

    return (
        calle_selected,
        calle_seleccionada,
        selected_calle_cruza_seleccionada,
        calle_seleccionada_names,
        numeros_portales_seleccionada,
        alert_message,
    )


def get_cruce(
    calle_seleccionada,
    numeros_portales_seleccionada,
    selected_calle_seleccionada,
    selected_calle_cruza_seleccionada,
    alert_message,
):
    """
    Encuentra el cruce seleccionado a partir del portal o del nombre de la calle que cruza
    """
    cruce_seleccionada = find_cruce(
        calle_seleccionada,
        selected_calle_cruza_seleccionada,
        numeros_portales_seleccionada,
    )
    if cruce_seleccionada is None and selected_calle_cruza_seleccionada:
        alert_message += create_cruce_alert_message(
            selected_calle_cruza_seleccionada, selected_calle_seleccionada
        )
        selected_calle_cruza_seleccionada = None
    return cruce_seleccionada, selected_calle_cruza_seleccionada, alert_message


@app_route_blueprint.route("/")
def app_route() -> str:
    # Set all variables to default value
    cruce_salida = None
    cruce_llegada = None
    calle_salida = None
    calle_llegada = None
    calle_salida_names = []
    calle_llegada_names = []
    direcciones_d = []
    direcciones_v = []
    loc_d = None
    loc_v = None
    alert_message = ""
    numeros_portales_llegada = None
    numeros_portales_salida = None

    (
        selected_calle_salida,
        selected_calle_llegada,
        selected_calle_cruza_salida,
        selected_calle_cruza_llegada,
    ) = get_form(request)

    if selected_calle_salida:
        (
            selected_calle_salida,
            calle_salida,
            selected_calle_cruza_salida,
            calle_salida_names,
            numeros_portales_salida,
            alert_message,
        ) = get_cruces_from(
            selected_calle_salida, selected_calle_cruza_salida, alert_message
        )

    if selected_calle_llegada:
        (
            selected_calle_llegada,
            calle_llegada,
            selected_calle_cruza_llegada,
            calle_llegada_names,
            numeros_portales_llegada,
            alert_message,
        ) = get_cruces_from(
            selected_calle_llegada, selected_calle_cruza_llegada, alert_message
        )

    if selected_calle_cruza_salida:
        cruce_salida, selected_calle_cruza_salida, alert_message = get_cruce(
            calle_salida,
            numeros_portales_salida,
            selected_calle_salida,
            selected_calle_cruza_salida,
            alert_message,
        )

    if selected_calle_cruza_llegada:
        cruce_llegada, selected_calle_cruza_llegada, alert_message = get_cruce(
            calle_llegada,
            numeros_portales_llegada,
            selected_calle_llegada,
            selected_calle_cruza_llegada,
            alert_message,
        )

    # Si se han encontrado los dos cruces, se crea el camino.
    if cruce_salida and cruce_llegada:
        # Si es el mismo cruce, se muestra el error
        if cruce_salida == cruce_llegada:
            alert_message = f"El punto de partida y el destino son el mismo. "
        else:
            # Se busca el camino
            loc_d, direcciones_d, loc_v, direcciones_v = get_caminos_minimos(
                cruce_salida,
                cruce_llegada,
                current_app.config["grafo_distancias"],
                current_app.config["grafo_velocidades"],
            )

    # Se crea el camino
    m = create_map(cruce_salida, cruce_llegada, loc_d, loc_v)

    m.get_root().render()
    map = m.get_root().html.render()
    header = m.get_root().header.render()
    script = m.get_root().script.render()

    if alert_message:
        alert_message += "Por favor, vuelva a intentarlo."

    return render_template_string(
        html_text,
        names=current_app.config["calles_names"],
        map=map,
        selected_calle_salida=selected_calle_salida,
        selected_calle_llegada=selected_calle_llegada,
        selected_calle_cruza_salida=selected_calle_cruza_salida,
        selected_calle_cruza_llegada=selected_calle_cruza_llegada,
        calle_salida_names=calle_salida_names,
        calle_llegada_names=calle_llegada_names,
        header=header,
        script=script,
        direcciones_d=direcciones_d,
        direcciones_v=direcciones_v,
        alert_message=alert_message,
    )
