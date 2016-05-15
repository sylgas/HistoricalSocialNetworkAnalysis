import networkx as nx


class GroupsFinder:
    def __init__(self, graph):
        self.graph = graph

    def find_groups_cpm(self, min_k):
        return nx.k_clique_communities(self.graph, min_k)

    def find_groups_louvain(self):
        pass
