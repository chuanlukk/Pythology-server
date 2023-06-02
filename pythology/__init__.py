# 构造文件
# 每一个包含__init__.py构造文件的文件夹都被视作包
# 包让我们使用文件夹来组织模块（.py文件）
# 当包或包内的模块被导入时，构造文件会被自动执行
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('pythology')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

# 为了让使用程序实例app注册的视图函数，错误处理函数，自定义命令函数等和程序实例关联起来
# 我们需要在构造文件中导入这些模块。
# 因为这些模块也需要从构造文件中导入程序实例，
# 所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
from pythology import views, errors, commands