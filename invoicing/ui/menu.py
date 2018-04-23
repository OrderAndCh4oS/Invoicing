from ansi_colours import AnsiColours as Colour

from ui.style import Style
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


