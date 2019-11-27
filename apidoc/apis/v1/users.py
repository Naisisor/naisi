from flask import g
from flask.views import MethodView
from webargs.flaskparser import use_kwargs

from apidoc.apis.v1 import api_v1
from apidoc.apis.v1.auth import auth_required
from apidoc.libs.args_schema import PaginateSchema
from apidoc.models import User, ProjectCollect, URLCollect, SystemCollect
from apidoc.response import response


class UsersAPI(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, page, per_page):
        paginate = User.query.paginate(page, per_page, error_out=False)
        data = {
            'projects': [p.to_json() for p in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)

    def post(self):
        return response()


class UserAPI(MethodView):
    decorators = [auth_required]

    def get(self, user_id):
        """ 获取用户信息 """
        if user_id == g.current_user.id:
            user = g.current_user
        else:
            user = User.query.get(user_id)
        if not user:
            return response(code=1, message='用户不存在')
        return response(data={'user': user.to_json()})

    def post(self):
        return response()


class UserSupportProjects(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, user_id, page, per_page):
        """ 获取用户所创建的项目 """
        user = User.query.get_or_404(user_id)
        paginate = user.projects.paginate(
            page, per_page, error_out=False)
        data = {
            'projects': [p.to_json() for p in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserSupportSystems(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, user_id, page, per_page):
        """ 获取用户所创建的系统 """
        user = User.query.get_or_404(user_id)
        paginate = user.systems.paginate(
            page, per_page, error_out=False)
        data = {
            'systems': [s.to_json() for s in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserSupportURLs(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, user_id, page, per_page):
        """ 获取用户所创建的 uri """
        user = User.query.get_or_404(user_id)
        paginate = user.urls.paginate(
            page, per_page, error_out=False)
        data = {
            'urls': [u.to_json() for u in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserCollectionProjects(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, user_id, page, per_page):
        """ 获取用户收藏的项目 """
        user = User.query.get_or_404(user_id)
        paginate = ProjectCollect.query.with_parent(user).order_by(
            ProjectCollect.timestamp.desc()).paginate(
            page, per_page, error_out=False)
        data = {
            'projects': [c.project.to_json() for c in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserCollectionSystems(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, user_id, page, per_page):
        """ 获取用户收藏的系统 """
        user = User.query.get_or_404(user_id)
        paginate = SystemCollect.query.with_parent(user).order_by(
            SystemCollect.timestamp.desc()).paginate(
            page, per_page, error_out=False)
        data = {
            'systems': [c.systems.to_json() for c in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserCollectionURLs(MethodView):

    @use_kwargs(PaginateSchema)
    def get(self, user_id, page, per_page):
        """ 获取用户收藏的 URL """
        user = User.query.get_or_404(user_id)
        paginate = URLCollect.query.with_parent(user).order_by(
            URLCollect.timestamp.desc()).paginate(
            page, per_page, error_out=False)
        data = {
            'urls': [c.systems.to_json() for c in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


api_v1.add_url_rule('/users', view_func=UsersAPI.as_view('users'), methods=['GET', 'POST'])
api_v1.add_url_rule('/users/<int:user_id>', view_func=UserAPI.as_view('user'), methods=['GET'])
api_v1.add_url_rule('/users/<int:user_id>/projects',
                    view_func=UserSupportProjects.as_view('support-projects'),
                    methods=['GET'])
api_v1.add_url_rule('/users/<int:user_id>/systems', view_func=UserSupportSystems.as_view('support-systems'),
                    methods=['GET'])
api_v1.add_url_rule('/users/<int:user_id>/urls', view_func=UserSupportURLs.as_view('support-urls'), methods=['GET'])
api_v1.add_url_rule('/users/<int:user_id>/collection-projects',
                    view_func=UserSupportURLs.as_view('collection-projects'), methods=['GET'])
api_v1.add_url_rule('/users/<int:user_id>/collection-systems',
                    view_func=UserSupportURLs.as_view('collection-systems'), methods=['GET'])
api_v1.add_url_rule('/users/<int:user_id>/collection-urls',
                    view_func=UserSupportURLs.as_view('collection-urls'),
                    methods=['GET'])
