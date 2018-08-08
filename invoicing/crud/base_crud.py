from abc import ABCMeta

from ansi_colours import AnsiColours as Colour

from actions.action_collection import ActionCollection
from model_validation.field import ForeignKeyField, OneToManyField
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
            label = self.make_label(header)
            print('%s: %s' % (label, Colour.blue(str(item[header]))))

    def show_item_menu(self, id):
        Menu.create(self.table_name + ' Menu', ActionCollection())

    def add(self):
        print(Style.create_title('Add %s' % self.table_name))
        data = self.input_add_data()
        data['own'] = self.validate_model_data(data['own'])
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
                data['own'][key] = self.select_foreign_key_relationship(field.relationship)
            elif isinstance(field, OneToManyField):
                data['relation'][key] = self.select_foreign_key_relationship_inverse(field.relationship)
            else:
                data['own'][key] = input("%s: " % self.make_label(key))
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
            if (isinstance(field, ForeignKeyField)):
                if Menu.yes_no_question('Change %s?' % field.relationship.name):
                    data['own'][key] = self.select_foreign_key_relationship(field.relationship)
                else:
                    data['own'][key] = item[key]
            elif (isinstance(field, OneToManyField)):
                data['relation'][key] = self.select_foreign_key_relationship_inverse(field.relationship)
            else:
                data['own'][key] = self.update_field(item[key], self.make_label(key))
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

    def select_foreign_key_relationship(self, relationship_field):
        repository = relationship_field.repository()
        print(Style.create_title('Select %s' % relationship_field.name))
        paginated_menu = Pagination(repository)
        item = paginated_menu(
            find=repository.find_paginated,
            find_by_id=repository.find_by_id
        )
        return item[0]

    def make_paginated_menu(self):
        return self.paginated_menu()

    def make_label(self, header):
        return " ".join([word.capitalize() for word in header.split('_')])

    def select_foreign_key_relationship_inverse(self, relationship):
        foreign_keys = []
        repository = relationship.repository()
        while Menu.yes_no_question('Add %s' % relationship.name):
            print(Style.create_title('Select %s' % relationship.name))
            paginated_menu = Pagination(repository)
            item = paginated_menu(
                find=repository.find_paginated,
                find_by_id=repository.find_by_id
            )
            foreign_keys.append(item['id'])
        return (relationship.related_name, foreign_keys)
