from flask import Blueprint
from __project_name__.auth.controllers import Login, TokenRefresh

auth_api = Blueprint('auth_api', __name__)

auth_api.add_url_rule(
    '/token', view_func=Login.as_view('token'))
auth_api.add_url_rule(
    '/token/refresh', view_func=TokenRefresh.as_view('refresh-token'))
