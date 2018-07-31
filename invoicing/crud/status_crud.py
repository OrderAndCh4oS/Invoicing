from crud.base_crud import BaseCrud
from repository.status_repository import StatusRepository
from ui.menu import Menu
from ui.style import Style


class StatusCrud(BaseCrud, StatusRepository):
    # Todo: see if you can use a sub class for this sort of meta data ie:
    # class Meta():
    #     name = 'Statuses'
    #     table = 'status'
    def __init__(self):
        super().__init__('Statuses')
        super(StatusRepository, self).__init__('status')

    #  Todo: these methods should work like controllers, the current contents should be moved to a view layer
    def show(self):
        print(Style.create_title('Show Status'))
        status = Menu.select_row(self.find_all(), self.get_headers(), self.find_by_id)
        if status:
            print(Style.create_title('Status Data'))
            print('Title: ' + status['title'])
            print('Colour: ' + status['colour'])
            Menu.waitForInput()

    def add(self):
        print(Style.create_title('Add Status'))
        title = input("Title: ")
        colour = input("Colour: ")
        if len(title) > 0:
            self.insert({'title': title, 'colour': colour})
            self.save()
            self.check_rows_updated('Status Added')
        else:
            print('Status not added')
        Menu.waitForInput()

    def edit(self):
        print(Style.create_title('Edit Status'))
        status = Menu.select_row(self.find_all(), self.get_headers(), self.find_by_id)
        if status:
            title = self.update_field(status['title'], 'Title')
            colour = self.update_field(status['colour'], 'Colour')
            self.update(status['id'], {'title': title, 'colour': colour})
            self.save()
            self.check_rows_updated('Status Updated')
        else:
            print('No changes made')
        Menu.waitForInput()

    def delete(self):
        print(Style.create_title('Delete Status'))
        status = Menu.select_row(self.find_all(), self.get_headers(), self.find_by_id)
        if status:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this status or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove(status['id'])
                self.save()
                self.check_rows_updated('Status Deleted')
                Menu.waitForInput()
