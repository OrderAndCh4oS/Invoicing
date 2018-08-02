from model_validation.field import Field


class BaseModel:
    def __init__(self, **kwargs):
        self.fields = []
        for field, value in kwargs.items():
            attributes = self.__class__.__dict__
            if field in attributes and isinstance(attributes[field], Field):
                attributes[field].set_value(value)
                self.fields.append((field, attributes[field]))

    def validate(self):
        self.errors = {}
        for field, value in self.fields:
            value.validate()
            if not value.is_valid():
                self.errors[field] = value.get_error_message()
        self.is_valid = False if len(self.errors) else True

    def __str__(self):
        return "Errors: %s" % ', '.join([k + ": " + v for k, v in self.errors.items()]) if len(self.errors) else 'Valid'
