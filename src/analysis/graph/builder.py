import networkx as nx


class Graph:
    def __init__(self, db, nodes=None, since=None, to=None):
        self.db = db
        if nodes is None:
            self.nodes = self._build_nodes(since, to)
        else:
            self.nodes = list(nodes)
        self.graph = self.__build()

    def get(self):
        return self.graph

    def get_nodes(self):
        return self.nodes

    def __build(self):
        graph = nx.Graph()
        self._add_edges(graph)
        return graph

    def _add_edges(self, graph):
        raise NotImplementedError("Should have implemented this")

    def _build_nodes(self, since, to):
        raise NotImplementedError("Should have implemented this")


class SimpleGraph(Graph):
    def _build_nodes(self, since, to):
        if since is None and to is None:
            return self.db.find_persons_with_relations().distinct('url')
        return self.db.find_persons_in_period_with_relations(since, to).distinct('url')

    def _add_edges(self, graph):
        for relation in self.db.find_relations_for(self.nodes):
            graph.add_edge(relation['from'], relation['to'], {'name': relation['type']})


class AnalyticalGraph(Graph):
    def __init__(self, db, since=None, to=None):
        super(AnalyticalGraph, self).__init__(db, nodes=None, since=since, to=to)
        self.relations = []
        self.degree_centrality = nx.degree_centrality(self.graph)
        self.betweeness_centrality = nx.betweenness_centrality(self.graph)
        self.closeness_centrality = nx.closeness_centrality(self.graph)
        self.eigenvector_centrality = nx.eigenvector_centrality(self.graph)
        self.page_rank = nx.pagerank(self.graph)

    def get_relations(self):
        return self.relations

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

    def _add_edges(self, graph):
        for relation in self.db.find_relations_for(self.nodes.keys()):
            graph.add_edge(relation['from'], relation['to'], {'name': relation['type']})
            self.relations.append(relation)

    def _build_nodes(self, since, to):
        nodes = {}
        for person in self.db.find_persons_in_period_with_relations(since, to):
            nodes[person['url']] = person
        return nodes
