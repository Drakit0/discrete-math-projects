import rsa
import os
import re


def get_int_value(message):
    int_value = ""

    while not int_value.isnumeric():
        int_value = input(message)

    return int(int_value)


if __name__ == "__main__":
    
    name = input("Nombre: ")
    name_regex = re.compile(r"[A-Za-z0-9_]+")
    while name_regex.fullmatch(name) is None:
        print("Hay caracteres no permitidos.")
        name = input("Nombre: ")

    wrong_data = True

    while wrong_data:
        value_min = get_int_value("Valor mínimo para generar sus claves de RSA: ")
        value_max = get_int_value("Valor máximo para generar sus claves de RSA: ")

        print("Generando claves...")
        n, e, d = rsa.generar_claves(value_min, value_max)  # generar las claves

        if n == None or e == None:  # evaluación casos límite
            print(
                "Lo sentimos, el intervalo introducido no cuenta con al menos dos números primos, necesarios para obtener p y q."
            )
            print("Por favor, vuelva a intentarlo.")

        else:
            wrong_data = False

    print("Claves generadas")
    max_padding = rsa.max_theoretical_padding(n)  # obtener el máximo padding teórico
    num_padding = -1

    while num_padding < 0 or num_padding > max_padding:
        num_padding = get_int_value(
            f"Número de cifras de padding para la comunicación (el valor máximo es {max_padding}): "
        )

    while not (n and e and d):
        value_min = get_int_value("Valor mínimo para generar sus claves de RSA: ")
        value_max = get_int_value("Valor máximo para generar sus claves de RSA: ")
        n, e, d = rsa.generar_claves(value_min, value_max)

    os.makedirs("Usuarios", exist_ok=True)

    with open(f"Usuarios/pub_{name}.txt", "w", encoding="utf-8") as file:
        file.write(f"{n}\n{e}\n{num_padding}")

    with open(f"Usuarios/priv_{name}.txt", "w", encoding="utf-8") as file:
        file.write(str(d))

    print("Usuario registrado con éxito")
