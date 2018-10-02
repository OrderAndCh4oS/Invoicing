from datetime import datetime

from invoicing.model_validation.field import Field, ForeignKeyField, OneToManyField
from invoicing.model_validation.validations import IsString
from invoicing.models.base_model import BaseModel
from invoicing.models.client_model import ClientModel
from invoicing.models.job_model import JobModel
from invoicing.relationships.base_relationship import BaseRelationship, OneToManyRelationship
from invoicing.repository.client_repository import ClientRepository
from invoicing.repository.job_repository import JobRepository
from invoicing.ui.pagination import Pagination


def job_paginated_menu():
    job_repository = JobRepository()
    return Pagination(job_repository)(
        find=job_repository.find_paginated_join_staff_and_status,
        find_by_id=lambda id: job_repository.find_by_id(id, (
            'id', 'reference_code', 'title',
            'estimated_time', 'actual_time', 'deadline',
            'assigned_to', 'status_id'
        )))


class InvoiceModel(BaseModel):
    client_id = ForeignKeyField(
        BaseRelationship('Client', ClientRepository, ClientModel)
    )
    job = OneToManyField(
        OneToManyRelationship('invoice_id', 'Job', JobRepository, JobModel, paginated_menu=job_paginated_menu)
    )
    created_at = Field([IsString()], initial_value=datetime.now().strftime("%Y-%m-%d %H:%M"), updatable=False)
