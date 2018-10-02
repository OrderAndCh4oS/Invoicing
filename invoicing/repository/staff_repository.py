from invoicing.repository.base_repository import BaseRepository


class StaffRepository(BaseRepository):
    def __init__(self):
        super().__init__('staff')
