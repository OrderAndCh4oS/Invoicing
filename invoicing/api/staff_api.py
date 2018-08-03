from api.base_api import BaseAPI
from models.staff_model import StaffModel
from repository.staff_repository import StaffRepository


class StaffAPI(BaseAPI):

    def __init__(self):
        super().__init__(StaffRepository(), StaffModel())
