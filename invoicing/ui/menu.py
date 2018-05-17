from ansi_colours import AnsiColours as Colour

from ui.style import Style
from ui.table import Table
from validation.validation import Validation


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
    def choose_item(repository):
        item = False
        while not item:
            id = input('\nEnter an id to view or \'b\' to go back: ')
            if (id == 'b'):
                return False
            if not Validation.isNumber(id):
                print('Not a valid number')
                continue
            item = repository.find_by_id(id)
        return item

    @staticmethod
    def show_all(repository):
        rows = repository.find_all()
        headers = list(map(lambda x: x[0], repository.cursor.description))
        Table.create_table(headers, rows)

    @staticmethod
    def select_row(repository, title):
        print(Style.create_title(title))
        Menu.show_all(repository)
        return Menu.choose_item(repository)

    # Todo: update all select_row usages to use this instead
    # Todo: find a way to remove cursor from params
    @staticmethod
    def select_row_by(find, cursor, select):
        Menu.show_all_by(find, cursor)
        return Menu.choose_item_by(select)

    @staticmethod
    def yes_no_question(question):
        response = False
        while response not in ['y', 'Y', '', 'n', 'N']:
            response = input(question + ' (Y/n): ')
        return response in ['Y', 'y', '']

    @staticmethod
    def choose_item_by(select):
        item = False
        while not item:
            id = input('\nEnter an id to view or \'b\' to go back: ')
            if (id == 'b'):
                return False
            if not Validation.isNumber(id):
                print('Not a valid number')
                continue
            item = select(id)
        return item

    @staticmethod
    def show_all_by(find, cursor):
        rows = find()
        headers = list(map(lambda x: x[0], cursor.description))
        Table.create_table(headers, rows)
