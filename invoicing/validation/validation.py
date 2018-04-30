# Todo: This is garbage write validation that returns bools
# Todo: Remove print statements too
class Validation:
    @staticmethod
    def isNumber(number):
        try:
            number = int(number)
        except ValueError:
            number = -1
            print("Not a valid number")
        return number

    @staticmethod
    def isFloat(number):
        try:
            number = float(number)
        except ValueError:
            number = -1
            print("Not a valid number")
        return number

    @staticmethod
    def isNumberAndInRange(number, start, stop):
        number = Validation.isNumber(number)
        try:
            if number < start or number > stop:
                raise ValueError
        except ValueError:
            number = -1
            print('Number is not in range')
        return number