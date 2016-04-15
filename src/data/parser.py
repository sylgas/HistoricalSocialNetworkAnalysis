class PersonParser:
    def parse_persons_from(self, results):
        for result in results:
            self.__parse_person_from(result)

    def __parse_person_from(self, result):
        return dict(
            url=self._parse_url(result),
            name=self.__parse_name(result),
            role=self.__parse_role(result),
            dynasty=self.__parse_dynasty(result),
            firstYearOfActivity=self.__parse_first_year_of_activity(result),
            lastYearOfActivity=self.__parse_last_year_of_activity(result),
            ideology=self.__parse_ideology(result),
            nationality=self.__parse_nationality(result),
            relations=self.__parse_relations(result)
        )

    def _parse_url(self, result):
        pass

    def __parse_name(self, result):
        pass

    def __parse_role(self, result):
        pass

    def __parse_dynasty(self, result):
        pass

    def __parse_first_year_of_activity(self, result):
        pass

    def __parse_last_year_of_activity(self, result):
        pass

    def __parse_ideology(self, result):
        pass

    def __parse_nationality(self, result):
        pass

    def __parse_relations(self, result):
        pass
