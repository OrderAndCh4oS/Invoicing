from api.base_api import BaseAPI
from models.job_model import JobModel
from repository.job_repository import JobRepository


class JobAPI(BaseAPI):

    def __init__(self):
        super().__init__(JobRepository(), JobModel())
