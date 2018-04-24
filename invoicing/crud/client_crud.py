from crud_base import CrudBase
from repository.client_repository import ClientRepository
from repository.company_repository import CompanyRepository
from ui.menu import Menu
from ui.style import Style


class ClientCrud(CrudBase, ClientRepository):
    def __init__(self):
        super().__init__()
        self.menu('Client')

    def map_data(self, data):
        return {'id': data[0], 'fullname': data[1], 'email': data[2], 'telephone': data[3], 'client_id': data[4]}

    def show(self):
        print(Style.create_title('Show Client'))
        client = Menu.select_row(self, 'Clients')
        if client:
            print(Style.create_title('Client Data'))
            print('Fullname: ' + client['fullname'])
            print('Email: ' + client['email'])
            print('Telephone: ' + client['telephone'])
            print('Company ID: ' + client['company_id'])
            input('\nContinue?')

    def add(self):
        print(Style.create_title('Add Client'))
        fullname = input("Full Name: ")
        email = input("Email: ")
        telephone = input("Telephone: ")
        company = Menu.select_row(CompanyRepository(), 'Companies')
        if len(fullname) > 0:
            self.insert_client(fullname, email, telephone, company[0])
            self.save()
            self.check_rows_updated('Client Added')

    def edit(self):
        print(Style.create_title('Edit Client'))
        client = Menu.select_row(self, 'Clients')
        if client:
            client = self.map_data(client)
            fullname = input("Full Name (" + client['fullname'] + "): ")
            email = input("Email: (" + client['email'] + "): ")
            telephone = input("Telephone: (" + client['telephone'] + "): ")
            new_fullname = fullname if len(fullname) > 0 else client['fullname']
            new_email = email if len(email) > 0 else client['email']
            new_telephone = telephone if len(telephone) > 0 else client['telephone']
            if len(fullname) > 0:
                self.update_client(client['id'], new_fullname, new_email, new_telephone)
                self.save()
                self.check_rows_updated('Client Updated')

    # Todo: can be abstracted out
    def delete(self):
        print(Style.create_title('Delete Client'))
        client = Menu.select_row(self, 'Clients')
        if client:
            client = self.map_data(client)
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this client or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_client(client['id'])
                self.save()
                self.check_rows_updated('Client Deleted')
