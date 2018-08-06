from model_validation.validations import IsInteger, IsFloat, IsString, IsBoolean
from model_validation.validator import Validator


class Field(Validator):
    def __init__(self, validation_links=None, default_value=None, nullable=False):
        super().__init__()
        validation_links = validation_links if validation_links is not None else []
        if validation_links:
            self.set_validation_links(validation_links)
        self.value = default_value
        self.nullable = nullable

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "Value: %s: %s (%s)" % (self.value, self.error_message, 'valid' if self.is_valid() else 'invalid')


class IntegerField(Field):
    def __init__(self, validation_links=None, default_value=None, nullable=False):
        super().__init__(validation_links, default_value, nullable)
        self.set_validation_link(IsInteger(), front=True)

    def set_value(self, value):
        try:
            self.value = int(value)
        except:
            self.value = value


class StringField(Field):
    def __init__(self, validation_links=None, default_value=None, nullable=False):
        super().__init__(validation_links, default_value, nullable)
        self.set_validation_link(IsString(), front=True)

    def set_value(self, value):
        try:
            self.value = str(value)
        except:
            self.value = value


class BooleanField(Field):
    def __init__(self, validation_links=None, default_value=None, nullable=False):
        super().__init__(validation_links, default_value, nullable)
        self.set_validation_link(IsBoolean(), front=True)

    def set_value(self, value):
        try:
            self.value = bool(value)
        except:
            self.value = value


class FloatField(Field):
    def __init__(self, validation_links=None, default_value=None, nullable=False):
        super().__init__(validation_links, default_value, nullable)
        self.set_validation_link(IsFloat(), front=True)

    def set_value(self, value):
        try:
            self.value = float(value)
        except:
            self.value = value
