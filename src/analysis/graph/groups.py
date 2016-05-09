import community


class GroupsFinder:
    def __init__(self, graph):
        self.graph = graph

    def find_groups(self):
        partition = community.best_partition(self.graph)
        print(partition)
