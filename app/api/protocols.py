from flask import Blueprint, request

from app import db
from app.libs.common import is_contain_zh
from app.models import Protocol
from app.response import response

api = Blueprint('protocols', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_protocol(id):
    """ 获取协议 """
    project = Protocol.query.get_or_404(id)
    return response(data={'protocol': project.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_protocol(id):
    """ 删除协议 """
    # TODO 增加权限控制
    return response()


@api.route('/', methods=['POST'])
def new_protocol():
    """ 新建协议 """
    params = request.json
    name = params.get('name', '')
    if not name or is_contain_zh(name):
        return response(code=1, user_message='协议名不能为空且不能包含中文')
    cap_name = name.upper()
    existed_protocol = Protocol.query.filter_by(name=cap_name).first()
    if existed_protocol:
        return response(code=1, user_message='协议名已存在，请勿重复添加')
    protocol = Protocol(name=cap_name)
    db.session.add(protocol)
    db.session.commit()
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_protocol(id):
    """ 编辑协议 """
    protocol = Protocol.query.get_or_404(id)
    params = request.json
    name = params.get('name', '')
    if not name or is_contain_zh(name):
        return response(code=1, user_message='协议名不能为空且不能包含中文')
    cap_name = name.upper()
    existed_protocol = Protocol.query.filter_by(name=cap_name).first()
    if existed_protocol and existed_protocol.id != protocol.id:
        return response(code=1, user_message='协议名已存在，请勿重复添加')
    protocol.name = cap_name
    db.session.add(protocol)
    db.session.commit()
    return response()
