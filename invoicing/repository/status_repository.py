from invoicing.repository.base_repository import BaseRepository


class StatusRepository(BaseRepository):
    def __init__(self):
        super().__init__('status')
