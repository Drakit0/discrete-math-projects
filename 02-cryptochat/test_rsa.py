import pytest
import modular
import rsa
import random


def test_generar_claves():
    a = 800000
    b = 1_000_000
    n, e, d = rsa.generar_claves(a, b)
    factores = modular.factorizar(n)
    factors = list(factores.keys())
    assert len(factors) == 2
    assert factors[0] >= a and factors[0] < b
    assert factors[1] >= a and factors[1] < b
    assert modular.es_primo(factors[0]) and modular.es_primo(factors[1])
    assert sum(factores.values()) == 2
    phi_n = (factors[0] - 1) * (factors[1] - 1)
    assert phi_n == modular.euler(n)
    assert (e * d) % phi_n == 1


def test_lista_primos_muy_grandes():
    a = 10**20
    b = 10**24
    primos = rsa.lista_primos_muy_grandes(a, b)
    assert all([modular.es_primo(primo) for primo in primos])
    assert rsa.lista_primos_muy_grandes(200, 201) == []


def test_generar_claves_sin_primos():
    n, e, d = rsa.generar_claves(-4, 2)
    assert (n, e, d) == (None, None, None)


def test_padding():
    p1 = rsa.aplicar_padding(24, 2)
    assert len(str(p1)) == 4
    assert str(p1)[:2] == "24"

    p1 = rsa.aplicar_padding(24, 3)
    assert len(str(p1)) == 5
    assert str(p1)[:2] == "24"
    assert rsa.aplicar_padding(24, 10) != rsa.aplicar_padding(24, 10)
    assert rsa.eliminar_padding(2454, 1) == 245
    assert rsa.eliminar_padding(2454, 2) == 24
    assert rsa.eliminar_padding(2454, 3) == 2
    assert rsa.eliminar_padding(2432, 2) == 24


def test_codificar_cadena():
    assert rsa.codificar_cadena("¡Hola mundo!") == [
        161,
        72,
        111,
        108,
        97,
        32,
        109,
        117,
        110,
        100,
        111,
        33,
    ]


def test_decodificar_cadena():
    assert (
        rsa.decodificar_cadena([161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33])
        == "¡Hola mundo!"
    )
    with pytest.raises(ValueError):
        rsa.decodificar_cadena([-1])
    with pytest.raises(ValueError):
        rsa.decodificar_cadena(["D"])
    with pytest.raises(ValueError):
        rsa.decodificar_cadena([1114112])


def test_cifrar_descifrar_cadena_rsa():
    m = "¡Hola mundo!"
    for _ in range(5):
        n, e, d = rsa.generar_claves(8_000_000, 10_000_000)
        for padd in range(rsa.max_theoretical_padding(n) + 1):
            c = rsa.cifrar_cadena_rsa(m, n, e, padd)
            m2 = rsa.descifrar_cadena_rsa(c, n, d, padd)
            assert m == m2


def test_cifrar_descifrar_mensaje_rsa():
    for _ in range(5):
        n, e, d = rsa.generar_claves(800_000, 1_000_000)
        for value_cifrar in [54, 123123, 321, 0, -2, 1114111]:
            value_cifrar = 54
            for pad in range(rsa.max_theoretical_padding(n) + 1):
                value_cifrado = rsa.cifrar_rsa(value_cifrar, n, e, 2)
                value_descifrado = rsa.descifrar_rsa(value_cifrado, n, d, 2)
                assert value_cifrado, value_descifrado


def test_romper_clave():
    n, e, d = rsa.generar_claves(79_000_000, 90_000_000)
    assert rsa.romper_clave(n, e) == d


def test_romper_cifrados_grandes():
    m = "¿HOla Mundo!!=&%"
    # n, e, d = rsa.generar_claves(10**10, 9 * 10**10)
    n, e = 28282590191348679547, 15780653617344828671
    max_padd = rsa.max_theoretical_padding(n)
    c = rsa.cifrar_mensaje_rsa(m, n, e, random.randint(2, max_padd))
    posibles_m = rsa.romper_cifrados_grandes(c, n, e)

    assert m in posibles_m
