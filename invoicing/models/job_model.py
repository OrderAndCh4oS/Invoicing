from model_validation.field import Field
from model_validation.validations import IsString, IsRequired, IsInteger, IsFloat
from models.base_model import BaseModel


class JobModel(BaseModel):
    # id = Field([IsInteger()])
    reference_code = Field([IsString()])
    title = Field([IsRequired(), IsString()])
    description = Field([IsString()])
    status_id = Field([IsRequired(), IsInteger()])
    assigned_to = Field([IsRequired(), IsInteger()])
    # created_at = Field([IsString()])
    deadline = Field([IsString()])
    estimated_time = Field([IsRequired(), IsFloat()])
    # actual_time = Field([IsFloat()])
    # billable_time = Field([IsFloat()])
    # quote_id = Field([IsInteger()])
    project_id = Field([IsInteger()])
    # invoice_id = Field([IsInteger()])
    # completed = Field([IsBoolean()])
