from model_validation.field import StringField, RelationshipField
from model_validation.validations import IsRequired
from models.base_model import BaseModel
from models.company_model import CompanyModel
from relationships.base_relationship import BaseRelationship
from repository.company_repository import CompanyRepository


class ClientModel(BaseModel):
    fullname = StringField([IsRequired()])
    email = StringField()
    telephone = StringField()
    company_id = RelationshipField(
        BaseRelationship('Company', CompanyRepository, CompanyModel)
    )
