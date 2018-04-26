from abc import ABCMeta, abstractmethod

from actions.action import Action
from ui.menu import Menu


class BaseCrud(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def menu(self, table_name, actions=None):
        if actions is None:
            actions = [
                Action('1', 'View', self.show),
                Action('2', 'Add', self.add),
                Action('3', 'Edit', self.edit),
                Action('4', 'Delete', self.delete),
                Action('b', 'Back', False)
            ]
        Menu.create('Manage ' + table_name, actions)

    def update_field(self, current_value, field_name):
        value = input(field_name + "(" + current_value + "): ")
        new_value = value if len(value) > 0 else current_value
        return new_value

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass