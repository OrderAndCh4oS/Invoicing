from invoicing.model_validation.field import StringField
from invoicing.model_validation.validations import IsRequired
from invoicing.models.base_model import BaseModel


class CompanyModel(BaseModel):
    # Todo: find way all fields to be null or empty if not required
    name = StringField([IsRequired()])
    address = StringField()
