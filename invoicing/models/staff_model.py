from model_validation.field import Field
from model_validation.validations import IsString, IsFloat, IsInteger
from models.base_model import BaseModel


class StaffModel(BaseModel):
    id = Field([IsInteger()], nullable=True)
    first_name = Field([IsString()])
    last_name = Field([IsString()])
    job_title = Field([IsString()])
    rate = Field([IsFloat()])
