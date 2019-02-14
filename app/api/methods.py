from flask import Blueprint

from app.models import Method
from app.response import response

api = Blueprint('methods', __name__)


@api.route('/<int:id>')
def get_method(id):
    method = Method.query.get_or_404(id)
    return response(data={'method': method.to_json()})
