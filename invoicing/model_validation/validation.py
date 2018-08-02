class Validation:
    def __init__(self, error_message='is not valid'):
        self.error_message = error_message

    def __call__(self, field):
        pass

    def validation_check(self, field, check):
        if not check:
            field.set_valid(False)
            field.set_error_message(self.error_message)
        else:
            field.set_valid(True)
