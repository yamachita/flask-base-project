from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from __project_name__.user.services import user_services
from __project_name__.base.services import validate_input
from __project_name__.extensions import limiter
from __project_name__.utils import filters
from __project_name__.middlewares.permissions import user_permission
from __project_name__.user.schemas import (
    EmailSchema, PasswordSchema,
    UserInputSchema, UserOutputSchema,
    UserUpdateSchema, UserPartialUpdateSchema,
    NewPasswordSchema)


class UserCurrent(MethodView):

    decorators = [jwt_required()]

    def get(self):

        user = user_services.get_by_id(get_jwt_identity())
        output_schema = filters.get_schema(query_string=request.args,
                                           schema_cls=UserOutputSchema)
        output_fields = filters.get_fields(request.args)

        response = output_schema.from_orm(user).dict(include=output_fields)

        return response, 200


class UserCreate(MethodView):

    decorators = [limiter.limit('6/minute')]

    @validate_input(UserInputSchema)
    def post(self, data: UserInputSchema):

        user = user_services.create(data)
        response = UserOutputSchema.from_orm(user).dict()
        return response, 201


class UserDetails(MethodView):

    decorators = [user_permission]

    def get(self, user_id: int):

        user = user_services.get_by_id(user_id)
        output_schema = filters.get_schema(query_string=request.args,
                                           schema_cls=UserOutputSchema)

        output_fields = filters.get_fields(request.args)

        response = output_schema.from_orm(user).dict(include=output_fields)

        return response, 201

    @validate_input(UserUpdateSchema)
    def put(self, user_id: int, data: UserUpdateSchema):

        user = user_services.get_by_id(user_id)
        user = user_services.update(model_instance=user, data=data)
        response = UserOutputSchema.from_orm(user).dict()
        return response, 200

    @validate_input(UserPartialUpdateSchema)
    def patch(self, user_id: int, data: UserPartialUpdateSchema):

        user = user_services.get_by_id(user_id)
        user = user_services.update(model_instance=user, data=data)
        response = UserOutputSchema.from_orm(user).dict()
        return response, 200

    def delete(self, user_id: int):

        user_services.delete(user_id)
        return {}, 204


class EmailPassword(MethodView):

    decorators = [limiter.limit('6/hour')]

    @validate_input(EmailSchema)
    def post(self, data: EmailSchema):

        user_services.reset_password_email(data.email)

        return {}, 204


class ResetPassword(MethodView):

    decorators = [jwt_required()]

    @validate_input(PasswordSchema)
    def patch(self, data: PasswordSchema):

        user_services.reset_password(get_jwt_identity(), data.password)

        return {}, 204


class ChangePassword(MethodView):

    decorators = [jwt_required()]

    @validate_input(NewPasswordSchema)
    def patch(self, data: NewPasswordSchema):

        if user_services.change_password(get_jwt_identity(),
                                         password=data.password,
                                         new_password=data.new_passowrd):
            return {}, 204

        return {'error': 'invalid password'}, 400
