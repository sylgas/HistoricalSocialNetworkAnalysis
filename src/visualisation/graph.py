import networkx as nx
from matplotlib import pylab as pl


class GraphDrawer:
    def draw(self, graph):
        pos = nx.random_layout(graph)

        pl.figure()
        nx.draw(graph, pos=pos)
        pl.show()
