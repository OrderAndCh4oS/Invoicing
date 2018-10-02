from invoicing.crud.base_crud import BaseCrud
from invoicing.models.status_model import StatusModel
from invoicing.repository.status_repository import StatusRepository


class StatusCrud(BaseCrud):
    def __init__(self):
        super().__init__('Statuses', StatusRepository, StatusModel)
