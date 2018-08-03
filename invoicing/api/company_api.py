from api.base_api import BaseAPI
from models.company_model import CompanyModel
from repository.company_repository import CompanyRepository


class CompanyAPI(BaseAPI):

    def __init__(self):
        super().__init__(CompanyRepository(), CompanyModel())
