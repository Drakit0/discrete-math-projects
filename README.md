# Discrete Mathematics projects

Three programming projects from Discrete Mathematics (Matemática Discreta), second year of the Mathematical Engineering and Artificial Intelligence degree at Universidad Pontificia Comillas ICAI, first semester of 2023-24. They were done in pairs by group GP01B: Pablo Tuñón Laguna and Jorge Vančo Sampedro. The code is Python, the comments and docstrings are in Spanish, and the reports in each `report/` folder are in Spanish too.

Each project builds on the previous one.

| Folder | What it is |
|---|---|
| `01-number-theory-toolkit/` | `modular.py`, a library of modular arithmetic routines (primality, sieving, factoring, gcd, modular inverse and power, Euler phi, Legendre symbol, congruence systems, square roots, quadratic equations), and IMAT-LAB, a command interpreter with a Tk window and a batch mode on top of it |
| `02-cryptochat/` | A textbook RSA implementation with padding and two attacks, a script that registers users and key files, and a terminal chat that encrypts and decrypts messages between two users |
| `03-madrid-gps/` | A graph library written from scratch (Dijkstra, Prim, Kruskal), a rebuild of Madrid's street graph from the city's open data, and a Flask web app that gives driving directions between two addresses |

Dates, taken from the file timestamps: project 1 from September to October 2023, project 2 from October to November 2023, project 3 from November 2023 to January 2024 (one file in project 3 was edited again in February 2024).

## Repository layout

Every folder has its own README with how to run it, what was checked and what is not included. The folders are self contained, so `modular.py` appears in both projects 1 and 2 (the same file).

## What is not here

The assignments came with teacher material that belongs to the course and is not included: the assignment statements, the function templates the signatures and docstrings were written against (`modular.py`, `rsa.py`, `grafo.py`, `callejero.py`), the benchmark input files for project 1, the slides, the books and the problem sheets. The docstrings of the required functions follow the templates, the implementations are the authors' work. The lecturers' correction sheets, the sample user key files and messages, scratch files, earlier drafts, a factoring routine taken from a third party (`QS.py`), Office temporary files and caches are also left out.

The large Madrid address file (`direcciones.csv`, about 95 MB) is not included. The street intersections file is, with attribution, see `03-madrid-gps/README.md`.

## Known limitations

These are the state of the code as submitted in 2023. They were found when the code was checked again and are listed in the project READMEs:

- `resolver_sistema_congruencias` keeps its intermediate values in Python complex numbers, which are floating point, so systems with several equations and large coefficients can return wrong answers.
- `raiz_mod_p`, and through it the quadratic equation solver, returns wrong roots for part of the primes congruent to 1 modulo 8.

## Licence

The code is under the MIT licence (see `LICENSE`). The street intersections data is published by the Ayuntamiento de Madrid under CC BY 4.0 and keeps its own terms.
