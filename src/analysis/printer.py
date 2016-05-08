class FunctionPrinter:
    @staticmethod
    def print_statistic(fun, *attributes):
        name = fun.__name__
        for attribute in attributes:
            name += ' ' + str(attribute)
        result = fun(*attributes)
        print(name.upper() + ':' + str(result))
