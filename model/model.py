import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._listaCountry = DAO.getAllCountry()
        self._listaAnni = DAO.getAllYears()
        self._grafo = nx.Graph()
        self.retailer = None
        self._idMapRetailer = {}
        self._volumi = {}
        self._bestPath = []
        self._bestWeight = 0

    def getBestPath(self, maxArchi):
        self._bestPath = []  # tupla fatta da bestPath
        self._bestWeight = 0
        for n in self._grafo.nodes:
            parziale = [n]
            peso = 0
            self.ricorsione(parziale, peso, maxArchi)

    def ricorsione(self, parziale, peso, maxArchi):
        if len(parziale) - 1 == maxArchi:
            if parziale[0] == parziale[-1] and peso > self._bestWeight:
                self._bestPath = copy.deepcopy(parziale)
                self._bestWeight = peso
                return
            else:
                return

        vicini = list(self._grafo[parziale[-1]])
        for v in self._grafo[parziale[-1]]:
            if (len(parziale) == maxArchi and v == parziale[0]) or (v not in parziale):
                parziale.append(v)
                peso += self._grafo[parziale[-2]][v]['weight']
                self.ricorsione(parziale, peso, maxArchi)
                peso -= self._grafo[parziale[-2]][v]['weight']
                parziale.pop()

    def getVolumi(self):
        for n in self._grafo.nodes:
            vicini = list(self._grafo[n])
            for v in self._grafo[n]:
                if n not in self._volumi:
                    self._volumi[n] = self._grafo[n][v]['weight']
                else:
                    self._volumi[n] += self._grafo[n][v]['weight']

    def creaGrafo(self, country, anno):
        self._grafo.clear()
        self.addNodes(country)
        self.addEdges(anno, country)

    def addNodes(self, country):
        self.retailer = DAO.getRetailer(country)
        self._grafo.add_nodes_from(self.retailer)
        for node in self.retailer:
            self._idMapRetailer[node.Retailer_code] = node

    def addEdges(self, anno, country):
        connection = DAO.getConnection(country, int(anno))
        for c in connection:
            self._grafo.add_edge(self._idMapRetailer[c[0]], self._idMapRetailer[c[1]], weight=c[3])

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
