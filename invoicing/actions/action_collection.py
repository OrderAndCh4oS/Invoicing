from invoicing.actions.action import Action


class ActionCollection:

    def __init__(self, *args, exit_action=None):
        self.actions = []
        self.count = 0
        for arg in args:
            self.count += 1
            self.actions.append(Action(str(self.count), arg[0], arg[1]))
        self.actions.append(exit_action or Action('b', 'Back', False))

    def add_action(self, label, action):
        self.count += 1
        self.actions.insert(-1, Action(str(self.count), label, action))

    def add_actions(self, *args):
        for arg in reversed(args):
            self.count += 1
            self.actions.insert(-1, Action(str(self.count), arg[0], arg[1]))
