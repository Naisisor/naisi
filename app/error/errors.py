from app.decorators import logger_error
from app.error import bp_error
from app.response import response


@bp_error.app_errorhandler(400)
@logger_error
def bad_request(error):
    return response(code=error.code, message=error.description,
                    user_message='坏请求 400 Bad Request')


@bp_error.app_errorhandler(404)
@logger_error
def page_not_fount(error):
    return response(code=error.code, message=error.description,
                    user_message='未查询到资源')


@bp_error.app_errorhandler(500)
@logger_error
def internal_server_error(error):
    return response(code=error.code, message=error.description,
                    user_message='服务异常')


@bp_error.app_errorhandler(Exception)
@logger_error
def exception(error):
    error_code = hasattr(error, 'code') and error.code or 1
    if hasattr(error, 'description'):
        message = error.description
    else:
        message = error.args[0]
    return response(
        code=error_code,
        message=message,
        user_message='未知错误')
