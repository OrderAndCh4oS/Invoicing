class Validation:
    @staticmethod
    def is_number(number):
        try:
            int(number)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_float(number):
        try:
            float(number)
        except ValueError:
            return False
        return True

    @staticmethod
    def is_number_and_in_range(number, start, stop):
        if Validation.is_number(number) and number >= start and number <= stop:
            return True
        return False
