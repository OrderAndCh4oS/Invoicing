from model_validation.field import StringField
from model_validation.validations import IsRequired
from models.base_model import BaseModel


class CompanyModel(BaseModel):
    # Todo: find way all fields to be null or empty if not required
    name = StringField([IsRequired()])
    address = StringField()
