import traceback
from functools import wraps

from flask import current_app, request


def logger_error(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        current_app.logger.error(f'\n请求 URL: {request.url}\n错误信息：{traceback.format_exc()}')
        return f(*args, **kwargs)

    return decorator
