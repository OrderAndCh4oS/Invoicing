from datetime import datetime

from model_validation.field import RelationshipField, Field
from model_validation.validations import IsString
from models.base_model import BaseModel
from models.client_model import ClientModel
from relationships.base_relationship import BaseRelationship
from repository.client_repository import ClientRepository


class ProjectModel(BaseModel):
    date = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
    client_id = RelationshipField(
        BaseRelationship('Client', ClientRepository, ClientModel)
    )
    # Todo: add one to many relationship type
