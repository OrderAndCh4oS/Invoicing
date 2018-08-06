class Action:
    def __init__(self, key, label, action=None):
        self.key = key
        self.label = label
        self.action = action

    def __repr__(self):
        return self.label

    def check_input(self, input_value):
        return input_value == self.key

    def execute(self):
        if self.action:
            self.action()
