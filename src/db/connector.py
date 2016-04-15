from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class DatabaseConnector:
    def __init__(self, host, port, name):
        client = MongoClient(host, port)
        db = client[name]
        self.persons = db.persons
        self.ensure_indexes()

    def ensure_indexes(self):
        self.persons.ensure_index('url', unique=True)

    def save_persons(self, persons):
        try:
            self.persons.insert_many(persons)
        except DuplicateKeyError as e:
            print("Tried to insert person duplicate. Should not happen!\n" + str(e))
