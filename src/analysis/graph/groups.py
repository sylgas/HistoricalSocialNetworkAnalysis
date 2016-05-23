from collections import Counter

import community as louvain
import networkx as nx


class GroupsFinder:
    def __init__(self, graph):
        self.graph = graph

    def find_groups_cpm(self, min_k):
        return nx.k_clique_communities(self.graph, min_k)

    def find_groups_louvain(self, res=1):
        return louvain.best_partition(self.graph, resolution=res)

    def print_groups_louvain(self, resolution_list, all=False):
        for resolution in resolution_list:
            groups = dict(self.find_groups_louvain(res=resolution))
            val_counter = Counter(groups.values())

            print(val_counter)
            print(str(resolution) + '\t' + str(len(set(groups.values()))))
            if all:
                print(groups)

    def print_groups_cpm(self, klist, all=False):
        for k in klist:
            groups = list(self.find_groups_cpm(k))
            print(str(k) + '\t' + str(len(groups)))
            if all:
                print(groups)
