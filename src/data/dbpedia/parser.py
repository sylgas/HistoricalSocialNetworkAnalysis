import re


class PersonParser:
    RESOURCE_REGEXES = [r'http://dbpedia\.org/resource/(?P<value>[^\(\)]*)(\(.*\))*',
                        r'"“*(?P<value>.*[^“”"])”*"@.+',
                        r'(?P<value>.*)']

    def parse_and_save_persons(self, db):
        urls = db.find_distinct_urls()
        for url in urls:
            raw_persons = db.find_raw_persons_for(url)
            raw_roles = db.find_raw_roles_for(url)
            raw_relations = db.find_raw_relations_for(url)
            raw_redirects = db.find_raw_redirects_for(url)
            person = self.__parse_person_from(url, raw_persons, raw_roles, raw_relations, raw_redirects)
            db.save_person(person)

    def __parse_person_from(self, url, raw_persons, raw_roles, raw_relations, raw_redirects):
        return dict(
            url=url,
            name=self.__parse_name(raw_persons),
            role=self.__parse_role(raw_roles),
            dynasty=self.__parse_dynasty(raw_persons),
            firstYearOfActivity=self.__parse_first_year_of_activity(raw_persons),
            lastYearOfActivity=self.__parse_last_year_of_activity(raw_persons),
            ideology=self.__parse_ideology(raw_persons),
            nationality=self.__parse_nationality(raw_persons),
            relations=self.__parse_relations(raw_relations, raw_redirects)
        )

    @staticmethod
    def __extract_first_attribute_string_value(collection, *attributes):
        return PersonParser.__extract_string_value(
            PersonParser.__extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def __extract_date_value(collection, *attributes):
        return PersonParser.__parse_date(PersonParser.__extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def __extract_first_attribute_value(collection, *attributes):
        for element in collection:
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

    # todo:
    def __parse_role(self, raw_roles):
        pass

    def __parse_relations(self, raw_relations, raw_redirects):
        pass
