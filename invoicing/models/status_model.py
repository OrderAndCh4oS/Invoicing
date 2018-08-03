from model_validation.field import Field
from model_validation.validations import IsString
from models.base_model import BaseModel


class StatusModel(BaseModel):
    title = Field([IsString()])
    colour = Field([IsString()])
