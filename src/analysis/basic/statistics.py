from src.common.enums import Relation, Type


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

    def count_persons_types(self):
        type_list = []
        for type_group in Type().get_types():
            for type in type_group:
                type_list.append((type, self.count_persons_by_type(type)))
        return sorted(type_list, key=lambda x: x[1], reverse=True)

    def count_persons_by_ages(self):
        data = [0] * 13
        cursor = self.db.find_all_persons()
        for person in cursor:
            avg_year = (person['firstYearOfActivity'] + person['lastYearOfActivity']) / 2
            if avg_year <= 900:
                data[0] += 1
            elif avg_year > 2000:
                data[12] += 1
            else:
                for i in range(10, 21):
                    if avg_year < i * 100:
                        data[i - 9] += 1
                        break
        return [
            ('< X', data[0]), ('X', data[1]), ('XI', data[2]), ('XII', data[3]), ('XIII', data[4]), ('XIV', data[5]),
            ('XV', data[6]), ('XVI', data[7]), ('XVII', data[8]), ('XVIII', data[9]), ('XIX', data[10]),
            ('XX', data[11]), ('XXI', data[12])
        ]
