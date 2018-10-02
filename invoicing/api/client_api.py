from invoicing.api.base_api import BaseAPI
from invoicing.models.client_model import ClientModel
from invoicing.repository.client_repository import ClientRepository


class ClientAPI(BaseAPI):

    def __init__(self):
        super().__init__(ClientRepository(), ClientModel())
