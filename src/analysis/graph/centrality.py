import operator

import networkx as nx

from src.analysis.printer import FunctionPrinter


class CentralityMeasurer:
    def __init__(self, graph):
        self.graph = graph

    def print_all(self):
        FunctionPrinter.print_statistic(self.degree_centrality_ranking)
        FunctionPrinter.print_statistic(self.betweeness_centrality_ranking)
        FunctionPrinter.print_statistic(self.closeness_centrality_ranking)
        FunctionPrinter.print_statistic(self.eigenvector_centrality_ranking)
        FunctionPrinter.print_statistic(self.page_rank_ranking)

    def degree_centrality_ranking(self):
        res = nx.degree_centrality(self.graph)
        return self.create_ranking(res)

    def betweeness_centrality_ranking(self):
        # results = nx.betweenness_centrality(self.graph, k=200)
        results = nx.betweenness_centrality(self.graph)
        return self.create_ranking(results)

    def closeness_centrality_ranking(self):
        results = nx.closeness_centrality(self.graph)
        return self.create_ranking(results)

    def eigenvector_centrality_ranking(self):
        try:
            results = nx.eigenvector_centrality(self.graph)
        except nx.NetworkXError:
            print('Eigenvector error')
            results = {}

        return self.create_ranking(results)

    def page_rank_ranking(self):
        results = nx.pagerank(self.graph)
        return self.create_ranking(results)

    def sum_centrality(self):
        degree = nx.degree_centrality(self.graph)
        betweeness = nx.betweenness_centrality(self.graph)
        closeness = nx.closeness_centrality(self.graph)
        eigenvector = nx.eigenvector_centrality(self.graph)
        page_rank = nx.pagerank(self.graph)
        centrality = dict()
        for key in degree.keys():
            centrality[key] = degree[key] + betweeness[key] + closeness[key] + eigenvector[key] + page_rank[key]
        return centrality

    def print_sum_centrality(self):
        degree = nx.degree_centrality(self.graph)
        self.print_ranking(degree)
        betweeness = nx.betweenness_centrality(self.graph)
        self.print_ranking(betweeness)
        closeness = nx.closeness_centrality(self.graph)
        self.print_ranking(closeness)
        eigenvector = nx.eigenvector_centrality(self.graph)
        self.print_ranking(eigenvector)
        page_rank = nx.pagerank(self.graph)
        self.print_ranking(page_rank)
        centrality = dict()
        for key in degree.keys():
            centrality[key] = (degree[key] + betweeness[key] + closeness[key] + eigenvector[key] + page_rank[key]) / 5
        self.print_ranking(centrality)
        return centrality

    def print_ranking(self, results):
        ranking = self.create_ranking(results)
        print(ranking)

    @staticmethod
    def create_ranking(results):
        sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_results[0: 20]
