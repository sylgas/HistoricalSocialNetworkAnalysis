from src.analysis.basic.statistics import Statistics
from src.analysis.graph.centrality import CentralityMeasurer
from src.common.db.connector import DatabaseConnector
from src.common.enums import Relation
from src.visualisation.Plotter import Plotter


def draw_relation_plot(plotter, statistics):
    data = [(Relation.POLITICS.name, statistics.count_relations_by_type(Relation.POLITICS.name)),
            (Relation.SCHOOLING.name, statistics.count_relations_by_type(Relation.SCHOOLING.name)),
            (Relation.COLLABORATION.name, statistics.count_relations_by_type(Relation.COLLABORATION.name)),
            (Relation.PERSONAL.name, statistics.count_relations_by_type(Relation.PERSONAL.name)),
            (Relation.OTHER.name, statistics.count_relations_by_type(Relation.OTHER.name))
            ]
    plotter.bar_plot('Relations', 'Type', 'Count', data)


def draw_type_plot(plotter, statistics):
    data = statistics.count_persons_types()
    plotter.bar_plot('Types', 'Types', 'Count', data[:15])


def draw_person_by_age_plot(plotter, statistics):
    data = statistics.count_persons_by_ages()
    plotter.bar_plot('Ages', 'Age', 'Count', data)


def draw_all_plots(statistics):
    plotter = Plotter()
    draw_relation_plot(plotter, statistics)
    draw_type_plot(plotter, statistics)
    draw_person_by_age_plot(plotter, statistics)


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
