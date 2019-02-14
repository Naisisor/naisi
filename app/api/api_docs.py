from flask import Blueprint

from app.response import response

api = Blueprint('api-docs', __name__)


@api.route('/api-docs/<int:id>')
def get_api_doc(id):
    return response()
