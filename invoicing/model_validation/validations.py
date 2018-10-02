from datetime import datetime

from invoicing.model_validation.validation import Validation


class IsRequired(Validation):
    def __init__(self, error_message='is required'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, bool(field.value))
        return field


class IsString(Validation):
    def __init__(self, error_message='is not a string'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, str))
        return field


class IsInteger(Validation):
    def __init__(self, error_message='is not an integer'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, int))
        return field


class IsList(Validation):
    def __init__(self, error_message='is not a list'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, list))
        return field


class IsCallable(Validation):
    def __init__(self, error_message='is not a list'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, True)
        return field

class IsBoolean(Validation):
    def __init__(self, error_message='is not a boolean'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, bool))
        return field


class IsFloat(Validation):
    def __init__(self, error_message='is not a float'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, float))
        return field


class MaxLength(Validation):
    def __init__(self, max, error_message='is too long'):
        super().__init__(error_message)
        self.max = max

    def __call__(self, field):
        self.validation_check(field, len(field.value) <= self.max)
        return field


class MinLength(Validation):
    def __init__(self, min, error_message='is too short'):
        super().__init__(error_message)
        self.min = min

    def __call__(self, field):
        self.validation_check(field, len(field.value) >= self.min)
        return field


class IsDate(Validation):
    def __init__(self, format="%d-%m-%y", error_message='is not a valid date'):
        super().__init__(error_message)
        self.format = format

    def __call__(self, field):
        self.validation_check(field, self.check_date(field.value))
        return field

    def check_date(self, value):
        try:
            datetime.strptime(value, self.format)
            return True
        except ValueError:
            return False
