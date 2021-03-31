from flask import Flask

from __project_name__.config import flask_config

from __project_name__.extensions import db, migrate, jwt, mail, limiter
from __project_name__.exceptions import global_exceptions
from __project_name__.boilerplate.commands import create_api, init_project

from __project_name__.user.routes import user_api
from __project_name__.auth.routes import auth_api


def create_app(config_name):

    ### Application ###
    app = Flask(__name__)
    app.config.from_object(flask_config[config_name])

    ### Commands ###
    app.cli.add_command(create_api)
    app.cli.add_command(init_project)

    ### Throttle ###
    limiter.init_app(app)

    ### Exceptions ###
    global_exceptions.init_app(app)

    ### Database ###
    db.init_app(app)
    migrate.init_app(app, db)

    ### JWT ###
    jwt.init_app(app)

    ### Mail ###
    mail.init_app(app)

    ### BluePrints ###
    app.register_blueprint(user_api)
    app.register_blueprint(auth_api)

    return app
