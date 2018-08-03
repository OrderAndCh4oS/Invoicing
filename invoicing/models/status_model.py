from model_validation.field import Field
from model_validation.validations import IsString, IsRequired, IsInteger
from models.base_model import BaseModel


class StatusModel(BaseModel):
    id = Field(IsInteger())
    title = Field(IsRequired(), IsString())
    color = Field(IsRequired(), IsString())
