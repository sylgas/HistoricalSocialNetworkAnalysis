import operator

import networkx as nx

from src.analysis.graph.builder import GraphBuilder
from src.analysis.printer import FunctionPrinter


class CentralityMeasurer:
    def __init__(self, db, since, to):
        self.db = db
        self.graph = GraphBuilder(db, since, to).build()

    def print_all(self):
        FunctionPrinter.print_statistic(self.degree_centrality_ranking)
        FunctionPrinter.print_statistic(self.betweeness_centrality_ranking())
        FunctionPrinter.print_statistic(self.closeness_centrality_ranking())
        FunctionPrinter.print_statistic(self.eigenvector_centrality_ranking())
        FunctionPrinter.print_statistic(self.page_rank_ranking())

    def degree_centrality_ranking(self):
        res = nx.degree_centrality(self.graph)
        return self.__create_ranking(res)

    def betweeness_centrality_ranking(self):
        results = nx.betweenness_centrality(self.graph)
        return self.__create_ranking(results)

    def closeness_centrality_ranking(self):
        results = nx.closeness_centrality(self.graph)
        return self.__create_ranking(results)

    def eigenvector_centrality_ranking(self):
        results = nx.eigenvector_centrality(self.graph)
        return self.__create_ranking(results)

    def page_rank_ranking(self):
        results = nx.pagerank(self.graph)
        return self.__create_ranking(results)

    @staticmethod
    def __create_ranking(results):
        sorted_results = sorted(results.items(), key=operator.itemgetter(1))
        return sorted_results[0, 10]
