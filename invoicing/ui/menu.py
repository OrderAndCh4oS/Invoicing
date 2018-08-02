from ansi_colours import AnsiColours as Colour

from ui.table import Table
from value_validation.value_validation import Validation


class Menu:
    @staticmethod
    def create(title, actions):
        user_selection = 0
        keys = []
        while True:
            print(title)
            for action in actions:
                print(Colour.green(action.key) + ": " + str(action))
                keys.append(action.key)
            while user_selection not in keys:
                user_selection = input('\nSelect an option: ')
            for action in actions:
                if action.check_input(user_selection):
                    action.execute()
            if user_selection == 'b' or user_selection == 'q':
                break
            else:
                user_selection = 0

    @staticmethod
    def choose_item_by_id(find_by_id):
        item = False
        while not item:
            id = input('\nEnter an id to view or \'b\' to go back: ')
            if (id == 'b'):
                return False
            if not Validation.isNumber(id):
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
    def waitForInput():
        input('\nContinue?')
