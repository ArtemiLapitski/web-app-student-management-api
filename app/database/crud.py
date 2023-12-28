from sqlalchemy import insert, select, delete, func
from app.database.connection import session
from app.database.models import StudentModel, GroupModel, CourseModel, course_student_table


def add_student(first_name: str, last_name: str, courses: list, group: str = None):

    with session:
        group_id = session.scalars(
            select(GroupModel.group_id).where(GroupModel.group_name == group)).first()
        student_id = session.execute(
            insert(StudentModel).values(group_id=group_id, first_name=first_name, last_name=last_name)
        ).inserted_primary_key[0]

        for course_name in courses:
            course_id = session.scalars(select(CourseModel.course_id)
                                        .where(CourseModel.course_name == course_name)).first()
            session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))

        session.commit()

    return student_id


def get_student(student_id: int) -> dict:
    with session:
        name_and_group_data = session.execute(
            select(StudentModel.first_name, StudentModel.last_name, GroupModel.group_name)
            .join(GroupModel, GroupModel.group_id == StudentModel.group_id)
            .where(StudentModel.student_id == student_id)
        ).first()

        courses_row = session.execute(select(CourseModel.course_name)
                                      .join(course_student_table,
                                            course_student_table.c.course_id == CourseModel.course_id)
                                      .where(course_student_table.c.student_id == student_id))

        courses = [course[0] for course in courses_row]

        if not name_and_group_data:
            name_and_group_data = session.execute(select(StudentModel.first_name, StudentModel.last_name,)
                                                  .where(StudentModel.student_id == student_id)).first()

            student_data = {
                'student_id': student_id,
                'first_name': name_and_group_data[0],
                'last_name': name_and_group_data[1],
                'group': 'no_group',
                'courses': courses
                            }
        else:
            student_data = {
                'student_id': student_id,
                'first_name': name_and_group_data[0],
                'last_name': name_and_group_data[1],
                'group': name_and_group_data[2],
                'courses': courses
                            }

    return student_data


def get_groups_lte_student_count(students_count: int) -> list:
    with session:
        groups = session.execute(select(GroupModel.group_name)
                              .join_from(StudentModel, GroupModel, isouter=True)
                              .group_by(GroupModel.group_name)
                              .having(func.count(StudentModel.student_id) <= students_count)
                              ).all()
    return [group[0] if group[0] else "no_group" for group in groups]


def get_students_for_course(course_name: str) -> list:
    with session:
        students_for_course = session.execute(
            select(StudentModel.first_name, StudentModel.last_name)
            .join(course_student_table, course_student_table.c.student_id == StudentModel.student_id)
            .join(CourseModel, course_student_table.c.course_id == CourseModel.course_id)
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
        courses_for_student = session.execute(select(course_student_table.c.course_id)
                                              .where(course_student_table.c.student_id == student_id)).all()
    return course_id in [course_id[0] for course_id in courses_for_student]


def add_course_to_student(student_id: int, course_id: int):
    with session:
        session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))
        session.commit()


def delete_student_from_course(student_id: int, course_id: int):
    with session:
        session.execute(delete(course_student_table)
                        .where(course_student_table.c.student_id == student_id)
                        .where(course_student_table.c.course_id == course_id))
        session.commit()
