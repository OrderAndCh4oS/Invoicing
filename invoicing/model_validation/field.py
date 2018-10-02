from invoicing.model_validation.validations import IsInteger, IsFloat, IsString, IsBoolean, IsDate, IsCallable
from invoicing.model_validation.validator import Validator
from invoicing.relationships.base_relationship import BaseRelationship, OneToManyRelationship


class Field(Validator):
    def __init__(self, validation_links=None, **kwargs):
        super().__init__()
        kwargs.setdefault('initial_value', None)
        kwargs.setdefault('default_value', None)
        kwargs.setdefault('updatable', True)
        validation_links = validation_links if validation_links is not None else []
        if validation_links:
            self.set_validation_links(validation_links)
        self.initial_value = kwargs.get('initial_value')
        self.default_value = kwargs.get('default_value')
        self.value = kwargs.get('initial_value')
        self.updatable = kwargs.get('updatable')

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return "Value: %s: %s (%s)" % (self.value, self.error_message, 'valid' if self.is_valid() else 'invalid')


class IntegerField(Field):
    def __init__(self, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.set_validation_link(IsInteger(), front=True)

    def set_value(self, value):
        try:
            self.value = int(value)
        except:
            self.value = value


class DateField(Field):
    def __init__(self, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.set_validation_link(IsDate(), front=True)
        self.set_validation_link(IsString(), front=True)

    def set_value(self, value):
        try:
            self.value = str(value)
        except:
            self.value = value


class StringField(Field):
    def __init__(self, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.set_validation_link(IsString(), front=True)

    def set_value(self, value):
        try:
            self.value = str(value)
        except:
            self.value = value


class BooleanField(Field):
    def __init__(self, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.set_validation_link(IsBoolean(), front=True)

    def set_value(self, value):
        try:
            self.value = bool(value)
        except:
            self.value = value


class FloatField(Field):
    def __init__(self, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.set_validation_link(IsFloat(), front=True)

    def set_value(self, value):
        try:
            self.value = float(value)
        except:
            self.value = value


class ForeignKeyField(Field):
    def __init__(self, relationship: BaseRelationship, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.relationship = relationship
        self.set_validation_link(IsInteger(), front=True)

    def set_value(self, value):
        try:
            self.value = int(value)
        except:
            self.value = value


class OneToManyField(Field):
    def __init__(self, relationship: OneToManyRelationship, validation_links=None, **kwargs):
        super().__init__(validation_links=validation_links, **kwargs)
        self.relationship = relationship
        self.set_validation_link(IsCallable(), front=True)

    def set_value(self, value):
        self.value = value
