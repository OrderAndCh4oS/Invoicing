from datetime import datetime

from model_validation.field import StringField, IntegerField, FloatField, BooleanField, Field, RelationshipField
from model_validation.validations import IsRequired, IsString
from models.base_model import BaseModel
from models.invoice_model import InvoiceModel
from models.project_model import ProjectModel
from relationships.base_relationship import BaseRelationship
from repository.invoice_repository import InvoiceRepository
from repository.project_repository import ProjectRepository


class JobModel(BaseModel):
    title = StringField([IsRequired()])
    description = StringField([IsRequired()])
    assigned_to = IntegerField([IsRequired()])
    status_id = IntegerField([IsRequired()])
    deadline = StringField([IsRequired()])
    estimated_time = FloatField([IsRequired()])
    actual_time = FloatField()
    billable_time = FloatField()
    project_id = RelationshipField(
        BaseRelationship('Project', ProjectRepository, ProjectModel)
    )
    invoice_id = RelationshipField(
        BaseRelationship('Invoice', InvoiceRepository, InvoiceModel)
    )
    date = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
    completed = BooleanField()
