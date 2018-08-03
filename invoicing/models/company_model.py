from model_validation.field import Field
from model_validation.validations import IsString
from models.base_model import BaseModel


class CompanyModel(BaseModel):
    # Todo: find way all fields to be null or empty if not required
    name = Field([IsString()])
    address = Field([IsString()], nullable=True)
