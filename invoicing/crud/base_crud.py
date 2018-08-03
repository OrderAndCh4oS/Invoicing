from abc import ABCMeta, abstractmethod

from actions.action import Action
from ui.menu import Menu
from ui.style import Style


class BaseCrud(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self, table_name):
        self.table_name = table_name

    def menu(self):
        title = Style.create_title('Manage ' + self.table_name)
        actions = [
            Action('1', 'View', self.show),
            Action('2', 'Add', self.add),
            Action('3', 'Edit', self.edit),
            Action('4', 'Delete', self.delete),
            Action('b', 'Back', False)
        ]
        Menu.create(title, actions)

    def update_field(self, current_value, field_name):
        value = input(field_name + "(" + str(current_value) + "): ")
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
