import json
from datetime import datetime

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash

from apidoc.extensions import db


class Role(db.Model):
    """ 角色表 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class ProjectCollect(db.Model):
    """ 用户关注的项目的关系表 """
    __tablename__ = 'project_collect'
    collector_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    collected_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        'User',
        back_populates='project_collections',
        lazy='joined')
    project = db.relationship(
        'Project',
        back_populates='project_collectors',
        lazy='joined')


class SystemCollect(db.Model):
    """ 用户关注的系统的关系表 """
    __tablename__ = 'system_collect'
    collector_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    collected_id = db.Column(
        db.Integer,
        db.ForeignKey('systems.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        'User',
        back_populates='system_collections',
        lazy='joined')
    system = db.relationship(
        'System',
        back_populates='system_collectors',
        lazy='joined')


class URLCollect(db.Model):
    """ 用户关注的 url 的关系表 """
    __tablename__ = 'url_collect'
    collector_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True)
    collected_id = db.Column(
        db.Integer,
        db.ForeignKey('urls.id'),
        primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        'User',
        back_populates='url_collections',
        lazy='joined')
    url = db.relationship(
        'URL',
        back_populates='url_collectors',
        lazy='joined')


class User(db.Model):
    """ 用户表 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    projects = db.relationship(
        'Project',
        back_populates='supporter',
        lazy='dynamic')
    systems = db.relationship(
        'System',
        back_populates='supporter',
        lazy='dynamic')
    urls = db.relationship('URL', back_populates='supporter', lazy='dynamic')
    api_docs = db.relationship('APIDoc', back_populates='editor')
    project_collections = db.relationship(
        'ProjectCollect',
        back_populates='user',
        cascade='all,delete-orphan')
    system_collections = db.relationship(
        'SystemCollect',
        back_populates='user',
        cascade='all, delete-orphan')
    url_collections = db.relationship(
        'URLCollect',
        back_populates='user',
        cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'id': self.id,
            'email': self.email,
            'name': self.name or self.username,
            'username': self.username,
            'avatar': '',
            'projects_url': url_for(
                endpoint='api_v1.support-projects',
                user_id=self.id,
                _external=True),
            'systems_url': url_for(
                endpoint='api_v1.support-systems',
                user_id=self.id,
                _external=True),
            'urls_url': url_for(
                endpoint='api_v1.support-urls',
                user_id=self.id,
                _external=True)}
        return json_user


class Project(db.Model):
    """ 项目列表 """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.Text, default='')
    domains = db.Column(db.Text)
    c_time = db.Column(db.DateTime, default=datetime.utcnow)
    supporter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    supporter = db.relationship('User', back_populates='projects')
    systems = db.relationship(
        'System',
        back_populates='project',
        cascade='all',
        lazy='dynamic')
    project_collectors = db.relationship(
        'ProjectCollect',
        back_populates='project',
        cascade='all, delete-orphan')

    def to_json(self, author=True):
        json_project = {
            'id': self.id,
            'name': self.name or '',
            'desc': self.desc or self.name,
            'domains': json.loads(self.domains or '[]'),
            'create_time': str(self.c_time)
        }
        if author is True:
            json_project['supporter'] = self.supporter.to_json()
        return json_project


class System(db.Model):
    """ 系统列表 """
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.Text)
    domains = db.Column(db.Text, comment="列表 json 串，包含 dev、test、stage、online 环境")
    c_time = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    supporter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    supporter = db.relationship('User', back_populates='systems')
    project = db.relationship('Project', back_populates='systems')
    urls = db.relationship(
        'URL',
        back_populates='system',
        cascade='all',
        lazy='dynamic')
    system_collectors = db.relationship(
        'SystemCollect',
        back_populates='system',
        cascade='all, delete-orphan')

    def to_json(self):
        json_system = {
            'id': self.id,
            'name': self.name or '',
            'desc': self.desc or self.name,
            'domains': json.loads(self.domains or '[]'),
            'create_time': str(self.c_time),
            'project': self.project.to_json(author=False),
            'supporter': self.supporter.to_json()
        }
        return json_system


class Protocol(db.Model):
    """ 协议 """
    __tablename__ = 'protocols'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, comment='协议名称')

    urls = db.relationship('URL', back_populates='protocol', cascade='all')
    methods = db.relationship(
        'Method',
        back_populates='protocol',
        lazy='dynamic')

    def to_json(self):
        json_protocol = {
            'id': self.id,
            'name': self.name,
            'methods': [method.to_json() for method in self.methods]
        }
        return json_protocol


class Method(db.Model):
    """ 请求方式列表 """
    __tablename__ = 'methods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    protocol_id = db.Column(db.Integer, db.ForeignKey('protocols.id'))

    protocol = db.relationship('Protocol', back_populates='methods')
    api_docs = db.relationship('APIDoc', back_populates='method')

    def to_json(self):
        json_method = {
            'id': self.id,
            'name': self.name,
            'protocol': {
                'id': self.protocol.id,
                'name': self.protocol.name
            }
        }
        return json_method


class URL(db.Model):
    """ 接口列表 """
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(128), index=True)
    desc = db.Column(db.String(128), default='')
    c_time = db.Column(db.DateTime, default=datetime.utcnow)
    protocol_id = db.Column(db.Integer, db.ForeignKey('protocols.id'))
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    supporter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    supporter = db.relationship('User', back_populates='urls')
    protocol = db.relationship('Protocol', back_populates='urls')
    system = db.relationship('System', back_populates='urls')
    api_docs = db.relationship('APIDoc', back_populates='url', lazy='dynamic', cascade='all')
    url_collectors = db.relationship(
        'URLCollect',
        back_populates='url',
        cascade='all, delete-orphan')

    def to_json(self):
        json_url = {
            'id': self.id,
            'path': self.path,
            'desc': self.desc or '',
            'create_time': str(self.c_time),
            'protocol': self.protocol.to_json(),
            'supporter': self.supporter.to_json()
        }
        return json_url


class APIDoc(db.Model):
    __tablename__ = 'api_docs'
    id = db.Column(db.Integer, primary_key=True)
    request_params = db.Column(db.Text, comment='请求参数')
    resp_params = db.Column(db.Text, comment='响应参数')
    resp_body = db.Column(db.Text, comment='响应体 json 字符串')
    edit_time = db.Column(db.DateTime, default=datetime.utcnow)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    editor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    editor = db.relationship('User', back_populates='api_docs')
    url = db.relationship('URL', back_populates='api_docs')
    method = db.relationship('Method', back_populates='api_docs')

    def to_json(self):
        json_api_doc = {
            'id': self.id,
            'request_param': self.request_param,
            'response_param': self.response_param,
            'response_body': self.response_body,
            'edit_time': str(self.edit_time),
            'editor': self.editor.to_json(),
            'url_details': url_for('api_v1.urls', url_id=self.url_id, _external=True)
        }
        if self.method is not None:
            json_api_doc['method'] = self.method.to_json()
        return json_api_doc


@db.event.listens_for(APIDoc.edit_time, 'set', named=True)
def update_edit_time(**kwargs):
    """ 更新接口文档的编辑时间 """
    target = kwargs.get('target')
    if target.edit_time is not None:
        target.edit_time = datetime.utcnow()
