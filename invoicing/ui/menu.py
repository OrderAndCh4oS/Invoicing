from ansi_colours import AnsiColours as Colour

from ui.style import Style
from ui.table import Table
from validation.validation import Validation


class Menu:
    @staticmethod
    def create(title, options):
        user_selection = 0
        print(Style.create_title(title))
        for i, option in enumerate(options):
            print(Colour.green(str(i + 1)) + ": " + option)
        while user_selection not in [i for i in range(1, len(options) + 1)]:
            user_selection = input('\nSelect an option: ')
            user_selection = Validation.isNumberAndInRange(user_selection, 1, len(options))
        return user_selection

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
