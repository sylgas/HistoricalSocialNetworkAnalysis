from src.common.enums import Relation


class Statistics:
    def __init__(self, db):
        self.db = db

    def print_all(self):
        self.print_statistic(self.count_persons)
        self.print_statistic(self.count_persons_with_name)
        self.print_statistic(self.count_persons_with_dynasty)
        self.print_statistic(self.count_persons_with_ideology)
        self.print_statistic(self.count_persons_with_nationality)
        self.print_statistic(self.count_persons_with_role)
        self.print_count_persons_by_type_statistic()
        self.print_statistic(self.count_persons_with_relations)
        self.print_statistic(self.count_relations)
        self.print_count_relations_by_type_statistic()
        self.print_statistic(self.count_incorrect_persons)

    def print_count_persons_by_type_statistic(self):
        person_types = self.db.find_distinct_person_types()
        for person_type in person_types:
            self.print_statistic(self.count_persons_by_type, person_type)

    def print_count_relations_by_type_statistic(self):
        for relation_type in Relation:
            self.print_statistic(self.count_relations_by_type, relation_type.name)

    @staticmethod
    def print_statistic(fun, *attributes):
        name = fun.__name__
        for attribute in attributes:
            name += ' ' + str(attribute)
        result = fun(*attributes)
        print(name.upper() + ':' + str(result))

    def count_persons(self):
        return self.db.count_all_persons()

    def count_persons_by_type(self, type):
        return self.db.count_all_persons({'type': type})

    def count_relations(self):
        return self.db.count_all_relations()

    def count_relations_by_type(self, relation_type):
        return self.db.count_all_relations({'type': relation_type})

    def count_persons_with_name(self):
        return self.db.count_all_persons({'name': {'$ne': ''}})

    def count_persons_with_dynasty(self):
        return self.db.count_all_persons({'dynasty': {'$ne': ''}})

    def count_persons_with_ideology(self):
        return self.db.count_all_persons({'ideology': {'$ne': ''}})

    def count_persons_with_nationality(self):
        return self.db.count_all_persons({'nationality': {'$ne': ''}})

    def count_persons_with_role(self):
        return self.db.count_all_persons({'role': {'$ne': ''}})

    def count_persons_with_relations(self):
        return self.db.count_all_persons({'hasRelation': True})

    def count_incorrect_persons(self):
        res = self.db.count_all_persons({'$or': [
            {'url': {'$exists': False}},
            {'url': ''},
            {'type': {'$exists': False}},
            {'type': ''},
            {'firstYearOfActivity': {'$exists': False}},
            {'firstYearOfActivity': ''},
            {'lastYearOfActivity': {'$exists': False}},
            {'lastYearOfActivity': ''}
        ]})
        if res > 0:
            print('Data is incorrect. Run CLEANER!')
        return res
