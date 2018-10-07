from api.base_api import BaseAPI
from models.invoice_model import InvoiceModel
from repository.invoice_repository import InvoiceRepository


class InvoiceAPI(BaseAPI):

    def __init__(self):
        super().__init__(InvoiceRepository(), InvoiceModel())
