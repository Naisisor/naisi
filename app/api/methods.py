from flask import Blueprint

from app import db
from app.models import Method
from app.response import response

api = Blueprint('methods', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_method(id):
    method = Method.query.get_or_404(id)
    return response(data={'method': method.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_method(id):
    method = Method.query.get_or_404(id)
    if method.api_docs:
        return response(code=1, user_message='此方法已经被使用，请联系管理员')
    db.session.delete(id)
    db.session.commit()
    return response()


@api.route('/', methods=['POST'])
def new_method():
    return response()


@api.route('/', methods=['PUT'])
def edit_method():
    return response()
