"""
rsa.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP01B
Integrantes:
    - Jorge Vančo
    - Pablo Tuñón

Descripción:
Librería para la realización de cifrado y descifrado usando el algoritmo RSA.
"""
import modular as modular
import random as rd
from typing import Tuple, List
import math
import time


def generar_claves(min_primo: int, max_primo: int) -> Tuple[int, int, int]:
    """Toma dos primos entre min_primo (incluido) y max_primo (excluido) y devuelve
    n,e,d
    donde (n,e) es la clave pública y d la clave privada para RSA

    Args:
        min_primo (int): Límite inferior para los primo p1 y p2 usados en la clave
        max_primo (int): Límite superior para los primo p1 y p2 usados en la clave


    Returns:
        n (int): Módulo para RSA, formado por el producto de dos primos p1 y p2 tales que
            min_primo<=p1, p2 < max_primo
        e (int): Exponente de la clave pública para RSA con módulo n=p1*p2
        d (int): Exponente de la clave privada para RSA con módulo n

    Raises: None
    """

    if min_primo > max_primo:
        min_primo, max_primo = max_primo, min_primo

    try:
        prime_list = modular.lista_primos(min_primo, max_primo)

    except OverflowError:
        prime_list = lista_primos_muy_grandes(min_primo, max_primo)

    except MemoryError:
        prime_list = lista_primos_muy_grandes(min_primo, max_primo)

    if (
        prime_list == None or len(prime_list) <= 1
    ):  # Eliminación de casos en los que sólo quedaría un elemento o 0 elementos en la lista
        return None, None, None

    length = len(prime_list)

    p = prime_list[rd.randint(0, length - 1)]
    q = prime_list[rd.randint(0, length - 1)]

    while p == q:
        q = prime_list[rd.randint(0, length - 1)]

    n = p * q
    phi_n = n - p - q + 1  # (p - 1) * (q - 1)
    e = None

    while not e or not modular.coprimos(e, phi_n):
        e = rd.randint(phi_n // 2, phi_n - 1)

    d = modular.inversa_mod_p(e, phi_n)  # Cálculo de d

    return (n, int(e), int(d))


def lista_primos_muy_grandes(a, b):
    primos = []
    maximum = b - 1
    minimum = a
    t0 = time.time()

    if a % 6 == 1 and modular.es_primo(a):
        primos.append(a)

    minimum += 5 - a % 6
    maximum -= (maximum % 6 + 1) % 6

    print(minimum, maximum, maximum + 2)

    if a <= 2 < b:
        primos.append(2)

    if a <= 3 < b:
        primos.append(3)

    if maximum < minimum:
        return primos

    if modular.es_primo(maximum):
        primos.append(maximum)
    if maximum + 2 < b and modular.es_primo(maximum + 2):
        primos.append(maximum + 2)

    m = (a + b - 1) // 2 - a

    maximum -= 6

    middle1 = m + a
    middle2 = m + a - 1
    print(middle1, middle2)
    middle1 += 5 - middle1 % 6
    middle2 -= (middle2 % 6 + 1) % 6
    print(middle1, middle2)

    if modular.es_primo(middle2):
        primos.append(middle2)

    middle2 -= 6

    for i in range(0, (m + 1) // 2, 6):
        anadir_primo_mod_6_arriba(minimum + i, primos)
        anadir_primo_mod_6_arriba(maximum - i, primos)
        anadir_primo_mod_6_arriba(middle1 + i, primos)
        anadir_primo_mod_6_arriba(middle2 - i, primos)

        if len(primos) >= 2000:
            break

        elif len(primos) >= 2 and time.time() - t0 > 10:
            break
        elif time.time() - t0 > 15:
            break

    return primos


def anadir_primo_mod_6_arriba(num: int, primos: list) -> None:
    """Añade a la lista priimos, si son primos, en número num, y num + 2

    Args:
        num (int): el número que se quere comprobar si es primo
        primos (list): la lista de primos
    """
    if num not in primos and modular.es_primo(num):
        primos.append(num)

    if num + 2 not in primos and modular.es_primo(num + 2):
        primos.append(num + 2)


def max_theoretical_padding(n: int) -> int:
    """Calcula el número de dígitos de padding máximo posible a partir de la clave pública

    Args:
        n (int): Módulo de la clave pública de RSA

    Returns:
        int: el valor de dígitos máximos de padding posibles
    """
    maximun = max(int(math.log10(n / 1114112 + 1)), 0)
    return maximun


def aplicar_padding(m: int, digitos_padding: int) -> int:
    """Dado un mensaje y un número de dígitos de padding, añade
    digitos_padding cifras aleatorias a la derecha del mensaje

    Args:
        m (int): Mensaje sin padding
        digitos_padding (int): Número de cifras de padding


    Returns:
        int: entero formado por los dígitos de m seguidos de digitos_padding cifras aleatorias.

    Raises: None

    Example:
        aplicar_padding(24,2)=2419
        aplicar_padding(24,2)=2403
        aplicar_padding(24,3)=24718
        aplicar_padding(24,3)=24845
    """

    if digitos_padding == 0:
        return m

    if digitos_padding < 0:
        digitos_padding = -digitos_padding

    padding = rd.randint(10 ** (digitos_padding - 1), 10 ** (digitos_padding) - 1)
    if m < 0:
        padding = -padding
    return m * 10**digitos_padding + padding


def eliminar_padding(m: int, digitos_padding: int) -> int:
    """Dado un mensaje con padding de digitos_padding cifras al
    final del mismo, elimina dichas cifras aleatorias y devuelve
    el resto de cifras del mensaje

    Args:
        m (int): Mensaje con padding
        digitos_padding (int): Número de cifras de padding


    Returns:
        int: entero resultante de eliminar las últimas digitos_padding cifras de m.

    Raises: None

    Example:
        eliminar_padding(2454,1)=245
        eliminar_padding(2454,2)=24
        eliminar_padding(2454,3)=2
        eliminar_padding(2432,2)=24
    """

    if m == None:
        return None

    return m // (10**digitos_padding)


def cifrar_rsa(m: int, n: int, e: int, digitos_padding: int) -> int:
    """Dado un mensaje m entero, un módulo y exponente que formen parte
    de una clave pública de RSA, con m<n*10^{-digitos_padding}, y un número
    de dígitos de padding, aplica el padding al mensaje y lo cifra
    usando RSA con módulo n y exponente e.

    Args:
        m (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA
        digitos_padding (int): Número de cifras de padding


    Returns:
        int: entero resultante de agregar el padding a m y aplicar RSA.

    Raises: None
    """

    if m == None or m < 0:  # Casos en los que el mensaje falla
        return None

    if (n == 0 or e == 0):  # Comprobación de que módulos, exponente y los dígitos de padding no son 0 o negativos
        return None

    if n < 0:
        n = -n

    if e < 0:
        e = -e

    if digitos_padding < 0:
        digitos_padding = -digitos_padding

    if digitos_padding > len(str(n)):  # El padding no puede ser mayor que el módulo o habría error en el cifrado
        return None

    m_padding = aplicar_padding(m, digitos_padding)  # Aplicación de padding
    cipher_text = modular.potencia_mod_p(m_padding, e, n)  # Cifrar como m^e mod(n)

    return cipher_text


def descifrar_rsa(c: int, n: int, d: int, digitos_padding: int) -> int:
    """Dado un cifrado c entero que haya sido cifrado con RSA usando
    digitos_padding cifras de padding al final del mensaje y el
    módulo y exponente privado, n y d que formen la clave privada de RSA cuya pareja se
    utilizó para cifrar c, descifra c y elimina el padding, devolviendo
    el mensaje original.

    Args:
        c (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA usado para cifrar
        d (int): Exponente de la clave privada de RSA cuya pareja se utilizó para cifrar c
        digitos_padding (int): Número de cifras de padding usados para cifrar c


    Returns:
        int: entero resultante de descifrar c usando RSA con módulo m y exponente e y después eliminar el padding al resultado.

    Raises: None
    """
    if (n == 0 or d == 0 or c is None or c < 0):  # Comprobación de que módulos, exponente son cero
        return None

    if n < 0:
        n = -n

    if d < 0:
        d = -d

    if digitos_padding < 0:
        digitos_padding = -digitos_padding
        
    if digitos_padding > len(str(n)):  # El padding no puede ser mayor que el módulo o habría error en el descifrado
        return None

    m_plain = modular.potencia_mod_p(c, d, n)  # Descifrado como c^d mod(n)
    m_plain = eliminar_padding(m_plain, digitos_padding)  # Eliminación de padding
    
    return m_plain


def codificar_cadena(s: str) -> List[int]:
    """Convierte una cadena de caracteres a la lista de
    enteros que representa el valor unicode cada uno de sus caracteres.

    Args:
        s (str): cadena en texto plano

    Returns:
        int: lista de enteros que representan el código unicode de cada carácter de la cadena s.

    Raises: None.

    Example:
        codificar_cadena("¡Hola mundo!")=[161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33]
    """

    if type(s) != str or len(s) == 0:  # Verifica que la cadena sea un dato correcto
        return None

    return [ord(letter) for letter in s]  # Creación de lista de ascii


def decodificar_cadena(m: List[int]) -> str:
    """Convierte una lista de enteros que representen caracteres unicode
    en la cadena que representan.

    Args:
        m (List[int]): lisa de enteros que representan los códigos unicode de una cadena de caracteres.

    Returns:
        str: cadena que representa

    Raises:
        ValueError: Si alguno de los enteros no representa un caracter unicode válido.

    Example:
        decodificar_cadena([161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33])="¡Hola mundo!"
    """

    if len(m) == 0:
        return None

    decodified_string = ""

    for number in m:
        # Evaluación de casos en los que chr daría error
        if type(number) != int or number < 0 or number > 1114112:
            raise ValueError("Algún entero no representa un caracter unicode válido")

        else:
            decodified_string += chr(number)  # Conversión de ascii a string

    return decodified_string


def cifrar_cadena_rsa(s: str, n: int, e: int, digitos_padding: int) -> List[int]:
    """Encripta carácter a carácter una cadena de caracteres usando RSA con clave púbica (n,e)
    y digitos_padding cifras de padding al final del mensaje y devuelve la lista de enteros
    que representan el mensaje cifrado correspondiente.
    Args:
        s (str): texto claro
        n (int): módulo para RSA
        e (int): clave pública para RSA
        digitos_padding (int): número de dígitos de padding que deben usarse para el cifrado del mensaje.

    Returns:
        List[int]: lista de enteros que representa el mensaje cifrado con RSA para la clave dada.

    Raises: None
    """

    ascii_message = codificar_cadena(s)
    if ascii_message is None:
        return None

    ciphered_text = []

    for ascii_number in ascii_message:
        if ascii_number is None:
            return None

        else:
            ciphered_text.append(cifrar_rsa(ascii_number, n, e, digitos_padding))

    return ciphered_text


def descifrar_cadena_rsa(cList: List[int], n: int, d: int, digitos_padding: int) -> str:
    """Dado un mensaje cifrado con RSA usando la clave pública cuya clave privada asociada es (n,d)
    y digitos_padding cifras de padding al final del mensaje, devuelve la cadena orignal.
    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        d (int): clave privada para RSA
        digitos_padding (int): número de dígitos de padding usados para el cifrado de cList.

    Returns:
        str: cadena que representa el texto claro correspondiente al mensaje cifrado cList.

    Raises:
        ValueError: Si, tras decodificar, alguno de los enteros del mensaje no representa un caracter unicode válido.
    """

    if len(cList) == 0:
        return None

    deciphered_text = []

    for c in cList:
        if c is None:
            return None

        else:
            deciphered_text.append(descifrar_rsa(c, n, d, digitos_padding))

    try:
        decoded_text = decodificar_cadena(deciphered_text)
        
    except ValueError as e:
        raise ValueError(e)

    return decoded_text


def cifrar_mensaje_rsa(s: str, n: int, e: int, digitos_padding: int) -> str:
    
    return " ".join(str(char) for char in cifrar_cadena_rsa(s, n, e, digitos_padding))


def descifrar_mensaje_rsa(c: str, n: int, d: int, digitos_padding: int) -> str:
    
    cList = [int(num) for num in c.split(" ")]
    
    try:
        return descifrar_cadena_rsa(cList, n, d, digitos_padding)
    
    except ValueError as e:
        raise ValueError(e)


def romper_clave(n: int, e: int) -> int:
    """A partir de una clave pública válida (n,e), recupera la clave privada d tal que
    de = 1 (mod phi(n)).

    Args:
        n (int): módulo para RSA
        e (int): clave pública para RSA

    Returns:
        int: clave privada d

    Raises:
        ValueError: Si no existe ninguna clave privada d compatible con la clave pública (n,e).
    """

    factores = modular.factorizar(n)
    factores_exponentes = factores.items()
    phi_n = 1

    for f, exp in factores_exponentes:
        phi_n *= f ** (exp - 1) * (f - 1)

    try:
        d = modular.inversa_mod_p(e, phi_n)

    except ValueError:
        raise ValueError()

    return d


def ataque_texto_elegido(cList: List[int], n: int, e: int, padding_digits:int) -> str:
    """Ejecuta un ataque de texto claro elegido sobre un mensaje que ha sido encriptado
    con RSA plano sin usar padding a partir de su clave pública.

    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        e (int): clave pública para RSA
        padding_digits (int): número de dígitos de padding usados

    Returns:
        str: texto plano descifrado para el mensaje cifrado cList

    Raises:
        ValueError: Si el mensaje no se corresponde con ningún texto plano que haya sido codificado con RSA sin padding.
    """

    m = ""
    cifrado = generar_diccionario(n, e, padding_digits)
    for c in cList:
        try:
            m += cifrado[c]

        except KeyError:
            raise ValueError(
                "El mensaje no se corresponde con ningún texto plano que haya sido codificado con RSA sin padding."
            )

    return m


def generar_diccionario(n: int, e: int, padding_digits:int) -> dict:
    """Genera un diccionario con todas

    Args:
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA
        padding_digits (int): dígitos de padding usados para cifrar

    Returns:
        cifrado (dict): el diccionario con los cifrados de cada valor unicode como clave
    """
    
    cifrado = dict()
    max_unicode = 1114112

    for unicode in range(0, max_unicode):
        cifrado[cifrar_rsa(unicode, n, e, padding_digits)] = chr(unicode)

    return cifrado


def romper_cifrados_grandes(c: str, n: int, e: int) -> list:
    """Descifra textos que han sido cifrados con RSA usando padding y con una n generada a partir de dos
    números primos que pueden tener más de diez dígitos.

    Args:
        c (str): texto encriptado
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA

    Returns:
        list[str]: una lista con todas las posibles opciones para el texto descifrado
    """
    d = romper_clave(n, e)
    print(f"A continuación se muestra la n: {n}, la e:{e} y la d:{d} usadas para cifrar el mensaje a descifrar.")
    
    max_padding = max_theoretical_padding(n)
    posibles_m = []

    for padding in range(0, max_padding + 1):
        try:
            m = descifrar_mensaje_rsa(c, n, d, padding)
            print(m)
            posibles_m.append(m)

        except ValueError:
            print("No puede ser con padding", padding)

    return posibles_m
