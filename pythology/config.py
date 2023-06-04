# 配置文件
# 使用类来组织配置
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    # Flask 应用程序的密钥，用于保护 Web 表单数据免受跨站点请求伪造 (CSRF) 攻击。
    # 如果环境变量中没有设置密钥，则默认使用字符串 dev key
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # SQLAlchemy 的一个配置变量,用于控制是否跟踪对象的修改并发送信号。
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    # SQLAlchemy 数据库的 URI，指定了应用程序将连接的数据库的位置和类型
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', prefix + os.path.join(basedir, 'data-dev.db'))


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = prefix + ':memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    # 如果环境变量中没有设置数据库 URI，则默认使用 dev_db 变量中定义的数据库 URI。
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}