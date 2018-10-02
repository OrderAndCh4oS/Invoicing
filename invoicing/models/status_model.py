from invoicing.model_validation.field import StringField
from invoicing.model_validation.validations import IsRequired
from invoicing.models.base_model import BaseModel


class StatusModel(BaseModel):
    title = StringField([IsRequired()])
    colour = StringField([IsRequired()])
