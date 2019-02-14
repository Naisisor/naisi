from flask import Blueprint

from app.models import URL
from app.response import response

api = Blueprint('urls', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_url(id):
    url = URL.query.get_or_404(id)
    return response(data={'url': url.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_url(id):
    URL.query.filter_by(id=id).delete(synchronize_session=False)
    return response()


@api.route('/', methods=['POST'])
def new_url():
    return response()


@api.route('/', methods=['PUT'])
def edit_url():
    return response()
