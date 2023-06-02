# 数据库模型
# from datetime import datetime
from pythology import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(20))
    gender = db.Column(db.String(1)) # M or F
    school = db.Column(db.String(20))
    major = db.Column(db.String(25))
    enrollment_date = db.Column(db.Integer)

