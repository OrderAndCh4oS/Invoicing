from abc import ABCMeta, abstractmethod

from ui.menu import Menu


class BaseCrud(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def menu(self, table):
        crud = ['View ' + table, 'Add ' + table, 'Edit ' + table, 'Delete ' + table, 'Back']
        user_selection = Menu.create('Manage ' + table, crud)
        if user_selection == 1:
            self.show()
        elif user_selection == 2:
            self.add()
        elif user_selection == 3:
            self.edit()
        elif user_selection == 4:
            self.delete()

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