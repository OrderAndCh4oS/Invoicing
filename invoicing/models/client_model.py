from invoicing.model_validation.field import StringField, ForeignKeyField
from invoicing.model_validation.validations import IsRequired
from invoicing.models.base_model import BaseModel
from invoicing.models.company_model import CompanyModel
from invoicing.relationships.base_relationship import BaseRelationship
from invoicing.repository.company_repository import CompanyRepository


class ClientModel(BaseModel):
    fullname = StringField([IsRequired()])
    email = StringField()
    telephone = StringField()
    company_id = ForeignKeyField(
        BaseRelationship('Company', CompanyRepository, CompanyModel)
    )
