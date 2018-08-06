from model_validation.field import StringField, IntegerField
from models.base_model import BaseModel


class ProjectModel(BaseModel):
    reference_code = StringField(nullable=True)
    date = StringField(nullable=True)
    client_id = IntegerField()  # Todo validate relation exists
