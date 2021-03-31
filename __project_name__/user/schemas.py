from typing import Dict, Optional

from flask import url_for
from pydantic import BaseModel, EmailStr, AnyHttpUrl, validator

from __project_name__.base.schemas import BaseOutputSchema


class BaseUserSchema(BaseModel):

    name: str
    username: str
    email: EmailStr

    class Config:
        extra = 'forbid'


class UserInputSchema(BaseUserSchema):

    password: constr(regex=r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!#&]{6,6}$')

    class Config:
        extra = 'forbid'


class UserOutputSchema(BaseOutputSchema, BaseUserSchema):

    links: Dict[str, AnyHttpUrl] = []

    @validator('links', pre=True, always=True)
    def set_links(cls, v, values):
        links = {'self': url_for(
            'user_api.user_details', user_id=values['id'], _external=True)}
        return links


class UserUpdateSchema(BaseUserSchema):
    pass


class UserPartialUpdateSchema(BaseModel):

    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]

    class Config:
        extra = 'forbid'


class EmailSchema(BaseModel):

    email: EmailStr

    class Config:
        extra = 'forbid'


class PasswordSchema(BaseModel):

    password: constr(regex=r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!#&]{6,6}$')

    class Config:
        extra = 'forbid'


class NewPasswordSchema(BaseModel):

    password: constr(regex=r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!#&]{6,6}$')
    new_passowrd: constr(regex=r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!#&]{6,6}$')

    class Config:
        extra = 'forbid'
