from datetime import datetime

from dateutil.relativedelta import relativedelta

from model_validation.field import StringField, FloatField, Field, ForeignKeyField, \
    DateField
from model_validation.validations import IsRequired, IsString
from models.base_model import BaseModel
from models.project_model import ProjectModel
from models.staff_model import StaffModel
from models.status_model import StatusModel
from relationships.base_relationship import BaseRelationship
from repository.project_repository import ProjectRepository
from repository.staff_repository import StaffRepository
from repository.status_repository import StatusRepository


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
