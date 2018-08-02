from model_validation.validation import Validation


class IsRequired(Validation):
    def __init__(self, error_message='is required'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, True if field.value else False)
        return field


class IsType(Validation):
    def __init__(self, field_type, error_message='is not a string'):
        super().__init__(error_message)
        self.field_type = field_type

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, self.field_type))
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


class IsBoolean(Validation):
    def __init__(self, error_message='is not an integer'):
        super().__init__(error_message)

    def __call__(self, field):
        self.validation_check(field, isinstance(field.value, bool))
        return field


class IsFloat(Validation):
    def __init__(self, error_message='is not an integer'):
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
