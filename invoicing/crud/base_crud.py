from abc import ABCMeta

from actions.action_collection import ActionCollection
from model_validation.field import ForeignKeyField
from ui.menu import Menu
from ui.pagination import Pagination
from ui.style import Style


class BaseCrud(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self, table_name, repository, model):
        self.table_name = table_name
        self.repository = repository()
        self.model = model()
        self.paginated_menu = Pagination(self.repository)
        self.menu_actions = ActionCollection(
            ('View', self.show),
            ('Add', self.add),
            ('Edit', self.edit),
            ('Delete', self.delete)
        )

    def show(self):
        print(Style.create_title('Show %s' % self.table_name))
        item = self.make_paginated_menu()
        if item:
            self.show_item_detail(item)
            self.show_item_menu(item['id'])

    def show_item_detail(self, item):
        print(Style.create_title('%s Data' % self.table_name))
        for header in self.repository.get_headers():
            label = self.make_label(header)
            print('%s: %s' % (label, item[header]))

    def add(self):
        print(Style.create_title('Add %s' % self.table_name))
        data = {}
        for (key, field) in self.model:
            if field.initial_value is not None:
                data[key] = field.initial_value
            elif isinstance(field, ForeignKeyField):
                data[key] = self.select_foreign_key_relationship(field.relationship)
            else:
                data[key] = input("%s: " % self.make_label(key))
        self.model(**data)
        self.model.validate()
        if self.model.is_valid():
            self.repository.insert(data)
            self.repository.save()
            self.repository.check_rows_updated('%s Added' % self.table_name)
            self.add_relations()
        else:
            print(Style.create_title('%s not added' % self.table_name))
            for (key, value) in self.model.get_errors().items():
                print("%s: %s" % (key.capitalize(), value))
        Menu.wait_for_input()

    def edit(self):
        print(Style.create_title('Edit %s' % self.table_name))
        item = self.make_paginated_menu()
        if item:
            print(Style.create_title('Add %s' % self.table_name))
            data = {}
            for (key, field) in self.model:
                if not field.updatable:
                    continue
                if (isinstance(field, ForeignKeyField)):
                    if Menu.yes_no_question('Update %s Relationship?' % field.relationship.name):
                        data[key] = self.select_foreign_key_relationship(field.relationship)
                    else:
                        data[key] = item[key]
                else:
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
                self.add_relations()
            else:
                print(Style.create_title('%s not updated' % self.table_name))
                for (key, value) in self.model.get_errors().items():
                    print("%s: %s" % (key.capitalize(), value))
        else:
            print('No changes made')
        Menu.wait_for_input()

    def delete(self):
        print(Style.create_title('Delete %s' % self.table_name))
        item = self.make_paginated_menu()
        if item:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this item or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_relations(item['id'])
                self.repository.remove(item['id'])
                self.repository.save()
                self.repository.check_rows_updated('%s Deleted' % self.table_name)
                Menu.wait_for_input()

    def menu(self):
        Menu.create('Manage ' + self.table_name, self.menu_actions)

    def make_paginated_menu(self):
        return self.paginated_menu()

    def make_label(self, header):
        return " ".join([word.capitalize() for word in header.split('_')])

    def update_field(self, current_value, field_name):
        value = input(field_name + "(" + str(current_value) + "): ")
        new_value = value if len(value) > 0 else current_value
        return new_value

    def select_foreign_key_relationship(self, relationship_field):
        repository = relationship_field.repository()
        print(Style.create_title('Select %s' % relationship_field.name))
        paginated_menu = Pagination(repository)
        item = paginated_menu(
            find=repository.find_paginated,
            find_by_id=repository.find_by_id
        )
        return item[0]

    # Todo create and implement add_one_to_many_relationships
    def add_one_to_many_relationships(self, one_to_many_field):
        repository = one_to_many_field.repository()
        print(Style.create_title('Add %s' % one_to_many_field.name))
        while Menu.yes_no_question('Add job'):
            pass

    def show_item_menu(self, id):
        Menu.create(self.table_name + ' Menu', ActionCollection())

    def add_relations(self):
        pass

    def remove_relations(self, id):
        pass
