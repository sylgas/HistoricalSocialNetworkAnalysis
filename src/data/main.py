from src.common.db.connector import DatabaseConnector
from src.data.dbpedia.cleaner import DatePersonCleaner
from src.data.dbpedia.parser import RoleParser, PersonParser
from src.data.dbpedia.reader import DbpediaReader


def save_raw_data(db):
    print("Saving raw dbpedia data...")

    reader = DbpediaReader(db)

    # reader.save_raw_persons()
    # print("Raw persons saved")
    #
    # reader.save_raw_roles()
    # print('Raw roles saved')

    reader.save_raw_relations()
    print('Raw relations saved')

    reader.save_raw_redirects()
    print('Raw relations updated with redirects')

    print('Finished saving raw dbpedia data')


def parse_data(db):
    print('Parsing data...')

    parser = PersonParser(db)
    parser.parse()

    parser = RoleParser(db)
    parser.parse()

    print('Finished parsing data')


def clean_data(db):
    print('Cleaning data...')

    cleaner = DatePersonCleaner(db)
    cleaner.clean()

    print('Finished cleaning data')


def main():
    print('Starting...')
    db = DatabaseConnector('localhost', 27017, 'historical-relations')

    # save_raw_data(db)
    # parse_data(db)
    # clean_data(db)

    print('Finished')


if __name__ == '__main__':
    main()
