from abc import ABCMeta

from actions.action import Action
from ui.menu import Menu
from ui.style import Style


class BaseCrud(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self, table_name, repository, model):
        self.table_name = table_name
        self.repository = repository
        self.model = model

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

    def show_item_menu(self, id):
        title = Style.create_title(self.table_name + ' Menu')
        actions = [
            Action('b', 'Back', False)
        ]
        Menu.create(title, actions)

    def make_label(self, header):
        return " ".join([word.capitalize() for word in header.split('_')])

    def show(self):
        print(Style.create_title('Show %s' % self.table_name))
        item = Menu.pagination_menu(self.repository)
        if item:
            print(Style.create_title('%s Data' % self.table_name))
            for header in self.repository.get_headers():
                label = self.make_label(header)
                print('%s: %s' % (label, item[header]))
            self.show_item_menu(item['id'])

    def add(self):
        print(Style.create_title('Add %s' % self.table_name))
        data = {}
        for (key, field) in self.model:
            data[key] = input("%s: " % self.make_label(key))
        self.model(**data)
        self.model.validate()
        if self.model.is_valid:
            self.repository.insert(data)
            self.repository.save()
            self.repository.check_rows_updated('%s Added' % self.table_name)
        else:
            print(Style.create_title('%s not added' % self.table_name))
            for (key, value) in self.model.get_errors().items():
                print("%s: %s" % (key.capitalize(), value))
        Menu.wait_for_input()

    def edit(self):
        print(Style.create_title('Edit %s' % self.table_name))
        item = Menu.pagination_menu(self.repository)
        if item:
            print(Style.create_title('Add %s' % self.table_name))
            data = {}
            for (key, field) in self.model:
                data[key] = self.update_field(item[key], self.make_label(key))
            self.model(**data)
            self.model.validate()
            if self.model.is_valid:
                self.repository.update(
                    item['id'],
                    data
                )
                self.repository.save()
                self.repository.check_rows_updated('%s Updated' % self.table_name)
            else:
                print(Style.create_title('%s not updated' % self.table_name))
                for (key, value) in self.model.get_errors().items():
                    print("%s: %s" % (key.capitalize(), value))
        else:
            print('No changes made')
        Menu.wait_for_input()

    def delete(self):
        print(Style.create_title('Delete %s' % self.table_name))
        item = Menu.pagination_menu(self.repository)
        if item:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this item or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.repository.remove(item['id'])
                self.repository.save()
                self.repository.check_rows_updated('%s Deleted' % self.table_name)
                Menu.wait_for_input()
