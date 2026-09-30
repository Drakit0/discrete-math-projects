# 03 Madrid GPS

Third project of Discrete Mathematics (Comillas ICAI, November 2023 to January 2024), by Pablo Tuñón Laguna and Jorge Vančo Sampedro (group GP01B). It is a small car navigator for the city of Madrid. The street map is rebuilt as a graph from the city council's open data, and a Flask web page takes two addresses and shows the shortest and the fastest route on a map with turn-by-turn directions.

## How it works

- `grafo.py`: a graph class written from scratch, directed or undirected, stored as adjacency dictionaries with a data object and a weight on each edge. It has vertex and edge insertion and removal, degrees, Dijkstra's algorithm with a binary heap, shortest path, Prim, Kruskal and a conversion to a NetworkX graph. The assignment forbade calling NetworkX for the algorithms.
- `callejero.py`: the `Cruce` (crossing) and `Calle` (street) classes and the table of maximum speeds by street type that the assignment gave.
- `clean_dgt.py`: reads the two CSV files (the encoding is detected with `chardet`), trims names, converts the degree-minute-second coordinates to decimal degrees, builds full street names and splits house numbers.
- `create_graph.py`: builds the two graphs.
  1. Crossings that lie within `R` centimetres of each other (1,500 in `gps.py`) are merged into one vertex, so a roundabout is a single node rather than one per street that meets it.
  2. A `Calle` object is created for every street code found in either file.
  3. For each street its crossings are ordered along the street and consecutive ones are joined by an edge. `get_aristas` starts at one crossing, takes the nearest as the next, and uses the sign of a dot product to decide how to chain the rest.
  4. Every edge carries the street name, its length and the travel time at the street's speed. One graph is weighted by length, the other by time.
- `functions.py`: builds the directions from a path. A turn is left or right by the sign of the cross product of the two edge vectors, and the program says "continue straight" when the angle is small. Instructions give the distance in metres along each street, the ordinal number of the crossing where to turn, the total length and the estimated time. The same file draws the route on a Folium map and finds the crossing for a house number (the nearest crossing on that street) or for a street that crosses.
- `flask_app.py`, `html_text.py`: the web page. You type two streets (the page suggests names from the data), then a house number or a crossing street for each. The map then shows two flags, a green route for the shortest distance and a blue one for the shortest time, and a table of directions for each.
- `gps.py`: builds the graphs and starts the Flask server.
- `report/P3GP01B.pdf`: the group's report, in Spanish, with the reconstruction method, the structure of the program and screenshots of the page.

## How to run

1. Get the data. `cruces.csv` is included. `direcciones.csv` is not, see [DATA.md](DATA.md) for where to download it. Put it in this folder.
2. Install the requirements and start the app:

```
pip install -r requirements.txt
python gps.py
```

3. Open http://127.0.0.1:5000 in a browser. The map tiles and scripts are loaded from the internet by Folium.

The graph is built every time the program starts, and that takes several minutes (see below).

`requirements.txt` is the list of pinned versions from 2023. The code also ran, unchanged, with current releases on Python 3.12 (pandas 3.0, Flask 3.0, Folium 0.20, NetworkX 3.3). Running `python create_graph.py` instead of `gps.py` builds the graph and draws it with matplotlib.

## What was checked

In 2026 the graphs were rebuilt from the January 2024 data files with `R = 1500`, and the Flask test client was used instead of starting a server:

- The graph has 13,276 vertices, 20,552 edges and 8,697 street objects. Start to ready took about 8 minutes on a laptop: roughly 200 seconds loading and cleaning the two CSV files and 258 seconds building the graphs (the program prints the second time).
- A route from Calle de Alcalá 156 to Calle de Serrano 114 is computed in 0.4 seconds. It is 27 crossings, 2.19 km and an estimated 3 minutes, with instructions such as turning right onto Calle de las Mártires Concepcionistas, going straight 281 metres and turning at the second crossing.
- `GET /` and a route request both return HTTP 200 and the route page comes back without an error message.
- `grafo.py` was checked on 200 random weighted graphs against NetworkX: the Dijkstra path lengths and the Prim and Kruskal tree weights matched every time.

The directions were not compared with a real navigator.

## Known limitations

- The graph is an approximation, as the assignment said. The intersections file covers mainly the streets of the municipality of Madrid, every street is treated as two-way, and streets that are not straight are joined crossing to crossing in a straight line.
- The start-up time is long. Most of it goes to the row-by-row cleaning of the CSV files and the grouping of crossings with pandas. It has not been profiled.
- `flask_app.py` uses Flask's development server and keeps the graphs in the app configuration. It is meant to run on one machine.

## What is not included

`direcciones.csv` (download note above), the assignment statement, the graph template and the lecturers' test script for `grafo.py`, the earlier version of the code and the in-class NetworkX exercise notebook.
