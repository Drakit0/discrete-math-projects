"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP01B
Integrantes:
    - Pablo Tuñón Laguna
    - Jorge Vančo Sampedro

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin parámetros,
lanzaría la interfaz de usuario para el modo interactivo.
"""

from typing import TextIO, List
import modular
import re
from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog


def primo(n: int) -> str:
    """
    Calcula si el número es primo o no

    Args:
        n (int): el número

    Returns:
        (str): Sí si es primo, No si no lo es
    """
    if modular.es_primo(n):
        return "Sí"
    return "No"


def primos(a: int, b: int) -> str:
    """
    Calcula la lista de primos de [a, b)

    Args:
        a(int): limite inferior
        b(int): limite superior

    Returns:
        (str): los números primos, NE si no hay números primos en el intervalo
    """
    lista = modular.lista_primos(a, b)
    if not lista:
        return "NE"
    else:
        return str(lista)[1:-1]


def factorizar(n: int) -> str:
    """
    Calcula los factores del número

    Args:
        n(int): el número

    Returns:
        (str): los factores con su exponente
    """
    return str(modular.factorizar(n))[1:-1]


def mcd(*args) -> str:
    """
    Calcula el mcd de dos o más números

    Args:
        los números
    Returns:
        (str): el mcd
    """
    if len(args) > 2:
        return str(modular.mcd_n(args))
    return str(modular.mcd(*args))


def bezout(*args) -> str:
    """
    Calcula el máximo común divisor d de k (a1, a2, ..., ak)números enteros
    junto con k enteros (b1, b2, ..., bk) tales que
        d=a1 * b1 + ... + ak + bk
    Args:
        los números enteros a1, ..., ak

    Returns:
        (str): el mcd con los coeficientes b1,...,bk
    """
    if len(args) > 2:
        return str(modular.bezout_n(args))
    return str(modular.bezout(*args))


def coprimos(a, b) -> str:
    if modular.coprimos(a, b):
        return "Sí"
    return "No"


def pow(base, exp, p) -> str:
    try:
        return str(modular.potencia_mod_p(base, exp, p))
    except ZeroDivisionError:
        return "NE"


def inv(n, p) -> str:
    try:
        return str(modular.inversa_mod_p(n, p))
    except ZeroDivisionError:
        return "NE"


def euler(n) -> str:
    """
    Calcula la phi de euler de n

    n(int):
    """
    phi = modular.euler(n)
    return str(phi) if phi else "NE"


def legendre(n, p) -> str:
    try:
        return str(modular.legendre(n, p))
    except ZeroDivisionError:
        return "NE"


def resolverSistema(alist, blist, plist) -> str:
    try:
        r, m = modular.resolver_sistema_congruencias(alist, blist, plist)
        return f"{r} (mod {m})"
    except modular.IncompatibleEquationError:
        return "Incompatible Equation Error"


def cipolla(n: int, p: int) -> int:
    """Encuentra, si existen las raices cuadradas de n mod(p).

    Args:
        n (int): Entero del que se desean hallar las raices.
        p (int): Módulo. Se asume que es un número primo.

    Returns:
        int: Enteros x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.
    """

    if modular.legendre(n, p) == 0:
        return "0"

    roots = modular.cipolla(n, p)

    if roots[0] == roots[1]:
        return str(roots[0])  # Si son iguales, solo hay una raiz
    else:
        return str(roots)[1:-1]  # Si son distintas, hay dos raices


def raiz(n: int, p: int) -> int:
    """Encuentra, si existen las raices cuadradas de n mod(p).

    Args:
        n (int): Entero del que se desean hallar las raices.
        p (int): Módulo. Se asume que es un número primo.

    Returns:
        int: Enteros x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.
    """

    if modular.legendre(n, p) == 0:
        return "0"

    roots = modular.raiz_mod_p(n, p)

    if roots[0] == roots[1]:
        return str(roots[0])  # Si son iguales, solo hay una raiz
    else:
        return str(roots)[1:-1]  # Si son distintas, hay dos raices


def ecCuadratica(a, b, c, p) -> str:
    """
    Calcula las soluciones de la ecuación a*x^2 + b*x + c = 0 mod(p)

    Args:
        a,b,c (int): los coeficientes de la ecuación
        p (int): el número primo

    returns:
        (str): las soluciones, "NE" si no hay
    """
    try:
        solutions = modular.ecuacion_cuadratica(a, b, c, p)
        if not solutions:
            return "NE"
        if solutions[0] == solutions[1]:
            return str(solutions[0])

        return str(solutions)[1:-1]
    except modular.IncompatibleEquationError:
        return "NE"


def get_args_sistema(args) -> List[List[int]]:
    """
    Transforma las listas de los argumentos a listas de python

    Args:
        args(str): listas en str

    Returns:
        (List[List[int], List[int], List[int]]): lista con las listas en formato correcto para resolverSistema
    """
    alist, blist, plist = [], [], []
    for lista in args:
        lista = lista.strip()[1:-1].split(";")
        alist.append(int(lista[0]))
        blist.append(int(lista[1]))
        plist.append(int(lista[2]))
    return [alist, blist, plist]


def ejecutar_lineas(lineas: List, results: List) -> None:
    """
    Ejecuta cada comando linea por linea

    Args:
        lineas (list): lista de lineas
        results (list): lista para añadir los resultados

    """
    for line in lineas:
        if line == "":
            results.append("")
        else:
            function_regex = re.compile(r"(.+)\((.*)\)")
            try:
                match = function_regex.search(line)
                func = match.group(1)
                args = match.group(2).split(",")
                if func == "resolverSistema":
                    args = get_args_sistema(args)

                else:
                    args = [int(i) for i in args]

                result = commands[func](*args)
                results.append(result)
            except Exception:
                results.append("NOP")


def run_commands(fin: TextIO, fout: TextIO) -> None:
    """
    Recibe un manejador fin de un fichero de texto ya abierto para lectura y otro de un fichero de salida
    ya abierto para escritura y ejecuta línea por línea los comandos proporcionados por fin,
    escribiendo los resultados en fout.
    Si fin y fout no corresponden con la entrada y salida estándar, esta función
    ejecuta el modo de procesamiento
    por lotes de IMAT-LAB para la entrada fin, guardando el resultado en el fichero fout.

    Args:
        fin (TextIO): Fichero de entrada. Manejador de un fichero de texto ya abierto para lectura.
        fout (TextIO): Fichero de salida. Manejador de un fichero de texto ya abierto para escritura.

    Returns: None

    Raises: None

    Examples:
        run_commands(sys.stdin,sys.stdout) lanza el modo interactivo y ejecuta línea por línea los comandos que
            el usuario lanza desde la entrada estándar.
    """
    results = []
    lineas = fin.readlines()
    ejecutar_lineas(lineas, results)
    fout.write("\n".join(results))


def execute_commands():
    """
    Ejecuta los comandos en el modo interactivo
    """
    global command_text
    global output_text

    commands_to_execute = command_text.get("1.0", "end")
    output_text.delete("1.0", "end")

    results = []
    lineas = commands_to_execute.split("\n")[:-1]
    ejecutar_lineas(lineas, results)
    output_text.insert("end", "\n".join(results))


def run_commands_file():
    """
    Lee el fichero y lo ejecuta
    Imprime el resultado y lo guarda en otro fichero
    """
    global file1_entry
    global file2_entry
    in_file = file1_entry.get()
    out_file = file2_entry.get()
    try:
        with open(in_file, "r", encoding="utf-8") as fin:
            with open(out_file, "w", encoding="utf-8") as fout:
                run_commands(fin, fout)

        with open(out_file, "r", encoding="utf-8") as fout:
            output_text.insert("end", fout.read())
    except Exception as e:
        messagebox.showerror("Error", str(e))


def select_file(file):
    """
    Selecciona un fichero para poder leerlo o escribir en él
    """
    global file1_entry
    global file2_entry

    file_path = filedialog.askopenfilename()
    if file_path:
        if file == "file1":
            file1_entry.delete(0, "end")
            file1_entry.insert(0, file_path)
        else:
            file2_entry.delete(0, "end")
            file2_entry.insert(0, file_path)


commands: dict = {
    "primo": primo,
    "primos": primos,
    "factorizar": factorizar,
    "mcd": mcd,
    "bezout": bezout,
    "coprimos": coprimos,
    "pow": pow,
    "inv": inv,
    "euler": euler,
    "legendre": legendre,
    "resolverSistema": resolverSistema,
    "raiz": raiz,
    "ecCuadratica": ecCuadratica,
}


if __name__ == "__main__":
    root = tk.Tk()
    root.title("IMAT-LAB")
    try:
        root.iconbitmap("Matlab_Logo.ico")
    except tk.TclError:
        pass  # el icono no se incluye en este repositorio
    root.configure(bg="#0067a3", width=85, padx=10, pady=10)

    get_file_frame = tk.Frame(root)
    get_file_frame.configure(bg="#0067a3")
    get_file_frame.pack()

    file_frame = tk.Frame(root)
    file_frame.configure(bg="#0067a3")
    file_frame.pack()

    execute_file_button = tk.Frame(root)
    execute_file_button.configure(bg="#0067a3")
    execute_file_button.pack()

    label_frame = tk.Frame(root)
    label_frame.configure(bg="#0067a3")
    label_frame.pack()

    text_frame = tk.Frame(root)
    text_frame.configure(bg="#0067a3")
    text_frame.pack()

    label = tk.Label(label_frame, width=40, text="Introduzca un comando:", bg="#0067a3")
    label.pack(side="left")

    output_label = tk.Label(label_frame, width=40, text="Output:", bg="#0067a3")
    output_label.pack(side="right")

    command_text = tk.Text(text_frame, height=20, width=40)
    command_text.pack(side="left")

    execute_button = tk.Button(root, text="Ejecutar", command=execute_commands)
    execute_button.pack()

    file1_button = tk.Button(
        get_file_frame,
        text="Select Input File",
        width=35,
        command=lambda: select_file("file1"),
    )
    file1_button.pack(side="left")

    file1_entry = tk.Entry(get_file_frame, width=40)
    file1_entry.pack(side="right")
    file2_button = tk.Button(
        file_frame,
        width=35,
        text="Select Output File",
        command=lambda: select_file("file2"),
    )
    file2_button.pack(side="left")

    file2_entry = tk.Entry(file_frame, width=40)
    file2_entry.pack(side="right")

    execute_button2 = tk.Button(
        execute_file_button,
        text="Ejecutar comandos de ficheros",
        command=run_commands_file,
    )
    execute_button2.pack()

    output_text = tk.Text(text_frame, height=20, width=40)
    output_text.pack(side="right")

    root.mainloop()
