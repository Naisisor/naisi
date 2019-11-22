from flask import request
from flask.views import MethodView

from apidoc.extensions import db
from apidoc.apis.v1 import api_v1
from apidoc.libs.common import is_contain_zh
from apidoc.models import URL, System, User, Protocol
from apidoc.response import response


class URLsAPI(MethodView):
    def get(self, sys_id):
        """ 获取项目下的项目集 """
        system = System.query.get_or_404(sys_id)
        urls = system.urls.all()
        return response(data={'urls': [u.to_json() for u in urls]})

    def post(self, sys_id):
        """ 新建 URL"""
        system = System.query.get_or_404(sys_id)
        params = request.json
        path = params.get('path', '').strip().replace(' ', '')
        protocol_id = params.get('protocol_id', 0)
        supporter_id = params.get('supporter_id', 0)
        if not (params and protocol_id and sys_id and supporter_id) and is_contain_zh(path):
            return response(code=1, message='参数错误，且接口中不能包含中文')
        protocol = Protocol.query.get_or_404(protocol_id)
        supporter = User.query.get_or_404(supporter_id)

        # 判断 path 是否存在
        exited_url = system.urls.filter(URL.path == path).first()
        if exited_url:
            return response(code=1, message=f'{path} 已存在，请勿重复添加')

        url = URL(
            path=path,
            desc=params.get('desc'),
            protocol_id=protocol.id,
            system_id=system.id,
            supporter_id=supporter.id)
        db.session.add(url)
        db.session.commit()
        return response()


class URLAPI(MethodView):
    def get(self, url_id):
        """ 获取 URL 详情 """
        url = URL.query.get_or_404(url_id)
        return response(data={'url': url.to_json()})

    def delete(self, url_id):
        """ 删除 URL """
        URL.query.filter_by(id=url_id).delete(synchronize_session=False)
        return response()

    def put(self, url_id):
        """ 编辑 url """
        url = URL.query.get_or_404(url_id)
        params = request.json
        path = params.get('path', '').strip().replace(' ', '')
        protocol_id = params.get('protocol_id', 0)
        system_id = params.get('system_id', 0)
        supporter_id = params.get('supporter_id', 0)
        if not (params and protocol_id and system_id and supporter_id) and is_contain_zh(path):
            return response(code=1, message='参数错误，且接口中不能包含中文')
        protocol = Protocol.query.get_or_404(protocol_id)
        system = System.query.get_or_404(system_id)
        supporter = User.query.get_or_404(supporter_id)

        # 判断 path 是否存在
        existed_url = system.urls.filter(URL.path == path).first()
        if existed_url and existed_url.id != url.id:
            return response(code=1, message=f'{path} 已存在，请勿重复添加')

        url.path = path
        url.desc = params.get('desc'),
        url.protocol_id = protocol.id,
        url.system_id = system.id,
        url.supporter_id = supporter.id
        db.session.add(url)
        db.session.commit()
        return response()

    def patch(self, url_id):
        return response()


api_v1.add_url_rule('/systems/<int:sys_id>/urls',
                    view_func=URLsAPI.as_view('urls'),
                    methods=['GET', 'POST'])
api_v1.add_url_rule('/url/<int:url_id>', view_func=URLAPI.as_view('url'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
