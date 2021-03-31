from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from __project_name__.user.services import user_services


def user_permission(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = user_services.get_by_id(get_jwt_identity())
        if kwargs.get('user_id') != user.id and user.is_admin == False:
            return {'error': 'Unauthorized user'}, 401
        else:
            return func(*args, **kwargs)
    return wrapper
