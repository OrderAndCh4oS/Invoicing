from model_validation.field import Field
from model_validation.validations import IsRequired, IsString, MinLength, MaxLength
from models.base_model import BaseModel


class Company(BaseModel):
    name = Field([IsRequired(), IsString()])
    address = Field([IsString()])


if __name__ == '__main__':
    valid = Field([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='Hey there')
    required = Field([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='')
    not_string = Field([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value=123)
    too_long = Field([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='Hey there shit head')
    too_short = Field([IsRequired(), IsString(), MaxLength(10), MinLength(3)], default_value='Hi')
    print('Valid: %s' % valid.validate())
    print('Required: %s' % required.validate())
    print('Not a String: %s' % not_string.validate())
    print('Too Long: %s' % too_long.validate())
    print('Too Short: %s' % too_short.validate())
    company = Company(name='John', address='A street', oh_no='blah')
    company.validate()
    print('Valid company:', company)
    invalid_company = Company(name='', address=26)
    invalid_company.validate()
    print('Invalid company:', invalid_company)
