from crud import Crud
from invoicing.database import Database
from repository.company_repository import CompanyRepository
from ui.style import Style
from ui.table import Table
from ui.menu import Menu
from validation.validation import Validation


class Company(Crud):
    def __init__(self):
        self.repository = CompanyRepository()
        self.menu('Company')
        self.repository.close_connection()

    def map_company_data(self, company):
        return {'id': company[0], 'name': company[1], 'address': company[2]}

    def show(self):
        print(Style.create_title('Show Company'))
        company = self.choose_company()
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
            self.repository.insert_company(address, name)
            self.repository.check_rows_updated('Company Added')
        else:
            print('No company added')


    def edit(self):
        print(Style.create_title('Edit Company'))
        company = self.choose_company()
        if company:
            name = input("Name (" + company['name'] + "): ")
            address = input("Name (" + company['address'] + "): ")
            new_name = name if len(name) > 0 else company['name']
            new_address = address if len(address) > 0 else company['address']
            self.repository.update_company(company['id'], new_name, new_address)
            self.repository.check_rows_updated('Company Updated')
        else:
            print('No changes made')

    def delete(self):
        print(Style.create_title('Delete Company'))
        company = self.choose_company()
        if company:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this company or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.repository.remove_company(company['id'])
                self.repository.check_rows_updated('Company Deleted')

    def show_companies(self):
        rows = self.repository.find_companies()
        headers = list(map(lambda x: x[0], self.repository.cursor.description))
        print(Style.create_title('Companies'))
        Table.create_table(headers, rows)

    def choose_company(self):
        self.show_companies()
        company = False
        while not company:
            id = input('\nEnter company id to view or \'b\' to go back: ')
            if (id == 'b'):
                return False
            if Validation.isNumber(id) == -1:
                continue
            company = self.repository.find_companies_by_id(id)
        return self.map_company_data(company)
