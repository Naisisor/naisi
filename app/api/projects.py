from flask import Blueprint, request, current_app

from app import db
from app.models import Project, User, System
from app.response import response

api = Blueprint('projects', __name__)


@api.route('/', methods=['GET'])
def get_projects():
    """ 获取所有系统 """
    # TODO 增加分页功能
    projects = Project.query.order_by(Project.c_time.desc()).all()
    return response(data={'projects': [project.to_json() for project in projects]})


@api.route('/<int:id>', methods=['GET'])
def get_project(id):
    """ 获取项目 """
    project = Project.query.get_or_404(id)
    return response(data={'project': project.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    """ 删除项目 """
    # TODO 增加权限控制
    project = Project.query.get_or_404(id)
    if project.systems.count() > 0:
        return response(code=1, message='项目中存在系统，无法删除')
    db.session.delete(project)
    db.session.commit()
    return response(message='删除成功')


@api.route('/', methods=['POST'])
def new_project():
    """ 新建项目 """
    params = request.json
    name = params.get('name', None)
    desc = params.get('desc', '') if params.get('desc', '') else name
    supporter_id = params.get('supporter_id', 0)
    if not (name and supporter_id):
        return response(code=1, message='参数错误')
    exited_project = Project.query.filter_by(name=name).first()
    if exited_project:
        return response(code=1, message='项目已存在，请勿重复添加')
    supporter = User.query.get_or_404(supporter_id)
    project = Project(name=name,
                      desc=desc,
                      domain=params.get('domain', '{}'),
                      supporter_id=supporter.id)
    db.session.add(project)
    db.session.commit()
    return response(data={'project': project.to_json()})


@api.route('/<int:id>', methods=['PUT'])
def edit_project(id):
    """ 编辑项目 """
    project = Project.query.get_or_404(id)
    params = request.json
    name = params.get('name', '')
    supporter_id = params.get('supporter_id', 0)
    if not (name and supporter_id):
        return response(code=1, message='参数错误')
    existed_project = Project.query.filter_by(name=name).first()
    if existed_project and existed_project.id != project.id:
        return response(code=1, message='项目已存在，请勿重复添加')
    supporter = User.query.get_or_404(supporter_id)
    project.name = name
    project.desc = params.get('desc', '')
    project.domain = params.get('domain', '')
    project.supporter_id = supporter.id
    db.session.add(project)
    db.session.commit()
    return response()


@api.route('/<int:id>/systems/', methods=['GET'])
def get_project_systems(id):
    """ 获取项目下的项目集 """
    project = Project.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get(
        'per_page',
        current_app.config['API_DOC_PER_PAGE'],
        type=int)
    paginate = project.systems.order_by(System.id.desc()).paginate(
        page, per_page, error_out=False)
    data = {
        'systems': [s.to_json() for s in paginate.items],
        'count': paginate.total,
        'paginate': paginate.page
    }
    return response(data=data)
