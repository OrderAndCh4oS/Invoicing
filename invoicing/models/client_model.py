from model_validation.field import StringField, IntegerField
from models.base_model import BaseModel


class ClientModel(BaseModel):
    fullname = StringField()
    email = StringField(nullable=True)
    telephone = StringField(nullable=True)
    company_id = IntegerField()  # Todo validate relation exists
