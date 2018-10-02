from invoicing.repository.base_repository import BaseRepository


class CompanyRepository(BaseRepository):
    def __init__(self):
        super().__init__('company')
