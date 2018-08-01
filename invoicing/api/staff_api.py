from api.base_api import BaseAPI
from repository.staff_repository import StaffRepository


class StaffAPI(BaseAPI):

    def __init__(self):
        super().__init__(StaffRepository())
