from SPARQLWrapper import SPARQLWrapper, JSON

from src import get_resource
from src.common.enums import Relation


class DbpediaReader:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    @staticmethod
    def __print_query_results(results):
        print(len(results['results']['bindings']))
        # for result in results["results"]["bindings"]:
        #     print(result["label"]["value"])

    # noinspection PyDefaultArgument
    def __read_results_from_query_resource(self, resource_name, args=[]):
        query = get_resource(resource_name.format(args))
        print(query)

        results = self.__exec_query(query)
        DbpediaReader.__print_query_results(results)
        return results['results']['bindings']

    def __exec_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()

    def read_raw_persons(self):
        return self.__read_results_from_query_resource('person_query.txt')

    def read_raw_roles(self):
        return self.__read_results_from_query_resource('role_query.txt')

    def read_raw_relations(self):
        json = []
        for relation in Relation:
            self.__create_raw_relation(relation.name, self.__read_raw_relations_for_type(relation))
        return json

    def __read_raw_relations_for_type(self, relation):
        names = relation.get_relations_names()
        relations = []
        for name in names:
            relations.extend(self.__read_results_from_query_resource('relation_query.txt', name))
        return relations

    def read_raw_redirects(self):
        return self.__create_raw_relation(Relation.OTHER.name,
                                          self.__read_results_from_query_resource('wiki_redirect_query.txt'))

    def __create_raw_relation(self, type, relations):
        return dict(type=type,
                    relations=relations)
