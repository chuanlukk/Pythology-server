# 视图函数
from pythology import app


@app.route('/login')
def index():
    return "Hello Flask"