from flask import Blueprint

# 实例化Blueprint类就获得了蓝本对象
# 第一个参数是蓝本的名字，第二个参数是蓝本所在的包或模块
# 蓝本实例是一个用于注册路由等操作的临时对象
test_bp = Blueprint('test', __name__)

# 蓝本中的视图函数通过蓝本类实例提供的route()装饰器注册

@test_bp.route('/test')
def test_fn():
    return "Hello Blueprint"

