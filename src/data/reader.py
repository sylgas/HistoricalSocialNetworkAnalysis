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

    def read(self):
        query = get_resource('person_query.txt')
        print(query)
        results = self.__exec_query(query)
        DbpediaReader.__print_query_results(results)

    def __exec_query(self, query):
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        return self.sparql.query().convert()
