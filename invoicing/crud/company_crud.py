from crud.base_crud import BaseCrud
from crud.client_crud import ClientCrud
from repository.company_repository import CompanyRepository
from ui.menu import Menu
from ui.style import Style


class CompanyCrud(BaseCrud):
    def __init__(self):
        super().__init__('Companies')
        self.repository = CompanyRepository()

    def show(self):
        company = Menu.select_row(self.repository.find_all(), self.repository.get_headers(), self.repository.find_by_id)
        if company:
            print(Style.create_title('Company Data'))
            print('Name: ' + company['name'])
            print('Address: ' + company['address'])
            Menu.waitForInput()

    def add(self):
        print(Style.create_title('Add Company'))
        name = input("Name: ")
        address = input("Address: ")
        if len(name) > 0:
            self.repository.insert({'name': name, 'address': address})
            self.repository.save()
            self.repository.check_rows_updated('Company Added')
        else:
            print('Company not added')
        Menu.waitForInput()

    def edit(self):
        print(Style.create_title('Edit Company'))
        company = Menu.select_row(self.repository.find_all(), self.repository.get_headers(), self.repository.find_by_id)
        if company:
            name = self.update_field(company['name'], 'Name')
            address = self.update_field(company['address'], 'Address')
            self.repository.update(company['id'], {'name': name, 'address': address})
            self.repository.save()
            self.repository.check_rows_updated('Company Updated')
        else:
            print('No changes made')
        Menu.waitForInput()

    def delete(self):
        print(Style.create_title('Delete Company'))
        company = Menu.select_row(self.repository.find_all(), self.repository.get_headers(), self.repository.find_by_id)
        if company:
            user_action = False
            while not user_action == 'delete':
                user_action = input(
                    'Type \'delete\' to remove this company and ALL associated data or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                ClientCrud().delete_clients_by_company_id(company['id'])
                self.repository.remove(company['id'])
                self.repository.save()
                self.repository.check_rows_updated('Company Deleted')
                Menu.waitForInput()
