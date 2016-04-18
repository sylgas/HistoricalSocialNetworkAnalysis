import re


class Parser(object):
    RESOURCE_REGEXES = [r'http://dbpedia\.org/resource/(?P<value>[^\(\)]*)(\(.*\))*',
                        r'"“*(?P<value>.*[^“”"])”*"@.+',
                        r'(?P<value>.*)']

    @staticmethod
    def __extract_first_attribute_string_value(collection, *attributes):
        return Parser.__extract_string_value(
            Parser.__extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def __extract_date_value(collection, *attributes):
        return Parser.__parse_date(Parser.__extract_first_attribute_value(collection, *attributes))

    @staticmethod
    def __extract_first_attribute_value(element, *attributes):
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

    @staticmethod
    def __parse_date(date_string):
        if "\"" in date_string:
            return date_string[1:5]
        else:
            return date_string[:4]
