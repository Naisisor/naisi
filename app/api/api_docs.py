from flask import Blueprint

from app.models import APIDoc
from app.response import response

api = Blueprint('api-docs', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_api_doc(id):
    """ 获取 API 文档 """
    doc = APIDoc.query.get_or_404(id)
    return response(data={'doc': doc.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_api_doc(id):
    """ 删除 API 文档 """
    return response()


@api.route('/', methods=['POST'])
def new_api_doc():
    """ 新建 API 文档 """
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_api_doc(id):
    """ 编辑 API 文档 """
    return response()
