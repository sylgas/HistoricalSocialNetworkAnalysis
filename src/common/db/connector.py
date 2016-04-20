from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class DatabaseConnector:
    def __init__(self, host, port, name):
        client = MongoClient(host, port)
        db = client[name]
        self.persons = db.persons
        self.raw_persons = db.raw_persons
        self.raw_roles = db.raw_roles
        self.raw_relations = db.raw_relations
        self.ensure_indexes()

    def ensure_indexes(self):
        self.persons.ensure_index('url', unique=True)

    def find_distinct_urls(self):
        return [elem['_id'] for elem in
                list(self.raw_persons.aggregate([{'$group': {'_id': '$body.value'}}], allowDiskUse=True))]

    def insert_person(self, person):
        try:
            self.persons.insert_one(person)
        except DuplicateKeyError as e:
            # print("Tried to insert person duplicate. Should not happen!\n" + str(e))
            pass

    def save_raw_persons(self, json):
        try:
            self.raw_persons.insert_many(json)
        except DuplicateKeyError as e:
            print("Tried to insert raw_person duplicate. Should not happen!\n" + str(e))

    def save_raw_roles(self, json):
        try:
            self.raw_roles.insert_many(json)
        except DuplicateKeyError as e:
            print("Tried to insert role duplicate. Should not happen!\n" + str(e))

    def save_raw_relations(self, json):
        try:
            self.raw_relations.insert_one(json)
        except DuplicateKeyError as e:
            print("Tried to insert relation duplicate. Should not happen!\n" + str(e))

    def find_raw_persons_for(self, url):
        return self.raw_persons.find({'body.value': url})

    def find_all_raw_roles(self):
        return self.raw_roles.find()

    def find_raw_relations_for(self, url):
        return self.raw_relations.find({'body.value': url})

    def find_persons_in_period(self, since, to):
        return self.persons.find(
            {'$or': [{'$and': [{'firstYearOfActivity': {'$gte': since}}, {'firstYearOfActivity': {'$lte': to}}]},
                     {'$and': [{'lastYearOfActivity': {'$gte': since}}, {'lastYearOfActivity': {'$lte': to}}]}]})

    def find_all_persons(self, query={}):
        return self.persons.find(query)

    def count_all_persons(self, query={}):
        return self.persons.count(query)

    def find_one_person(self, query={}):
        return self.persons.find_one(query)

    def save_person(self, person):
        self.persons.save(person)
