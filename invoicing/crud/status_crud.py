from crud.base_crud import BaseCrud
from models.status_model import StatusModel
from repository.status_repository import StatusRepository


class StatusCrud(BaseCrud):
    def __init__(self):
        super().__init__('Statuses', StatusRepository, StatusModel)
