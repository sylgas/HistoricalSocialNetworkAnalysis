import re


class PersonParser:
    RESOURCE_REGEXES = [r'http://dbpedia\.org/resource/(?P<value>[^\(\)]*)(\(.*\))*',
                        r'"“*(?P<value>.*[^“”"])”*"@.+',
                        r'(?P<value>.*)']

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
    def __extract_first_attribute_string_value(collection, *attributes):
        return PersonParser.__extract_string_value(
            PersonParser.__extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def __extract_date_value(collection, *attributes):
        return PersonParser.__parse_date(PersonParser.__extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def __extract_first_attribute_value(element, *attributes):
        for attribute in attributes:
            if attribute in element:
                return element[attribute]['value']
        return ''

    @staticmethod
    def __extract_string_value(value):
        expression = value.strip()
        for regex in PersonParser.RESOURCE_REGEXES:
            pattern = re.compile(regex)
            match = pattern.search(expression)
            if match:
                result = match.group('value')
                return result.replace('_', ' ').strip()

    @staticmethod
    def __parse_date(date_string):
        if "\"" in date_string:
            return date_string[1:5]
        else:
            return date_string[:4]

    @staticmethod
    def __parse_name(raw_persons):
        return PersonParser.__extract_first_attribute_string_value(raw_persons, 'birthName', 'name', 'pseudonym',
                                                                   'givenName', 'nick')

    @staticmethod
    def __parse_dynasty(raw_persons):
        return PersonParser.__extract_first_attribute_string_value(raw_persons, 'dynasty', 'familyName', 'surname')

    @staticmethod
    def __parse_first_year_of_activity(raw_persons):
        return PersonParser.__parse_date(
            PersonParser.__extract_first_attribute_value(raw_persons, 'activeYearsStartYear', 'activeYearsStartDate',
                                                         'birthYear', 'birthDate'))

    @staticmethod
    def __parse_last_year_of_activity(raw_persons):
        return PersonParser.__parse_date(
            PersonParser.__extract_first_attribute_value(raw_persons, 'activeYearsEndYear', 'activeYearsEndDate',
                                                         'deathYear', 'deathDate'))

    @staticmethod
    def __parse_ideology(raw_persons):
        return PersonParser.__extract_first_attribute_string_value(raw_persons, 'ideology')

    @staticmethod
    def __parse_nationality(raw_persons):
        return PersonParser.__extract_first_attribute_string_value(raw_persons, 'nationality', 'citizenship', 'country',
                                                                   'stateOfOrigin')

    @staticmethod
    def __parse_url(raw_person):
        return raw_person['body']['value']
