from crud.base_crud import BaseCrud
from repository.client_repository import ClientRepository
from repository.company_repository import CompanyRepository
from ui.menu import Menu
from ui.style import Style


class ClientCrud(BaseCrud, ClientRepository):
    def __init__(self):
        super().__init__()
        self.menu('Client')

    def show(self):
        print(Style.create_title('Show Client'))
        client = Menu.select_row(self, 'Clients')
        if client:
            print(Style.create_title('Client Data'))
            print('Fullname: ' + client['fullname'])
            print('Email: ' + client['email'])
            print('Telephone: ' + client['telephone'])
            print('Company: ' + client['company_name'])
            print('Address: ' + client['company_address'])
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Client'))
        fullname = input("Full Name: ")
        email = input("Email: ")
        telephone = input("Telephone: ")
        company = Menu.select_row(CompanyRepository(), 'Select Company')
        if len(fullname) > 0 and company:
            self.insert_client(fullname, email, telephone, company[0])
            self.save()
            self.check_rows_updated('Client Added')
        else:
            print('Client not added')

    def edit(self):
        print(Style.create_title('Edit Client'))
        client = Menu.select_row(self, 'Clients')
        if client:
            fullname = self.update_field(client['fullname'], 'Fullname')
            email = self.update_field(client['email'], 'Email')
            telephone = self.update_field(client['telephone'], 'Telephone')
            if len(fullname) > 0:
                self.update_client(client['id'], fullname, email, telephone)
                self.save()
                self.check_rows_updated('Client Updated')

    def delete(self):
        print(Style.create_title('Delete Client'))
        client = Menu.select_row(self, 'Clients')
        if client:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this client or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_client(client['id'])
                self.save()
                self.check_rows_updated('Client Deleted')
