from functools import wraps
from typing import Generic, TypeVar, Type, Optional, List, Tuple, Union, Callable, Any

from flask import request
from pydantic import BaseModel

from __project_name__.base.models import BaseORMModel
from __project_name__.extensions import db


ModelType = TypeVar('ModelType', bound=BaseORMModel)
InputSchemaType = TypeVar('InputSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCRUDServices(Generic[ModelType, InputSchemaType, UpdateSchemaType]):

    ''' Base CRUD services '''

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, id: int) -> ModelType:
        return self.model.query.get_or_404(id)

    def get_by_filter(self, **kwargs) -> Optional[ModelType]:
        return self.model.query.filter_by(**kwargs).first()

    def get_all_by_filter(self, page: int = 1,
                          per_page: int = 100,
                          order_by: object = None,
                          **kwargs) -> Tuple[List[ModelType], Optional[str], Optional[str]]:

        pagination = self.model.query.filter_by(**kwargs).order_by(order_by).paginate(
            page=page, per_page=per_page, error_out=False)

        next_page = pagination.next_num if pagination.has_next else None
        prev_page = pagination.prev_num if pagination.has_prev else None

        return (pagination.items, next_page, prev_page, pagination.total)

    def get_all(self, page: int = 1, per_page: int = 100,
                order_by: object = None) -> Tuple[List[ModelType], Optional[str], Optional[str]]:

        pagination = self.model.query.order_by(order_by).paginate(
            page=page, per_page=per_page, error_out=False)

        next_page = pagination.next_num if pagination.has_next else None
        prev_page = pagination.prev_num if pagination.has_prev else None

        return (pagination.items, next_page, prev_page, pagination.total)

    def create(self, data: InputSchemaType) -> ModelType:

        model_instance = self.model(**data.dict())
        model_instance.save()
        return model_instance

    def update(self, model_instance: ModelType, data: UpdateSchemaType) -> ModelType:

        data_dict = data.dict(exclude_unset=True)

        for field in vars(model_instance):
            if field in data_dict:
                setattr(model_instance, field, data_dict[field])

        model_instance.update()
        return model_instance

    def delete(self, model: Union[ModelType, int]) -> None:

        if isinstance(model, int):
            self.model.query.filter_by(id=model).delete()
        else:
            db.session.delete(model)
        db.session.commit()


RFunc = Callable[..., Any]


def validate_input(data_schema: Type[BaseModel]) -> Callable[[RFunc], RFunc]:
    def decorator_validate_input(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            input_schema: BaseModel = data_schema.parse_obj(request.json)
            return func(*args, data=input_schema, **kwargs)
        return wrapper
    return decorator_validate_input
