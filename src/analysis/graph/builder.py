import networkx as nx


class Graph:
    def __init__(self, db, nodes=None, since=None, to=None):
        self.db = db
        if nodes is None:
            self.nodes = self.__build_nodes(since, to)
        else:
            self.nodes = list(nodes)

        self.graph = self.__build()

    def get(self):
        return self.graph

    def get_nodes(self):
        return self.nodes

    def __find_relations(self, urls):
        return self.db.find_relations_for(urls)

    def __build(self):
        graph = nx.Graph()
        self.__add_edges(graph, self.__find_relations(self.__get_node_urls()))
        return graph

    @staticmethod
    def __add_edges(graph, relations):
        for relation in relations:
            graph.add_edge(relation['from'], relation['to'], {'name': relation['type']})

    def __build_nodes(self, since, to):
        raise NotImplementedError("Should have implemented this")

    def __get_node_urls(self):
        raise NotImplementedError("Should have implemented this")


class SimpleGraph(Graph):
    def __build_nodes(self, since, to):
        return self.db.find_persons_in_period_with_relations(since, to).distinct('url')

    def __get_node_urls(self):
        return self.nodes


class AnalyticalGraph(Graph):
    def __init__(self, db, since, to):
        super(AnalyticalGraph, self).__init__(db, since, to)
        self.degree_centrality = nx.degree_centrality(self.graph)
        self.betweeness_centrality = nx.betweenness_centrality(self.graph)
        self.closeness_centrality = nx.closeness_centrality(self.graph)
        self.eigenvector_centrality = nx.eigenvector_centrality(self.graph)
        self.page_rank = nx.pagerank(self.graph)

    def get_degree_centrality(self):
        return self.degree_centrality

    def get_betweeness_centrality(self):
        return self.betweeness_centrality

    def get_closeness_centrality(self):
        return self.closeness_centrality

    def get_eigenvector_centrality(self):
        return self.eigenvector_centrality

    def get_page_rank(self):
        return self.page_rank

    def __build_nodes(self, since, to):
        nodes = {}
        for person in self.db.find_persons_in_period_with_relations(since, to):
            nodes[person['url']] = person
        return nodes

    def __get_node_urls(self):
        return self.nodes.keys()
