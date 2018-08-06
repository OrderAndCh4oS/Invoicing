from crud.base_crud import BaseCrud
from crud.client_crud import ClientCrud
from models.company_model import CompanyModel
from repository.company_repository import CompanyRepository


class CompanyCrud(BaseCrud):
    def __init__(self):
        super().__init__('Companies', CompanyRepository, CompanyModel)

    # Todo: See if this can be removed
    # def make_paginated_data(self, limit, page):
    #     return {"data": self.repository.find_paginated(limit=limit, page=page),
    #             "headers": self.repository.get_headers()}

    def remove_relations(self, id):
        ClientCrud().delete_clients_by_company_id(id)
