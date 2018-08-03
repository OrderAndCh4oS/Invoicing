from model_validation.field import Field
from model_validation.validations import IsString, IsInteger
from models.base_model import BaseModel


class InvoiceModel(BaseModel):
    # id = Field([IsInteger()])
    reference_code = Field([IsString()])
    date = Field([IsString()], nullable=True)
    client = Field([IsInteger()])  # Todo validate relation exists
