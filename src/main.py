from src.data.parser import PersonParser
from src.data.reader import DbpediaReader
from src.db.connector import DatabaseConnector


def main():
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    reader = DbpediaReader()

    json = reader.read_raw_persons()
    db.save_raw_persons(json)

    parser = PersonParser()
    persons = parser.parse_persons_from(db.raw_persons)


if __name__ == '__main__':
    main()
