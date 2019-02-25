from flask import Blueprint, request

from app import db
from app.models import URL, System, User, Protocol
from app.response import response

api = Blueprint('urls', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_url(id):
    url = URL.query.get_or_404(id)
    return response(data={'url': url.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_url(id):
    URL.query.filter_by(id=id).delete(synchronize_session=False)
    return response()


@api.route('/', methods=['POST'])
def new_url():
    params = request.json
    path = params.get('path', '').strip().replace(' ', '')
    protocol_id = params.get('protocol_id', 0)
    system_id = params.get('system_id', 0)
    supporter_id = params.get('supporter_id', 0)
    if not (params and protocol_id and system_id and supporter_id):
        return response(code=1, user_message='参数错误')
    protocol = Protocol.query.get_or_404(protocol_id)
    system = System.query.get_or_404(system_id)
    supporter = User.query.get_or_404(supporter_id)

    # 判断 path 是否存在
    exited_url = system.urls.filter(URL.path == path).first()
    if exited_url:
        return response(code=1, user_message=f'{path} 已存在，请勿重复添加')

    url = URL(
        path=path,
        desc=params.get('desc'),
        protocol_id=protocol.id,
        system_id=system.id,
        supporter_id=supporter.id)
    db.session.add(url)
    db.session.commit()
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_url(id):
    url = URL.query.get_or_404(id)
    params = request.json
    path = params.get('path', '').strip().replace(' ', '')
    protocol_id = params.get('protocol_id', 0)
    system_id = params.get('system_id', 0)
    supporter_id = params.get('supporter_id', 0)
    if not (params and protocol_id and system_id and supporter_id):
        return response(code=1, user_message='参数错误')
    protocol = Protocol.query.get_or_404(protocol_id)
    system = System.query.get_or_404(system_id)
    supporter = User.query.get_or_404(supporter_id)

    # 判断 path 是否存在
    exited_url = system.urls.filter(URL.path == path).first()
    if exited_url and exited_url.id != url.id:
        return response(code=1, user_message=f'{path} 已存在，请勿重复添加')

    url.path = path
    url.desc = params.get('desc'),
    url.protocol_id = protocol.id,
    url.system_id = system.id,
    url.supporter_id = supporter.id
    db.session.add(url)
    db.session.commit()
    return response()
