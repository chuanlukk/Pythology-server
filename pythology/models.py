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


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(1)) # M or F
    school = db.Column(db.String(20))
    major = db.Column(db.String(25))
    enrollment_date = db.Column(db.Integer)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    # 课程和学生是多对多的关系，课程和学生的关系由course_student表来维护
    students = db.relationship('Student', secondary='course_student', back_populates='courses')


class CourseStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    grade = db.Column(db.Integer)
    # 课程和学生是多对多的关系，课程和学生的关系由course_student表来维护
    course = db.relationship('Course', back_populates='students')
    student = db.relationship('Student', back_populates='courses')

