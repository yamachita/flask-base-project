import uuid

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from __project_name__.storage.services import storage


class MediaStorage(MethodView):

    decorators = [jwt_required()]

    allowed_formats = ['jpg', 'png', 'mp4']

    def get(self):

        media_format = request.args.get('media_format')

        if not media_format or media_format not in self.allowed_formats:
            return {'media_format': ['Must be one of: jpg, mp4, png']}, 401

        file_key = f'{uuid.uuid4().hex}.{media_format}'

        url = storage.put_url(file_key=file_key)

        return {'media_url': url, 'media_name': file_key}, 200
