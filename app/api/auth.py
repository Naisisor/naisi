from app.libs.api_doc_blueprint import APIDocBlueprint
from app.response import response

api = APIDocBlueprint('auth')


@api.route('/register')
def register():
    return response()
