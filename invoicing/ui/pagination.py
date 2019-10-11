from ansi_colours import AnsiColours as Colour

from invoicing.repository.base_repository import BaseRepository
from invoicing.ui.menu import Menu
from invoicing.ui.style import Style
from invoicing.ui.table import Table
from invoicing.value_validation.value_validation import Validation


class Pagination:

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def __call__(self, limit=5, find=None, find_by_id=None):
        self.limit = limit
        self.find_paginated = self.repository.find_paginated if not find else find
        self.find_by_id = self.repository.find_by_id if not find_by_id else find_by_id
        self.total = self.repository.get_count()[0]
        self.page = 1
        return self.menu()

    def menu(self):
        result = False
        while not result:
            self.paginated_table()
            self.pagination_text()
            user_input = input('\nEnter an %s, use %s and %s to navigate, or %s to go back: ' % (
                Colour.green("'id'"),
                Colour.green("<"),
                Colour.green(">"),
                Colour.green("b")
            ))
            if (user_input == 'b'):
                break
            if self.should_change_page(user_input):
                self.change_page(user_input)
                continue
            if not Validation.is_number(user_input):
                print('Command not recognised')
                continue
            result = self.find_by_id(user_input)
            if not result:
                Menu.wait_for_input('An item with that ID was not found. Press any key to continue.')
        return result

    def paginated_table(self):
        Table.create_table(
            self.find_paginated(limit=self.limit, page=self.page),
            self.repository.get_headers()
        )

    def pagination_text(self):
        text = ""
        if self.page > 1:
            text += "%s previous | " % Colour.green('<')
        text += "page %d" % self.page
        if self.page * self.limit < self.total:
            text += " | next %s" % Colour.green('>')
        print(Style.create_underline(text))
        print(text)
        print(Style.create_underline(text))

    def should_change_page(self, user_input):
        return user_input is '<' or user_input is '>'

    def change_page(self, user_input):
        if self.page is not 1 and user_input is '<':
            self.page -= 1
        elif self.page * self.limit < self.total and user_input is '>':
            self.page += 1
