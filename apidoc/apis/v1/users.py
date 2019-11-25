from flask import current_app, request, jsonify
from flask.views import MethodView

from apidoc.apis.v1 import api_v1
from apidoc.apis.v1.auth import generate_token
from apidoc.apis.v1.errors import api_abort
from apidoc.models import User, ProjectCollect, URLCollect, SystemCollect
from apidoc.response import response


class AuthTokenAPI(MethodView):

    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            return api_abort(code=400, message='Either the username or password was invalid.')

        token, expiration = generate_token(user)
        headers = {
            'Cache-Control': 'no-store',
            'Pragma': 'no-cache'
        }

        data = {
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expiration
        }

        return response(data=data, headers=headers)


class UsersAPI(MethodView):

    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
        paginate = User.query.paginate(
            page, per_page, error_out=False)
        data = {
            'projects': [p.to_json() for p in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)

    def post(self):
        return response()


class UserAPI(MethodView):

    def get(self, user_id):
        """ 获取用户信息 """
        user = User.query.get_or_404(user_id)
        if not user:
            return response(code=1, message='此用户不存在')
        return response(data={'user': user.to_json()})

    def post(self):
        return response()


class UserSupportProjects(MethodView):

    def get(self, user_id):
        """ 获取用户所创建的项目 """
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
        paginate = user.projects.paginate(
            page, per_page, error_out=False)
        data = {
            'projects': [p.to_json() for p in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserSupportSystems(MethodView):

    def get(self, user_id):
        """ 获取用户所创建的系统 """
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
        paginate = user.systems.paginate(
            page, per_page, error_out=False)
        data = {
            'systems': [s.to_json() for s in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserSupportURLs(MethodView):

    def get(self, user_id):
        """ 获取用户所创建的 uri """
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
        paginate = user.urls.paginate(
            page, per_page, error_out=False)
        data = {
            'urls': [u.to_json() for u in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


class UserCollectionProjects(MethodView):

    def get(self, user_id):
        """ 获取用户收藏的项目 """
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
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

    def get(self, user_id):
        """ 获取用户收藏的系统 """
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
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

    def get(self, user_id):
        """ 获取用户收藏的 URL """
        user = User.query.get_or_404(user_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get(
            'per_page',
            current_app.config['API_DOC_PER_PAGE'],
            type=int)
        paginate = URLCollect.query.with_parent(user).order_by(
            URLCollect.timestamp.desc()).paginate(
            page, per_page, error_out=False)
        data = {
            'urls': [c.systems.to_json() for c in paginate.items],
            'count': paginate.total,
            'paginate': paginate.page
        }
        return response(data=data)


api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
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
