from ansi_colours import AnsiColours as Colour

from invoicing.actions.action_collection import ActionCollection
from invoicing.ui.style import Style
from invoicing.ui.table import Table
from invoicing.value_validation.value_validation import Validation


class Menu:
    @staticmethod
    def create(title, action_collection: ActionCollection):
        user_input = 0
        keys = []
        while True:
            print(Style.create_title(title))
            for action in action_collection.actions:
                print(Colour.green(action.key) + ": " + str(action))
                keys.append(action.key)
            while user_input not in keys:
                user_input = input('\nSelect an option: ')
            for action in action_collection.actions:
                if action.check_input(user_input):
                    action.execute()
            if user_input == 'b' or user_input == 'q':
                break
            else:
                user_input = 0

    @staticmethod
    def choose_item_by_id(find_by_id):
        item = False
        while not item:
            id = input('\nEnter an id to view or \'b\' to go back: ')
            if id == 'b':
                return False
            if not Validation.is_number(id):
                print('Not a valid number')
                continue
            item = find_by_id(id)
        return item

    @staticmethod
    def select_row(rows, headers, find_by_id):
        Table.create_table(rows, headers)
        return Menu.choose_item_by_id(find_by_id)

    @staticmethod
    def yes_no_question(question):
        response = False
        while response not in ['y', 'Y', '', 'n', 'N']:
            response = input(question + ' (Y/n): ')
        return response in ['Y', 'y', '']

    @staticmethod
    def wait_for_input(text=None):
        input('\nPress %s to continue.' % Colour.green('enter') if not text else "\n%s" % text)
