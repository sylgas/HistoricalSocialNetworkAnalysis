from SPARQLWrapper import SPARQLWrapper, JSON

from src import get_resource


class DbpediaReader:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    @staticmethod
    def __print_query_results(results):
        print(results)
        # for result in results["results"]["bindings"]:
        #     print(result["label"]["value"])

    def __read_results(self, resource_name):
        query = get_resource(resource_name)
        print(query)

        results = self.__exec_query(query)
        DbpediaReader.__print_query_results(results)
        return results['results']['bindings']

    def __exec_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()

    def read_raw_persons(self):
        return self.__read_results('person_query.txt')

    def read_raw_roles(self):
        return self.__read_results('role_query.txt')

    def read_raw_relations(self):
        return self.__read_results('relation_query.txt')

    def read_raw_redirects(self):
        return self.__read_results('wiki_redirect_query.txt')
