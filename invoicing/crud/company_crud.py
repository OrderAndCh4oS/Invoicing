from crud.base_crud import BaseCrud
from crud.client_crud import ClientCrud
from repository.company_repository import CompanyRepository
from ui.menu import Menu
from ui.style import Style


class CompanyCrud(BaseCrud, CompanyRepository):
    def __init__(self):
        super().__init__('Companies')
        super(CompanyRepository, self).__init__('companies')

    def show(self):
        print(Style.create_title('Show Company'))
        company = Menu.select_row(self, 'Companies')
        if company:
            print(Style.create_title('Company Data'))
            print('Name: ' + company['name'])
            print('Address: ' + company['address'])
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Company'))
        name = input("Name: ")
        address = input("Address: ")
        if len(name) > 0:
            self.insert({'name': name, 'address': address})
            self.save()
            self.check_rows_updated('Company Added')
        else:
            print('Company not added')

    def edit(self):
        print(Style.create_title('Edit Company'))
        company = Menu.select_row(self, 'Companies')
        if company:
            name = self.update_field(company['name'], 'Name')
            address = self.update_field(company['address'], 'Address')
            self.update(company['id'], {'name': name, 'address': address})
            self.save()
            self.check_rows_updated('Company Updated')
        else:
            print('No changes made')

    def delete(self):
        print(Style.create_title('Delete Company'))
        company = Menu.select_row(self, 'Companies')
        if company:
            user_action = False
            while not user_action == 'delete':
                user_action = input(
                    'Type \'delete\' to remove this company and ALL associated data or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                ClientCrud().delete_clients_by_company_id(company['id'])
                self.remove(company['id'])
                self.save()
                self.check_rows_updated('Company Deleted')
