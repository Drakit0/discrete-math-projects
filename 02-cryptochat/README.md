# 02 Cryptochat (RSA)

Second project of Discrete Mathematics (Comillas ICAI, autumn 2023), by Pablo Tuñón Laguna and Jorge Vančo Sampedro (group GP01B). It builds an RSA library on top of the modular arithmetic of project 1, a script that registers users, and a terminal chat that encrypts and decrypts messages between two of them. Keys are kept in plain text files on purpose: the assignment was about seeing how RSA works, not about key storage.

## What is here

- `rsa.py`: the RSA library.
  - `generar_claves(min_primo, max_primo)` picks two different random primes in the range and returns `(n, e, d)`. For ranges too large to sieve it falls back to `lista_primos_muy_grandes`, which searches candidates of the form 6k+-1 from the start, the middle and the end of the range and stops after 2,000 primes or a time limit.
  - `aplicar_padding` and `eliminar_padding` append and strip random decimal digits at the end of the message number. `max_theoretical_padding(n)` gives the most digits a key of that size can take.
  - `cifrar_rsa` and `descifrar_rsa` work on integers, `cifrar_cadena_rsa` and `descifrar_cadena_rsa` on strings character by character (Unicode code points), and `cifrar_mensaje_rsa` and `descifrar_mensaje_rsa` read and write the ciphertext as integers separated by spaces.
  - `romper_clave(n, e)` factors `n` with the factoring routine of `modular.py` and rebuilds the private key.
  - `ataque_texto_elegido` builds a dictionary from the ciphertext of each of the 1,114,112 Unicode code points and looks the message up character by character. It breaks messages encrypted without padding.
  - `romper_cifrados_grandes` breaks the key by factoring and then tries every padding length up to the maximum, printing each one that decodes.
- `registrarusuario.py`: asks for a name, a range for the two primes and the number of padding digits, and writes `Usuarios/pub_<name>.txt` (n, e and the padding on three lines) and `Usuarios/priv_<name>.txt` (d).
- `criptochat.py`: asks for the two user names, then whether to encrypt (C), decrypt (D) or quit (S). It encrypts with the other user's public key and padding, decrypts with the own private key, reads ciphertext typed by hand or from a file in `Mensajes/`, and can save the result as `Mensajes/<sender>_<receiver>_<C or D>_<number>.txt` without overwriting older files.
- `modular.py`: the library from project 1 (the same file as in `01-number-theory-toolkit/`).
- `test_rsa.py`: pytest tests for `rsa.py`.
- `report/P2GP01B.pdf`: the group's report, in Spanish.

## How to run

```
pip install -r requirements.txt
python registrarusuario.py       # run once per user, for example "alice" and "bob"
python criptochat.py             # then enter alice, bob, and choose C
python -m pytest test_rsa.py
```

Primes between 800,000 and 1,000,000 with 3 padding digits work well for a first try. The `Usuarios/` and `Mensajes/` folders are created when needed.

## What was checked

- Two users were registered, a message from the first to the second was encrypted with `criptochat.py`, and it was decrypted as the second user.
- `python -m pytest test_rsa.py` passes all 10 tests in about a minute on Python 3.12 (key generation, padding, string encoding, encrypt and decrypt, key breaking, large primes).
- The project was written against Python 3.10 and 3.11.

## Known limitations

- The modular arithmetic has the two issues listed in `01-number-theory-toolkit/README.md`. They do not affect encryption and decryption, but `modular.resolver_sistema_congruencias` and `modular.raiz_mod_p` are not used here.
- The scheme is a teaching exercise. Keys are small, padding is a run of random digits and encryption is character by character, so it is not secure, which is what the two attacks show.
- `ataque_texto_elegido` builds its dictionary on every call, which took about a minute for a 12-digit modulus on Python 3.12.

## What is not included

The assignment statement and the function template, the two example users and messages produced while testing, the ciphertext that the course handed out for the decryption exercise, scratch files and copies of project 1. One test that used that ciphertext was removed from `test_rsa.py` because it called `ataque_texto_elegido` with an outdated signature.
