from model_validation.field import StringField
from model_validation.validations import IsRequired
from models.base_model import BaseModel


class StatusModel(BaseModel):
    title = StringField([IsRequired()])
    colour = StringField([IsRequired()])
