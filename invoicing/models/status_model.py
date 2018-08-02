from model_validation.field import Field
from model_validation.validations import IsString, IsRequired, IsInteger
from models.base_model import BaseModel


class ClientModel(BaseModel):
    title = Field(IsRequired(), IsString())
    color = Field(IsRequired(), IsString())
    id = Field(IsInteger())  # Todo validate relation exists
