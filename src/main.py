from src.data.parser import PersonParser
from src.data.reader import DbpediaReader
from src.db.connector import DatabaseConnector


def save_raw_data(db, reader):
    print("Saving raw data...")

    json = reader.read_raw_persons()
    db.save_raw_persons(json)
    print("Raw persons saved")

    json = reader.read_raw_roles()
    db.save_raw_roles(json)
    print('Raw roles saved')

    json = reader.read_raw_relations()
    db.save_raw_relations(json)
    print('Raw relations saved')

    urls = db.find_distinct_urls()
    json = reader.read_raw_redirects(urls)
    db.update_raw_relations(json)
    print('Raw relations updated with redirects')

    print('Finished saving raw data')


def parse_data(db):
    print('Parsing data...')

    parser = PersonParser()
    parser.parse_and_save_persons(db)

    print('Finished parsing data')


def main():
    print('Starting...')
    db = DatabaseConnector('localhost', 27017, 'historical-relations')
    reader = DbpediaReader()

    save_raw_data(db, reader)
    # parse_data(db)

    print('Finished')


if __name__ == '__main__':
    main()
