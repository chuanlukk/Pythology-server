# 视图函数
from flask import current_app


@current_app.route('/login')
def index():
    return "Hello Flask"