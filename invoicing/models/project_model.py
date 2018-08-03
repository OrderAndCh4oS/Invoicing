from model_validation.field import Field
from model_validation.validations import IsString, IsInteger
from models.base_model import BaseModel


class ProjectModel(BaseModel):
    id = Field(IsInteger())
    reference_code = Field(IsString())
    date = Field(IsString())
    client = Field(IsInteger())  # Todo validate relation exists
