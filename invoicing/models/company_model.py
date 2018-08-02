from model_validation.field import Field
from model_validation.validations import IsRequired, IsString
from models.base_model import BaseModel


class Company(BaseModel):
    name = Field([IsRequired(), IsString()])
    address = Field([IsString()])
