from flask import request
from flask.views import MethodView

from apidoc.extensions import db
from apidoc.apis.v1 import api_v1
from apidoc.libs.common import is_contain_zh
from apidoc.models import Method, Protocol
from apidoc.response import response


class MethodsAPI(MethodView):
    def get(self, protocol_id):
        protocol = Protocol.query.get_or_404(protocol_id)
        return response(data={'methods': [m.to_json() for m in protocol.methods]})

    def post(self, protocol_id):
        """ 新建方法 """
        params = request.json
        name = params.get('name', '')
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


class MethodAPI(MethodView):
    def get(self, m_id):
        """ 获取方法信息 """
        method = Method.query.get_or_404(id)
        return response(data={'method': method.to_json()})

    def delete(self, m_id):
        """ 删除方法 """
        method = Method.query.get_or_404(m_id)
        # TODO 增加权限控制
        if method.api_docs:
            return response(code=1, message='此方法已经被使用，请联系管理员')
        db.session.delete(method)
        db.session.commit()
        return response()

    def put(self, m_id):
        """ 编辑方法 """
        method = Method.query.get_or_404(m_id)
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

    def patch(self, m_id):
        return response()


api_v1.add_url_rule('/protocols/<int:protocol_id>/methods', view_func=MethodsAPI.as_view('methods'),
                    methods=['GET', 'POST'])
api_v1.add_url_rule('/methods/<int:m_id>', view_func=MethodAPI.as_view('method'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
