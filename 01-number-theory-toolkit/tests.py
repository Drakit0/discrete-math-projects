import modular

if __name__ == "__main__":
    print("ES_PRIMO:")
    print(modular.es_primo(7) is True)
    print(modular.es_primo(88) is False)
    print(modular.es_primo(892348798284365) is False)
    print(modular.es_primo(547867) is False)
    print("LISTA PRIMOS: ")
    # print(modular.lista_primos(1, 100))
    # print(modular.lista_primos(2, 20))
    print(modular.lista_primos(1, 11) == [2, 3, 5, 7])
    # print(modular.lista_primos(24, 29))
    print("FACTORIZAR:")
    print(modular.factorizar(21) == {3: 1, 7: 1})
    print(modular.factorizar(16) == {2: 4})
    print(modular.factorizar(12) == {2: 2, 3: 1})
    print(modular.factorizar(547867) == {653: 1, 839: 1})
    print(modular.factorizar(973249872) == {2: 4, 3: 1, 7: 1, 1021: 1, 2837: 1})
    print(modular.factorizar(24808028291) == {28789: 1, 861719: 1})
    # print(modular.factorizar(4611411168))
    # print(modular.factorizar(3065595194))
    print("MCD:")
    print(modular.mcd(10, 15) == 5)
    print(
        modular.mcd(
            278080845893291346484653985009024455015364345,
            449944260275667013518207286615096324842360050,
        )
        == 17785
    )
    print("MCD_N:")
    print(modular.mcd_n([4, 10, 14]) == 2)
    print("COPRIMOS:")
    print(modular.coprimos(3, 5) is True)
    print(modular.coprimos(35, 5) is False)
    print("BEZOUT:")
    print(modular.bezout(6, 10) == (2, 2, -1))
    print("BEZOUT_N:")
    print(modular.bezout_n([4, 10, 14]) == (2, (-2, 1, 0)))
    print("POTENCIA:")
    print(modular.potencia_mod_p(-3, -8, 7) == 4)
    print(modular.potencia_mod_p(4, 13, 497) == 445)
    # print(modular.potencia_mod_p(7138614207, -2503539524883, 3761614773))
    print("EULER")
    print(modular.euler(36) == 12)
    print("INVERSA:")
    print(modular.inversa_mod_p(30**19, 53) == 30)
    print("LEGENDRE")
    print(modular.legendre(1, 3) == 1)
    print(modular.legendre(2, 3) == -1)
    print(modular.legendre(13, 13) == 0)
    print(modular.legendre(2, 11) == -1)
    print(modular.legendre(30, 127) == 1)
    print("SISTEMA CONGRUENCIAS:")
    print(
        modular.resolver_sistema_congruencias([1, 1, 1], [2, 3, 2], [3, 5, 7])
        == (23, 105)
    )
    print(
        modular.resolver_sistema_congruencias([2, 1, 1], [1, 2, 3], [5, 6, 7])
        == (38, 210)
    )
    # print(modular.resolver_sistema_congruencias([2, 3, 2], [2, 2, 4], [6, 7, 8]))
    # print(modular.resolver_sistema_congruencias([5, 3, 2], [2, 2, 4], [6, 7, 8]))
    # print(
    #     modular.resolver_sistema_congruencias([6519037604], [8972153143], [1297334945])
    #     == (113638352, 1297334945)
    # )
    # print(modular.resolver_sistema_congruencias([6], [26], [22]))
    # print(modular.resolver_sistema_congruencias([1], [26], [22]))
    # print(modular.inversa_mod_p(9375237921, 8456819090))
    # print(modular.inversa_mod_p(4990397538, 9057014326))
    # print(modular.inversa_mod_p(12911677, 7361))
    # print(
    #     modular.resolver_sistema_congruencias(
    #         [9375237921, 8364969966, 8456819090],
    #         [4990397538, 9824496521, 9057014326],
    #         [12911677, 8361923, 7361],
    #     )
    # )

    # print(modular.coprimos(391, 7361))
    # print(modular.inversa_mod_p(391, 7361))
    # print(modular.resolver_sistema_congruencias([1, 1, 1], [5, 23, 33], [28, 30, 35]))
    print("QUADRATIC:")
    print(modular.ecuacion_cuadratica(1, 6, 5, 17), [16, 12])
    print(modular.ecuacion_cuadratica(1, 3, 11, 13), [6, 4])
    print(modular.ecuacion_cuadratica(1, 0, -1, 7), [1, 6])
    print("RAIZ")

    print(modular.raiz_mod_p(10, 13) == (6, 7))
    print(modular.raiz_mod_p(8218, 10007))
    # print("CIPOLLA")
