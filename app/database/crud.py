from sqlalchemy import func
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel
from app.database.db import db


def add_student(first_name: str, last_name: str, courses: list, group: str) -> int:
    if group:
        group_id = db.session.query(GroupModel).filter_by(group_name=group).first().group_id
    else:
        group_id = None

    student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
    db.session.add(student)
    db.session.commit()
    student_id = student.student_id

    for course_name in courses:

        course_id = db.session.query(CourseModel).filter_by(course_name=course_name).first().course_id
        db.session.add(CourseStudentModel(course_id=course_id, student_id=student_id))

    db.session.commit()

    return student_id


def get_student(student_id: int) -> dict:
    is_group = db.session.query(StudentModel.query.filter(StudentModel.student_id == student_id)
                                .filter(StudentModel.group_id != None).exists()).scalar()

    if is_group:
        student = db.session.query(StudentModel.first_name, StudentModel.last_name, GroupModel.group_name,
                                   func.array_agg(CourseModel.course_name)) \
            .filter(CourseStudentModel.course_id == CourseModel.course_id) \
            .filter(GroupModel.group_id == StudentModel.group_id) \
            .filter(StudentModel.student_id == student_id) \
            .filter(CourseStudentModel.student_id == StudentModel.student_id) \
            .group_by(StudentModel.first_name, StudentModel.last_name, GroupModel.group_name).first()
    else:
        student = db.session.query(StudentModel.first_name, StudentModel.last_name, None,
                                   func.array_agg(CourseModel.course_name)) \
            .filter(CourseStudentModel.course_id == CourseModel.course_id) \
            .filter(StudentModel.student_id == student_id) \
            .filter(CourseStudentModel.student_id == StudentModel.student_id) \
            .group_by(StudentModel.first_name, StudentModel.last_name).first()

    return {
        'student_id': student_id,
        'first_name': student[0],
        'last_name': student[1],
        'group': student[2],
        'courses': student[3]
    }


def get_groups_lte_student_count(students_count: int) -> list:
    groups = (db.session.query(GroupModel.group_name)
              .join(StudentModel)
              .having(func.count(StudentModel.student_id) <= students_count)
              .group_by(GroupModel.group_name).all())

    return [group[0] for group in groups]


def get_students_for_course(course_name: str) -> list:
    students_for_course = (db.session.query(StudentModel.first_name, StudentModel.last_name)
                           .join(CourseStudentModel, CourseStudentModel.student_id == StudentModel.student_id)
                           .join(CourseModel, CourseStudentModel.course_id == CourseModel.course_id)
                           .where(CourseModel.course_name == course_name)
                           .all())

    return [f"{first_name} {last_name}" for first_name, last_name in students_for_course]


def delete_student(student_id: int):
    student = db.session.query(StudentModel).filter_by(student_id=student_id).first()
    db.session.delete(student)
    db.session.commit()


def add_course_to_student(student_id: int, course_id: int):
    db.session.add(CourseStudentModel(course_id=course_id, student_id=student_id))
    db.session.commit()


def delete_student_from_course(student_id: int, course_id: int):
    instance = (db.session.query(CourseStudentModel)
                .where(CourseStudentModel.student_id == student_id)
                .where(CourseStudentModel.course_id == course_id)
                .first())
    db.session.delete(instance)
    db.session.commit()
