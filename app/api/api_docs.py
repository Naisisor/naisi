from flask import Blueprint, request

from app import db
from app.models import APIDoc, URL, User, Method
from app.response import response

api = Blueprint('docs', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_api_doc(id):
    """ 获取 API 文档 """
    doc = APIDoc.query.get_or_404(id)
    return response(data={'doc': doc.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_api_doc(id):
    """ 删除 API 文档 """
    # TODO 增加权限控制
    return response()


@api.route('/', methods=['POST'])
def new_api_doc():
    """ 新建 API 文档 """
    params = request.json
    url_id = params.get('url_id', 0)
    method_id = params.get('method_id', 0)
    editor_id = params.get('editor_id', 0)
    if not (url_id and method_id and editor_id):
        return response(code=1, user_message='参数缺失')
    editor = User.query.get_or_404(editor_id)
    method = Method.query.get_or_404(method_id)
    url = URL.query.get_or_404(url_id)
    existed_doc = url.api_docs.filter(APIDoc.method_id == method_id).frist()
    if existed_doc:
        return response(code=1, user_message=f'{url.path} 接口中已存在 {method.name} 请求，请勿重复添加')
    doc = APIDoc(
        request_params=params.get('request_params', '{}'),
        resp_params=params.get('resp_params', '{}'),
        resp_body=params.get('resp_body', '{}'),
        url_id=url.id,
        method_id=method.id,
        editor_id=editor.id
    )
    db.session.add(doc)
    db.session.commit()
    return response()


@api.route('/<int:id>', methods=['PUT'])
def edit_api_doc(id):
    """ 编辑 API 文档 """
    doc = APIDoc.query.get_or_404(id)
    params = request.json
    editor_id = params.get('editor_id', 0)
    if not editor_id:
        return response(code=1, user_message='用户字段缺失')
    editor = User.query.get_or_404(editor_id)
    doc.request_params = params.get('request_params', '{}')
    doc.resp_params = params.get('resp_params', '{}')
    doc.resp_body = params.get('resp_body', '{}')
    doc.editor_id = editor.id
    db.session.add(doc)
    db.session.commit()
    return response()
