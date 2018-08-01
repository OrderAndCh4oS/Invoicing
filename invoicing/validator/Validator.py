class Validator():
    def __init__(self):
        self.valid = False

    def is_valid(self):
        return self.valid

    def set_valid(self, is_valid):
        self.valid = is_valid
