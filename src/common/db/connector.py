from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError


class DatabaseConnector:
    def __init__(self, host, port, name):
        client = MongoClient(host, port)
        db = client[name]
        self.persons = db.persons
        self.relations = db.relations
        self.raw_persons = db.raw_persons
        self.raw_roles = db.raw_roles
        self.raw_relations = db.raw_relations
        self.raw_types = db.raw_types
        self.ensure_indexes()

    def ensure_indexes(self):
        self.persons.ensure_index('url', unique=True)
        self.relations.create_index([('from', ASCENDING), ('to', ASCENDING), ('type', ASCENDING)], unique=True)
        self.persons.create_index('hasRelation', sparse=True)

    def find_distinct_urls_from_raw_persons(self):
        return [elem['_id'] for elem in
                list(self.raw_persons.aggregate([{'$group': {'_id': '$body.value'}}], allowDiskUse=True))]

    def insert_person(self, person):
        try:
            self.persons.insert_one(person)
        except DuplicateKeyError as e:
            # print("Tried to insert person duplicate. Should not happen!\n" + str(e))
            pass

    def insert_relation(self, relation):
        try:
            self.relations.insert_one(relation)
        except DuplicateKeyError as e:
            # print("Tried to insert relation duplicate. Should not happen!\n" + str(e))
            pass

    def insert_raw_persons(self, json):
        try:
            self.raw_persons.insert_many(json)
        except DuplicateKeyError as e:
            print("Tried to insert raw_person duplicate. Should not happen!\n" + str(e))

    def insert_raw_roles(self, json):
        try:
            self.raw_roles.insert_many(json)
        except DuplicateKeyError as e:
            print("Tried to insert role duplicate. Should not happen!\n" + str(e))

    def insert_raw_relations(self, json):
        try:
            self.raw_relations.insert_one(json)
        except DuplicateKeyError as e:
            print("Tried to insert relation duplicate. Should not happen!\n" + str(e))

    def save_raw_types(self, json):
        try:
            self.raw_types.insert_many(json)
        except DuplicateKeyError as e:
            print("Tried to insert relation duplicate. Should not happen!\n" + str(e))

    def find_raw_persons_for(self, url):
        return self.raw_persons.find({'body.value': url})

    def find_all_raw_roles(self):
        return self.raw_roles.find()

    def find_all_raw_types(self):
        return self.raw_types.find()

    def find_all_raw_relations(self):
        return self.raw_relations.find(no_cursor_timeout=True)

    def find_raw_relations_for(self, url):
        return self.raw_relations.find({'body.value': url})

    def find_raw_types_for(self, url):
        return self.raw_types.find({'body.value': url})

    def find_persons_in_period(self, since, to):
        return self.persons.find(
            {'$or': [{'$and': [{'firstYearOfActivity': {'$gte': since}}, {'firstYearOfActivity': {'$lte': to}}]},
                     {'$and': [{'lastYearOfActivity': {'$gte': since}}, {'lastYearOfActivity': {'$lte': to}}]}]})

    def find_relations_for(self, urls):
        return self.relations.find({'$or': [
            {'to': {'$in': urls}},
            {'from': {'$in': urls}}
        ]})

    def find_all_persons(self, query={}):
        return self.persons.find(query)

    def find_all_raw_persons(self, query={}):
        return self.raw_persons.find(query)

    def count_all_persons(self, query={}):
        return self.persons.count(query)

    def find_all_relations(self, query={}):
        return self.relations.find(query)

    def count_all_relations(self, query={}):
        return self.relations.count(query)

    def find_one_person(self, query={}):
        return self.persons.find_one(query)

    def save_person(self, person):
        self.persons.save(person)

    def find_distinct_person_types(self):
        return self.persons.distinct('type')

    def update_persons(self, find_query, update_query):
        self.persons.update(find_query, update_query)

    def relation_exists(self, raw_relation):
        return self.relations.count(
            {'$and': [{'from': raw_relation['body']['value']}, {'to': raw_relation['relation']['value']}]}) > 0

    def relation_persons_exist(self, relation):
        return self.persons.count({'$or': [{'url': relation['from']}, {'url': relation['to']}]}) > 1
