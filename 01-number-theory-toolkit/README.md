# 01 Number theory toolkit (IMAT-LAB)

First project of Discrete Mathematics (Comillas ICAI, autumn 2023), by Pablo Tuñón Laguna and Jorge Vančo Sampedro (group GP01B). The assignment was a modular arithmetic library and an interpreter for it called IMAT-LAB. The course also timed the programs on large batches of commands, so speed mattered.

## What is here

- `modular.py`: the library. All functions work on Python integers.
  - `es_primo`: deterministic Miller-Rabin with the published witness sets for numbers below about 3.3e24, and trial division over 6k+-1 candidates above that.
  - `lista_primos(a, b)`: primes in [a, b) with a sieve that first removes the multiples of 2 and 3.
  - `factorizar`: Pollard's rho, falling back to trial division when it finds no factor.
  - `mcd`, `bezout`, `mcd_n`, `bezout_n`, `coprimos`: Euclid's algorithm, the extended version, and their versions for lists of numbers.
  - `potencia_mod_p`: square and multiply, with negative exponents handled through the modular inverse and negative moduli through their absolute value.
  - `inversa_mod_p`, `euler`, `legendre`.
  - `resolver_sistema_congruencias`: systems `a_i x = b_i (mod p_i)` whose moduli need not be coprime.
  - `raiz_mod_p`, `cipolla`, `ecuacion_cuadratica`: square roots and quadratic equations modulo a prime.
  - `function` prints a joke message when a user keeps typing invalid options. It is called by project 2.
- `imatlab.py`: the interpreter. Commands are `primo`, `primos`, `factorizar`, `mcd`, `bezout`, `coprimos`, `pow`, `inv`, `euler`, `legendre`, `resolverSistema`, `raiz` and `ecCuadratica`, one per line, for example `pow(3,200,13)` or `resolverSistema([1;1;3],[4;7;11])`. Running the file opens a Tk window with a command box, an output box and a batch mode that reads commands from one text file and writes the results to another. `run_commands(fin, fout)` does the same from code. A line that cannot be evaluated prints `NOP`, and an undefined operation prints `NE`.
- `imatlab_benchmark.py`: times and profiles `imatlab` over command files.
- `tests.py`: a script of hand-written checks that print `True` or `False` for each one.
- `report/P1GP01B.pdf`: the group's report, in Spanish. It explains the algorithms that were tried and why some were dropped. Its bibliography lists the sources the algorithms were taken from, for example the tabulated Miller-Rabin witness sets, Pollard's rho, a published square root algorithm modulo p and a paper on speeding up Euclid's algorithm.

## Which version of modular.py this is

The file is the version from the start of project 2 (November 2023), not the one handed in for project 1. It fixes errors found after the first delivery: `lista_primos` listed 49 as a prime, and negative moduli were not handled in the modular power and inverse. Project 2 uses the same file.

## How to run

```
pip install -r requirements.txt
python imatlab.py        # opens the window (needs tkinter)
python tests.py          # quick checks
```

From Python:

```python
import imatlab
out = []
imatlab.ejecutar_lineas(["primo(97)", "factorizar(360)", "mcd(84,36)"], out)
print(out)   # ['Sí', '3: 2, 2: 3, 5: 1', '12']
```

The window icon of the original was a MATLAB logo and is not included. `imatlab.py` skips it when the file is missing, which is the only change to the submitted code besides the library version above.

## What was checked

In 2026 the course's benchmark input files (about 205,000 commands in eight files, supplied by the lecturers and not included here) were run through `imatlab.ejecutar_lineas` and the results were compared with SymPy and the standard library (Python 3.12, on a laptop):

| Input file | Commands | Time | Result |
|---|---|---|---|
| primosTest | 109,999 (`primo`, `primos`, `coprimos`) | 2.4 s | all match |
| factorTest | 1,048 | 0.6 s | products and primality of the factors match |
| mcdTest | 39,501 | 3.4 s | all match |
| potenciaTest | 6,997 | 0.6 s | all match for positive moduli |
| invTest | 41,499 | 11 s | all match for positive moduli |
| eulerTest | 999 | 0.4 s | all match |
| sistemaTest | 1,391 | 0.2 s | 999 of 999 one-equation systems match, 58 of 392 systems with two to nine equations match |
| cuadraticaTest | 3,998 | 0.5 s | see below |

In `tests.py` every check that prints a boolean gives `True`. The last few lines print values to compare by eye.

## Known limitations

- `resolver_sistema_congruencias` carries the running solution in a Python complex number (real part the remainder, imaginary part the modulus). Complex numbers are floating point, so once the values pass 2^53 the result is wrong. On random systems with coefficients up to 1,000 it matched an independent solver in 2,000 of 2,000 cases, with coefficients up to 10^7 in 1,642 of 2,000.
- `raiz_mod_p` returns wrong roots for some primes congruent to 1 modulo 8 (for primes below 400, 640 of 1,380 residues). It is correct for the other residue classes that were tried. `ecuacion_cuadratica` uses it, and 231 of the 1,986 solvable equations in `cuadraticaTest` come out wrong. `cipolla` was right on every residue tested for primes below 300, but it is linear in the prime and too slow for the benchmark.
- `es_primo` above 3.3e24 falls back to trial division, which is impractical for large primes.

## What is not included

The benchmark input files, the assignment statement, the function template, the lecturers' correction, the window icon, the earlier drafts (`cipolla.py`, `Draft.py`, an alternative copy of `modular.py`) and `QS.py`, a quadratic sieve taken from a public repository that was only used for timing comparisons in the report.
