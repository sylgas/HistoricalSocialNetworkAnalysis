from src.analysis.basic.statistics import GraphStatistics
from src.analysis.graph.builder import AnalyticalGraph
from src.analysis.graph.groups import GroupsFinder, GroupComparator
from src.visualisation.Plotter import Plotter


class PeriodComparator:
    def __init__(self, db, start_date, section, end_date):
        self.dates = (start_date, section, end_date)
        self.old_graph = AnalyticalGraph(db, since=start_date, to=section)
        self.new_graph = AnalyticalGraph(db, since=section, to=end_date)
        old_groups = self.__find_groups(self.old_graph)
        new_groups = self.__find_groups(self.new_graph)
        self.similar_groups = GroupComparator(self.old_graph, old_groups, self.new_graph, new_groups).get_similar_group()

    @staticmethod
    def __find_groups(graph):
        return GroupsFinder(graph.get()).find_groups_cpm(4)

    def save_similar_groups(self, filename):
        with open(filename, 'w', encoding='UTF-8') as file:
            for comparation in self.similar_groups:
                file.write("Similarity ratio: {0}\n".format(comparation[2]))
                # file.write("Group in {0} - {1}\n".format(self.dates[0], self.dates[1]))
                # for person in comparation[0].get_nodes():
                #     file.write(person)
                #     file.write("\n")
                # file.write("Group in {0} - {1}\n".format(self.dates[1], self.dates[2]))
                # for person in comparation[1].get_nodes():
                #     file.write(person)
                #     file.write("\n")
                # file.write("\n")
                file.write("Profile 1.\n")
                file.write("Count: {0}\n".format(comparation[0].get()['count']))
                file.write("Top person: {0}\n".format(comparation[0].get()['top_person']['url']))
                file.write("Type: {0}\n".format(comparation[0].get()['type']))
                file.write("Nationality: {0}\n".format(comparation[0].get()['nationality']))
                file.write("Degree centrality: {0}\n".format(comparation[0].get()['degree_centrality']))
                file.write("Betweeness centrality: {0}\n".format(comparation[0].get()['betweeness_centrality']))
                file.write("Closeness centrality: {0}\n".format(comparation[0].get()['closeness_centrality']))
                file.write("Eigenvector centrality: {0}\n".format(comparation[0].get()['eigenvector_centrality']))
                file.write("Page rank: {0}\n\n".format(comparation[0].get()['page_rank']))

                file.write("Profile 2.\n")
                file.write("Count: {0}\n".format(comparation[1].get()['count']))
                file.write("Top person: {0}\n".format(comparation[1].get()['top_person']['url']))
                file.write("Type: {0}\n".format(comparation[1].get()['type']))
                file.write("Nationality: {0}\n".format(comparation[1].get()['nationality']))
                file.write("Degree centrality: {0}\n".format(comparation[1].get()['degree_centrality']))
                file.write("Betweeness centrality: {0}\n".format(comparation[1].get()['betweeness_centrality']))
                file.write("Closeness centrality: {0}\n".format(comparation[1].get()['closeness_centrality']))
                file.write("Eigenvector centrality: {0}\n".format(comparation[1].get()['eigenvector_centrality']))
                file.write("Page rank: {0}\n\n".format(comparation[1].get()['page_rank']))

                file.write("Profiles differences\n")
                file.write("Count: {0}\n".format(comparation[3]['count']))
                file.write("Top person: {0} -> {1}\n".format(comparation[3]['top_person'][0]['url'], comparation[3]['top_person'][1]['url']))
                file.write("Type: {0} -> {1}\n".format(comparation[3]['type'][0], comparation[3]['type'][1]))
                file.write("Nationality: {0} -> {1}\n".format(comparation[3]['nationality'][0], comparation[3]['nationality'][1]))
                file.write("Degree centrality: {0}\n".format(comparation[3]['degree_centrality']))
                file.write("Betweeness centrality: {0}\n".format(comparation[3]['betweeness_centrality']))
                file.write("Closeness centrality: {0}\n".format(comparation[3]['closeness_centrality']))
                file.write("Eigenvector centrality: {0}\n".format(comparation[3]['eigenvector_centrality']))
                file.write("Page rank: {0}\n".format(comparation[3]['page_rank']))
                file.write("************************************************\n\n")

    def save_basic_stat(self):
        plotter = Plotter()
        ogs = GraphStatistics(self.old_graph)
        print("OG count: " + str(ogs.count()))
        plotter.bar_plot('1800 - 1830 Relations', 'Type', 'Count', ogs.count_relation_types())
        plotter.bar_plot('1800 - 1830 Types', 'Type', 'Count', ogs.count_persons_types())

        ngs = GraphStatistics(self.new_graph)
        print("NG count: " + str(ngs.count()))
        plotter.bar_plot('1830 - 1860 Relations', 'Type', 'Count', list(ngs.count_relation_types()))
        plotter.bar_plot('1830 - 1860 Types', 'Type', 'Count', list(ngs.count_persons_types()))




