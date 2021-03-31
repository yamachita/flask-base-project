from typing import Optional
from pydantic import BaseSettings, AnyHttpUrl, Field, PostgresDsn


class Config(BaseSettings):

    # Project
    PROJECT_NAME: str

    # Storage
    STORAGE_ACCESS_KEY_ID: str
    STORAGE_SECRET_ACCESS_KEY: str
    STORAGE_REGION: str
    STORAGE_BUCKET_ENDPOINT: AnyHttpUrl
    STORAGE_BUCKET_NAME: str
    STORAGE_BUCKET_FOLDER: str

    # JWT (min)
    JWT_EXPIRATION_TIME: int = 15
    JWT_REFRESH_EXPIRATION_TIME: int = 30

    # Requests limiter
    DEFAULT_LIMITS: str = '1000/day'


class FlaskConfig(BaseSettings):

    # App
    SECRET_KEY: str
    JSON_SORT_KEYS: bool = False

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JWT_SECRET_KEY: str = Field(..., env='SECRET_KEY')

    # Mail
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False

    # Max input size
    MAX_CONTENT_LENGTH: Optional[int] = None


class DevConfig(FlaskConfig):

    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = Field(
        None, env='DEV_DATABASE_URI')


class TestConfig(FlaskConfig):

    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = Field(
        None, env='TEST_DATABASE_URI')


class StagingConfig(FlaskConfig):

    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = Field(
        None, env='STAGING_DATABASE_URI')


class ProductionConfig(FlaskConfig):

    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = Field(
        None, env='PROD_DATABASE_URI')


config = Config()
flask_config = {'DEV': DevConfig(),
                'TEST': TestConfig(),
                'STAGING': StagingConfig(),
                'PRODUCTION': ProductionConfig()}
