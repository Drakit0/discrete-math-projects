"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP01B
Integrantes:
    - Jorge Vančo
    - Pablo Tuñón 

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""


from typing import Tuple, List, Dict
import numpy as np
import random


class IncompatibleEquationError(Exception):
    pass


def es_primo(n: int) -> bool:
    """Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero

    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None

    Examples:
        es_primo(5)=true
        es_primo(4)=false
    """

    if n <= 3:
        return n > 1
    if (n & 1) == 0 or n % 3 == 0:
        return False

    # calculamos s y d tal que (2^s)*d = n - 1
    s = 0
    d = n - 1
    while (d & 1) == 0:
        s += 1
        d >>= 1

    a_list = get_miller_rabin_a(n)

    if a_list:
        for a in a_list:
            x = potencia_mod_p(a, d, n)

            for _ in range(s):
                y = potencia_mod_p(x, 2, n)
                if y == 1 and x != 1 and x != n - 1:
                    return False
                x = y
            if y != 1:
                return False
        return True

    limit = int(n**0.5) + 1
    for i in range(5, limit, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True


def get_miller_rabin_a(n) -> List[int]:
    if n < 2047:
        return [2]
    if n < 1373653:
        return [2, 3]
    if n < 9080191:
        return [31, 73]
    if n < 25326001:
        return [2, 3, 5]
    if n < 3215031751:
        return [2, 3, 5, 7]
    if n < 4759123141:
        return [2, 7, 61]
    if n < 1122004669633:
        return [2, 13, 23, 1662803]
    if n < 2152302898747:
        return [2, 3, 5, 7, 11]
    if n < 3474749660383:
        return [2, 3, 5, 7, 11, 13]
    if n < 341550071728321:
        return [2, 3, 5, 7, 11, 13, 17]
    if n < 3825123056546413051:
        return [2, 3, 5, 7, 11, 13, 17, 19, 23]
    if n < 18446744073709551616:
        return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n < 318665857834031151167461:
        return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if n < 3317044064679887385961981:
        return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    # print(n)
    # return range(2, min(n - 2, int(2 * np.log(n) ** 2)))
    return


def lista_primos(a, b) -> List[int]:
    """
    Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)
    Se usa una implementación de la criba de Euler

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)

    Returns:
        bool: true si el entero es un número primo. false en caso contrario.

    Raises: None

    Examples:
        lista_primos(1,11)=[2,3,5,7]
    """

    if b <= a or b <= 0:
        return None

    is_prime = [True] * b
    primes = []

    start = max(4, (a + 1) // 2 * 2)
    for k in range(start, b, 2):
        is_prime[k] = False
    start = max(9, a // 3 * 3)
    for k in range(start, b, 3):
        is_prime[k] = False

    for p in range(5, int((b - 1) ** 0.5) + 1):
        for j in (p, p + 2):
            if is_prime[j]:
                start = max(j * j, (a + j - 1) // j * j)
                for i in range(start, b, j):
                    is_prime[i] = False

    for p in range(max(2, a), b):
        if is_prime[p]:
            primes.append(p)

    return primes


def pollar_rho(n, x, y) -> int:
    # Pollar rho
    x = 2
    y = 2
    d = 1

    g = lambda x: (x**2 + 1) % n

    while d == 1:
        x = g(x)
        y = g(g(y))
        d = mcd(abs(x - y), n)

    if d == n:
        is_perfect, square = is_perfect_square(d)
        if is_perfect:
            return square
        if es_primo(d):
            return d
        return
    else:
        return d


def is_perfect_square(n: int) -> Tuple[bool, int]:
    """
    Función que dice si el número n es un cuadrado perfecto o no

    Args:
        n (int): número del que se quiere saber si es cuadrado perfecto o no

    Returns:
        tuple (bool, int): Si es cuadrado perfecto o no, la raíz cuadrada de n
    """
    root = int(np.sqrt(n))
    return np.square(root) == n, root


def simple_factorization(n: int, factores=None) -> Dict[int, int]:
    """
    Algoritmo básico para factorizar

    Args:
        n (int): El número a factorizar
        factores (dict): diccionario de factores (es usado para añadir factores si ya se había factorizado parte)

    Returns:
        factores (dict): diccionario con los factores y sus exponentes
    """
    if factores is None:
        factores = {}

    if es_primo(n):
        factores[n] = 1
        return factores

    for small_prime in [2, 3]:
        while n % small_prime == 0:
            n //= small_prime
            factores[small_prime] = factores.get(small_prime, 0) + 1
    primo = 5
    while n > 1:
        if es_primo(n):
            factores[int(n)] = 1
            return factores
        if es_primo(primo):
            while n % primo == 0:
                n //= primo
                factores[primo] = factores.get(primo, 0) + 1
        if es_primo(primo + 2):
            while n % (primo + 2) == 0:
                n //= primo + 2
                factores[primo + 2] = factores.get(primo + 2, 0) + 1

        primo += 6

    return factores


def factorizar(n: int) -> Dict[int, int]:
    """Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.

    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    """
    if n == 0:
        return [0]
    x = 2
    y = 2
    factores = dict()

    if n < 0:
        n *= -1

    while n > 1:
        if es_primo(n):
            factores[n] = 1
            return factores

        factor = pollar_rho(n, x, y)
        if factor:
            if not es_primo(factor):
                factores_factor = factorizar(factor)
                for factor in factores_factor:
                    while n % factor == 0:
                        n //= factor
                        factores[factor] = factores.get(factor, 0) + 1
            else:
                while n % factor == 0:
                    n //= factor
                    factores[factor] = factores.get(factor, 0) + 1
        else:
            return simple_factorization(n, factores)
        x += 1
        y += 1

    return factores


def mcd(a: int, b: int) -> int:
    """
    Calcula el máximo común divisor de dos enteros a y b.

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.

    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples
        mcd(10,15)=5
    """

    if a == 0:
        return b
    if b == 0:
        return a
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    if a == b:
        return a
    if b > a:
        a, b = b, a

    if a - b == 1:
        return 1

    while b != 0:
        diff = a - b
        if diff > b:
            a = diff
        else:
            a, b = b, diff
        a, b = b, a % b

    return a


def bezout(a: int, b: int) -> Tuple[int, int, int]:
    """
    Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
        d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.

    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples
        bezout(6,10)=(2,2,-1)
    """

    a_positivo = True
    b_positivo = True

    if a < 0:
        a *= -1
        a_positivo = False
    if b < 0:
        b_positivo = False
        b *= -1

    s = 0
    old_s = 1
    t = 1
    old_t = 0
    resto = b
    resto_anterior = a

    while resto != 0:
        quotient = resto_anterior // resto
        resto_anterior, resto = resto, resto_anterior - quotient * resto
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return (
        resto_anterior,
        old_s if a_positivo else -old_s,
        old_t if b_positivo else -old_t,
    )


def mcd_n(nlist: List[int]) -> int:
    """
    Dada una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.

    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples
        mcd([4,10,14])=2
    """
    n_mcd = nlist[0]
    for i in range(1, len(nlist)):
        n_mcd = mcd(n_mcd, nlist[i])
    return n_mcd


def bezout_n(nlist: List[int]) -> Tuple[int, List[int]]:
    """
    Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.

    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    n_mcd = nlist[0]
    b_list = []
    n_mcd = nlist[0]
    for i in range(1, len(nlist)):
        n_mcd, x, y = bezout(n_mcd, nlist[i])
        if len(b_list) == 0:
            b_list.append(x)
        b_list.append(y)
    return n_mcd, tuple(b_list)


def coprimos(n: int, m: int) -> bool:
    """
        Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.

    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples
        coprimos(14,20)=false
        coprimos(14,15)=true
    """
    if n < m:
        n, m = m, n
    if n == m:
        return False
    n, m = m, n - m
    if m == 1:
        return True
    for p in [2, 3, 5, 7, 13, 17]:
        if n % p == 0:
            if m % p == 0:
                return False

    return mcd(n, m) == 1


def potencia_mod_p(base: int, exp: int, p: int) -> int:
    """
    Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.

    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0.
    """
    if p == 1:
        return 0

    elif p == 0:
        raise ZeroDivisionError

    elif p < 0:
        p = -p

    # if base < 0:
    if exp < 0:
        exp = abs(exp)
        base = inversa_mod_p(base, p)

    result = 1
    base %= p

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % p

        exp = exp >> 1
        base = (base * base) % p

    return result


def inversa_mod_p(n: int, p: int) -> int:
    """
    Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.

    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    """

    if p == 0:
        raise ZeroDivisionError

    elif p < 0:
        p = -p

    if n < 0 or n > p:
        n %= p

    y = n
    n = p
    a = 0
    b = 1

    while y != 0:
        a, b = b, a - n // y * b
        n, y = y, n % y

    if n == 1:
        return a % p

    else:
        raise ZeroDivisionError


def euler(n: int) -> int:
    """
    Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

        Args:
            n (int): Número entero positivo.

        Returns:
            int: Función phi de Euler de n.

        Raises: None
    """
    if n < 0:
        return

    factores = factorizar(n)
    phi = n

    for p in factores:
        phi *= 1 - 1 / p

    return int(phi)


def legendre(n: int, p: int) -> int:
    """
    Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.

    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.
    """
    if p == 0:
        raise ZeroDivisionError

    if n == -1:
        return (-1) ** ((p - 1) // 2)

    if n == 2:
        return (-1) ** ((p**2 - 1) // 8)

    leg = potencia_mod_p(n, (p - 1) // 2, p)

    if leg > 1:
        return -1

    return leg


def resolver_sistema_congruencias(
    alist: List[int], blist: List[int], plist: List[int]
) -> Tuple[int, int]:
    """
    Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias

    a_i * x = b_i (mod p_i)   i=1,...,n

    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]

    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.
    """

    X = None
    for a, b, p in zip(alist, blist, plist):
        if b % mcd(a, p) != 0:
            raise IncompatibleEquationError

        if X is not None:
            k = a * X
            a = k.imag % p
            b = (b - k.real) % p

        mcd_ecuacion = mcd_n([a, b, p])

        if mcd_ecuacion > 1:
            a, b, p = a // mcd_ecuacion, b // mcd_ecuacion, p // mcd_ecuacion

        if b % mcd(a, p) != 0:
            raise IncompatibleEquationError

        x = p * 1j + (inversa_mod_p(a, p) * b) % p

        if X is not None:
            X = X.imag * x + X.real

        else:
            X = x

    return int(X.real), int(X.imag)


def cuadratic_residue(n: int, p: int) -> bool:
    """Comprueba si n es un cuadrado módulo p.

    Args:
        n (int): Número entero.
        p (int): Módulo.

    Returns:
        bool: True si n es un cuadrado módulo p, False en caso contrario.
    """
    # Si el símbolo de Legendre es 1, es un cuadrado módulo p
    return legendre(n, p) == 1


def raiz_mod_p(n: int, p: int) -> list:
    """Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.

    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.
    """

    if legendre(n, p) == -1:
        return []

    n %= p
    a = 2

    if n == 0 or n == 1:
        return (n, -n % p)

    if p == 2:
        return (n, -n % p)

    while legendre(a, p) == 1:
        a += 1

    n_pow = p - 1
    a_pow = 0

    while n_pow % 2 == 0:
        n_pow //= 2
        a_pow //= 2

        if potencia_mod_p(n, n_pow, p) % p * (potencia_mod_p(a, a_pow, p) % p) == p - 1:
            a_pow += (p - 1) // 2

    n_pow = (n_pow + 1) // 2
    a_pow //= 2

    sqrt = potencia_mod_p(n, n_pow, p) * potencia_mod_p(a, a_pow, p) % p
    sqrts = [sqrt, -sqrt % p]
    sqrts.sort()

    return tuple(sqrts)


def cipolla_mult(a: int, n: int, p: int) -> int:
    """
    Función para calcular las multiplicaciones usadas en el algoritmo de Cipolla
    se multiplica sucesivas veces (a*1 + w^0.5) y se busca mantener los coeficientes de w**0.5 y de 1

    Args:
        a(int): número que no es un no residuo cuadrático módulo p
        n(int): el número del que se quiere calcular la raíz módulo p
        p(int): el número primo

    Returns:
        new_a(int): una raíz, el coeficiente de 1 en el resultado final de las multiplicaciones (new_a + coef_w * w**0.5)
    """
    f_exp = (p + 1) // 2
    exp = 1
    w = a**2 - n

    new_a = a
    new_coef_w = 1
    while 2 * exp < f_exp:
        new_a, new_coef_w = (new_a**2 + new_coef_w**2 * w) % p, (
            2 * new_a * new_coef_w
        ) % p
        exp *= 2

    while exp < f_exp:
        new_a, new_coef_w = (a * new_a + new_coef_w * w) % p, (
            a * new_coef_w + new_a
        ) % p
        exp += 1

    return new_a


def cipolla(n, p):
    """
    Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.

    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.
    """
    n %= p
    if n == 0 or n == 1:
        return (n, -n % p)

    if not cuadratic_residue(n, p):  # Si n no es un cuadrado módulo p, no tiene raices
        raise IncompatibleEquationError(
            f"\nLo sentimos, {n} no es un cuadrado módulo {p}."
        )
    phi = p - 1

    if potencia_mod_p(n, phi // 2, p) != 1:
        return

    if p % 4 == 3:
        x = potencia_mod_p(n, (p + 1) // 4, p)
        return (x, -x % p)

    a = 1
    while legendre(a**2 - n, p) != -1:
        a += 1

    b = cipolla_mult(a, n, p)

    sols = [b, -b % p]
    sols.sort()

    return sols


def ecuacion_cuadratica(a: int, b: int, c: int, p: int) -> Tuple[int, int]:
    """
    Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

        Args:
            a (int): Coeficiente de x^2.
            b (int): Coeficiente de x.
            c (int): Término independiente.
            p (int): Módulo. Se asume que es un número primo.

        Returns: (x1,x2)
            x1 (int): Primera solución. Entero entre 0 y p-1.
            x2 (int): Segunda solución. Entero entre 0 y p-1.

        Raises:
            IncompatibleEquationError: Si no es posible resolver la ecuación.
    """

    if mcd(2 * a, p) != 1:
        raise IncompatibleEquationError
    solutions = []
    square = (b**2 - 4 * a * c) % p
    try:
        for sol in raiz_mod_p(square, p):
            solutions.append((inversa_mod_p(2 * a, p) * (-b + sol)) % p)
        solutions.sort()
        return solutions
    except IncompatibleEquationError as e:
        raise IncompatibleEquationError(e)


def function(counter: int):
    aleat = random.randint(counter % 8, 9)

    if aleat == 4:
        print("¡Venga McFly!")

    elif aleat == 8:
        print("Come on, it's not rocket science...")
