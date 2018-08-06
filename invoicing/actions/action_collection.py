from actions.action import Action


class ActionCollection:

    def __init__(self, *actions, exit_action=None):
        self.actions = []
        self.count = 0
        for action in actions:
            self.count += 1
            self.actions.append(Action(str(self.count), action[0], action[1]))
        self.actions.append(exit_action or Action('b', 'Back', False))

    def add_action(self, label, action):
        self.count += 1
        self.actions.insert(-1, Action(str(self.count), label, action))
