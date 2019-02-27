from flask import Blueprint, request

from app import db
from app.models import System, Project, User
from app.response import response

api = Blueprint('systems', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_system(id):
    """ 获取系统信息 """
    system = System.query.get_or_404(id)
    return response(data={'system': system.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_system(id):
    """ 删除系统 """
    # TODO 增加权限控制
    System.query.filter_by(id=id).delete(synchronize_session=False)
    return response()


@api.route('/', methods=['POST'])
def new_system():
    """ 新建系统 """
    params = request.json
    name = params.get('name', '')
    supporter_id = params.get('supporter_id', 0)
    project_id = params.get('project_id', 0)
    if not (name and supporter_id and project_id):
        return response(code=1, user_message='参数不能为空')
    supporter = User.query.get_or_404(supporter_id)
    project = Project.query.get_or_404(project_id)
    existed_system = project.systems.filter(System.name == name).first()
    if existed_system:
        return response(code=1, user_message=f'系统 {name} 已存在，请勿重复添加')
    system = System(name=name,
                    desc=params.get('desc', ''),
                    domain=params.get('domain', ''),
                    project_id=project.id,
                    supporter_id=supporter.id)
    db.session.add(system)
    db.session.commit()
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_system(id):
    """ 删除系统 """
    system = System.query.get_or_404(id)
    params = request.json
    name = params.get('name', '')
    supporter_id = params.get('supporter_id', 0)
    project_id = params.get('project_id', 0)
    if not (name and supporter_id and project_id):
        return response(code=1, user_message='参数不能为空')
    supporter = User.query.get_or_404(supporter_id)
    project = Project.query.get_or_404(project_id)
    existed_system = project.systems.filter(System.name == name).first()
    if existed_system and existed_system.id != system.id:
        return response(code=1, user_message=f'系统 {name} 已存在，请勿重复添加')
    system.name = name
    system.desc = params.get('desc', ''),
    system.domain = params.get('domain', '')
    system.project_id = project.id
    system.supporter_id = supporter.id
    db.session.add(system)
    db.session.commit()
    return response()
