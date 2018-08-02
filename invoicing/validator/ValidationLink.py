class Validator():
    def __init__(self):
        self.valid = False
        self.validation_links = []
        self.error_message = None

    def is_valid(self):
        return self.valid

    def set_valid(self, is_valid):
        self.valid = is_valid

    def set_validation_links(self, validation_links):
        for validation_link in validation_links:
            ValidationLink(self.validation_links, validation_link)

    def set_error_message(self, message):
        self.error_message = message

    def get_error_message(self):
        return self.error_message

    def validate(self):
        self.error_message = None
        return self.validation_links[0](self)


class Validation:
    def __init__(self, error_message='is not valid'):
        self.error_message = error_message

    def __call__(self, data) -> Validator:
        pass

    def validation_check(self, data, check):
        if not check:
            data.set_valid(False)
            data.set_error_message(self.error_message)
        else:
            data.set_valid(True)


class ValidationLink():
    def __init__(self, chain, validation: Validation):
        self.validation = validation
        self.chain = chain
        self.chain.append(self)

    def next(self):
        location = self.chain.index(self)
        if not self.end():
            return self.chain[location + 1]

    def end(self):
        return (self.chain.index(self) + 1 >= len(self.chain))

    def __call__(self, data: Validator):
        validator = self.validation(data)
        if not validator.is_valid() or self.end(): return validator
        return self.next()(data)


class Data(Validator):
    def __init__(self, validation_links, default_value=None):
        super().__init__()
        self.value = default_value
        self.set_validation_links(validation_links)

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "Value: %s: %s (%s)" % (self.value, self.error_message, 'valid' if self.is_valid() else 'invalid')


class IsRequired(Validation):
    def __init__(self, error_message='is required'):
        super().__init__(error_message)

    def __call__(self, data: Data):
        self.validation_check(data, True if data.value else False)
        return data


class IsString(Validation):
    def __init__(self, error_message='is not a string'):
        super().__init__(error_message)

    def __call__(self, data: Data):
        self.validation_check(data, isinstance(data.value, str))
        return data


class IsInteger(Validation):
    def __init__(self, error_message='is not an integer'):
        super().__init__(error_message)

    def __call__(self, data: Data):
        self.validation_check(data, isinstance(data.value, int))
        return data


class MaxLength(Validation):
    def __init__(self, max, error_message='is too long'):
        super().__init__(error_message)
        self.max = max

    def __call__(self, data: Data):
        self.validation_check(data, len(data.value) <= self.max)
        return data


class MinLength(Validation):
    def __init__(self, min, error_message='is too short'):
        super().__init__(error_message)
        self.min = min

    def __call__(self, data: Data):
        self.validation_check(data, len(data.value) >= self.min)
        return data


class BaseModel:

    def fields(self):
        field_list = []
        for k in dir(self):
            v = getattr(self, k)
            if isinstance(v, Data):
                field_list.append((k, v))

        return field_list

    def validate(self):
        self.errors = {}
        for field, value in self.fields():
            value.validate()
            if not value.is_valid():
                self.errors[field] = value.get_error_message()
        self.is_valid = False if len(self.errors) else True

    def __str__(self):
        return "Errors: %s" % ', '.join(self.errors) if len(self.errors) else 'Valid'


class Person(BaseModel):
    first_name = Data([IsRequired(), IsString(), MaxLength(10), MinLength(3)])
    age = Data([IsRequired(), IsInteger()])

    def __init__(self, first_name, age):
        super().__init__()
        self.first_name.set_value(first_name)
        self.age.set_value(age)


if __name__ == '__main__':
    valid = Data([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='Hey there')
    required = Data([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='')
    not_string = Data([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value=123)
    too_long = Data([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='Hey there shit head')
    too_short = Data([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='Hi')
    print('Valid: %s' % valid.validate())
    print('Required: %s' % required.validate())
    print('Not a String: %s' % not_string.validate())
    print('Too Long: %s' % too_long.validate())
    print('Too Short: %s' % too_short.validate())
    person = Person('John', 54)
    person.validate()
    print('Valid person:', person)
    invalid_person = Person('', 'not a number')
    invalid_person.validate()
    print('Invalid person:', invalid_person)
