from src.analysis.basic.statistics import Statistics
from src.analysis.graph.centrality import CentralityMeasurer
# from src.analysis.graph.groups import GroupsFinder
from src.analysis.period.period import PeriodComparator
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
    PeriodComparator(db, 1939, 1945, 1960)

    # print("Building graph...")
    # graph = SimpleGraph(db, since=1939, to=1945).get()
    # print("Finished building graph")
    #
    # # print_centralities(graph)
    # finder = GroupsFinder(graph)
    # print(finder.find_groups_cpm(5))
    # print("Finished...")
    # GroupsFinder(graph).print_groups_cpm(range(2, 13))

    print("Finished...")


if __name__ == '__main__':
    main()
