from sqlalchemy import insert, select, delete, func
from app.database.connection import session
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel


def get_list_of_courses() -> list:
    with session:
        all_courses = session.execute(select(CourseModel.course_name)).all()

    return [course_name[0] for course_name in all_courses]


def get_list_of_groups() -> list:
    with session:
        all_groups = session.execute(select(GroupModel.group_name)).all()

    return [group[0] for group in all_groups]


def check_student_id(student_id: int):
    with session:
        is_student = bool(session.execute(
            select(StudentModel.student_id).where(StudentModel.student_id == student_id)
        ).all())

    return is_student


def check_course_id(course_id: int):
    with session:
        is_course = bool(
            session.execute(select(CourseModel.course_id).where(CourseModel.course_id == course_id)).all())
    return is_course


def check_course_for_student(student_id: int, course_id: int):
    with session:
        courses_for_student = session.execute(select(CourseStudentModel.course_id)
                                              .where(CourseStudentModel.student_id == student_id)).all()
    return course_id in [course_id[0] for course_id in courses_for_student]