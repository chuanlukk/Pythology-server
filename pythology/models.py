# 数据库模型
# from datetime import datetime
from .extensions import db

association_table = db.Table('association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')))


class Admin(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))


class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(1)) # M or F
    school = db.Column(db.String(20))
    major = db.Column(db.String(25))
    enrollment_date = db.Column(db.Integer)
    courses = db.relationship('Course',
                              secondary=association_table,
                              back_populates='students')


class Course(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20))
    teacher = db.Column(db.String(20))
    credit = db.Column(db.Integer)
    time = db.Column(db.String(20))
    location = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    description = db.Column(db.Text)
    school = db.Column(db.String(20))
    major = db.Column(db.String(25))
    grade = db.Column(db.Integer)
    students = db.relationship('Student',
                                secondary=association_table,
                                back_populates='courses')


