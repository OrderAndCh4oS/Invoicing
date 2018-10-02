from invoicing.model_validation.field import FloatField, StringField
from invoicing.model_validation.validations import IsRequired
from invoicing.models.base_model import BaseModel


class StaffModel(BaseModel):
    first_name = StringField([IsRequired()])
    last_name = StringField([IsRequired()])
    job_title = StringField([IsRequired()])
    rate = FloatField([IsRequired()])
