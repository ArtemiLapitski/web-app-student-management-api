from sqlalchemy import insert, select, delete, func
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
        # groups = session.execute(select(GroupModel.group_name)
        #                       .join_from(StudentModel, GroupModel, isouter=True)
        #                       .group_by(GroupModel.group_name)
        #                       .having(func.count(StudentModel.student_id) <= students_count)
        #                       ).all()

        groups = (session.query(GroupModel.group_name)
                  .join(StudentModel)
                  .having(func.count(StudentModel.student_id) <= students_count)
                  .group_by(GroupModel.group_name).all())

    return [group[0] for group in groups]


def get_students_for_course(course_name: str) -> list:
    with session:
        students_for_course = session.execute(
            select(StudentModel.first_name, StudentModel.last_name)
            .join(CourseStudentModel, CourseStudentModel.student_id == StudentModel.student_id)
            .join(CourseModel, CourseStudentModel.course_id == CourseModel.course_id)
            .where(CourseModel.course_name == course_name)
        ).all()

    return [f"{first_name} {last_name}" for first_name, last_name in students_for_course]


def get_list_of_courses() -> list:
    with session:
        all_courses = session.execute(select(CourseModel.course_name)).all()

    return [course_name[0] for course_name in all_courses]


def get_list_of_groups() -> list:
    with session:
        all_groups = session.execute(select(GroupModel.group_name)).all()

    return [group[0] for group in all_groups]


def delete_student(student_id: int):
    with session:
        session.execute(delete(StudentModel).where(StudentModel.student_id == student_id))
        session.commit()


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


def add_course_to_student(student_id: int, course_id: int):
    with session:
        session.execute(insert(CourseStudentModel).values(course_id=course_id, student_id=student_id))
        session.commit()


def delete_student_from_course(student_id: int, course_id: int):
    with session:
        session.execute(delete(CourseStudentModel)
                        .where(CourseStudentModel.student_id == student_id)
                        .where(CourseStudentModel.course_id == course_id))
        session.commit()
