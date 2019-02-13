from app.libs.api_doc_blueprint import APIDocBlueprint
from app.models import User
from app.response import response

api = APIDocBlueprint('users')


@api.route('/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        return response(code=1, user_message='此用户不存在')
    return response(data={'user': user.to_json()})


@api.route('/<int:id>/projects')
def get_user_create_project(id):
    user = User.query.get(id)
    projects = [p.to_json() for p in user.projects]
    return response(data={'projects': projects})
