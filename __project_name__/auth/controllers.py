from flask.views import MethodView
import flask_jwt_extended as jwt

from __project_name__.auth.schemas import LoginInputSchema
from __project_name__.auth import auth_services
from __project_name__.user.schemas import UserOutputSchema
from __project_name__.base.services import validate_input


class Login(MethodView):

    @validate_input(LoginInputSchema)
    def post(self, data: LoginInputSchema):

        login = auth_services.login(
            password=data.password, email=data.email, username=data.username)

        if not login:
            return {'error': 'invalid email, username or password'}, 401

        user, token, refresh_token = login

        return {'user': UserOutputSchema.from_orm(user).dict(),
                'token': token,
                'refresh_token': refresh_token}, 200


class TokenRefresh(MethodView):

    decorators = [jwt.jwt_required(refresh=True)]

    def get(self):

        user_id = jwt.get_jwt_identity()
        user, token, refresh_token = auth_services.token_refresh(user_id)

        return {'user': UserOutputSchema.from_orm(user).dict(),
                'token': token,
                'refresh_token': refresh_token}, 200
