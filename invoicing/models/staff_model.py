from model_validation.field import Field
from model_validation.validations import IsString, IsRequired, IsFloat
from models.base_model import BaseModel


class StaffModel(BaseModel):
    # id = Field([IsInteger()])
    first_name = Field([IsRequired(), IsString()])
    last_name = Field([IsRequired(), IsString()])
    job_title = Field([IsRequired(), IsString()])
    rate = Field([IsRequired(), IsFloat()])
