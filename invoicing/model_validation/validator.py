from invoicing.model_validation.validation_link import ValidationLink


class Validator():
    nullable = False
    value = None

    def __init__(self):
        self.valid = False
        self.validation_links = []
        self.error_message = None

    def is_valid(self):
        return self.valid

    def set_valid(self, is_valid):
        self.valid = is_valid

    def is_nullable(self):
        return self.nullable

    def is_null(self):
        return self.value is None

    def set_validation_links(self, validation_links):
        for validation_link in validation_links:
            ValidationLink(self.validation_links, validation_link)

    def set_validation_link(self, validation_link, front=False):
        ValidationLink(self.validation_links, validation_link, front)

    def set_error_message(self, message):
        self.error_message = message

    def get_error_message(self):
        return self.error_message

    def validate(self):
        self.error_message = None
        return self.validation_links[0](self)
