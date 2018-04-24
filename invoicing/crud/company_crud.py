from crud_base import CrudBase
from repository.company_repository import CompanyRepository
from ui.menu import Menu
from ui.style import Style


class CompanyCrud(CrudBase, CompanyRepository):
    def __init__(self):
        super().__init__()
        self.menu('Company')

    def map_data(self, data):
        return {'id': data[0], 'name': data[1], 'address': data[2]}

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
            self.insert_company(address, name)
            self.save()
            self.check_rows_updated('Company Added')
        else:
            print('No company added')

    def edit(self):
        print(Style.create_title('Edit Company'))
        company = Menu.select_row(self, 'Companies')
        if company:
            name = input("Name (" + company['name'] + "): ")
            address = input("Name (" + company['address'] + "): ")
            new_name = name if len(name) > 0 else company['name']
            new_address = address if len(address) > 0 else company['address']
            self.update_company(company['id'], new_name, new_address)
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
                user_action = input('Type \'delete\' to remove this company or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_company(company['id'])
                self.save()
                self.check_rows_updated('Company Deleted')
