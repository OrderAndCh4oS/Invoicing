from crud.base_crud import BaseCrud
from crud.project_crud import ProjectCrud
from models.client_model import ClientModel
from repository.client_repository import ClientRepository
from ui.menu import Menu
from ui.style import Style


class ClientCrud(BaseCrud):
    def __init__(self):
        super().__init__('Clients', ClientRepository(), ClientModel())

    def make_pagination_menu(self):
        return Menu.pagination_menu(
            self.repository,
            find=self.repository.find_paginated_join_companies,
            find_by_id=self.repository.find_by_id_join_company
        )

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
