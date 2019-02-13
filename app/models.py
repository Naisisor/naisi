from datetime import datetime

from . import db


class Role(db.Model):
    """ 角色表 """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


class ProjectCollect(db.Model):
    """ 用户关注的项目的关系表 """
    __tablename__ = 'project_collect'
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    collector = db.relationship('User', back_populates='project_collections', lazy='joined')
    collected = db.relationship('Project', back_populates='project_collectors', lazy='joined')


class SystemCollect(db.Model):
    """ 用户关注的系统的关系表 """
    __tablename__ = 'system_collect'
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('systems.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    collector = db.relationship('User', back_populates='system_collections', lazy='joined')
    collected = db.relationship('System', back_populates='system_collectors', lazy='joined')


class URICollect(db.Model):
    """ 用户关注的 uri 的关系表 """
    __tablename__ = 'uri_collect'
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('uri.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    collector = db.relationship('User', back_populates='uri_collections', lazy='joined')
    collected = db.relationship('URI', back_populates='uri_collectors', lazy='joined')


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
    uri = db.relationship('URI', back_populates='creator')
    api_docs = db.relationship('APIDoc', back_populates='editor')
    project_collections = db.relationship('ProjectCollect', back_populates='collector', cascade='all,delete-orphan')
    system_collections = db.relationship('SystemCollect', back_populates='collector', cascade='all, delete-orphan')
    uri_collections = db.relationship('URICollect', back_populates='collector', cascade='all, delete-orphan')

    def to_json(self):
        json_user = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'username': self.username
        }
        return json_user


class Project(db.Model):
    """ 项目列表 """
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128), default='')
    hosts = db.Column(db.Text)
    c_time = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('User', back_populates='projects')
    systems = db.relationship('System', back_populates='project', cascade='all')
    project_collectors = db.relationship('ProjectCollect', back_populates='collected', cascade='all, delete-orphan')

    def to_json(self):
        json_project = {
            'id': self.id,
            'name': self.name or '',
            'desc': self.desc,
            'hosts': self.hosts,
            'create_time': str(self.c_time),
            'creator': self.creator.name
        }
        return json_project


class System(db.Model):
    """ 系统列表 """
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128))
    hosts = db.Column(db.Text, comment="json 串，包含 dev、test、stage、online 环境")
    c_time = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    creator = db.relationship('User', back_populates='systems')
    project = db.relationship('Project', back_populates='systems')
    uri = db.relationship('URI', back_populates='system', cascade='all')
    system_collectors = db.relationship('SystemCollect', back_populates='collected', cascade='all, delete-orphan')

    def to_json(self):
        json_system = {
            'id': self.id,
            'name': self.name or '',
            'desc': self.desc,
            'hosts': self.hosts,
            'create_time': str(self.c_time),
            'creator': self.creator.name
        }
        return json_system


class Protocol(db.Model):
    """ 协议 """
    __tablename__ = 'protocols'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), comment='协议名称')

    uri = db.relationship('URI', back_populates='protocol', cascade='all')
    methods = db.relationship('Method', back_populates='protocol')

    def to_json(self):
        json_protocol = {
            'id': self.id,
            'name': self.methods
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
            'name': self.name
        }
        return json_method


class URI(db.Model):
    """ 接口列表 """
    __tablename__ = 'uri'
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(128), unique=True, index=True)
    desc = db.Column(db.String(128))
    c_time = db.Column(db.DateTime, default=datetime.utcnow)
    protocol_id = db.Column(db.Integer, db.ForeignKey('protocols.id'))
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('User', back_populates='uri')
    protocol = db.relationship('Protocol', back_populates='uri')
    system = db.relationship('System', back_populates='uri')
    api_docs = db.relationship('APIDoc', back_populates='uri', cascade='all')
    uri_collectors = db.relationship('URICollect', back_populates='collected', cascade='all, delete-orphan')

    def to_json(self):
        json_uri = {
            'id': self.id,
            'name': self.name or '',
            'desc': self.desc,
            'hosts': self.hosts,
            'create_time': str(self.c_time),
            'creator': self.creator.name
        }
        return json_uri


class APIDoc(db.Model):
    __tablename__ = 'api_docs'
    id = db.Column(db.Integer, primary_key=True)
    request_param = db.Column(db.Text, comment='请求参数')
    response_param = db.Column(db.Text, comment='响应参数')
    response_body = db.Column(db.Text, comment='响应体 json 字符串')
    edit_time = db.Column(db.DateTime, default=datetime.utcnow)
    uri_id = db.Column(db.Integer, db.ForeignKey('uri.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))
    editor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    editor = db.relationship('User', back_populates='api_docs')
    uri = db.relationship('URI', back_populates='api_docs')
    method = db.relationship('Method', back_populates='api_docs')

    def to_json(self):
        json_api_doc = {
            'id': self.id,
            'name': self.name or '',
            'desc': self.desc,
            'hosts': self.hosts,
            'edit_time': str(self.edit_time),
            'editor': self.editor.name
        }
        return json_api_doc


@db.event.listens_for(APIDoc.edit_time, 'set', named=True)
def update_edit_time(**kwargs):
    """ 更新接口文档的编辑时间 """
    target = kwargs.get('target')
    if target.edit_time is not None:
        target.edit_time = datetime.utcnow()
