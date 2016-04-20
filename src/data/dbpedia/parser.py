import re


class Parser(object):
    RESOURCE_REGEXES = [r'http://dbpedia\.org/resource/(?P<value>[^\(\)]*)(\(.*\))*',
                        r'"“*(?P<value>.*[^“”"])”*"@.+',
                        r'(?P<value>.*)']

    @staticmethod
    def extract_first_attribute_string_value(collection, *attributes):
        return Parser.__extract_string_value(
            Parser.extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def extract_first_attribute_value(element, *attributes):
        for attribute in attributes:
            if attribute in element:
                return element[attribute]['value']
        return ''

    @staticmethod
    def __extract_string_value(value):
        expression = value.strip()
        for regex in Parser.RESOURCE_REGEXES:
            pattern = re.compile(regex)
            match = pattern.search(expression)
            if match:
                result = match.group('value')
                return result.replace('_', ' ').strip()

    def __init__(self, db):
        self.db = db

    def parse(self):
        raise NotImplementedError("Should have implemented this")


class PersonParser(Parser):
    def parse(self):
        cursor = self.db.find_all_raw_persons()
        for raw_person in cursor:
            person = self.__parse_person_from(raw_person)
            self.db.insert_person(person)

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

    @staticmethod
    def __parse_date(date_string):
        if "\"" in date_string:
            return date_string[1:5]
        else:
            return date_string[:4]

    @staticmethod
    def __extract_date_value(collection, *attributes):
        return PersonParser.__parse_date(Parser.extract_first_attribute_value(collection, *attributes))

    def __parse_name(self, raw_persons):
        return self.extract_first_attribute_string_value(raw_persons, 'birthName', 'name', 'pseudonym',
                                                         'givenName', 'nick')

    def __parse_dynasty(self, raw_persons):
        return self.extract_first_attribute_string_value(raw_persons, 'dynasty', 'familyName', 'surname')

    def __parse_first_year_of_activity(self, raw_persons):
        return self.__extract_date_value(raw_persons, 'activeYearsStartYear', 'activeYearsStartDate',
                                         'birthYear', 'birthDate')

    def __parse_last_year_of_activity(self, raw_persons):
        return self.__extract_date_value(raw_persons, 'activeYearsEndYear', 'activeYearsEndDate',
                                         'deathYear', 'deathDate')

    def __parse_ideology(self, raw_persons):
        return self.extract_first_attribute_string_value(raw_persons, 'ideology')

    def __parse_nationality(self, raw_person):
        return self.extract_first_attribute_string_value(raw_person, 'nationality', 'citizenship', 'country',
                                                         'stateOfOrigin')


class RoleParser(Parser):
    def parse(self):
        cursor = self.db.find_all_raw_roles()
        for raw_role in cursor:
            person = self.db.find_one_person({'url': raw_role['body']['value']})
            if person is None:
                continue
            self.__assign_role_if_none(person, raw_role)

    def __assign_role_if_none(self, person, raw_role):
        if 'role' not in person:
            role = self.extract_first_attribute_string_value(raw_role, 'profession', 'occupation', 'discipline',
                                                             'speciality')
            person['role'] = role
            self.db.save_person(person)


class RelationParser(Parser):
    def parse(self):
        cursor = self.db.find_raw_relations()
        for raw_relation_group in cursor:
            for raw_relation in raw_relation_group['relations']:
                relation = self.__parse_relation_from(raw_relation_group['type'], raw_relation)
                self.db.insert_relation(relation)

    @staticmethod
    def __parse_relation_from(relation_type, raw_relation):
        return dict(
            url1=raw_relation['body']['value'],
            url2=raw_relation['relation']['value'],
            type=relation_type
        )
