from invoicing.crud.base_crud import BaseCrud
from invoicing.models.company_model import CompanyModel
from invoicing.repository.company_repository import CompanyRepository


class CompanyCrud(BaseCrud):
    def __init__(self):
        super().__init__('Companies', CompanyRepository, CompanyModel)
