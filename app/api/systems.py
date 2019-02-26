from flask import Blueprint

from app.models import System
from app.response import response

api = Blueprint('systems', __name__)


@api.route('/<int:id>', methods=['GET'])
def get_system(id):
    """ 获取系统信息 """
    system = System.query.get_or_404(id)
    return response(data={'system': system.to_json()})


@api.route('/<int:id>', methods=['DELETE'])
def delete_system(id):
    """ 删除系统 """
    # TODO 增加权限控制
    System.query.filter_by(id=id).delete(synchronize_session=False)
    return response()


@api.route('/', methods=['POST'])
def new_system():
    """ 新建系统 """
    return response()


@api.route('/', methods=['PUT'])
def edit_system():
    """ 删除系统 """
    return response()
