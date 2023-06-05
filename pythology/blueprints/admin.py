from flask import Blueprint, request, jsonify, make_response, g
from pythology.extensions import db
from pythology.models import Student, Admin, Course, Classroom

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
        # 判断与已有课程是否时间冲突
        time_conflict = Course.query.filter_by(week=data['week'], admin_id=g.user_id).filter(
            Course.start < data['end'], Course.end > data['start']).first()
        if time_conflict:
            res['msg'] = "与已有课程时间冲突"
            res['status'] = 0
        else:
            # 判断教室是否时间冲突
            classroom_time_conflict = Course.query.filter_by(week=data['week'], classroom_id=data['classroom']).filter(
                Course.start < data['end'], Course.end > data['start']).first()
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
                    # 建立课程与教室关系
                    classroom_id=data['classroom'],
                    # 建立教师与课程关系
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
        res['msg'] = "课程不存在，请检查课程id"
        res['status'] = 0

    print('send res:', res)
    return jsonify(res)