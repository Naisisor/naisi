from flask import Blueprint, current_app

main_bp = Blueprint('main', __name__)


@main_bp.route('/favicon.ico')
def favicon():
    # 返回 shortcut icon
    return current_app.send_static_file('favicon.ico')
