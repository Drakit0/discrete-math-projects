import rsa
import os
import modular


def key_upload(user_name: str) -> dict:
    """Se sube la información de cada usuario que se va a comunicar de la carpeta de usuarios."""
    try:
        with open(
            f"Usuarios/priv_{user_name}.txt", "r", encoding="utf-8"
        ) as file:  # Lectura de la clave privada
            d = int(file.read())

        with open(
            f"Usuarios/pub_{user_name}.txt", "r", encoding="utf-8"
        ) as file:  # Lectura de la clave pública, el modulo y el padding
            n = int(file.readline())
            e = int(file.readline())
            padding = int(file.readline())

    except FileNotFoundError:
        raise FileNotFoundError(f"El usuario {user_name} no existe.")

    return {"d": d, "n": n, "e": e, "padding": padding}


def message_cipher(users_info: dict) -> str:
    """Cifrado de mensaje a través de rsa haciendo uso de un padding."""

    plain_text = input(
        f"Introduzca el texto plano que desea cifrar para {users_info['name']}:\n"
    )
    ciphered_text = rsa.cifrar_mensaje_rsa(
        plain_text, users_info["n"], users_info["e"], users_info["padding"]
    )  # Cifrado del mensaje
    print(ciphered_text)

    return ciphered_text


def message_decipher(users_info: dict, user_1: str) -> str:
    """Descifrado de texto cifrado a través de rsa."""

    ciphered_text = input(f"Introduzca el mensaje cifrado proveniente de {user_1}:\n")

    try:
        plain_text = rsa.descifrar_mensaje_rsa(
            ciphered_text, users_info["n"], users_info["d"], users_info["padding"]
        )  # Descifrado del mensaje
        print(plain_text)

    except ValueError as e:
        raise ValueError(f"No se ha podido descifrar el mensaje {ciphered_text}")
        plain_text = "*"  # En caso de que el mensaje no se pueda descifrar, se devuelve un asterisco

    return plain_text


def format_text(text: str) -> str:  # Función para formatear el texto
    """Formateo del texto para que sea descifrado."""

    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("'", "")
    text = text.replace(",", "")

    return [int(c) for c in text.split(" ")]


def get_mensajes_disponibles(receptor, emisor):
    mensajes_disponibles = []
    mensajes = os.listdir("Mensajes")
    
    for mensaje in mensajes:
        if mensaje.startswith(f"{emisor}_{receptor}"):
            mensajes_disponibles.append(mensaje)
            
    return mensajes_disponibles


if __name__ == "__main__":
    program_running = True
    
    while program_running:
        print("\n")
        not_users = True
        message = None
        
        while not_users:
            user_1 = input("Introduzca su nombre de usuario: ")
            user_2 = input(
                "Introduzca el nombre de usuario con el que quiere comunicarse: "
            )

            users_info = {}

            try:  # Se sube la información de los usuarios
                users_info["usuario_1"] = key_upload(user_1)
                users_info["usuario_1"]["name"] = user_1
                users_info["usuario_2"] = key_upload(user_2)
                users_info["usuario_2"]["name"] = user_2
                
                not_users = False

            except FileNotFoundError as e:
                print(e)

        value = ""
        counter = 0

        while value not in (
            "C",
            "D",
            "S",
        ):  # Se elige si se quiere cifrar, descifrar o salir
            value = input("Desea cifrar (C), descifrar (D) o salir (S)?: ")
            value = value.upper()

            if value != "C" and value != "D" and value != "S":
                counter += 1
                modular.function(counter)

        if value == "C":
            message = message_cipher(users_info["usuario_2"])  # Se cifra el mensaje
            message = message.split(" ")

        elif value == "D":
            answer = ""

            while answer not in (
                "F",
                "H",
            ):  # Se elige si se quiere descifrar un fichero o un mensaje escrito a mano
                answer = input(
                    "Desea descifrar un fichero ya cargado (F) o un mensage escrito a mano (H)?: "
                )
                answer = answer.upper()

            if answer == "F":
                read = False
                while not read:
                    os.makedirs("Mensajes", exist_ok = True)
                    mensajes_disponibles = get_mensajes_disponibles(user_1, user_2)
                    
                    if len(mensajes_disponibles) > 0:
                        print("Ficheros disponibles:")
                        print(", ".join(mensajes_disponibles))
                        print()

                        try:  # Se descifra el fichero
                            file_name = input(
                                "Introduzca el nombre del fichero que desea descifrar: "
                            )
                            if file_name in mensajes_disponibles:
                                decipher_file = open(
                                    f"Mensajes/{file_name}", "r", encoding="utf-8"
                                )
                                ciphered_text = decipher_file.read()
                                decipher_file.close()
                                ciphered_text = format_text(ciphered_text)

                                plain_text = rsa.descifrar_cadena_rsa(
                                    ciphered_text,
                                    users_info["usuario_1"]["n"],
                                    users_info["usuario_1"]["d"],
                                    users_info["usuario_1"]["padding"],
                                )
                                print(plain_text)
                                read = True
                        except FileNotFoundError:
                            print(f"El fichero {file_name} no existe.")
                    else:
                        print(
                            "No hay mensajes disponibles para descifrar provenientes de",
                            user_2,
                        )
                        print()
                        read = True
                        answer_saving_file = "N"

            else:  # Se descifra el mensaje escrito a mano
                try:
                    plain_text = message_decipher(
                        users_info["usuario_1"], users_info["usuario_2"]["name"]
                    )
                    plain_txt = [plain_text]
                except ValueError as e:
                    print(e)
                    print()
                    answer_saving_file = "N"

        else:
            program_running = False
            
        answer_saving_file = ""

        while (
            answer_saving_file not in ("G", "N") and program_running and message != None
        ):  # Opción de guardar el mensaje descifrado
            print("En caso de que desee guardar el resultado, este se guardará como:")
            print(
                "Emisor_Receptor_Tipo de acción ejecutada_Número de veces ejecutada la acción."
            )
            answer_saving_file = input(
                "Desea guardar (G) o no guardar (N) en un txt la operación realizada: "
            )

            answer_saving_file = answer_saving_file.upper()

            if answer_saving_file == "G":  # Se guarda el mensaje descifrado
                os.makedirs(
                    "Mensajes", exist_ok=True
                )  # Se crea la carpeta de mensajes si no existe
                existing_files = [
                    file
                    for file in os.listdir("Mensajes")
                    if file.startswith(f"{user_1}_{user_2}_{value}_")
                ]

                if (
                    len(existing_files) > 0
                ):  # Se comprueba si ya existe un fichero con el mismo nombre y se le añade un indice al final
                    existing_indices = [
                        int(file.split("_")[-1].replace(".txt", ""))
                        for file in existing_files
                    ]
                    last_index = existing_indices[-1] + 1

                else:
                    last_index = 1

                with open(
                    f"Mensajes/{user_1}_{user_2}_{value}_{last_index}.txt",
                    "w",
                    encoding="utf-8",
                ) as file:  # Se guarda el mensaje descifrado
                    file.write(str(message))
