from flask import Blueprint, request

from app import db
from app.libs.common import is_contain_zh
from app.models import Method, Protocol
from app.response import response

api = Blueprint('methods', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_method(id):
    """ 获取方法信息 """
    method = Method.query.get_or_404(id)
    return response(data={'method': method.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_method(id):
    """ 删除方法 """
    method = Method.query.get_or_404(id)
    # TODO 增加权限控制
    if method.api_docs:
        return response(code=1, message='此方法已经被使用，请联系管理员')
    db.session.delete(id)
    db.session.commit()
    return response()


@api.route('/', methods=['POST'])
def new_method():
    """ 新建方法 """
    params = request.json
    name = params.get('name', '')
    protocol_id = params.get('protocol_id', 0)
    if not (name and protocol_id) or is_contain_zh(name):
        return response(code=1, message='参数错误，且方法名不能包含中文')
    protocol = Protocol.query.get_or_404(protocol_id)
    cap_name = name.upper()
    existed_method = protocol.methods.filter(Method.name == cap_name).first()
    if existed_method:
        return response(code=1, message=f'请求方式 {cap_name} 已存在请勿重复添加')
    method = Method(name=cap_name, protocol_id=protocol_id)
    db.session.add(method)
    db.session.commit()
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_method(id):
    """ 编辑方法 """
    method = Method.query.get_or_404(id)
    params = request.json
    name = params.get('name', '')
    protocol_id = params.get('protocol_id', 0)
    if not (name and protocol_id) or is_contain_zh(name):
        return response(code=1, message='参数错误，且方法名不能包含中文')
    protocol = Protocol.query.get_or_404(protocol_id)
    cap_name = name.upper()
    existed_method = protocol.methods.filter(Method.name == cap_name).first()
    if existed_method and existed_method.id != method.id:
        return response(code=1, message=f'请求方式 {cap_name} 已存在请勿重复添加')
    method.name = cap_name
    method.protocol_id = protocol_id
    db.session.add(method)
    db.session.commit()
    return response()
