from invoicing.api.base_api import BaseAPI
from invoicing.models.staff_model import StaffModel
from invoicing.repository.staff_repository import StaffRepository


class StaffAPI(BaseAPI):

    def __init__(self):
        super().__init__(StaffRepository(), StaffModel())
