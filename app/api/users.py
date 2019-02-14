from flask import Blueprint, current_app, request

from app.models import User, ProjectCollect, URLCollect, SystemCollect
from app.response import response

api = Blueprint('users', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return response(code=1, user_message='此用户不存在')
    return response(data={'user': user.to_json()})


@api.route('/<int:id>/projects', methods=['GET'])
def get_user_created_projects(id):
    """ 获取用户所创建的项目 """
    user = User.query.get_or_404(id)
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


@api.route('/<int:id>/systems', methods=['GET'])
def get_user_created_systems(id):
    """ 获取用户所创建的系统 """
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get(
        'per_page',
        current_app.config['API_DOC_PER_PAGE'],
        type=int)
    paginate = user.systems.paginate(
        page, per_page, error_out=False)
    data = {
        'projects': [s.to_json() for s in paginate.items],
        'count': paginate.total,
        'paginate': paginate.page
    }
    return response(data=data)


@api.route('/<int:id>/urls', methods=['GET'])
def get_user_created_urls(id):
    """ 获取用户所创建的 uri """
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get(
        'per_page',
        current_app.config['API_DOC_PER_PAGE'],
        type=int)
    paginate = user.urls.paginate(
        page, per_page, error_out=False)
    data = {
        'projects': [u.to_json() for u in paginate.items],
        'count': paginate.total,
        'paginate': paginate.page
    }
    return response(data=data)


@api.route('/<int:id>/collection-projects', methods=['GET'])
def get_user_collection_projects(id):
    """ 获取用户收藏的项目 """
    user = User.query.get_or_404(id)
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


@api.route('/<int:id>/collection-systems', methods=['GET'])
def get_user_collection_systems(id):
    """ 获取用户收藏的系统 """
    user = User.query.get_or_404(id)
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


@api.route('/<int:id>/collection-urls', methods=['GET'])
def get_user_collection_urls(id):
    """ 获取用户收藏的 URL """
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get(
        'per_page',
        current_app.config['API_DOC_PER_PAGE'],
        type=int)
    paginate = URLCollect.query.with_parent(user).order_by(
        URLCollect.timestamp.desc()).paginate(
        page, per_page, error_out=False)
    data = {
        'systems': [c.systems.to_json() for c in paginate.items],
        'count': paginate.total,
        'paginate': paginate.page
    }
    return response(data=data)
