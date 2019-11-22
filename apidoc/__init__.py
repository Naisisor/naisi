import os

from flask import Flask

from apidoc.apis.v1 import api_v1
from apidoc.decorators import logger_error
from apidoc.extensions import db, migrate
from apidoc.models import Role, User, Project, System, URL, APIDoc, Protocol, Method, ProjectCollect, SystemCollect, \
    URLCollect
from apidoc.response import response
from apidoc.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprint(app)
    register_errorhandlers(app)
    register_shell_context(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprint(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def register_errorhandlers(app):
    @app.errorhandler(400)
    @logger_error
    def bad_request(e):
        return response(code=e.code, message=e.description)

    @app.errorhandler(404)
    @logger_error
    def page_not_fount(e):
        return response(code=e.code, message=e.description)

    @app.errorhandler(500)
    @logger_error
    def internal_server_error(e):
        return response(code=e.code, message=e.description)

    @app.errorhandler(Exception)
    @logger_error
    def exception(e):
        error_code = hasattr(e, 'code') and e.code or 1
        if hasattr(e, 'description'):
            message = e.description
        else:
            message = e.args[0]
        return response(
            code=error_code,
            message=message)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db,
            Role=Role,
            User=User,
            Project=Project,
            System=System,
            URL=URL,
            APIDoc=APIDoc,
            Protocol=Protocol,
            Method=Method,
            ProjectCollect=ProjectCollect,
            SystemCollect=SystemCollect,
            URLCollect=URLCollect
        )
