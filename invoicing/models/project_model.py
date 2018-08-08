from datetime import datetime

from model_validation.field import ForeignKeyField, Field, StringField
from model_validation.validations import IsString
from models.base_model import BaseModel
from models.client_model import ClientModel
from relationships.base_relationship import BaseRelationship
from repository.client_repository import ClientRepository


class ProjectModel(BaseModel):
    title = StringField()
    created_at = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
    client_id = ForeignKeyField(
        BaseRelationship('Client', ClientRepository, ClientModel)
    )
    # Todo: add one to many relationship type
