from model_validation.field import Field


class BaseModel:
    is_valid = False
    errors = {}
    fields = None

    def __call__(self, **kwargs):
        self.errors = {}
        self.is_valid = False
        for field, value in kwargs.items():
            attributes = self.__class__.__dict__
            if field in attributes and isinstance(attributes[field], Field):
                attributes[field].set_value(value)

    def get_fields(self):
        if not self.fields:
            self.fields = []
            for field, value in self.__class__.__dict__.items():
                if isinstance(value, Field):
                    self.fields.append((field, value))
        return self.fields

    def validate(self):
        for field, value in self.get_fields():
            value.validate()
            if not value.is_valid() and not (value.is_nullable() and value.is_null()):
                self.errors[field] = value.get_error_message()
        self.is_valid = False if len(self.errors) else True

    def get_errors(self):
        return self.errors

    def __str__(self):
        return "Errors: %s" % ', '.join([k + ": " + v for k, v in self.errors.items()]) if len(self.errors) else 'Valid'
