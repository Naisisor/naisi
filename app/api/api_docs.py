from app.libs.api_doc_blueprint import APIDocBlueprint
from app.response import response

api = APIDocBlueprint('api-docs')


@api.route('/api-docs/<int:id>')
def get_api_doc(id):
    return response()
