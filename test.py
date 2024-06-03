import copy

import networkx as nx

from database.DAO import DAO
from model.model import Model

# retailer = DAO.getRetailer("France")
# conn = DAO.getConnection("France",2015)
model = Model()
# grafo = model.creaGrafo("White", 2018)
# v0 = model._idMapProduct[94110]
"""vicini = sorted(grafo[v0], key=lambda x: grafo[v0][x]['weight'])
for v in vicini:
    print(grafo[v0][v]['weight'])"""


class Test:
    def __init__(self):
        self.grafo = nx.Graph()
        self._volumi = {}
        self._bestPath = []
        self._bestWeight = 0

    def createGraph(self):
        self.grafo.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

        # Aggiungi archi con pesi
        self.grafo.add_edge('A', 'B', weight=1)
        self.grafo.add_edge('A', 'C', weight=2)
        self.grafo.add_edge('B', 'C', weight=2)
        self.grafo.add_edge('B', 'D', weight=3)
        self.grafo.add_edge('C', 'D', weight=4)
        self.grafo.add_edge('C', 'E', weight=5)
        self.grafo.add_edge('D', 'E', weight=1)

        return self.grafo

    def getVolumi(self):
        for n in self.grafo.nodes:
            vicini = list(self.grafo[n])
            for v in self.grafo[n]:
                if n not in self._volumi:
                    self._volumi[n] = self.grafo[n][v]['weight']
                else:
                    self._volumi[n] += self.grafo[n][v]['weight']

        return self._volumi

    def getBestPath(self, maxArchi):
        self._bestPath = []  # tupla fatta da (bestPath, peso)
        self._bestWeight = 0

        for n in self.grafo.nodes:
            parziale = [n]  # tupla fatta da (percorso)
            peso = 0
            self.ricorsione(parziale, peso, maxArchi)

        return self._bestPath

    def ricorsione(self, parziale, peso, maxArchi):
        if len(parziale) - 1 == maxArchi:
            if parziale[0] == parziale[-1] and peso > self._bestWeight:
                self._bestPath = copy.deepcopy(parziale)
                self._bestWeight = peso
                return
            else:
                return

        for v in self.grafo[parziale[-1]]:
            if (len(parziale) == maxArchi and v == parziale[0]) or (v not in parziale):
                parziale.append(v)
                peso += self.grafo[parziale[-2]][v]['weight']
                self.ricorsione(parziale, peso, maxArchi)
                parziale.pop()


if __name__ == '__main__':
    t = Test()
    grafo = t.createGraph()
    path = t.getVolumi()
    bestPath = t.getBestPath(3)
    print(t._bestPath)
    print(t._bestWeight)
