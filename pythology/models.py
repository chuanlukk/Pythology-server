# 数据库模型
from .extensions import db

association_table = db.Table('association',
    db.Column('student_id', db.String(10), db.ForeignKey('student.id')),
    db.Column('course_id', db.String(10), db.ForeignKey('course.id')))


class Admin(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    school = db.Column(db.Integer)
    courses = db.relationship('Course', backref='admin', lazy='select')


class Classroom(db.Model):
    id = db.Column(db.String(10), primary_key=True) # 4-312
    capacity = db.Column(db.Integer)
    courses = db.relationship('Course', backref='classroom', lazy='select')


class Student(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(1)) # M or F
    school = db.Column(db.Integer)
    major = db.Column(db.Integer)
    enrollment_date = db.Column(db.Integer)
    courses = db.relationship('Course',
                              secondary=association_table,
                              back_populates='students')


class Course(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    school = db.Column(db.Integer)
    major = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    name = db.Column(db.String(20))
    teacher = db.Column(db.String(20))
    credit = db.Column(db.Integer)
    week = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    description = db.Column(db.Text)
    admin_id = db.Column(db.String(10), db.ForeignKey('admin.id'))
    classroom_id = db.Column(db.String(10), db.ForeignKey('classroom.id'))
    students = db.relationship('Student',
                                secondary=association_table,
                                back_populates='courses')


