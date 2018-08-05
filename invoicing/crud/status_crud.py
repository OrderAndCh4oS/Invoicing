from crud.base_crud import BaseCrud
from repository.status_repository import StatusRepository
from ui.menu import Menu
from ui.style import Style


class StatusCrud(BaseCrud):
    # Todo: see if you can use a sub class for this sort of meta data ie:
    def __init__(self):
        super().__init__('Statuses')
        self.repository = StatusRepository()

    #  Todo: these methods should work like controllers, the current contents should be moved to a view layer
    def show(self):
        print(Style.create_title('Show Status'))
        status = Menu.pagination_menu(self.repository)
        if status:
            print(Style.create_title('Status Data'))
            print('Title: ' + status['title'])
            print('Colour: ' + status['colour'])
            Menu.wait_for_input()

    def add(self):
        print(Style.create_title('Add Status'))
        title = input("Title: ")
        colour = input("Colour: ")
        if len(title) > 0:
            self.repository.insert({'title': title, 'colour': colour})
            self.repository.save()
            self.repository.check_rows_updated('Status Added')
        else:
            print('Status not added')
        Menu.wait_for_input()

    def edit(self):
        print(Style.create_title('Edit Status'))
        status = Menu.pagination_menu(self.repository)
        if status:
            title = self.update_field(status['title'], 'Title')
            colour = self.update_field(status['colour'], 'Colour')
            self.repository.update(status['id'], {'title': title, 'colour': colour})
            self.repository.save()
            self.repository.check_rows_updated('Status Updated')
        else:
            print('No changes made')
        Menu.wait_for_input()

    def delete(self):
        print(Style.create_title('Delete Status'))
        status = Menu.pagination_menu(self.repository)
        if status:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this status or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.repository.remove(status['id'])
                self.repository.save()
                self.repository.check_rows_updated('Status Deleted')
                Menu.wait_for_input()
