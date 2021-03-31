import datetime

import bcrypt
import flask_jwt_extended as jwt

from __project_name__.base.models import BaseORMModel
from __project_name__.extensions import db


class User(BaseORMModel):

    __tablename__ = 'users'

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.LargeBinary(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password) -> None:
        self.password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash)

    def token(self, time: int = 600) -> str:
        return jwt.create_access_token(
            identity=self.id,
            expires_delta=datetime.timedelta(minutes=time))
