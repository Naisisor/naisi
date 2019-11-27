from flask import Blueprint, current_app
from flask.views import MethodView
from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from apidoc.apis.v1.auth import generate_token
from apidoc.apis.v1.errors import api_abort
from apidoc.extensions import db
from apidoc.models import User
from apidoc.response import response

main_bp = Blueprint('main', __name__)


class FaviconAPI(MethodView):

    def get(self):
        return current_app.send_static_file('favicon.ico')


account_args = {
    'username': fields.Str(required=True, validate=validate.Length(min=6, max=18)),
    'password': fields.Str(validate=validate.Length(min=6, max=18))
}


class RegisterAPI(MethodView):

    @use_kwargs({'email': fields.Str(required=True, validate=validate.Email(error='邮件格式错误'))}, locations=('form',))
    @use_kwargs(account_args, locations=('form',))
    def post(self, email, username, password):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return response(code=1, message=f'邮箱 {user.email} 已存在')
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return response(code=1, message=f'用户名 {user.username} 已存在')

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return response(message='注册成功')


class AuthTokenAPI(MethodView):

    @use_kwargs({'grant_type': fields.Str(required=True,
                                          validate=validate.Equal('password',
                                                                  error='The grant type must be password.'))},
                locations=('form',))
    @use_kwargs(account_args, locations=('form',))
    def post(self, grant_type, username, password):
        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
            return api_abort(code=400, message='Either the username or password was invalid.')

        token, expiration = generate_token(user)
        headers = {
            'Cache-Control': 'no-store',
            'Pragma': 'no-cache'
        }

        data = {
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expiration
        }

        return response(data=data, headers=headers)


main_bp.add_url_rule('/favicon.ico', view_func=FaviconAPI.as_view('favicon'), methods=['GET'])
main_bp.add_url_rule('/register', view_func=RegisterAPI.as_view('register'), methods=['POST'])
main_bp.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
