from src.analysis.basic.statistics import Statistics
from src.analysis.graph.builder import SimpleGraph
from src.analysis.graph.centrality import CentralityMeasurer
# from src.analysis.graph.groups import GroupsFinder
from src.analysis.graph.groups import GroupsFinder
from src.common.db.connector import DatabaseConnector


def print_statistics(db):
    statistics = Statistics(db)
    statistics.print_all()


def print_centralities(graph):
    measurer = CentralityMeasurer(graph)
    measurer.print_all()


def main():
    print("Starting...")
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    print_statistics(db)

    print("Building graph...")
    graph = SimpleGraph(db, since=1939, to=1945).get()
    print("Finished building graph")
    # print_centralities(graph)
    # GroupsFinder(graph).print_groups_cpm(range(2, 13))
    GroupsFinder(graph).print_groups_louvain([0.0002, 1.0, 200.0])

    print("Finished...")


if __name__ == '__main__':
    main()
