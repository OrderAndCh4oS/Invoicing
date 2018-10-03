from datetime import datetime

from invoicing.model_validation.field import ForeignKeyField, Field, StringField
from invoicing.model_validation.validations import IsString
from invoicing.models.base_model import BaseModel
from invoicing.models.company_model import CompanyModel
from invoicing.relationships.base_relationship import BaseRelationship
from invoicing.repository.company_repository import CompanyRepository


class ProjectModel(BaseModel):
    title = StringField()
    created_at = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
    company_id = ForeignKeyField(
        BaseRelationship('Company', CompanyRepository, CompanyModel)
    )
    # Todo: add one to many relationship type
