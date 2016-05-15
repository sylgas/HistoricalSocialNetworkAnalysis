import networkx as nx
from matplotlib import pylab as pl


class GraphDrawer:
    def draw(self, graph):
        pl.figure()
        g = nx.draw(graph)
        pl.show()
