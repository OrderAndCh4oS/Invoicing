from model_validation.field import Field
from model_validation.validations import IsString, IsFloat
from models.base_model import BaseModel


class StaffModel(BaseModel):
    first_name = Field([IsString()])
    last_name = Field([IsString()])
    job_title = Field([IsString()])
    rate = Field([IsFloat()])
