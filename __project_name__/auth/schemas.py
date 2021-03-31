from typing import Optional
from pydantic import BaseModel, EmailStr, root_validator


class LoginInputSchema(BaseModel):

    email: Optional[EmailStr]
    username: Optional[str]
    password: constr(regex=r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!#&]{6,8}$')

    @root_validator
    def validate_email_username(cls, values):
        if values.get('email') is None and values.get('username') is None:
            raise ValueError('email or username required')
        return values
