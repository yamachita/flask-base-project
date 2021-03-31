import json

from flask import jsonify

from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


class AppExceptions:

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        @app.errorhandler(HTTPException)
        def handler(e):
            response = e.get_response()
            response.data = json.dumps({'code': e.code,
                                        'name': e.name,
                                        'description': e.description})
            response.content_type = 'application/json'
            response.status_code = e.code
            return response

        @app.errorhandler(ValidationError)
        def handler(e):
            return jsonify(e.errors()), 400

        @app.errorhandler(SQLAlchemyError)
        def handler(e):
            return {'errors': str(e.orig)}, 400


global_exceptions = AppExceptions()
