from SPARQLWrapper import SPARQLWrapper, JSON

from src import get_resource
from src.common.enums import Relation


class DbpediaReader:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    @staticmethod
    def __print_query_results(title, results):
        print(title + " " + len(results['results']['bindings']))

    def __read_results_from_query_resource(self, resource_name, *args):
        query = get_resource(resource_name).format(*args)
        results = self.__exec_query(query)
        return results['results']['bindings']

    def __read_results_from_query_resource_batched(self, resource_name, *args):
        result = []
        offset = 0
        while True:
            batch = self.__read_results_from_query_resource(resource_name, *args, offset)
            if len(batch) == 0:
                break
            offset += 10000
            result.extend(batch)

        DbpediaReader.__print_query_results(resource_name, result)
        return result

    def __exec_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()

    def read_raw_persons(self):
        return self.__read_results_from_query_resource_batched('person_query.txt')

    def read_raw_roles(self):
        return self.__read_results_from_query_resource_batched('role_query.txt')

    def read_raw_relations(self):
        json = []
        for relation in Relation:
            relations = self.__read_raw_relations_for_type(relation)
            json.append(self.__create_raw_relation(relation.name, relations))
        return json

    def __read_raw_relations_for_type(self, relation):
        names = relation.get_relations_names()
        relations = []
        for name in names:
            relations.extend(self.__read_results_from_query_resource_batched('relation_query.txt', name))
        return relations

    def read_raw_redirects(self, urls):
        results = []
        for url in urls:
            result = self.__create_raw_relation(Relation.OTHER.name,
                                                self.__read_results_from_query_resource_batched(
                                                    'wiki_redirect_query.txt', url))
            results.extend(result)
        return results

    def __create_raw_relation(self, type, relations):
        return dict(type=type, relations=relations)
