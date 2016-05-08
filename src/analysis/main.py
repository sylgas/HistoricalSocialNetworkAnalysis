from src.analysis.basic.statistics import Statistics
from src.analysis.graph.centrality import CentralityMeasurer
from src.common.db.connector import DatabaseConnector


def print_statistics(db):
    statistics = Statistics(db)
    statistics.print_all()


def print_centralities(db):
    measurer = CentralityMeasurer(db)
    measurer.print_all()


def main():
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    # print_statistics(db)
    print_centralities(db)


if __name__ == '__main__':
    main()
