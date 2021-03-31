from typing import Generic, TypeVar, Optional, List
from datetime import datetime

from pydantic import BaseModel, create_model
from pydantic.generics import GenericModel


DataT = TypeVar('DataT', bound=BaseModel)


class BaseOutputSchema(BaseModel):

    id: int
    create_time: Optional[datetime]
    update_time: Optional[datetime]

    class Config:
        orm_mode = True
        extra = 'forbid'

    @classmethod
    def add_fields(cls, **fields):
        return create_model('NewModel', __base__=cls, **fields)


class BaseListSchema(GenericModel, Generic[DataT]):

    __root__: List[DataT]

    class Config:
        orm_mode = True
