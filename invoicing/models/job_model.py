from model_validation.field import StringField, IntegerField, FloatField, BooleanField
from model_validation.validations import IsRequired
from models.base_model import BaseModel


class JobModel(BaseModel):
    reference_code = StringField()
    title = StringField([IsRequired()])
    description = StringField([IsRequired()])
    assigned_to = IntegerField([IsRequired()])
    status_id = IntegerField([IsRequired()])
    deadline = StringField([IsRequired()])
    estimated_time = FloatField([IsRequired()])
    actual_time = FloatField()
    billable_time = FloatField()
    project_id = IntegerField([IsRequired()])
    quote_id = IntegerField()
    invoice_id = IntegerField()
    created_at = StringField()
    completed = BooleanField()
