from pymongo import MongoClient


class DatabaseConnector:
    def __init__(self, host, port, name):
        client = MongoClient(host, port)
        db = client[name]
        self.persons = db.persons
        self.ensure_indexes()

    def ensure_indexes(self):
        self.persons.ensure_index('id', unique=True)
