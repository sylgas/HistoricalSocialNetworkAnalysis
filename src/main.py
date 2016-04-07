from src.data.reader import DbpediaReader


def main():
    # db = DatabaseConnector('localhost', 27017, 'historical-relations')
    reader = DbpediaReader()
    reader.read()


if __name__ == '__main__':
    main()
