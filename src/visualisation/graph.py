import networkx as nx
from matplotlib import pylab as pl

from src.analysis.graph.builder import GraphBuilder


class GraphDrawer:
    def draw(self, graph):
        pos = nx.random_layout(graph)

        pl.figure()
        nx.draw(graph, pos=pos)
        pl.show()

    def draw_groups(self, db, groups):
        pl.figure()
        index = 0.0
        # {node: (float) groupId}
        node_group = dict()
        for group in groups:
            index += 1.0
            for node in group:
                node_group[node] = index

        graph = GraphBuilder(db, nodes=node_group.keys()).build()

        node_groups_values = set(node_group.values())
        r = 1 / len(node_groups_values)

        # color param for cmap in [0.0,1.0]
        colors = [(node_group.get(node, 0.0) * r) for node in graph.nodes()]

        nx.draw_shell(graph, cmap=pl.get_cmap('jet'), node_color=colors)
        pl.show()
