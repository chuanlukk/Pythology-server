from flask import Blueprint, request, jsonify, make_response, g
from pythology.extensions import db
from pythology.models import Student, Admin, Course

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def before_request():
    g.user_id = request.args.get('id')
    # g.user = Admin.query.get(g.user_id)


@admin_bp.route('/create', methods=['GET', 'POST'])
def create_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    existing_course = Course.query.get(data['course_id'])
    print('existing_course:', existing_course)
    if existing_course:
        res['msg'] = "课程已存在"
        res['status'] = 0
    else:
        new_course = Course(
            id=data['course_id'],
            name=data['name'],
            teacher=data['teacher'],
            school=data['school'],
            major=data['major'],
            grade=data['grade'],
            credit=data['credit'],
            week=data['week'],
            start=data['start'],
            end=data['end'],
            classroom=data['classroom'],
            # 建立关系
            admin_id=g.user_id
        )
        db.session.add(new_course)
        db.session.commit()
        res['msg'] = "课程创建成功"
        res['status'] = 1

    print('send res:', res)
    return jsonify(res)


@admin_bp.route('/delete', methods=['GET', 'POST'])
def delete_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    existing_course = Course.query.get(data['course_id'])
    print('existing_course:', existing_course)
    if existing_course:
        # 删除课程，自动解除关系
        db.session.delete(existing_course)
        db.session.commit()
        res['msg'] = "删除成功"
        res['status'] = 1
    else:
        res['msg'] = "目标课程不存在"
        res['status'] = 0

    print('send res:', res)
    return jsonify(res)