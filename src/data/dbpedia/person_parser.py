from src.data.dbpedia.parser import Parser


class PersonParser(Parser):
    def parse_and_save_persons(self, db):
        cursor = db.find_all_raw_persons()
        for raw_person in cursor:
            person = self.__parse_person_from(raw_person)
            db.save_person(person)

    def __parse_person_from(self, raw_person):
        return dict(
            url=self.__parse_url(raw_person),
            name=self.__parse_name(raw_person),
            dynasty=self.__parse_dynasty(raw_person),
            firstYearOfActivity=self.__parse_first_year_of_activity(raw_person),
            lastYearOfActivity=self.__parse_last_year_of_activity(raw_person),
            ideology=self.__parse_ideology(raw_person),
            nationality=self.__parse_nationality(raw_person),
        )

    @staticmethod
    def __parse_url(raw_person):
        return raw_person['body']['value']

    def __parse_name(self, raw_persons):
        return self.__extract_first_attribute_string_value(raw_persons, 'birthName', 'name', 'pseudonym',
                                                           'givenName', 'nick')

    def __parse_dynasty(self, raw_persons):
        return self.__extract_first_attribute_string_value(raw_persons, 'dynasty', 'familyName', 'surname')

    def __parse_first_year_of_activity(self, raw_persons):
        return self.__extract_date_value(raw_persons, 'activeYearsStartYear', 'activeYearsStartDate',
                                         'birthYear', 'birthDate')

    def __parse_last_year_of_activity(self, raw_persons):
        return self.__extract_date_value(raw_persons, 'activeYearsEndYear', 'activeYearsEndDate',
                                         'deathYear', 'deathDate')

    def __parse_ideology(self, raw_persons):
        return self.__extract_first_attribute_string_value(raw_persons, 'ideology')

    def __parse_nationality(self, raw_persons):
        return self.__extract_first_attribute_string_value(raw_persons, 'nationality', 'citizenship', 'country',
                                                           'stateOfOrigin')
