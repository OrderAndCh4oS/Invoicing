from invoicing.crud.base_crud import BaseCrud
from invoicing.models.client_model import ClientModel
from invoicing.repository.client_repository import ClientRepository


class ClientCrud(BaseCrud):
    def __init__(self):
        super().__init__('Clients', ClientRepository, ClientModel)

    def make_paginated_menu(self):
        return self.paginated_menu(
            find=self.repository.find_paginated_join_companies,
            find_by_id=self.repository.find_by_id_join_company
        )
