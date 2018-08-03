from model_validation.field import Field
from model_validation.validations import IsRequired, IsString
from models.base_model import BaseModel


class CompanyModel(BaseModel):
    # Todo: find way all fields to be null or empty if not required
    # id = Field([IsInteger()])
    name = Field([IsRequired(), IsString()])
    address = Field([IsString()])
