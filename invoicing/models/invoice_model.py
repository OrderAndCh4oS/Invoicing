from model_validation.field import StringField, IntegerField
from model_validation.validations import IsRequired
from models.base_model import BaseModel


class InvoiceModel(BaseModel):
    reference_code = StringField([IsRequired()])
    date = StringField()
    client_id = IntegerField([IsRequired()])  # Todo validate relation exists
