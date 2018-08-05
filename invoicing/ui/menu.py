from ansi_colours import AnsiColours as Colour

from repository.base_repository import BaseRepository
from ui.style import Style
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
    def wait_for_input():
        input('\nContinue?')

    @staticmethod
    def pagination_menu(repository: BaseRepository, limit=5, find=None, find_by_id=None):
        page = 1
        total = repository.get_count()[0]
        while True:
            find_paginated = repository.find_paginated if not find else find
            Table.create_table(
                find_paginated(limit=limit, page=page),
                repository.get_headers()
            )
            input_dialog = ""
            if page > 1:
                input_dialog += "'<' previous | "
            input_dialog += "page %d" % page
            if page * limit < total:
                input_dialog += " | next '>'"
            print(Style.create_underline(input_dialog))
            print(input_dialog)
            print(Style.create_underline(input_dialog))
            user_input = input('\nEnter an id, use \'<\' and \'>\' to navigate, or \'b\' to go back: ')
            if (user_input == 'b'):
                return False
            if page is not 1 and user_input is '<':
                page -= 1
            elif page * limit < total and user_input is '>':
                page += 1
            elif not Validation.isNumber(user_input):
                print('Not a valid number')
                continue
            else:
                find_by = repository.find_by_id if not find_by_id else find_by_id
                return find_by(user_input)
