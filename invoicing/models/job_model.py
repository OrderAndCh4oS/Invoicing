from model_validation.field import StringField, IntegerField, FloatField, BooleanField
from models.base_model import BaseModel


class JobModel(BaseModel):
    reference_code = StringField(nullable=True)
    title = StringField()
    description = StringField()
    assigned_to = IntegerField()
    status_id = IntegerField()
    deadline = StringField()
    estimated_time = FloatField()
    actual_time = FloatField(nullable=True)
    billable_time = FloatField(nullable=True)
    project_id = IntegerField()
    quote_id = IntegerField(nullable=True)
    invoice_id = IntegerField(nullable=True)
    created_at = StringField(nullable=True)
    completed = BooleanField(nullable=True)
