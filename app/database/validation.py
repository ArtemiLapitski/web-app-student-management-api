from sqlalchemy import select
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel
from app.database.db import db


def get_list_of_courses() -> list:
    all_courses = db.session.execute(select(CourseModel.course_name)).all()

    return [course_name[0] for course_name in all_courses]


def get_list_of_groups() -> list:
    all_groups = db.session.execute(select(GroupModel.group_name)).all()

    return [group[0] for group in all_groups]


def check_student_id(student_id: int):
    is_student = bool(db.session.execute(
        select(StudentModel.student_id).where(StudentModel.student_id == student_id)
    ).all())

    return is_student


def check_course_id(course_id: int):
    is_course = bool(
        db.session.execute(select(CourseModel.course_id).where(CourseModel.course_id == course_id)).all())
    return is_course


def check_course_for_student(student_id: int, course_id: int):
    courses_for_student = db.session.execute(select(CourseStudentModel.course_id)
                                          .where(CourseStudentModel.student_id == student_id)).all()
    return course_id in [course_id[0] for course_id in courses_for_student]
