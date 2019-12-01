import os
from pathlib import Path

basedir = Path(__file__).absolute().parent.parent


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_COMMIT_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PWD = os.environ.get('DATABASE_PWD')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.exmail.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    API_DOC_MAIL_SUBJECT_PREFIX = '[接口文档]'
    API_DOC_MAIL_SENDER = f'APIDocs <{MAIL_USERNAME}>'
    API_DOC_ADMIN = os.environ.get('FLASKY_ADMIN')
    API_DOC_PER_PAGE = 20
    API_DOC_SLOW_QUERY_THRESHOLD = 1

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{os.environ.get("DB_PWD")}@localhost/api_doc?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{os.environ.get("DB_PWD")}@localhost/api_doc?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{os.environ.get("DB_PWD")}@localhost/api_doc?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
