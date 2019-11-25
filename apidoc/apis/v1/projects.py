from flask import request
from flask.views import MethodView

from apidoc.extensions import db
from apidoc.apis.v1 import api_v1
from apidoc.models import Project, User
from apidoc.response import response


class ProjectsAPI(MethodView):

    def get(self):
        """ 获取所有项目 """
        projects = Project.query.order_by(Project.c_time.desc()).all()
        return response(data={'projects': [project.to_json() for project in projects]})

    def post(self):
        """ 新增项目 """
        params = request.json
        name = params.get('name', None)
        desc = params.get('desc', '')
        supporter_id = params.get('supporter_id', 0)
        if not (name and supporter_id):
            return response(code=1, message='参数错误')
        exited_project = Project.query.filter_by(name=name).first()
        if exited_project:
            return response(code=1, message='项目已存在，请勿重复添加')
        supporter = User.query.get_or_404(supporter_id)
        project = Project(name=name,
                          desc=desc,
                          domains=params.get('domains', '[]'),
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

    def put(self, project_id):
        """ 编辑项目 """
        project = Project.query.get_or_404(project_id)
        params = request.json
        name = params.get('name', '')
        supporter_id = params.get('supporter_id', 0)
        if not (name and supporter_id):
            return response(code=1, message='参数错误')
        existed_project = Project.query.filter_by(name=name).first()
        if existed_project and existed_project.id != project.id:
            return response(code=1, message='项目已存在，请勿重复添加')
        supporter = User.query.get_or_404(supporter_id)
        project.name = name
        project.desc = params.get('desc', '')
        project.domains = params.get('domains', '[]')
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
