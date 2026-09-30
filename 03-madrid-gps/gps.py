from create_graph import create_graphs
from flask_app import create_app, app_route_blueprint

path_cruces = "cruces.csv"
path_direcciones = "direcciones.csv"

R: int = 1500  # cm


if __name__ == "__main__":
    # Creamos los grafos
    (
        grafo_distancias,
        grafo_velocidades,
        calles,
        nombre_calles,
        cruces,
        direcciones_df,
    ) = create_graphs(path_cruces, path_direcciones, R)

    # Los nombres de las calles
    calles_names = sorted(nombre_calles.keys())

    app = create_app(
        nombre_calles,
        calles,
        direcciones_df,
        calles_names,
        grafo_distancias,
        grafo_velocidades,
    )
    app.register_blueprint(app_route_blueprint)

    app.run()