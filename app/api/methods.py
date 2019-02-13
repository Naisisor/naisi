from app.libs.api_doc_blueprint import APIDocBlueprint
from app.models import Method
from app.response import response

api = APIDocBlueprint('methods')


@api.route('/<int:id>')
def get_method(id):
    method = Method.query.get_or_404(id)
    return response(data={'method': method.to_json()})
