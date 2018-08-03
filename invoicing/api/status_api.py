from api.base_api import BaseAPI
from models.status_model import StatusModel
from repository.status_repository import StatusRepository


class StatusAPI(BaseAPI):

    def __init__(self):
        super().__init__(StatusRepository(), StatusModel())
