import datetime
import re

from src.common.enums import Relation
from src.common.helper import TypeHelper


class Parser(object):
    RESOURCE_REGEXES = [r'http://dbpedia\.org/resource/(?P<value>[^\(\)]*)(\(.*\))*',
                        r'"“*(?P<value>.*[^“”"])”*"@.+',
                        r'(?P<value>.*)']

    @staticmethod
    def regex_match(regex, expression):
        pattern = re.compile(regex, re.IGNORECASE)
        return pattern.search(expression)

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
            match = Parser.regex_match(regex, expression)
            if match:
                result = match.group('value')
                return result.replace('_', ' ').strip()

    def __init__(self, db):
        self.db = db

    def parse(self):
        raise NotImplementedError("Should have implemented this")


class PersonParser(Parser):
    YEAR_REGEXES = [r'.*(?P<year>[0-9]{4}).*', r'(?P<year>[0-9]+)']
    LIVING_REGEXES = [r'ALIVE', r'not dead', r'Living']

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
        for regex in PersonParser.YEAR_REGEXES:
            match = Parser.regex_match(regex, date_string)
            if match:
                return int(match.group('year'))

        for regex in PersonParser.LIVING_REGEXES:
            if Parser.regex_match(regex, date_string):
                return int(datetime.date.today().year)

        raise ValueError

    @staticmethod
    def __extract_date_value(element, *attributes):
        for attribute in attributes:
            if attribute in element:
                try:
                    return PersonParser.__parse_date(element[attribute]['value'])
                except ValueError:
                    continue
        return ''

    def __parse_name(self, raw_persons):
        return self.extract_first_attribute_string_value(raw_persons, 'birthName', 'name', 'pseudonym',
                                                         'givenName', 'nick')

    def __parse_dynasty(self, raw_persons):
        return self.extract_first_attribute_string_value(raw_persons, 'dynasty', 'house', 'familyName', 'surname')

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
                                                             'title1', 'office1', 'title2', 'office2', 'speciality')
            person['role'] = role
            self.db.save_person(person)


class RelationParser(Parser):
    def parse(self):
        cursor = self.db.find_all_raw_relations()
        for raw_relation_group in cursor:
            if raw_relation_group['type'] == Relation.OTHER.name:
                continue
            for raw_relation in raw_relation_group['relations']:
                relation = self.parse_relation_from(raw_relation_group['type'], raw_relation)
                self.db.insert_relation(relation)
        cursor.close()

    @staticmethod
    def parse_relation_from(relation_type, raw_relation):
        return {
            'from': raw_relation['body']['value'],
            'to': raw_relation['relation']['value'],
            'type': relation_type
        }


class RedirectParser(RelationParser):
    def parse(self):
        cursor = self.db.find_all_raw_relations()
        for raw_relation_group in cursor:
            if raw_relation_group['type'] == Relation.OTHER.name:
                for raw_relation in raw_relation_group['relations']:
                    if not self.db.relation_exists(raw_relation):
                        relation = self.parse_relation_from(Relation.OTHER.name, raw_relation)
                        self.db.insert_relation(relation)


class HasRelationParser(Parser):
    def parse(self):
        relations = self.db.find_all_relations()
        for relation in relations:
            self.db.update_persons(
                {'$or': [{'url': relation['to']}, {'url': relation['from']}]},
                {'$set': {'hasRelation': True}}
            )


class TypeParser(Parser):
    def parse(self):
        cursor = self.db.find_all_raw_types()
        for raw_type in cursor:
            person = self.db.find_one_person({'url': raw_type['body']['value']})
            if person is not None:
                self.update_type_if_needed(person, raw_type)
        self.__parse_if_empty()

    def __parse_if_empty(self):
        persons = self.db.find_all_persons({'type': {'$exists': False}})
        for person in persons:
            self.update_type(person, 'Person')

    def update_type_if_needed(self, person, raw_type):
        for index in range(len(TypeHelper.TYPES)):
            for tmp_type in TypeHelper.TYPES[index]:
                if 'type' in person and tmp_type == person['type']:
                    return
                if tmp_type in raw_type['type']['value']:
                    self.update_type(person, tmp_type)
                    return

    def update_type(self, person, new_type):
        person['type'] = new_type
        self.db.save_person(person)
