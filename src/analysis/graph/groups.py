import operator
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


class Profile:
    def __init__(self, nodes, graph):
        self.nodes = nodes
        self.graph = graph
        self.profile = {
            'count': len(nodes),
            'top_person': self.__find_top_person(),
            'type': self.__find_type(),
            'nationality': self.__find_nationality(),
            'degree_centrality': self.__find_degree_centrality(),
            'betweeness_centrality': self.__find_betweeness_centrality(),
            'closeness_centrality': self.__find_closeness_centrality(),
            'eigenvector_centrality': self.__find_eigenvector_centrality(),
            'page_rank': self.__find_page_rank()
        }

    def get(self):
        return self.profile

    def get_nodes(self):
        return self.nodes

    def __find_top_person(self):
        result = {}
        for url in self.nodes:
            result[url] = 0
        for url in self.nodes:
            result[url] += self.graph.get_degree_centrality()[url]
            result[url] += self.graph.get_betweeness_centrality()[url]
            result[url] += self.graph.get_closeness_centrality()[url]
            result[url] += self.graph.get_eigenvector_centrality()[url]
            result[url] += self.graph.get_page_rank()[url]
        sorted_results = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        return self.nodes[sorted_results[0][0]]

    def __find_type(self):
        types = {}
        for url in self.nodes():
            person = self.graph.get_nodes()[url]
            if person['type'] not in types:
                types[person['type']] = 0
            types[person['type']] += 1
        sorted_results = sorted(types.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_results[0][0]

    def __find_nationality(self):
        nationalities = {}
        for url in self.nodes():
            person = self.graph.get_nodes()[url]
            nationality = person['nationality']
            if nationality is '':
                continue
            if nationality not in nationalities:
                nationalities[person['nationality']] = 0
            nationalities[person['nationality']] += 1
        if len(nationalities) == 0:
            return ''
        sorted_results = sorted(nationalities.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_results[0][0]

    def __find_degree_centrality(self):
        return self.__find_average(self.graph.get_degree_centrality())

    def __find_betweeness_centrality(self):
        return self.__find_average(self.graph.get_betweeness_centrality())

    def __find_closeness_centrality(self):
        return self.__find_average(self.graph.get_closeness_centrality())

    def __find_eigenvector_centrality(self):
        return self.__find_average(self.graph.get_eigenvector_centrality())

    def __find_page_rank(self):
        return self.__find_average(self.graph.get_page_rank())

    def __find_average(self, centrality):
        value = 0
        for url in self.nodes:
            value += centrality[url]
        return value / len(centrality)


class ProfileComparator:
    def __init__(self, old_profile, new_profile):
        self.old_profile = old_profile
        self.new_profile = new_profile
        old_nodes = old_profile.get_nodes()
        new_nodes = new_profile.get_nodes()
        self.all_nodes_count = len(old_nodes) + len(new_nodes)
        self.common = list(set(old_nodes).intersection(new_nodes))
        self.old = [n for n in old_nodes if n not in self.common]
        self.new = [n for n in new_nodes if n not in self.common]

    # returns <0, 1> - the higher value the greater probability is the same group
    def get_similarity_factor(self):
        return (2.0 * len(self.common)) / self.all_nodes_count
