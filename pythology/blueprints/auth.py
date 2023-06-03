from flask import Blueprint, request, jsonify, make_response, g
from pythology.extensions import db
from pythology.models import Student, Admin, Course

auth_bp = Blueprint('auth', __name__)


@auth_bp.before_app_request
def before_request():
    g.id = request.args.get('id')
    g.admin = request.args.get('admin')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    model_class = Admin if data['admin'] else Student
    existing_user = model_class.query.get(data['id'])
    new_user = None

    print('existing_user:', existing_user)
    if existing_user:
        res['msg'] = "existed"
        res['status'] = 0
    else:
        print('model_class:', model_class)
        if data['admin']:
            new_user = Admin(
                id=data['id'],
                username=data['username'],
                password_hash=data['password']
            )
        else:
            new_user = Student(
                id=data['id'],
                username=data['username'],
                password_hash=data['password'],
                gender=data['gender'],
                school=data['school'],
                major=data['major'],
                enrollment_date=data['enrollment_date']
            )

        if new_user:
            db.session.add(new_user)
            db.session.commit()
            res['msg'] = "success"
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

    print('user:', user)
    if user:
        if user.password_hash == data['password']:
            if not data['admin']:
                courses = user.courses
                print('courses:', courses)
            res['msg'] = "success"
            res['status'] = 1
            res['courses'] = []
        else:
            res['msg'] = "wrong password"
            res['status'] = 0
    else:
        res['msg'] = "not existed"
        res['status'] = 0

    print('send res:', res)
    response = make_response(jsonify(res))
    return response




