from model_validation.field import StringField
from models.base_model import BaseModel


class CompanyModel(BaseModel):
    # Todo: find way all fields to be null or empty if not required
    name = StringField()
    address = StringField(nullable=True)
