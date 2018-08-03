from model_validation.field import Field
from model_validation.validations import IsString, IsInteger
from models.base_model import BaseModel


class ProjectModel(BaseModel):
    id = Field([IsInteger()], nullable=True)
    reference_code = Field([IsString()])
    date = Field([IsString()], nullable=True)
    client_id = Field([IsInteger()])  # Todo validate relation exists
