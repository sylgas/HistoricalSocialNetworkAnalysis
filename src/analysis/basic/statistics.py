class Statistics:
    def __init__(self, db):
        self.db = db

    def print_all(self):
        self.print_statistic(self.count_all_persons)
        self.print_statistic(self.count_all_relations)

    @staticmethod
    def print_statistic(fun):
        name = fun.__name__
        result = fun()
        print(name.upper(), str(result))

    def count_all_persons(self):
        return self.db.count_all_persons()

    def count_all_relations(self):
        return self.db.count_all_relations()
