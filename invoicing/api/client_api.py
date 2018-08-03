from api.base_api import BaseAPI
from models.client_model import ClientModel
from repository.client_repository import ClientRepository


class ClientAPI(BaseAPI):

    def __init__(self):
        super().__init__(ClientRepository(), ClientModel())
