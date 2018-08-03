from model_validation.validator import Validator


class Field(Validator):
    def __init__(self, validation_links, default_value=None, nullable=False):
        super().__init__()
        self.value = default_value
        self.set_validation_links(validation_links)
        self.nullable = nullable

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "Value: %s: %s (%s)" % (self.value, self.error_message, 'valid' if self.is_valid() else 'invalid')
