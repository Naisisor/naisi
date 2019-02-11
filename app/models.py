from datetime import datetime

from . import db


class Role(db.Model):
    """ 角色表 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class User(db.Model):
    """ 用户表 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    projects = db.relationship('Project', back_populates='creator')
    systems = db.relationship('System', back_populates='creator')


class Project(db.Model):
    """ 项目列表 """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='projects')
    systems = db.relationship('System', back_populates='project')


class System(db.Model):
    """ 系统列表 """
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    user = db.relationship('User', back_populates='systems')
    project = db.relationship('Project', back_populates='systems')
    uri = db.relationship('URI', back_populates='system')


class URI(db.Model):
    """ 接口列表 """
    __tablename__ = 'uri'
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(128), unique=True, index=True)
    desc = db.Column(db.String(128))
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))

    system = db.relationship('System', back_populates='uri')
    api_docs = db.relationship('APIDocs', back_populates='uri')


class Method(db.Model):
    """ 请求方式列表 """
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    api_docs = db.relationship('APIDocs', back_populates='method')


class APIDocs(db.Model):
    __tablename__ = 'api_docs'
    id = db.Column(db.Integer, primary_key=True)
    request_param = db.Column(db.Text)
    uri_id = db.Column(db.Integer, db.ForeignKey('uri.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'))

    uri = db.relationship('URI', back_populates='api_docs')
    method = db.relationship('Method', back_populates='api_docs')
