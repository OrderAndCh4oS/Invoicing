from crud.base_crud import BaseCrud
from models.company_model import CompanyModel
from repository.company_repository import CompanyRepository


class CompanyCrud(BaseCrud):
    def __init__(self):
        super().__init__('Companies', CompanyRepository, CompanyModel)
