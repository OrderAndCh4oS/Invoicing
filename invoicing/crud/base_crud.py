from abc import ABCMeta

from ansi_colours import AnsiColours as Colour

from invoicing.actions.action_collection import ActionCollection
from invoicing.model_validation.field import ForeignKeyField, OneToManyField
from invoicing.ui.menu import Menu
from invoicing.ui.pagination import Pagination
from invoicing.ui.style import Style
from invoicing.ui.relationship import Relationship


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

    def menu(self):
        Menu.create('Manage ' + self.table_name, self.menu_actions)

    def show(self):
        print(Style.create_title('Show %s' % self.table_name))
        item = self.make_paginated_menu()
        if item:
            self.show_item_detail(item)
            self.show_item_menu(item['id'])

    def show_item_detail(self, item):
        print(Style.create_title('%s Data' % self.table_name))
        for header in self.repository.get_headers():
            label = Style.make_label(header)
            print('%s: %s' % (label, Colour.blue(str(item[header]))))

    def show_item_menu(self, id):
        Menu.create(self.table_name + ' Menu', ActionCollection())

    def add(self):
        print(Style.create_title('Add %s' % self.table_name))
        data = self.input_add_data()
        self.validate_model_data(data['own'])
        if self.model.is_valid():
            self.save_data(data)
        else:
            self.display_errors('%s not added' % self.table_name)
        Menu.wait_for_input()

    def input_add_data(self):
        data = {'own': {}, 'relation': {}}
        for (key, field) in self.model:
            if field.initial_value is not None:
                data['own'][key] = field.initial_value
            elif isinstance(field, ForeignKeyField):
                foreign_key = Relationship.select_foreign_key_relationship(field.relationship)
                if foreign_key:
                    data['own'][key] = foreign_key
                else:
                    break
            elif isinstance(field, OneToManyField):
                foreign_key = Relationship.select_foreign_key_relationship_inverse(field.relationship)
                if foreign_key:
                    data['relation'][key] = foreign_key
                else:
                    break
            elif field.default_value is not None:
                user_input = input("%s (%s): " % (Style.make_label(key), field.default_value))
                if user_input is '':
                    user_input = field.default_value
                data['own'][key] = user_input
            else:
                data['own'][key] = input("%s: " % Style.make_label(key))
        return data

    def save_data(self, data):
        self.repository.insert(data['own'])
        self.repository.update_parent_foreign_keys(data['relation'])
        self.repository.save()
        self.repository.check_rows_updated('%s Added' % self.table_name)

    def edit(self):
        print(Style.create_title('Edit %s' % self.table_name))
        item = self.make_paginated_menu()
        if item:
            data = self.input_edit_data(item)
            data['own'] = self.validate_model_data(data['own'])
            if self.model.is_valid:
                self.save_update(data, item)
            else:
                self.display_errors('%s not updated' % self.table_name)
        else:
            print('No changes made')
        Menu.wait_for_input()

    def input_edit_data(self, item):
        data = {'own': {}, 'relation': {}}
        for (key, field) in self.model:
            if not field.updatable:
                continue
            if isinstance(field, ForeignKeyField):
                if Menu.yes_no_question('Change %s?' % field.relationship.name):
                    foreign_key = Relationship.select_foreign_key_relationship(field.relationship)
                    if foreign_key:
                        data['own'][key] = foreign_key
                else:
                    data['own'][key] = item[key]
            elif isinstance(field, OneToManyField):
                foreign_key = Relationship.select_foreign_key_relationship_inverse(field.relationship)
                if foreign_key:
                    data['relation'][key] = foreign_key
                else:
                    data['relation'][key] = item[key]
                # Todo: handle removing relationships
            else:
                data['own'][key] = self.update_field(item[key], Style.make_label(key))
        return data

    def validate_model_data(self, data):
        self.model(**data)
        self.model.validate()
        return data

    def save_update(self, data, item):
        self.repository.update(item['id'], data['own'])
        self.repository.update_parent_foreign_keys(data['relation'])
        self.repository.save()
        self.repository.check_rows_updated('%s Updated' % self.table_name)

    def update_field(self, current_value, field_name):
        value = input(field_name + "(" + str(current_value) + "): ")
        new_value = value if len(value) > 0 else current_value
        return new_value

    def display_errors(self, message):
        print(Style.create_title(message))
        for (key, value) in self.model.get_errors().items():
            print("%s: %s" % (key.capitalize(), Colour.red(value)))

    def delete(self):
        print(Style.create_title('Delete %s' % self.table_name))
        item = self.make_paginated_menu()
        if item:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'%s\' to remove this item or %s to cancel: ' % (
                    Colour.red('delete'),
                    Colour.green('c')
                ))
                if user_action == 'c':
                    return
            self.save_remove(item)
            Menu.wait_for_input()

    def save_remove(self, item):
        self.repository.remove(item['id'])
        self.repository.save()
        self.repository.check_rows_updated('%s Deleted' % self.table_name)

    def make_paginated_menu(self):
        return self.paginated_menu()

