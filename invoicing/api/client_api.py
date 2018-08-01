from api.base_api import BaseAPI
from repository.client_repository import ClientRepository


class ClientAPI(BaseAPI):

    def __init__(self):
        super().__init__(ClientRepository())
