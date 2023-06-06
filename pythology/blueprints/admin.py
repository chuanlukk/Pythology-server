from flask import Blueprint, request, jsonify, make_response, g
from pythology.extensions import db
from pythology.models import Student, Admin, Course, Classroom, association_table

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def before_request():
    g.user_id = request.args.get('id')
    g.user = Admin.query.get(g.user_id)


@admin_bp.route('/create', methods=['GET', 'POST'])
def create_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    # existing_course = Course.query.get(data['course_id'])
    # 判断与已有课程是否时间冲突
    time_conflict = Course.query.filter_by(week=data['week'], admin_id=g.user_id).filter(
        Course.start <= data['end'], Course.end >= data['start']).first()
    if time_conflict:
        res['msg'] = "与已有课程时间冲突"
        res['status'] = 0
    else:
        # 判断教室是否时间冲突
        classroom_time_conflict = Course.query.filter_by(week=data['week'], classroom_id=data['classroom']).filter(
            Course.start <= data['end'], Course.end >= data['start']).first()
        if classroom_time_conflict:
            res['msg'] = "教室时间冲突"
            res['status'] = 0
        else:
            # 如果教室不存在，创建教室
            existing_classroom = Classroom.query.get(data['classroom'])
            if not existing_classroom:
                new_classroom = Classroom(
                    id=data['classroom']
                )
                db.session.add(new_classroom)
                db.session.commit()
            # 生成10位随机课程id
            import random, string
            new_course_id = None
            while True:
                new_course_id = ''.join(random.sample(string.ascii_letters + string.digits, 10))
                print('new_course_id:', new_course_id)
                if not Course.query.get(new_course_id):
                    break
                else:
                    new_course_id = None
            new_course = Course(
                # id=data['course_id'],
                id=new_course_id,
                name=data['name'],
                teacher=data['teacher'],
                school=data['school'],
                major=data['major'],
                grade=data['grade'],
                credit=data['credit'],
                week=data['week'],
                start=data['start'],
                end=data['end'],
                # 建立课程与教室关系
                classroom_id=data['classroom'],
                # 建立教师与课程关系
                admin_id=g.user_id
            )
            db.session.add(new_course)
            db.session.commit()
            # 返回新的课程列表
            res['courses'] = [course.to_dict() for course in g.user.courses]
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
        res['courses'] = [course.to_dict() for course in g.user.courses]
        res['msg'] = "删除成功"
        res['status'] = 1
    else:
        res['msg'] = "课程不存在，请检查课程id"
        res['status'] = 0

    print('send res:', res)
    return jsonify(res)


@admin_bp.route('/get', methods=['GET', 'POST'])
def get_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    # 获取已有课程
    courses = Course.query.filter(Course.admin_id == g.user_id).all()
    if courses:
        res['status'] = 1
        res['courses'] = [course.to_dict() for course in courses]
        for course in res['courses']:
            course['count'] = association_table.query.filter_by(course_id=course['id']).count()
        res['msg'] = "获取已有课程成功"
    else:
        res['status'] = 0
        res['msg'] = "暂无课程"

    print('send res:', res)
    return jsonify(res)