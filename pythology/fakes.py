# 虚拟数据生成模块
from faker import Faker
from .extensions import db
from .models import Student, Admin, Course, CourseStudent

fake = Faker('zh_CN')


def fake_student(count=20):
    for i in range(count):
        student = Student(
            id = i+1,
            username=fake.name(),
        )
        db.session.add(student)
        try:
            db.session.commit()
        except:
            db.session.rollback()