# 用来存储和Flask相关的公开环境变量
# 安装python-dotemv后，环境变量优先级：手动 > .env > .flaskenv

# flask在FLASK_APP环境变量定义模块中寻找程序实例
# 程序主模块为app.py，于是设置FLASK_APP = app
FLASK_APP = pythology

# 默认为production，此时为开发环境，调试模式将开启
# 生产环境中部署程序时，绝不能开启调试模式
FLASK_ENV=development

# 设置主机地址对外可见
# FLASK_RUN_HOST=0.0.0.0

# FLASK_RUN_PORT=8000