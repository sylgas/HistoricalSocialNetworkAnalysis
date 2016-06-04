from src.analysis.graph.builder import AnalyticalGraph
from src.analysis.graph.groups import GroupsFinder, GroupComparator


class PeriodComparator:
    def __init__(self, db, start_date, section, end_date):
        old_graph = AnalyticalGraph(db, since=start_date, to=section)
        new_graph = AnalyticalGraph(db, since=section, to=end_date)
        old_groups = self.__find_groups(old_graph)
        new_groups = self.__find_groups(new_graph)
        self.similar_groups = GroupComparator(old_graph, old_groups, new_graph, new_groups).get_similar_group()
        print([z[2] for z in self.similar_groups])

    @staticmethod
    def __find_groups(graph):
        return GroupsFinder(graph.get()).find_groups_cpm(3)