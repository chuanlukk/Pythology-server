# 配置文件
import os
import sys

from pythology import app

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

dev_db = 'mysql://test:test@\'%\'/test'

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

# Flask 应用程序的密钥，用于保护 Web 表单数据免受跨站点请求伪造 (CSRF) 攻击。
# 如果环境变量中没有设置密钥，则默认使用字符串 secret string
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

# SQLAlchemy 的一个配置变量,用于控制是否跟踪对象的修改并发送信号。
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLAlchemy 数据库的 URI，指定了应用程序将连接的数据库的位置和类型
# 如果环境变量中没有设置数据库 URI，则默认使用 dev_db 变量中定义的数据库 URI。
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)