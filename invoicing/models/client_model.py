from model_validation.field import Field
from model_validation.validations import IsString, IsRequired, IsInteger
from models.base_model import BaseModel


class ClientModel(BaseModel):
    id = Field([IsInteger()])
    fullname = Field([IsRequired(), IsString()])
    email = Field([IsString()])
    telephone = Field([IsString()])
    company = Field([IsInteger()])  # Todo validate relation exists
