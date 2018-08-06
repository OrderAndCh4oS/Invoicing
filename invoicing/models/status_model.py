from model_validation.field import StringField
from models.base_model import BaseModel


class StatusModel(BaseModel):
    title = StringField()
    colour = StringField()
