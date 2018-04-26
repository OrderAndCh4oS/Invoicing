
class Action:
    def __init__(self, key, title, action=None):
        self.key = key
        self.title = title
        self.action = action

    def __repr__(self):
        return self.title

    def check_input(self, input_value):
        return input_value == self.key

    def execute(self):
        if self.action:
            self.action()