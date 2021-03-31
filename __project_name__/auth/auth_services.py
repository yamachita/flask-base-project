from typing import Tuple, Optional
from datetime import timedelta

import flask_jwt_extended as jwt

from __project_name__.config import config
from __project_name__.user.models import User
from __project_name__.user.services import user_services


def login(password: str, email: str = None, username: str = None) -> Optional[Tuple[User, str, str]]:

    if email:
        user = user_services.get_by_filter(email=email)
    elif username:
        user = user_services.get_by_filter(username=username)
    else:
        return None

    if not user or not user.verify_password(password):
        return None

    token = jwt.create_access_token(
        identity=user.id,
        expires_delta=timedelta(minutes=config.JWT_EXPIRATION_TIME),
        fresh=True)

    refresh_token = jwt.create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(minutes=config.JWT_REFRESH_EXPIRATION_TIME))

    return user, token, refresh_token


def token_refresh(user_id: int) -> Tuple[User, str, str]:

    user = user_services.get_by_id(id=user_id)

    token = jwt.create_access_token(
        identity=user.id,
        expires_delta=timedelta(minutes=config.JWT_EXPIRATION_TIME),
        fresh=True)

    refresh_token = jwt.create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(minutes=config.JWT_REFRESH_EXPIRATION_TIME))

    return user, token, refresh_token
