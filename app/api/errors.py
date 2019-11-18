from flask import Blueprint

from app.decorators import logger_error
from app.response import response

api = Blueprint('error', __name__)


@api.app_errorhandler(400)
@logger_error
def bad_request(e):
    return response(code=e.code, message=e.description)


@api.app_errorhandler(404)
@logger_error
def page_not_fount(e):
    return response(code=e.code, message=e.description)


@api.app_errorhandler(500)
@logger_error
def internal_server_error(e):
    return response(code=e.code, message=e.description)


@api.app_errorhandler(Exception)
@logger_error
def exception(e):
    error_code = hasattr(e, 'code') and e.code or 1
    if hasattr(e, 'description'):
        message = e.description
    else:
        message = e.args[0]
    return response(
        code=error_code,
        message=message)
