from repository.base_repository import BaseRepository
from ui.menu import Menu
from ui.style import Style
from ui.table import Table
from value_validation.value_validation import Validation


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
            user_input = input('\nEnter an id, use \'<\' and \'>\' to navigate, or \'b\' to go back: ')
            if (user_input == 'b'):
                break
            if self.should_change_page(user_input):
                self.change_page(user_input)
                continue
            if not Validation.isNumber(user_input):
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
            text += "'<' previous | "
        text += "page %d" % self.page
        if self.page * self.limit < self.total:
            text += " | next '>'"
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
