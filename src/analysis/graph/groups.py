import operator

import community as louvain
import networkx as nx


class GroupsFinder:
    LOUVAIN_GROUP_MIN_SIZE = 3

    def __init__(self, graph):
        self.graph = graph

    def find_groups_cpm(self, min_k):
        return nx.k_clique_communities(self.graph, min_k)

    def find_groups_louvain(self, res=1):
        node_to_id = louvain.best_partition(self.graph, resolution=res)
        group_ids = set(map(lambda node: node_to_id[node], node_to_id))
        groups = [[node for node in node_to_id if node_to_id[node] == group_id] for group_id in group_ids]
        groups = list(filter(lambda x: len(x) >= GroupsFinder.LOUVAIN_GROUP_MIN_SIZE, groups))
        return groups

    def print_groups_louvain(self, resolution_list, all=False):
        for resolution in resolution_list:
            groups = self.find_groups_louvain(res=resolution)
            print(str(resolution) + '\t' + str(len(groups)))
            if all:
                print(groups)

    def print_groups_cpm(self, klist, all=False, db=None):
        for k in klist:
            groups = list(self.find_groups_cpm(k))
            count = len(groups)
            print(str(k) + '\t' + str(count))
            # group_counts = dict(map(lambda node: (node, len(list(node))), groups))
            # counts = dict(Counter(group_counts.values()))
            # sorted_counts = collections.OrderedDict(sorted(counts.items()))
            # print(sorted_counts)
            # sum_density = 0
            # for group in groups:
            #     print('grupa ' + str(len(group)))
            #     g = SimpleGraph(db, nodes=group).get()
            #     print('graf' + str(len(g)))
            #     density = nx.bipartite.density(g, group)
            #     sum_density += density
            # print(str(sum_density/count))
            if all:
                print(groups)


class GroupComparator:
    def __init__(self, old_graph, old_groups, new_graph, new_groups):
        self.old_profiles = self.__find_profiles(old_graph, old_groups)
        self.new_profiles = self.__find_profiles(new_graph, new_groups)
        self.similar_groups = self.__find_similar_groups()

    def get_similar_group(self):
        return self.similar_groups

    @staticmethod
    def __find_profiles(graph, groups):
        result = []
        for g in groups:
            result.append((g, Profile(g, graph)))
        return result

    def __find_similar_groups(self):
        result = []
        for op in self.old_profiles:
            for np in self.new_profiles:
                pc = ProfileComparator(op[1], np[1])
                similarity = pc.get_similarity_factor()
                if similarity > 0:
                    result.append((op, np, similarity, pc.get_differences()))
        return sorted(result, key=lambda x: x[2], reverse=True)


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
        return self.graph.get_nodes()[sorted_results[0][0]]

    def __find_type(self):
        types = {}
        for url in self.nodes:
            person = self.graph.get_nodes()[url]
            # todo: usunac po przeparsowniu typow
            if isinstance(person['type'], dict):
                continue
            if person['type'] not in types:
                types[person['type']] = 0
            types[person['type']] += 1
        sorted_results = sorted(types.items(), key=operator.itemgetter(1), reverse=True)
        # todo: usunac po przeparsowniu typow
        if len(sorted_results) == 0:
            return ''
        return sorted_results[0][0]

    def __find_nationality(self):
        nationalities = {}
        for url in self.nodes:
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
        self.only_old = [n for n in old_nodes if n not in self.common]
        self.only_new = [n for n in new_nodes if n not in self.common]
        self.differences = self.__find_differences()

    # returns <0, 1> - the higher value the greater probability is the same group
    def get_similarity_factor(self):
        return (2.0 * len(self.common)) / self.all_nodes_count

    def get_differences(self):
        return self.differences

    def __find_differences(self):
        return {
            'count': self.old_profile.get()['count'] - self.new_profile.get()['count'],
            'top_person': (self.old_profile.get()['top_person'], self.new_profile.get()['top_person']),
            'type': (self.old_profile.get()['type'], self.new_profile.get()['type']),
            'nationality': (self.old_profile.get()['nationality'], self.new_profile.get()['nationality']),
            'degree_centrality': self.old_profile.get()['degree_centrality'] - self.new_profile.get()['degree_centrality'],
            'betweeness_centrality': self.old_profile.get()['betweeness_centrality'] - self.new_profile.get()['betweeness_centrality'],
            'closeness_centrality': self.old_profile.get()['closeness_centrality'] - self.new_profile.get()['closeness_centrality'],
            'eigenvector_centrality': self.old_profile.get()['eigenvector_centrality'] - self.new_profile.get()['eigenvector_centrality'],
            'page_rank': self.old_profile.get()['page_rank'] - self.new_profile.get()['page_rank'],
        }

