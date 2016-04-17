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
            person = self.__parse_person_from(raw_persons, raw_roles, raw_relations, raw_redirects)
            db.save_person(person)

    def __parse_person_from(self, raw_persons, raw_roles, raw_relations, raw_redirects):
        return dict(
            url=self._parse_url(raw_persons),
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
    def __extract_first_attribute_value(collection, *attributes):
        for element in collection:
            for attribute in attributes:
                if attribute in element:
                    return element[attribute]

    def __extract_string_value(self, value):
        expression = value.strip()
        for regex in PersonParser.RESOURCE_REGEXES:
            pattern = re.compile(regex)
            match = pattern.search(expression)
            if match:
                result = match.group('value')
                return result.replace('_', ' ').strip()

    def _parse_url(self, raw_persons):
        pass

    def __parse_name(self, raw_persons):
        pass

    def __parse_role(self, raw_roles):
        pass

    def __parse_dynasty(self, raw_persons):
        PersonParser.__extract_first_attribute_value(raw_persons, ['dynasty', 'familyName', 'surname'])

    def __parse_first_year_of_activity(self, raw_persons):
        pass

    def __parse_last_year_of_activity(self, raw_persons):
        pass

    def __parse_ideology(self, raw_persons):
        pass

    def __parse_nationality(self, raw_persons):
        pass

    def __parse_relations(self, raw_relations, raw_redirects):
        pass
