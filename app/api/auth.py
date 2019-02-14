from flask import Blueprint

from app.response import response

api = Blueprint('auth', __name__)


@api.route('/register')
def register():
    return response()
