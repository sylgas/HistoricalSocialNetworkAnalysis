from src.data.reader import DbpediaReader
from src.db.connector import DatabaseConnector


def main():
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    reader = DbpediaReader()
    # reader.read_persons()


if __name__ == '__main__':
    main()
