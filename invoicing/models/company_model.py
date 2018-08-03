from model_validation.field import Field
from model_validation.validations import IsRequired, IsString
from models.base_model import BaseModel


class CompanyModel(BaseModel):
    name = Field([IsRequired(), IsString()])
    address = Field([IsString()])
