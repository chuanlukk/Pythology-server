from flask import Blueprint, request, jsonify, make_response
from pythology.extensions import db
from pythology.models import Student, Admin, Course

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    model_class = Admin if data['admin'] else Student
    existing_user = model_class.query.get(data['id'])
    print('existing_user:', existing_user)

    new_user = None
    if existing_user:
        res['msg'] = "用户已存在"
        res['status'] = 0
    else:
        print('model_class:', model_class)
        if data['admin']:
            new_user = Admin(
                id=data['id'],
                username=data['username'],
                password_hash=data['password'],
                school=data['school']
            )
        else:
            new_user = Student(
                id=data['id'],
                username=data['username'],
                password_hash=data['password'],
                gender=data['gender'],
                school=data['school'],
                major=data['major'],
                grade=data['grade']
            )

        if new_user:
            db.session.add(new_user)
            db.session.commit()
            res['msg'] = "注册成功"
            res['status'] = 1

    print('send res:', res)
    return jsonify(res)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    model_class = Admin if data['admin'] else Student
    user = model_class.query.get(data['id'])
    # 判断用户是否存在
    if user:
        # 判断密码是否正确
        if user.password_hash == data['password']:
            res['course'] = [course.to_dict() for course in user.courses]
            res['msg'] = "登录成功"
            res['username'] = user.username
            res['school'] = user.school
            res['id'] = user.id
            res['status'] = 1
            if not data['admin']:
                res['major'] = user.major
                res['grade'] = user.grade
        else:
            res['msg'] = "学工号或密码错误"
            res['status'] = 0
    else:
        res['msg'] = "用户不存在，请检查学工号是否正确"
        res['status'] = 0

    print('send res:', res)
    return jsonify(res)