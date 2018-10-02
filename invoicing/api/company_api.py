from invoicing.api.base_api import BaseAPI
from invoicing.models.company_model import CompanyModel
from invoicing.repository.company_repository import CompanyRepository


class CompanyAPI(BaseAPI):

    def __init__(self):
        super().__init__(CompanyRepository(), CompanyModel())
