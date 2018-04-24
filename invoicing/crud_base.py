from abc import ABCMeta, abstractmethod

from ui.menu import Menu


class CrudBase(metaclass=ABCMeta):
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

    @abstractmethod
    def map_data(self, data):
        pass

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