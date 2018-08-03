class Validation:
    @staticmethod
    def isNumber(number):
        try:
            int(number)
        except ValueError:
            return False
        return True

    @staticmethod
    def isFloat(number):
        try:
            float(number)
        except ValueError:
            return False
        return True

    @staticmethod
    def isNumberAndInRange(number, start, stop):
        if Validation.isNumber(number) and number >= start and number <= stop:
            return True
        return False
