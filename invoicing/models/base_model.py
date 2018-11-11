import collections

from invoicing.model_validation.field import Field


class OrderedClassMembers(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(cls, name, bases, class_dict):
        result = type.__new__(cls, name, bases, dict(class_dict))
        exclude = set(dir(type))
        result.__fields__ = list(f for f in class_dict.keys() if f not in exclude)
        return result


class BaseModel(metaclass=OrderedClassMembers):
    valid = False
    errors = {}
    fields = None

    def __call__(self, **kwargs):
        self.valid = False
        self.errors = {}
        for field, value in kwargs.items():
            attributes = self.__class__.__dict__
            if field in attributes and isinstance(attributes[field], Field):
                attributes[field].set_value(value)

    def __iter__(self):
        for field in self.__fields__:
            if isinstance(self.__class__.__dict__[field], Field):
                yield (field, self.__class__.__dict__[field])

    def validate(self):
        for field, value in self:
            value.validate()
            if not value.is_valid():
                self.errors[field] = value.get_error_message()
        self.valid = False if len(self.errors) else True

    def is_valid(self):
        return self.valid

    def get_errors(self):
        return self.errors

    def __str__(self):
        return "Errors: %s" % ', '.join([k + ": " + v for k, v in self.errors.items()]) if len(self.errors) else 'Valid'
