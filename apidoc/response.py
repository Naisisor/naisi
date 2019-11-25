from flask import jsonify, make_response, request, current_app as app


def response(data=None, code=0, message='Success'):
    """ response 返回格式
    :param code: 错误码，类型 int，`0` 表示成功，非 `0` 表示失败
    :param message: 用户错误信息 类型 string
    :param data: 参数主体 类型 dict
    :return: 返回响应 body
    """
    if code != 0 and 'Success' == message:
        message = 'Failed'

    if data is None:
        data = {}

    headers = {
        'Access-Control-Allow-Origin': request.headers.get('origin'),
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST,GET,OPTIONS,PUT,DELETE',
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Headers': 'Accept,Authorization,Cache-Control,Content-Type,X-XSRF-TOKEN,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Mx-ReqToken,X-Requested-With'
    }

    response_body = {
        'code': code,
        'message': message,
        'data': data
    }
    app.logger.info(f'{response_body}')
    return make_response((jsonify(response_body), 200))
