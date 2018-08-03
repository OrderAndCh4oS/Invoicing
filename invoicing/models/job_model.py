from model_validation.field import Field
from model_validation.validations import IsString, IsInteger, IsFloat, IsBoolean
from models.base_model import BaseModel


class JobModel(BaseModel):
    reference_code = Field([IsString()], nullable=True)
    title = Field([IsString()])
    description = Field([IsString()])
    status_id = Field([IsInteger()])
    assigned_to = Field([IsInteger()])
    created_at = Field([IsString()], nullable=True)
    deadline = Field([IsString()])
    estimated_time = Field([IsFloat()])
    actual_time = Field([IsFloat()], nullable=True)
    billable_time = Field([IsFloat()], nullable=True)
    quote_id = Field([IsInteger()], nullable=True)
    project_id = Field([IsInteger()])
    invoice_id = Field([IsInteger()], nullable=True)
    completed = Field([IsBoolean()], nullable=True)
