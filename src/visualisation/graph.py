import networkx as nx
from matplotlib import pylab as pl
from networkx.drawing.nx_agraph import graphviz_layout

from src.analysis.graph.builder import SimpleGraph
from src.analysis.graph.centrality import CentralityMeasurer


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
        test = dict()
        for group in groups:
            index += 1.0
            for node in group:
                node_group[node] = index
                if node not in test:
                    test[node] = []
                test[node].append(index)
                if len(test[node]) > 1:
                    print(test[node])

        graph = SimpleGraph(db, nodes=node_group.keys()).get()
        centrality = nx.degree_centrality(graph)
        ranking = dict(CentralityMeasurer.create_ranking(centrality))

        node_groups_values = set(node_group.values())
        r = 1 / len(node_groups_values)

        # color param for cmap in [0.0,1.0]
        colors = [(node_group.get(node, 0.0) * r) for node in graph.nodes()]
        sizes = [v * 5000 for v in centrality.values()]
        labels = {node: self.create_label(node, ranking) for node in graph.nodes()}
        pos = graphviz_layout(graph)

        nx.draw_networkx_nodes(graph, pos=pos, cmap='Pastel1', node_color=colors, node_size=sizes)
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)
        nx.draw_networkx_edges(graph, pos, width=0.2)
        pl.show()

    @staticmethod
    def create_label(node, ranking):
        if node in ranking:
            return node.replace('http://dbpedia.org/resource/', '')
        return ''
