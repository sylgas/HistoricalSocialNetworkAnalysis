class PersonCleaner:
    def __init__(self, db):
        self.db = db

    def clean(self):
        raise NotImplementedError("Should have implemented this")


class DatePersonCleaner(PersonCleaner):
    def remove_where_no_dates(self):
        self.db.persons.remove({'firstYearOfActivity': '', 'lastYearOfActivity': ''})

    def clean(self):
        self.remove_where_no_dates()
