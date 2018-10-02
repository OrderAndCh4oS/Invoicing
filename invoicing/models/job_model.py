from datetime import datetime

from dateutil.relativedelta import relativedelta

from invoicing.model_validation.field import StringField, FloatField, Field, ForeignKeyField, \
    DateField
from invoicing.model_validation.validations import IsRequired, IsString
from invoicing.models.base_model import BaseModel
from invoicing.models.project_model import ProjectModel
from invoicing.models.staff_model import StaffModel
from invoicing.models.status_model import StatusModel
from invoicing.relationships.base_relationship import BaseRelationship
from invoicing.repository.project_repository import ProjectRepository
from invoicing.repository.staff_repository import StaffRepository
from invoicing.repository.status_repository import StatusRepository


class JobModel(BaseModel):
    project_id = ForeignKeyField(
        BaseRelationship('Project', ProjectRepository, ProjectModel)
    )
    title = StringField([IsRequired()])
    description = StringField([IsRequired()])
    estimated_time = FloatField([IsRequired()])
    deadline = DateField([IsRequired()],
                         default_value=(datetime.today() + relativedelta(months=1)).strftime("%d-%m-%y"))
    assigned_to = ForeignKeyField(
        BaseRelationship('Staff', StaffRepository, StaffModel)
    )
    status_id = ForeignKeyField(
        BaseRelationship('Status', StatusRepository, StatusModel)
    )
    created_at = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
