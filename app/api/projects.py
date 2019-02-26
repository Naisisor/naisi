from flask import Blueprint, request

from app import db
from app.models import Project, User
from app.response import response

api = Blueprint('projects', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_project(id):
    """ 获取项目 """
    project = Project.query.get_or_404(id)
    return response(data={'project': project.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    """ 删除项目 """
    # TODO 增加权限控制
    return response()


@api.route('/', methods=['POST'])
def new_project():
    """ 新建项目 """
    params = request.json
    name = params.get('name', None)
    supporter_id = params.get('supporter_id', 0)
    if not (name and supporter_id):
        return response(code=1, user_message='参数错误')
    exited_project = Project.query.filter_by(name=name).first()
    if exited_project:
        return response(code=1, user_message='项目已存在，请勿重复添加')
    supporter = User.query.get_or_404(supporter_id)
    project = Project(name=name,
                      desc=params.get('desc', ''),
                      domain=params.get('domain', '{}'),
                      supporter_id=supporter.id)
    db.session.add(project)
    db.session.commit()
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_project(id):
    """ 编辑项目 """
    project = Project.query.get_or_404(id)
    params = request.json
    name = params.get('name', '')
    supporter_id = params.get('supporter_id', 0)
    if not (name and supporter_id):
        return response(code=1, user_message='参数错误')
    existed_project = Project.query.filter_by(name=name).first()
    if existed_project and existed_project.id != project.id:
        return response(code=1, user_message='项目已存在，请勿重复添加')
    supporter = User.query.get_or_404(supporter_id)
    project.name = name
    project.desc = params.get('desc', '')
    project.domain = params.get('domain', '')
    project.supporter_id = supporter.id
    db.session.add(project)
    db.session.commit()
    return response()
