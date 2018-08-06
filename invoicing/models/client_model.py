from model_validation.field import StringField, RelationshipField
from models.base_model import BaseModel
from models.company_model import CompanyModel
from relationships.base_relationship import BaseRelationship
from repository.company_repository import CompanyRepository


class ClientModel(BaseModel):
    fullname = StringField()
    email = StringField(nullable=True)
    telephone = StringField(nullable=True)
    company_id = RelationshipField(
        BaseRelationship('Company', CompanyRepository, CompanyModel)
    )  # Todo validate relation exists
