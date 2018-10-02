from datetime import datetime

from invoicing.model_validation.field import ForeignKeyField, Field, StringField
from invoicing.model_validation.validations import IsString
from invoicing.models.base_model import BaseModel
from invoicing.models.client_model import ClientModel
from invoicing.relationships.base_relationship import BaseRelationship
from invoicing.repository.client_repository import ClientRepository


class ProjectModel(BaseModel):
    title = StringField()
    created_at = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
    client_id = ForeignKeyField(
        BaseRelationship('Client', ClientRepository, ClientModel)
    )
    # Todo: add one to many relationship type
