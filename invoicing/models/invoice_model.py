from datetime import datetime

from model_validation.field import Field, ForeignKeyField, OneToManyField
from model_validation.validations import IsString
from models.base_model import BaseModel
from models.client_model import ClientModel
from models.job_model import JobModel
from relationships.base_relationship import BaseRelationship, OneToManyRelationship
from repository.client_repository import ClientRepository
from repository.job_repository import JobRepository


class InvoiceModel(BaseModel):
    client_id = ForeignKeyField(
        BaseRelationship('Client', ClientRepository, ClientModel)
    )
    job = OneToManyField(
        OneToManyRelationship('invoice_id', 'Job', JobRepository, JobModel)
    )
    created_at = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
