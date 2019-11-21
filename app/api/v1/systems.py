from flask import request, current_app
from flask.views import MethodView

from app import db
from app.api.v1 import api_v1
from app.models import System, Project, User
from app.response import response


class SystemsAPI(MethodView):
    def get(self, project_id):
        """ 获取项目下的项目集 """
        project = Project.query.get_or_404(project_id)
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

    def post(self, project_id):
        """ 新建系统 """
        project = Project.query.get_or_404(project_id)
        params = request.json
        name = params.get('name', '')
        supporter_id = params.get('supporter_id', 0)
        if not (name and supporter_id and project_id):
            return response(code=1, message='参数不能为空')
        supporter = User.query.get_or_404(supporter_id)
        existed_system = project.systems.filter(System.name == name).first()
        if existed_system:
            return response(code=1, message=f'系统 {name} 已存在，请勿重复添加')
        system = System(name=name,
                        desc=params.get('desc', ''),
                        domains=params.get('domains', '[]'),
                        project_id=project.id,
                        supporter_id=supporter.id)
        db.session.add(system)
        db.session.commit()
        return response(data={'system': system.to_json()})


class SystemAPI(MethodView):
    def get(self, sys_id):
        """ 获取系统信息 """
        system = System.query.get_or_404(sys_id)
        return response(data={'system': system.to_json()})

    def delete(self, sys_id):
        """ 删除系统 """
        # TODO 增加权限控制，当系统下存在 api 接口文档则不允许删除
        System.query.filter_by(id=sys_id).delete(synchronize_session=False)
        return response()

    def put(self, sys_id):
        """ 编辑系统 """
        system = System.query.get_or_404(sys_id)
        params = request.json
        name = params.get('name', '')
        supporter_id = params.get('supporter_id', 0)
        project_id = params.get('project_id', 0)
        if not (name and supporter_id and project_id):
            return response(code=1, message='参数不能为空')
        supporter = User.query.get_or_404(supporter_id)
        project = Project.query.get_or_404(project_id)
        existed_system = project.systems.filter(System.name == name).first()
        if existed_system and existed_system.id != system.id:
            return response(code=1, message=f'系统 {name} 已存在，请勿重复添加')
        system.name = name
        system.desc = params.get('desc', ''),
        system.domains = params.get('domains', '[]')
        system.project_id = project.id
        system.supporter_id = supporter.id
        db.session.add(system)
        db.session.commit()
        return response(data={'system': system.to_json()})

    def patch(self, sys_id):
        return response()


api_v1.add_url_rule('/projects/<int:project_id>/systems', view_func=SystemsAPI.as_view('systems'),
                    methods=['GET', 'POST'])
api_v1.add_url_rule('/systems/<int:sys_id>', view_func=SystemAPI.as_view('system'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
