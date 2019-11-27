from flask.views import MethodView
from webargs.flaskparser import use_kwargs

from apidoc.apis.v1 import api_v1
from apidoc.extensions import db
from apidoc.libs.args_schema import PaginateSchema, PASysSchema
from apidoc.models import System, Project, User
from apidoc.response import response


class SystemsAPI(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, project_id, page, per_page):
        """ 获取项目下的项目集 """
        project = Project.query.get_or_404(project_id)
        paginate = project.systems.order_by(System.id.desc()).paginate(
            page, per_page, error_out=False)
        data = {
            'systems': [s.to_json() for s in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)

    @use_kwargs(PASysSchema)
    def post(self, project_id, name, desc, domains, supporter_id):
        """ 新建系统 """
        project = Project.query.get_or_404(project_id)
        supporter = User.query.get_or_404(supporter_id)

        existed_system = project.systems.filter(System.name == name).first()
        if existed_system:
            return response(code=1, message=f'系统 {name} 已存在，请勿重复添加')

        system = System(name=name,
                        desc=desc,
                        domains=domains,
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
        # TODO 增加权限控制，当系统下存在 apis 接口文档则不允许删除
        System.query.filter_by(id=sys_id).delete(synchronize_session=False)
        db.session.commit()
        return response()

    @use_kwargs(PASysSchema)
    def put(self, sys_id, name, desc, domains, supporter_id, project_id):
        """ 编辑系统 """
        system = System.query.get_or_404(sys_id)
        supporter = User.query.get_or_404(supporter_id)
        project = Project.query.get_or_404(project_id)

        existed_system = project.systems.filter(System.name == name).first()
        if existed_system and existed_system.id != system.id:
            return response(code=1, message=f'系统 {name} 已存在，请勿重复添加')

        system.name = name
        system.desc = desc,
        system.domains = domains
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
