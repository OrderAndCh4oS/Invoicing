from model_validation.field import Field
from model_validation.validations import IsString, IsInteger
from models.base_model import BaseModel


class StatusModel(BaseModel):
    id = Field([IsInteger()], nullable=True)
    title = Field([IsString()])
    colour = Field([IsString()])
