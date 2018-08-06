from model_validation.field import Field, StringField, IntegerField
from model_validation.validations import IsString
from models.base_model import BaseModel


class InvoiceModel(BaseModel):
    reference_code = Field([IsString()])
    date = StringField(nullable=True)
    client_id = IntegerField()  # Todo validate relation exists
