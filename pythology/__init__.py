# 构造文件
# 每一个包含__init__.py构造文件的文件夹都被视作包
# 包让我们使用文件夹来组织模块（.py文件）
# 当包或包内的模块被导入时，构造文件会被自动执行
import os

from flask import Flask
from .blueprints.test import test_bp
from .config import config
from .extensions import db


# 工厂函数接收配置名作为参数，返回创建的程序实例
# 工厂函数一般在程序包的构造文件中定义，
# 也可以在程序包内新创建的模块来存放，比如app.py或者factory.py
def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('pythology')
    # 加载配置
    app.config.from_object(config[config_name])
    # 避免工厂函数太长，可以将不同的注册分割到不同的函数中
    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册拓展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_commands(app)  # 注册自定义flask命令
    register_errors(app)  # 注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    return app


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(test_bp)


def register_commands(app):
    pass


def register_errors(app):
    pass


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


# 为了让使用程序实例app注册的视图函数，错误处理函数，自定义命令函数等和程序实例关联起来
# 我们需要在构造文件中导入这些模块。
# 因为这些模块也需要从构造文件中导入程序实例，
# 所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
from pythology import views, errors, commands
