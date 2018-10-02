from invoicing.api.base_api import BaseAPI
from invoicing.models.status_model import StatusModel
from invoicing.repository.status_repository import StatusRepository


class StatusAPI(BaseAPI):

    def __init__(self):
        super().__init__(StatusRepository(), StatusModel())
