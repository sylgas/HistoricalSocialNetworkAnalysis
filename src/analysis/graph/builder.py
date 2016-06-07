import networkx as nx

from src import BASE_DIR


class Graph:
    def __init__(self, db, nodes=None, since=None, to=None):
        self.db = db
        if nodes is None:
            self.nodes = self.build_nodes(since, to)
        else:
            self.nodes = list(nodes)
        self.graph = self.__build()

    def get(self):
        return self.graph

    def get_nodes(self):
        return self.nodes

    def subgraph(self, nbunch):
        return self.graph.subgraph(nbunch)

    def export(self, filename):
        f = open(BASE_DIR + '/export/' + filename, 'w', encoding='utf-8')
        f.write('Source\tTarget\tLabel\n')
        for from_edge, to_edge in self.graph.edges():
            data = self.graph.get_edge_data(from_edge, to_edge)
            f.write(from_edge + '\t' + to_edge + '\t' + data['name'] + '\n')
        f.close()

    def __build(self):
        graph = nx.Graph()
        self.add_edges(graph)
        return graph

    def add_edges(self, graph):
        raise NotImplementedError("Should have implemented this")

    def build_nodes(self, since, to):
        raise NotImplementedError("Should have implemented this")


class SimpleGraph(Graph):
    def build_nodes(self, since, to):
        if since is None and to is None:
            return self.db.find_persons_with_relations().distinct('url')
        return self.db.find_persons_in_period_with_relations(since, to).distinct('url')

    def add_edges(self, graph):
        for relation in self.db.find_relations_for(self.nodes):
            graph.add_edge(relation['from_name'], relation['to_name'], {'name': relation['type']})


class AnalyticalGraph(Graph):
    def __init__(self, db, since=None, to=None):
        self.relations = []
        super(AnalyticalGraph, self).__init__(db, nodes=None, since=since, to=to)
        print("Counting degree")
        self.degree_centrality = nx.degree_centrality(self.graph)
        print("Counting betweeness")
        self.betweeness_centrality = nx.betweenness_centrality(self.graph, k=10)
        print("Counting closeness")
        self.closeness_centrality = self.degree_centrality # nx.closeness_centrality(self.graph)
        print("Counting eigenvector")
        self.eigenvector_centrality = self.degree_centrality # nx.eigenvector_centrality(self.graph)
        print("Counting page rank")
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

    def add_edges(self, graph):
        for relation in self.db.find_relations_for(list(self.nodes.keys())):
            graph.add_edge(relation['from'], relation['to'], {'name': relation['type']})
            self.relations.append(relation)

    def build_nodes(self, since, to):
        nodes = {}
        for person in self.db.find_persons_in_period_with_relations(since, to):
            nodes[person['url']] = person
        return nodes
