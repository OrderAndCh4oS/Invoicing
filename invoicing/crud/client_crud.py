from crud.base_crud import BaseCrud
from crud.project_crud import ProjectCrud
from repository.client_repository import ClientRepository
from repository.company_repository import CompanyRepository
from ui.menu import Menu
from ui.style import Style


class ClientCrud(BaseCrud):
    def __init__(self):
        super().__init__('Clients')
        self.repository = ClientRepository()

    def show(self):
        print(Style.create_title('Show Client'))
        client = self.make_pagination_menu()
        if client:
            print(Style.create_title('Client Data'))
            print('Fullname: ' + client['fullname'])
            print('Email: ' + client['email'])
            print('Telephone: ' + client['telephone'])
            print('Company: ' + client['company_name'])
            print('Address: ' + client['company_address'])
            Menu.wait_for_input()

    def make_pagination_menu(self):
        return Menu.pagination_menu(
            self.repository,
            find=self.repository.find_paginated_join_companies,
            find_by_id=self.repository.find_by_id_join_company
        )

    def add(self):
        print(Style.create_title('Add Client'))
        fullname = input("Full Name: ")
        email = input("Email: ")
        telephone = input("Telephone: ")
        companyRepository = CompanyRepository()
        print(Style.create_title('Select Company'))
        company = Menu.pagination_menu(
            companyRepository,
            find=companyRepository.find_paginated,
            find_by_id=companyRepository.find_by_id
        )
        if len(fullname) > 0 and company:
            self.repository.insert({
                'fullname': fullname,
                'email': email,
                'telephone': telephone,
                'company_id': company[0]
            })
            self.repository.save()
            self.repository.check_rows_updated('Client Added')
        else:
            print('Client not added')
        Menu.wait_for_input()

    def edit(self):
        print(Style.create_title('Edit Client'))
        client = self.make_pagination_menu()
        if client:
            fullname = self.update_field(client['fullname'], 'Fullname')
            email = self.update_field(client['email'], 'Email')
            telephone = self.update_field(client['telephone'], 'Telephone')
            if len(fullname) > 0:
                self.repository.update(client['id'], {
                    'fullname': fullname,
                    'email': email,
                    'telephone': telephone
                })
                self.repository.save()
                self.repository.check_rows_updated('Client Updated')
                Menu.wait_for_input()

    def delete(self):
        print(Style.create_title('Delete Client'))
        client = self.make_pagination_menu()
        if client:
            user_action = False
            while not user_action == 'delete':
                user_action = input('Type \'delete\' to remove this client or \'c\' to cancel: ')
                if user_action == 'c':
                    return
            if user_action == 'delete':
                self.remove_children(client['id'])
                self.repository.remove(client['id'])
                self.repository.save()
                self.repository.check_rows_updated('Client Deleted')
                Menu.wait_for_input()

    def remove_children(self, client_id):
        ProjectCrud().delete_projects_by_client_id(client_id)

    def delete_clients_by_company_id(self, company_id):
        clients = self.repository.find_clients_by_company_id(company_id)
        for client in clients:
            self.remove_children(client['id'])
        self.repository.remove_clients_by_company_id(company_id)
        self.repository.save()
