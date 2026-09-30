"""
grafo.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP01B
Integrantes:
    - Pablo Tuñón Laguna
    - Jorge Vančo Sampedro

Descripción:
Librería para la creación y análisis de grafos dirigidos y no dirigidos.
"""

from typing import List, Tuple, Dict
import networkx as nx
import sys

import heapq  # Librería para la creación de colas de prioridad

INFTY: float = sys.float_info.max  # Distincia "infinita" entre nodos de un grafo


class Arista:
    def __init__(self, s, t, data, weight) -> None:
        self.u = s
        self.v = t
        self.data = data
        self.weight = weight

    def __repr__(self) -> str:
        return f"({self.u}, {self.v}, w: {self.weight}), data:{self.data}"

    def __eq__(self, other) -> bool:
        return self.u == other.u and self.v == other.v and self.data == other.data

    def __le__(self, other) -> bool:
        return self.weight <= other.weight

    def __ge__(self, other) -> bool:
        return self.weight >= other.weight

    def __gt__(self, other) -> bool:
        return self.weight > other.weight

    def __lt__(self, other) -> bool:
        return self.weight < other.weight

    def __hash__(self) -> int:
        return hash(f"({self.u}, {self.v}, {self.data}, {self.weight})")


class Grafo:
    """
    Clase que almacena un grafo dirigido o no dirigido y proporciona herramientas
    para su análisis.
    """

    def __init__(self, dirigido: bool = False) -> None:
        """Crea un grafo dirigido o no dirigido.

        Args:
            dirigido (bool): Flag que indica si el grafo es dirigido (verdadero) o no (falso).

        Returns:
            Grafo o grafo dirigido (según lo indicado por el flag)
            inicializado sin vértices ni aristas.
        """

        # Flag que indica si el grafo es dirigido o no.
        self.dirigido: bool = dirigido

        """
        Diccionario que almacena la lista de adyacencia del grafo.
        adyacencia[u]:  diccionario cuyas claves son la adyacencia de u
        adyacencia[u][v]:   Contenido de la arista (u,v), es decir, par (a,w) formado
                            por el objeto almacenado en la arista "a" (object) y su peso "w" (float).
        """
        self.adyacencia: Dict[object, Dict[object, Tuple[object, float]]] = {}

    #### Operaciones básicas del TAD ####
    def es_dirigido(self) -> bool:
        """Indica si el grafo es dirigido o no

        Args: None
        Returns: True si el grafo es dirigido, False si no.
        Raises: None
        """
        return self.dirigido

    def agregar_vertice(self, v: object) -> None:
        """Agrega el vértice v al grafo.

        Args:
            v (object): vértice que se quiere agregar. Debe ser "hashable".
        Returns: None
        Raises:
            TypeError: Si el objeto no es "hashable".
        """
        try:
            h: int = hash(v)
        except TypeError:
            raise TypeError(f"El objeto {v} no es hasheable")

        self.adyacencia[v] = dict()

    def agregar_arista(
        self, s: object, t: object, data: object = None, weight: float = 1
    ) -> None:
        """Si los objetos s y t son vértices del grafo, agrega
        una arista al grafo que va desde el vértice s hasta el vértice t
        y le asocia los datos "data" y el peso weight.
        En caso contrario, no hace nada.

        Args:
            s (object): vértice de origen (source).
            t (object): vértice de destino (target).
            data (object, opcional): datos de la arista. Por defecto, None.
            weight (float, opcional): peso de la arista. Por defecto, 1.
        Returns: None
        Raises:
            TypeError: Si s o t no son "hashable".
        """

        try:
            hash_s: int = hash(s)
            hash_t: int = hash(t)

        except TypeError as e:
            raise TypeError(e)

        if s in self.adyacencia and t in self.adyacencia:
            # Se crea el objeto arista
            arista = Arista(s, t, data, weight)

            # Se añade la arista s -> t
            self.adyacencia[s][t] = (arista, weight)

            # Si no es un grafo dirigido, tambien se añade la arista t -> s
            if not self.es_dirigido():
                self.adyacencia[t][s] = (arista, weight)

    def eliminar_vertice(self, v: object) -> None:
        """Si el objeto v es un vértice del grafo lo elimina.
        Si no, no hace nada.

        Args:
            v (object): vértice que se quiere eliminar.
        Returns: None
        Raises:
            TypeError: Si v no es "hashable".
        """
        
        try:
            hash_v: int = hash(v)
        except TypeError as e:
            raise TypeError(e)

        if v in self.adyacencia:
            # Elimina v de la adyacencia
            self.adyacencia.pop(v)

            # Elimina las aristas que van hasta el vertice v
            for vertice in self.adyacencia:
                if v in self.adyacencia[vertice]:
                    self.adyacencia[vertice].pop(v)

    def eliminar_arista(self, s: object, t: object) -> None:
        """Si los objetos s y t son vértices del grafo y existe
        una arista de u a v la elimina.
        Si no, no hace nada.

        Args:
            s: vértice de origen de la arista (source).
            t: vértice de destino de la arista (target).
        Returns: None
        Raises:
            TypeError: Si s o t no son "hashable".
        """
        try:
            hash_s: int = hash(s)
            hash_t: int = hash(t)

        except TypeError as e:
            raise TypeError(e)

        if s in self.adyacencia and t in self.adyacencia:
            adyacencia_s: Dict[object, Tuple[object, float]] = self.adyacencia[s]

            # Elimina la arista s -> t de la adyacencia de s
            if t in adyacencia_s:
                adyacencia_s.pop(t)

            # Si no es dirigido, se borra también la arista t -> s
            if not self.es_dirigido():
                adyacencia_t: Dict[object, Tuple[object, float]] = self.adyacencia[t]

                # Elimina la arista t -> s de la adyacencia de t
                if s in adyacencia_t:
                    adyacencia_t.pop(s)

    def obtener_arista(self, s: object, t: object) -> Tuple[object, float] or None:
        """Si los objetos s y t son vértices del grafo y existe
        una arista de u a v, devuelve sus datos y su peso en una tupla.
        Si no, devuelve None

        Args:
            s: vértice de origen de la arista (source).
            t: vértice de destino de la arista (target).
        Returns:
            Tuple[object,float]: Una tupla (a,w) con los datos "a" de la arista (s,t) y su peso
                "w" si la arista existe.
            None: Si la arista (s,t) no existe en el grafo.
        Raises:
            TypeError: Si s o t no son "hashable".
        """
        try:
            hash_s: int = hash(s)
            hash_t: int = hash(t)

        except TypeError as e:
            raise TypeError(e)

        adyacencia_s: Dict[object, Tuple[object, float]] | None = self.adyacencia.get(
            s, None
        )
        if adyacencia_s is not None:
            return adyacencia_s.get(t, None)

    def obtener_aristas(self) -> set:
        """
        Devuelve las aristas del grafo

        Returns:
            set: Las aristas del Grafo
        """
        A: set = set()
        for adyacencia_v in self.adyacencia.values():
            for arista in adyacencia_v.values():
                A.add(arista)

        return A

    def lista_vertices(self) -> List[object]:
        """Devuelve una lista con los vértices del grafo.

        Args: None
        Returns:
            List[object]: Una lista [v1,v2,...,vn] de los vértices del grafo.
        Raises: None
        """
        return list(self.adyacencia.keys())

    def lista_adyacencia(self, u: object) -> List[object] or None:
        """Si el objeto u es un vértice del grafo, devuelve
        su lista de adyacencia, es decir, una lista [v1,...,vn] con los vértices
        tales que (u,v1), (u,v2),..., (u,vn) son aristas del grafo.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns:
            List[object]: Una lista [v1,v2,...,vn] de los vértices del grafo
                adyacentes a u si u es un vértice del grafo
            None: si u no es un vértice del grafo
        Raises:
            TypeError: Si u no es "hashable".
        """
        try:
            hash_u: int = hash(u)

        except TypeError as e:
            raise TypeError(e)

        adyacencia_u: Dict[object, Tuple[object, float]] | None = self.adyacencia.get(
            u, None
        )

        if adyacencia_u is not None:
            adyacencia_u = list(adyacencia_u.keys())

        return adyacencia_u

    #### Grados de vértices ####
    def grado_saliente(self, v: object) -> int or None:
        """Si el objeto v es un vértice del grafo, devuelve
        su grado saliente, es decir, el número de aristas que parten de v.
        Si no, devuelve None.

        Args:
            v (object): vértice del grafo
        Returns:
            int: El grado saliente de u si el vértice existe
            None: Si el vértice no existe.
        Raises:
            TypeError: Si u no es "hashable".
        """
        try:
            hash_v: int = hash(v)

        except TypeError as e:
            raise TypeError(e)

        adyacencia_v: Dict[object, Tuple[object, float]] | None = self.adyacencia.get(
            v, None
        )

        if adyacencia_v is None:
            return None

        return len(adyacencia_v)

    def grado_entrante(self, v: object) -> int or None:
        """Si el objeto v es un vértice del grafo, devuelve
        su grado entrante, es decir, el número de aristas que llegan a v.
        Si no, devuelve None.

        Args:
            v (object): vértice del grafo
        Returns:
            int: El grado entrante de u si el vértice existe
            None: Si el vértice no existe.
        Raises:
            TypeError: Si v no es "hashable".
        """
        try:
            hash_v: int = hash(v)

        except TypeError as e:
            raise TypeError(e)

        if v not in self.adyacencia:
            return None

        if not self.es_dirigido():
            return self.grado_saliente(v)

        grado = 0
        for adyacencia_u in self.adyacencia.values():
            if v in adyacencia_u:
                grado += 1

        return grado

    def grado(self, v: object) -> int or None:
        """Si el objeto v es un vértice del grafo, devuelve
        su grado si el grafo no es dirigido y su grado saliente si
        es dirigido.
        Si no pertenece al grafo, devuelve None.

        Args:
            v (object): vértice del grafo
        Returns:
            int: El grado grado o grado saliente de u según corresponda
                si el vértice existe
            None: Si el vértice no existe.
        Raises:
            TypeError: Si v no es "hashable".
        """
        try:
            hash_v: int = hash(v)

        except TypeError as e:
            raise TypeError(e)

        if v not in self.adyacencia:
            return None

        return self.grado_saliente(v)

    #### Algoritmos ####
    def dijkstra(self, origen: object) -> Dict[object, object]:
        """Calcula un Árbol de Caminos Mínimos para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
        el árbol de la componente conexa que contiene a "origen".

        Args:
            origen (object): vértice del grafo de origen
        Returns:
            Dict[object,object]: Devuelve un diccionario que indica, para cada vértice alcanzable
                desde "origen", qué vértice es su padre en el árbol de caminos mínimos.
        Raises:
            TypeError: Si origen no es "hashable".
        Example:
            Si G.dijksra(1)={2:1, 3:2, 4:1} entonces 1 es padre de 2 y de 4 y 2 es padre de 3.
            En particular, un camino mínimo desde 1 hasta 3 sería 1->2->3.
        """
        try:
            hash_origen: int = hash(origen)

        except TypeError as e:
            raise TypeError(e)

        if origen not in self.adyacencia:
            return None

        padre = {}
        visitado = {}
        d = {}

        for v in self.adyacencia:
            padre[v] = None
            visitado[v] = False
            d[v] = INFTY

        d[origen] = 0
        Q = []

        heapq.heappush(Q, (d[origen], origen))

        while Q:
            _, nodo = heapq.heappop(Q)

            if visitado[nodo] == False:
                visitado[nodo] = True
                for x, arista in self.adyacencia[nodo].items():
                    a, w = arista

                    if d[x] > d[nodo] + w:
                        d[x] = d[nodo] + w
                        padre[x] = nodo
                        heapq.heappush(Q, (d[x], x))

        return padre

    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        """Calcula el camino mínimo desde el vértice origen hasta el vértice
        destino utilizando el algoritmo de Dijkstra.

        Args:
            origen (object): vértice del grafo de origen
            destino (object): vértice del grafo de destino
        Returns:
            List[object]: Devuelve una lista con los vértices del grafo por los que pasa
                el camino más corto entre el origen y el destino. El primer elemento de
                la lista es origen y el último destino.
        Example:
            Si G.dijksra(1,4)=[1,5,2,4] entonces el camino más corto en G entre 1 y 4 es 1->5->2->4.
        Raises:
            TypeError: Si origen o destino no son "hashable".
        """

        try:
            hash_origen: int = hash(origen)
            hash_destino: int = hash(destino)

        except TypeError as e:
            raise TypeError(e)

        if destino not in self.adyacencia or origen not in self.adyacencia:
            return None

        arbol_min = self.dijkstra(origen)
        camino = []
        buscando_camino = True

        while buscando_camino:
            camino.append(destino)
            destino = arbol_min[destino]

            if destino is None:
                buscando_camino = False
            elif destino == origen:
                camino.append(origen)
                buscando_camino = False

        return camino[::-1]

    def prim(self) -> Dict[object, object]:
        """Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.

        Args: None
        Returns:
            Dict[object,object]: Devuelve un diccionario que indica, para cada vértice del
                grafo, qué vértice es su padre en el árbol abarcador mínimo.
        Raises: None
        Example:
            Si G.prim()={2:1, 3:2, 4:1} entonces en un árbol abarcador mínimo tenemos que:
                1 es padre de 2 y de 4
                2 es padre de 3
        """
        Q: list = []
        padre = dict()
        coste_minimo = dict()

        # Inicializamos variables
        for v in self.lista_vertices():
            padre[v] = None
            coste_minimo[v] = INFTY
            heapq.heappush(Q, (coste_minimo[v], v))

        # Se recorren todos los vértices
        while Q:
            _, v = heapq.heappop(Q)

            for x in set(self.adyacencia[v]) & set((x for _, x in Q)):
                _, w = self.obtener_arista(v, x)

                if w < coste_minimo[x]:
                    indice: int = Q.index((coste_minimo[x], x))
                    coste_minimo[x] = w
                    padre[x] = v
                    Q[indice] = (w, x)
                    heapq.heapify(Q)

        return padre

    def kruskal(self) -> List[Tuple[object, object]]:
        """Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Kruskal.

        Args: None
        Returns:
            List[Tuple[object,object]]: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
                de los pares de vértices del grafo que forman las aristas
                del arbol abarcador mínimo.
        Raises: None
        Example:
            En el ejemplo anterior en que G.prim()={2:1, 3:2, 4:1} podríamos tener, por ejemplo,
            G.kruskal=[(1,2),(1,4),(3,2)]
        """

        L: list = []
        for a, w in self.obtener_aristas():
            heapq.heappush(L, (w, a))

        C: dict = {}
        aristas_aam: list = []

        # Se crean las componentes, al principio la componente a la que pertenece un vértice está formada por él mismo
        for v in self.adyacencia:
            C[v] = {v}

        while L:
            a: tuple = heapq.heappop(L)
            u = a[1].u
            v = a[1].v

            # Si no se producen ciclos al añadir la arista (no son de la misma componente los dos vértices):
            if C[u] != C[v]:
                aristas_aam.append((u, v))

                # Se actualizan las componentes de cada vértice
                C[u] = C[u] | C[v]
                for w in C[u]:
                    C[w] = C[u]

        return aristas_aam

    #### NetworkX ####
    def convertir_a_NetworkX(self) -> nx.Graph or nx.DiGraph:
        """Construye un grafo o digrafo de Networkx según corresponda
        a partir de los datos del grafo actual.

        Args: None
        Returns:
            networkx.Graph: Objeto Graph de NetworkX si el grafo es no dirigido.
            networkx.DiGraph: Objeto DiGraph si el grafo es dirigido.
            En ambos casos, los vértices y las aristas son los contenidos en el grafo dado.
        Raises: None
        """

        if self.dirigido == True:
            G = nx.digraph()

        else:
            G = nx.Graph()

        G.add_nodes_from(self.lista_vertices())

        edges = set()

        for node in G.nodes:
            for edge in self.lista_adyacencia(node):
                edges.add((node, edge))

        G.add_edges_from(list(edges))

        return G