from flask import Blueprint, current_app, request

from apidoc.extensions import db
from apidoc import response
from apidoc.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/favicon.ico')
def favicon():
    # 返回 shortcut icon
    return current_app.send_static_file('favicon.ico')


@main_bp.route('/register', methods=['POST'])
def register():
    email = request.form['email'].lower()

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return response(code=1, message=f'用户 {user.email} 已存在')

    name = request.form['name']
    password = request.form['password']

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return response(message='注册成功')
