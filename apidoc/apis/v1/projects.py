from flask.views import MethodView
from webargs.flaskparser import use_kwargs

from apidoc.apis.v1 import api_v1
from apidoc.extensions import db
from apidoc.libs.args_schema import PASysSchema
from apidoc.models import Project, User
from apidoc.response import response


class ProjectsAPI(MethodView):

    def get(self):
        """ 获取所有项目 """
        projects = Project.query.order_by(Project.c_time.desc()).all()
        return response(data={'projects': [project.to_json() for project in projects]})

    @use_kwargs(PASysSchema)
    def post(self, name, desc, domains, supporter_id):
        """ 新增项目 """
        exited_project = Project.query.filter_by(name=name).first()
        if exited_project:
            return response(code=1, message='项目已存在，请勿重复添加')

        supporter = User.query.get_or_404(supporter_id)
        project = Project(name=name,
                          desc=desc,
                          domains=domains,
                          supporter_id=supporter.id)
        db.session.add(project)
        db.session.commit()
        return response(data={'project': project.to_json()})


class ProjectAPI(MethodView):

    def get(self, project_id):
        """ 获取项目信息 """
        project = Project.query.get_or_404(project_id)
        return response(data={'project': project.to_json()})

    def delete(self, project_id):
        """ 删除项目 """
        # TODO 增加权限控制
        project = Project.query.get_or_404(project_id)
        if project.systems.count() > 0:
            return response(code=1, message='项目中存在系统，无法删除')
        db.session.delete(project)
        db.session.commit()
        return response(message='删除成功')

    @use_kwargs(PASysSchema)
    def put(self, project_id, name, desc, domains, supporter_id):
        """ 编辑项目 """
        project = Project.query.get_or_404(project_id)

        existed_project = Project.query.filter_by(name=name).first()
        if existed_project and existed_project.id != project.id:
            return response(code=1, message='项目已存在，请勿重复添加')

        supporter = User.query.get_or_404(supporter_id)
        project.name = name
        project.desc = desc
        project.domains = domains
        project.supporter_id = supporter.id
        db.session.add(project)
        db.session.commit()
        return response(data={'project': project.to_json()})

    def patch(self, project_id):
        """ 修改项目某一项参数 """
        Project.query.get_or_404(project_id)
        return response()


api_v1.add_url_rule('/projects',
                    view_func=ProjectsAPI.as_view('projects'),
                    methods=['GET', 'POST'])
api_v1.add_url_rule('/projects/<project_id>', view_func=ProjectAPI.as_view('project'),
                    methods=['GET', 'PUT', 'PATCH', 'DELETE'])
