from ansi_colours import AnsiColours as Colour

from ui.style import Style
from ui.table import Table
from validation.validation import Validation


class Menu:
    @staticmethod
    def create(actions):
        user_selection = 0
        keys = []
        for action in actions:
            print(Colour.green(action.key) + ": " + str(action))
            keys.append(action.key)
        while user_selection not in keys:
            user_selection = input('\nSelect an option: ')
        for action in actions:
            if action.check_input(user_selection):
                action.execute()
                break

    @staticmethod
    def choose_item(repository):
        item = False
        while not item:
            id = input('\nEnter an id to view or \'b\' to go back: ')
            if (id == 'b'):
                return False
            if Validation.isNumber(id) == -1:
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
