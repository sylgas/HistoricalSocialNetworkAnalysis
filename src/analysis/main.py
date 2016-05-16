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
    # print_statistics(db)

    print("Building graph...")
    graph = SimpleGraph(db, 1939, 1945).get()
    print("Finished building graph")

    # print_centralities(graph)
    finder = GroupsFinder(graph)
    finder.find_groups_cpm(5)
    print("Finished...")


if __name__ == '__main__':
    main()
