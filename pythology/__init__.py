# 构造文件
# 每一个包含__init__.py构造文件的文件夹都被视作包
# 包让我们使用文件夹来组织模块（.py文件）
# 当包或包内的模块被导入时，构造文件会被自动执行
import os
import click
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask, request
from .blueprints.test import test_bp
from .blueprints.auth import auth_bp
from .blueprints.admin import admin_bp
from .blueprints.student import student_bp
from .config import config
from .extensions import db
from .models import Student, Admin, Course, association_table, Classroom

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

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
    # 为了让日志记录器记录最低级别为INFO的日志
    # 首先将app.logger的日志级别设置为INFO
    app.logger.setLevel(logging.INFO)
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super().format(record)

    # 设置日志输出格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
    # 创建轮转文件类型的日志处理器
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/pythology.log'),
                                       maxBytes=10 * 1024 * 1024,
                                       backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    #app.debug属性存储用来判断程序是否开启了调试模式的布尔值
    if not app.debug:
        # 对app.logger调用addHandler()方法将处理器注册到logger对象中
        app.logger.addHandler(file_handler)



def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(test_bp, url_prefix='/test')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')


# 自定义flask命令
# 当我们安装Flask后，会自动添加一个flask命令脚本，
# 我们可以通过flask命令执行内置命令、拓展提供的命令或是我们自己定义的命令
def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--id', default='111', prompt=True, help='The username used to login.')
    @click.option('--password', default='111', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
    def init(id, password):
        """Building pythology, just for fun."""
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.filter('username' == '谢坤').first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.id = id
            admin.password_hash = password
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(id = id, username='谢坤', password_hash=password, school=1)
            db.session.add(admin)
        db.session.commit()
        click.echo('Done.')






def register_errors(app):
    pass


def register_shell_context(app):
    # 将db对象集成到Python shell上下文中
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,
                    Student=Student,
                    Admin=Admin,
                    Course=Course,
                    association_table=association_table,
                    Classroom=Classroom)


# 为了让使用程序实例app注册的视图函数，错误处理函数，自定义命令函数等和程序实例关联起来
# 我们需要在构造文件中导入这些模块。
# 因为这些模块也需要从构造文件中导入程序实例，
# 所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
from pythology import errors
