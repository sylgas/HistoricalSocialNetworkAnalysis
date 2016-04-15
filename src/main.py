from src.data.parser import PersonParser
from src.data.reader import DbpediaReader
from src.db.connector import DatabaseConnector


def save_raw_data(db, reader):
    json = reader.read_raw_persons()
    db.save_raw_persons(json)

    json = reader.read_raw_roles()
    db.save_raw_roles(json)

    json = reader.read_raw_relations()
    db.save_raw_relations(json)


def main():
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    reader = DbpediaReader()

    save_raw_data(db, reader)

    parser = PersonParser()
    persons = parser.parse_persons(db)


if __name__ == '__main__':
    main()
