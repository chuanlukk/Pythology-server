# 虚拟数据生成模块
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from pythology.extensions import db
from pythology.models import Admin, Student, Course, Classroom

fake = Faker(locale='zh_CN')



