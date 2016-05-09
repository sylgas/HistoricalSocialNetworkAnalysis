class Cleaner:
    def __init__(self, db):
        self.db = db

    def clean(self):
        raise NotImplementedError("Should have implemented this")


class DatePersonCleaner(Cleaner):
    def __remove_where_no_dates(self):
        self.db.persons.remove({'firstYearOfActivity': '', 'lastYearOfActivity': ''})

    def __fill_empty_years_fields(self):
        persons = self.db.find_all_persons({'firstYearOfActivity': ''})
        for person in persons:
            person['firstYearOfActivity'] = person['lastYearOfActivity'] - 40
            self.db.save_person(person)

        persons = self.db.find_all_persons({'lastYearOfActivity': ''})
        for person in persons:
            person['lastYearOfActivity'] = person['firstYearOfActivity'] + 20
            self.db.save_person(person)

    def clean(self):
        self.__remove_where_no_dates()
        self.__fill_empty_years_fields()


class RelationCleaner(Cleaner):
    def clean(self):
        cursor = self.db.find_all_relations()
        for relation in cursor:
            if not self.db.relation_persons_exist(relation):
                self.db.relations.remove({'_id': relation['_id']})
