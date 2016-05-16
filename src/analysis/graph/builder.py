import networkx as nx


class GraphBuilder:
    def __init__(self, db, nodes=None, since=None, to=None):
        self.db = db
        if nodes is None:
            self.nodes = self.build_nodes(db, since, to)
        else:
            self.nodes = list(nodes)

    @staticmethod
    def build_nodes(db, since, to):
        return db.find_persons_in_period_with_relations(since, to).distinct('url')

    def add_edges(self, graph):
        relations = self.db.find_relations_for(self.nodes)
        for relation in relations:
            graph.add_edge(relation['from'], relation['to'], {'name': relation['type']})

    def build(self):
        graph = nx.Graph()
        self.add_edges(graph)
        return graph
