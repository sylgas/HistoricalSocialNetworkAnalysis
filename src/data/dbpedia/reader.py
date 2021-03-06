from SPARQLWrapper import SPARQLWrapper, JSON

from src import get_resource
from src.common.enums import Relation


class DbpediaReader:
    def __init__(self, db):
        self.db = db
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    @staticmethod
    def __print_query_results(title, offset):
        print(title + " " + str(offset))
        pass

    def __read_results_from_query_resource(self, resource_name, *args):
        query = get_resource(resource_name).format(*args)
        results = self.__exec_query(query)
        return results['results']['bindings']

    def __save_results_from_query_resource_batched(self, save_method, resource_name, *args):
        offset = 0
        while True:
            batch = self.__read_results_from_query_resource(resource_name, *args, offset)
            save_method(batch)
            DbpediaReader.__print_query_results(resource_name, offset)

            if len(batch) < 10000:
                break
            offset += 10000

    def __exec_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()

    def save_raw_persons(self):
        return self.__save_results_from_query_resource_batched(self.db.insert_raw_persons, 'person_query.txt')

    def save_raw_roles(self):
        return self.__save_results_from_query_resource_batched(self.db.insert_raw_roles, 'role_query.txt')

    def save_raw_relations(self):
        for relation in Relation:
            self.__save_raw_relations_for_type(relation)

    def __save_raw_relations_for_type(self, relation):
        names = relation.get_relations_names()
        for name in names:
            self.__save_results_from_query_resource_batched(
                lambda data: self.db.insert_raw_relations(DbpediaReader.__create_relation_dict(relation.name, data)),
                'relation_query.txt', name)

    def save_raw_redirects(self):
        self.__save_results_from_query_resource_batched(
            lambda data: self.db.insert_raw_relations(DbpediaReader.__create_relation_dict(Relation.OTHER.name, data)),
            'wiki_redirect_query.txt')

    def save_raw_types(self):
        self.__save_results_from_query_resource_batched(self.db.save_raw_types, 'type_query.txt')

    @staticmethod
    def __create_relation_dict(name, relations):
        # print(relations)
        return dict(type=name, relations=relations)
