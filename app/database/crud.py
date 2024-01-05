from sqlalchemy import func
from app.database.connection import session
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel


def add_student(first_name: str, last_name: str, courses: list, group: str):

    with session:

        if group:
            group_id = session.query(GroupModel).filter_by(group_name=group).first().group_id
        else:
            group_id = None

        student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
        session.add(student)
        session.commit()
        student_id = student.student_id

        for course_name in courses:

            course_id = session.query(CourseModel).filter_by(course_name=course_name).first().course_id
            session.add(CourseStudentModel(course_id=course_id, student_id=student_id))

        session.commit()

        return student_id


def get_student(student_id: int) -> dict:
    with session:

        group = (session.query(GroupModel.group_name)
                 .filter(StudentModel.student_id == student_id)
                 .filter(StudentModel.group_id == GroupModel.group_id)
                 .first())
        if group:
            group = group[0]

        first_and_last_name = (session.query(StudentModel.first_name, StudentModel.last_name)
                               .filter(StudentModel.student_id == student_id)
                               .first())

        courses = (session.query(CourseModel.course_name)
                   .filter(CourseStudentModel.course_id == CourseModel.course_id)
                   .filter(CourseStudentModel.student_id == student_id)
                   .all())

        courses = [course[0] for course in courses]

    return {
                'student_id': student_id,
                'first_name': first_and_last_name[0],
                'last_name': first_and_last_name[1],
                'group': group,
                'courses': courses
            }


def get_groups_lte_student_count(students_count: int) -> list:
    with session:
        groups = (session.query(GroupModel.group_name)
                  .join(StudentModel)
                  .having(func.count(StudentModel.student_id) <= students_count)
                  .group_by(GroupModel.group_name).all())

    return [group[0] for group in groups]


def get_students_for_course(course_name: str) -> list:
    with session:
        students_for_course = (session.query(StudentModel.first_name, StudentModel.last_name)
                               .join(CourseStudentModel, CourseStudentModel.student_id == StudentModel.student_id)
                               .join(CourseModel, CourseStudentModel.course_id == CourseModel.course_id)
                               .where(CourseModel.course_name == course_name)
                               .all())

    return [f"{first_name} {last_name}" for first_name, last_name in students_for_course]


def delete_student(student_id: int):
    with session:
        student = session.query(StudentModel).filter_by(student_id=student_id).first()
        session.delete(student)
        session.commit()


def add_course_to_student(student_id: int, course_id: int):
    with session:
        session.add(CourseStudentModel(course_id=course_id, student_id=student_id))
        session.commit()


def delete_student_from_course(student_id: int, course_id: int):
    with session:
        instance = (session.query(CourseStudentModel)
                    .where(CourseStudentModel.student_id == student_id)
                    .where(CourseStudentModel.course_id == course_id)
                    .first())
        session.delete(instance)
        session.commit()
