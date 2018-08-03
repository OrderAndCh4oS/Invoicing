from model_validation.field import Field
from model_validation.validations import IsString, IsInteger
from models.base_model import BaseModel


class ClientModel(BaseModel):
    fullname = Field([IsString()])
    email = Field([IsString()], nullable=True)
    telephone = Field([IsString()], nullable=True)
    company_id = Field([IsInteger()])  # Todo validate relation exists
