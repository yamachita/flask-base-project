from flask import Blueprint

from __project_name__.user.controllers import (
    UserCurrent, UserCreate, UserDetails,
    EmailPassword, ChangePassword, ResetPassword)

user_api = Blueprint('user_api', __name__)

user_api.add_url_rule(
    '/users/current', view_func=UserCurrent.as_view('user_current'), methods=['GET'])
user_api.add_url_rule(
    '/users', view_func=UserCreate.as_view('user_create'), methods=['POST'])
user_api.add_url_rule(
    '/users/<int:user_id>', view_func=UserDetails.as_view('user_details'))
user_api.add_url_rule(
    '/pw/email', view_func=EmailPassword.as_view('email_reset'), methods=['POST'])
user_api.add_url_rule(
    '/pw/reset', view_func=ResetPassword.as_view('pw_reset'))
user_api.add_url_rule(
    '/pw/change', view_func=ChangePassword.as_view('pw_change'))
