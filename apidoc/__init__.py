import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask, request

from apidoc.apis.v1 import api_v1
from apidoc.decorators import logger_error
from apidoc.extensions import db, migrate, login_manager
from apidoc.models import Role, User, Project, System, URL, APIDoc, Protocol, Method, ProjectCollect, SystemCollect, \
    URLCollect
from apidoc.response import response
from apidoc.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprint(app)
    register_errorhandlers(app)
    register_shell_context(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
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
