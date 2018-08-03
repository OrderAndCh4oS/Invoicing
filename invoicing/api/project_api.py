from api.base_api import BaseAPI
from models.project_model import ProjectModel
from repository.project_repository import ProjectRepository


class ProjectAPI(BaseAPI):

    def __init__(self):
        super().__init__(ProjectRepository(), ProjectModel())
