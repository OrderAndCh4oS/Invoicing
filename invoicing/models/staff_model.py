from model_validation.field import FloatField, StringField
from models.base_model import BaseModel


class StaffModel(BaseModel):
    first_name = StringField()
    last_name = StringField()
    job_title = StringField()
    rate = FloatField()
