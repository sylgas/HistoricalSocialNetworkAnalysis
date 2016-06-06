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

    pc = PeriodComparator(db, 1939, 1945, 1958)
    pc.save_similar_groups("../plot/similarity.txt")

    # print("Building graph...")
    # builder = SimpleGraph(db)
    # graph = builder.get()
    # builder.export('all.csv')
    print("Finished building graph")
    # print_centralities(graph)
    # GroupsFinder(graph).print_groups_cpm(range(3, 13), db=db)
    # GroupsFinder(graph).print_groups_louvain([0.0002, 1.0, 200.0])


print("Finished...")

if __name__ == '__main__':
    main()
