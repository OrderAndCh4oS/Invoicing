from crud.base_crud import BaseCrud
from repository.status_repository import StatusRepository
from ui.menu import Menu
from ui.style import Style


class StatusCrud(BaseCrud, StatusRepository):
    def __init__(self):
        super().__init__()

    def show(self):
        print(Style.create_title('Show Status'))
        status = Menu.select_row(self, 'Statuses')
        if status:
            print(Style.create_title('Status Data'))
            print('Title: ' + status['title'])
            print('Colour: ' + status['colour'])
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Status'))
        title = input("Title: ")
        colour = input("Colour: ")
        if len(title) > 0:
            self.insert_status(title, colour)
            self.save()
            self.check_rows_updated('Status Added')
        else:
            print('Status not added')

    def edit(self):
        print(Style.create_title('Edit Status'))
        status = Menu.select_row(self, 'Statuses')
        if status:
            title = self.update_field(status['title'], 'Title')
            colour = self.update_field(status['colour'], 'Colour')
            self.update_status(status['id'], title, colour)
            self.save()
            self.check_rows_updated('Status Updated')
        else:
            print('No changes made')

    def delete(self):
        print(Style.create_title('Delete Status'))
        status = Menu.select_row(self, 'Statuses')
        if status:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this status or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_status(status['id'])
                self.save()
                self.check_rows_updated('Status Deleted')
