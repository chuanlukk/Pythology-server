from flask import Blueprint, request, jsonify, make_response, g
from pythology.extensions import db
from pythology.models import Student, Admin, Course
from sqlalchemy import and_, or_

student_bp = Blueprint('student', __name__)


@student_bp.before_request
def before_request():
    g.user_id = request.args.get('id')
    g.user = Student.query.get(g.user_id)
    print('request from :', g.user, g.user_id, g.user.username)


@student_bp.route('/add', methods=['GET', 'POST'])
def add_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    course = Course.query.get(data['course_id'])
    print('course:', course)
    if course:
        # 判断是否已选过相同课程
        if any(c.name == course.name for c in g.user.courses):
            res['msg'] = "您已选过相同课程"
            res['status'] = 0
        else:
            # 判断是否与已选课程产生时间冲突
            time_conflict = any(c.week == course.week and c.start <= course.end and c.end >= course.start for c in g.user.courses)
            if time_conflict:
                res['msg'] = "与已选课程产生时间冲突"
                res['status'] = 0
            else: # 选课成功
                g.user.courses.append(course)
                db.session.commit()
                res['msg'] = "选课成功"
                res['status'] = 1
                # # 返回新课表
                # res['courses'] = [c.to_dict() for c in g.user.courses]
                # # 返回新可选课程状态表
                # related_courses = Course.query.filter(
                #     or_(and_(Course.grade == data['grade'], Course.major == data['major']),
                #         and_(Course.grade == 0, Course.major == 0))).all()
                # res['related_courses'] = [c.to_dict() for c in related_courses]
                # # 标记已选课程
                # for c in res['related_courses']:
                #     c['selected'] = 1 if any(c['id'] == course.id for course in g.user.courses) else 0
                # # 标记时间冲突课程
                # for c in res['related_courses']:
                #     c['time_conflict'] = 1 if any(
                #         c['week'] == course.week and c['start'] <= course.end and c['end'] >= course.start for course in
                #         g.user.courses) else 0
    else: # 课程不存在
        res['msg'] = "课程不存在，请检查该课程id"
        res['status'] = 0

    print('send res:', res)
    return jsonify(res)


@student_bp.route('/remove', methods=['GET', 'POST'])
def remove_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    course = next((c for c in g.user.courses if c.id == data['course_id']), None)
    print('course:', course)
    if course:
        # res['courses'] = [c.to_dict() for c in g.user.courses]
        g.user.courses.remove(course)
        db.session.commit()
        res['msg'] = "退课成功"
        res['status'] = 1
        # # 返回新课表
        # res['courses'] = [c.to_dict() for c in g.user.courses]
        # # 返回新可选课程状态表
        # related_courses = Course.query.filter(or_(and_(Course.grade == data['grade'], Course.major == data['major']),
        #                                           and_(Course.grade == 0, Course.major == 0))).all()
        # res['related_courses'] = [c.to_dict() for c in related_courses]
        # # 标记已选课程
        # for c in res['related_courses']:
        #     c['selected'] = 1 if any(c['id'] == course.id for course in g.user.courses) else 0
        # # 标记时间冲突课程
        # for c in res['related_courses']:
        #     c['time_conflict'] = 1 if any(
        #         c['week'] == course.week and c['start'] <= course.end and c['end'] >= course.start for course in
        #         g.user.courses) else 0
    else: # 课程不存在
        res['msg'] = "课程不存在，请检查该课程id"
        res['status'] = 0

    print('send res:', res)
    return jsonify(res)


@student_bp.route('/get', methods=['GET', 'POST'])
def get_courses():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    # 获取所有可选课程
    courses = Course.query.filter(or_(and_(Course.grade==data['grade'], Course.major==data['major']), and_(Course.grade==0, Course.major==0))).all()
    if courses:
        res['status'] = 1
        res['courses'] = [course.to_dict() for course in courses]
        # 标记已选课程
        for course in res['courses']:
            # course['selected'] = 1 if g.user.courses.filter_by(id=course['id']).first() else 0
            course['selected'] = 1 if any(c.id == course['id'] for c in g.user.courses) else 0
        # 标记时间冲突课程
        for course in res['courses']:
            course['time_conflict'] = 1 if any(course['week'] == c.week and course['start'] <= c.end and course['end'] >= c.start for c in g.user.courses) else 0
        res['msg'] = "获取可选课程成功"
    else:
        res['status'] = 0
        res['msg'] = "无可选课程"

    print('send res:', res)
    return jsonify(res)


@student_bp.route('/find', methods=['GET', 'POST'])
def index_course():
    data = request.get_json()
    print('receive data:', data)

    res = {}
    # 获取所有可选选课程
    # 课程类型
    if data['type'] == 'all':
        courses = Course.query.filter(or_(and_(Course.grade == data['grade'], Course.major == data['major']),
                                          and_(Course.grade == 0, Course.major == 0))).all()
    elif data['type'] == 'major':
        courses = Course.query.filter(and_(Course.grade == data['grade'], Course.major == data['major'])).all()
    elif data['type'] == 'public':
        courses = Course.query.filter(and_(Course.grade == 0, Course.major == 0)).all()
    # 搜索
    if not data['keyword'] == '':
        courses = courses.query.filter(Course.name.like('%' + data['keyword'] + '%')).all()

    if courses:
        res['courses'] = [course.to_dict() for course in courses]
        # 课程状态
        if data['status'] == 'selected':
            res['courses'] = [course for course in res['courses'] if any(c.id == course['id'] for c in g.user.courses)]
        elif data['status'] == 'unselected':
            res['courses'] = [course for course in res['courses'] if not any(c.id == course['id'] for c in g.user.courses)]
        # 时间冲突
        if data['check_time']:
            res['courses'] = [course for course in res['courses'] if not any(course['week'] == c.week and course['start'] <= c.end and course['end'] >= c.start for c in g.user.courses)]

        # 标记已选课程
        for course in res['courses']:
            # course['selected'] = 1 if g.user.courses.filter_by(id=course['id']).first() else 0
            course['selected'] = 1 if any(c.id == course['id'] for c in g.user.courses) else 0
        # 标记时间冲突课程
        for course in res['courses']:
            course['time_conflict'] = 1 if any(
                course['week'] == c.week and course['start'] <= c.end and course['end'] >= c.start for c in
                g.user.courses) else 0
        res['status'] = 1
        res['msg'] = "获取可选课程成功"

    print('send res:', res)
    return jsonify(res)