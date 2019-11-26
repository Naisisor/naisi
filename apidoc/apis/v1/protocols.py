from flask import request
from flask.views import MethodView

from apidoc.apis.v1 import api_v1
from apidoc.extensions import db
from apidoc.libs.common import is_contain_zh
from apidoc.models import Protocol
from apidoc.response import response


class ProtocolsAPI(MethodView):

    def get(self):
        return response()

    def post(self):
        """ 新建协议 """
        params = request.json
        name = params.get('name', '')
        if not name or is_contain_zh(name):
            return response(code=1, message='协议名不能为空且不能包含中文')
        cap_name = name.upper()
        existed_protocol = Protocol.query.filter_by(name=cap_name).first()
        if existed_protocol:
            return response(code=1, message='协议名已存在，请勿重复添加')
        protocol = Protocol(name=cap_name)
        db.session.add(protocol)
        db.session.commit()
        return response()


class ProtocolAPI(MethodView):

    def get(self, protocol_id):
        """ 获取协议 """
        protocol = Protocol.query.get_or_404(id)
        return response(data={'protocol': protocol.to_json()})

    def delete(self, protocol_id):
        """ 删除协议 """
        # TODO 增加权限控制
        return response()

    def put(self, protocol_id):
        """ 编辑协议 """
        protocol = Protocol.query.get_or_404(id)
        params = request.json
        name = params.get('name', '')
        if not name or is_contain_zh(name):
            return response(code=1, message='协议名不能为空且不能包含中文')
        cap_name = name.upper()
        existed_protocol = Protocol.query.filter_by(name=cap_name).first()
        if existed_protocol and existed_protocol.id != protocol.id:
            return response(code=1, message='协议名已存在，请勿重复添加')
        protocol.name = cap_name
        db.session.add(protocol)
        db.session.commit()
        return response()

    def patch(self, protocol_id):
        return response()


api_v1.add_url_rule('/protocols', view_func=ProtocolsAPI.as_view('protocols'),
                    methods=['GET', 'POST'])
api_v1.add_url_rule('/protocols/<int:protocol_id>', view_func=ProtocolAPI.as_view('protocol'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
