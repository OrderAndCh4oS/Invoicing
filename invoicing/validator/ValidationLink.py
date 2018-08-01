class Validator():
    def __init__(self):
        self.valid = False
        self.validation_links = []

    def is_valid(self):
        return self.valid

    def set_valid(self, is_valid):
        self.valid = is_valid

    def set_validation_links(self, validation_links):
        for validation_link in validation_links:
            ValidationLink(self.validation_links, validation_link)

    def validate(self):
        return self.validation_links[0](self)


class Validation:
    def __call__(self, data) -> Validator: pass


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
    def __init__(self, data):
        super().__init__()
        self.data = data

    def __str__(self):
        return "Data %s Valid: %s" % (self.data, 'valid' if self.is_valid() else 'not valid')


class IsRequired(Validation):
    def __call__(self, data: Data):
        data.set_valid(True if data.data else False)
        return data


class IsString(Validation):
    def __call__(self, data: Data):
        data.set_valid(isinstance(data.data, str))
        return data


class MaxLength(Validation):
    def __init__(self, max):
        self.max = max

    def __call__(self, data: Data):
        data.set_valid(len(data.data) <= self.max)
        return data


class MinLength(Validation):
    def __init__(self, min):
        self.min = min

    def __call__(self, data: Data):
        data.set_valid(len(data.data) >= self.min)
        return data


if __name__ == '__main__':
    data = Data('')
    data.set_validation_links([IsRequired(), IsString(), MaxLength(10), MinLength(3)])
    print(data.validate())
