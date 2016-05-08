from src.analysis.basic.statistics import Statistics
from src.common.db.connector import DatabaseConnector


def main():
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    statistics = Statistics(db)
    statistics.print_all()


if __name__ == '__main__':
    main()
