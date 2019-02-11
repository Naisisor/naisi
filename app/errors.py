from app.decorators import logger_error
from app.response import response
from . import api


@api.app_errorhandler(400)
@logger_error
def bad_request(error):
    return response(code=1, user_message="坏请求 400 Bad Request",
                    message=str(error))


@api.app_errorhandler(404)
@logger_error
def page_not_fount(error):
    str_error = str(error)
    return response(code=1, user_message=str_error,
                    message=str_error)


@api.app_errorhandler(500)
@logger_error
def internal_server_error(error):
    str_error = str(error)
    return response(code=1, user_message=str_error,
                    message=str_error)


@api.app_errorhandler(Exception)
@logger_error
def exception(error):
    str_error = str(error)
    return response(code=1, message=str_error, user_message=str_error)
