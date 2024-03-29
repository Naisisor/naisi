import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler
from pathlib import Path

import click
from flask import Flask, request
from flask_sqlalchemy import get_debug_queries

from apidoc.apis.main import main_bp
from apidoc.apis.v1 import api_v1
from apidoc.decorators import logger_error
from apidoc.extensions import db, migrate, toolbar
from apidoc.models import Role, User, Project, System, URL, APIDoc, Protocol, Method, ProjectCollect, SystemCollect, \
    URLCollect
from apidoc.response import response
from apidoc.settings import config

basedir = Path(__file__).absolute().parent.parent


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_logging(app)
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_request_handlers(app)
    return app


def register_logging(app):
    log_path = basedir / 'logs'

    if log_path.is_dir() is False:
        log_path.mkdir()

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
    file_handler = RotatingFileHandler(log_path / 'api-doc.log',
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
    migrate.init_app(app, db)
    toolbar.init_app(app)


def register_blueprint(app):
    app.register_blueprint(main_bp, url_profix='/')
    app.register_blueprint(api_v1, url_prefix='/api/v1')


def register_errorhandlers(app):  # noqa
    @app.errorhandler(400)
    @logger_error
    def bad_request(e):
        return response(code=e.code, message=e.description)

    @app.errorhandler(404)
    @logger_error
    def page_not_fount(e):
        return response(code=e.code, message=e.description)

    @app.errorhandler(422)
    @logger_error
    def handle_validation_error(e):
        exc = e.exc

        message = ''
        for k, v in exc.messages.items():
            message += f'参数 {k} {" ".join(v)} '

        return response(code=e.code, message=message)

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


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--project', default=50, help='Quantity of projects, default is 10.')
    @click.option('--system', default=50, help='Quantity of systems, default is 50.')
    def forge(project, system):
        """Generate fake data."""
        from apidoc.fakes import fake_admin, fake_projects, fake_systems

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d projects...' % project)
        fake_projects(project)

        click.echo('Generating %d systems...' % system)
        fake_systems(system)


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            app.logger.warning(
                'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                % (q.duration, q.context, q.statement)
            )
        return response
