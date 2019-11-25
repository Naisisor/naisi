from flask import jsonify, make_response, current_app as app


def response(data=None, code=0, message='Success', headers=None):
    """ response 返回格式
    :param headers: 头部信息
    :param code: 错误码，类型 int，`0` 表示成功，非 `0` 表示失败
    :param message: 用户错误信息 类型 string
    :param data: 参数主体 类型 dict
    :return: 返回响应 body
    """
    if code != 0 and 'Success' == message:
        message = 'Failed'

    if data is None:
        data = {}

    response_body = {
        'code': code,
        'message': message,
        'data': data
    }
    app.logger.info(f'{response_body}')
    resp = jsonify(response_body)
    if headers is not None:
        resp.headers = {**resp.headers, **headers}
    return resp
