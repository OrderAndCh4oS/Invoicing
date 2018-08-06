from crud.base_crud import BaseCrud
from crud.project_crud import ProjectCrud
from models.client_model import ClientModel
from repository.client_repository import ClientRepository


class ClientCrud(BaseCrud):
    def __init__(self):
        super().__init__('Clients', ClientRepository, ClientModel)

    def make_pagination_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_companies,
            find_by_id=self.repository.find_by_id_join_company
        )

    def remove_relations(self, id):
        ProjectCrud().delete_projects_by_client_id(id)

    def delete_clients_by_company_id(self, company_id):
        clients = self.repository.find_clients_by_company_id(company_id)
        for client in clients:
            self.remove_relations(client['id'])
        self.repository.remove_clients_by_company_id(company_id)
        self.repository.save()
