from sqlalchemy import insert, select, delete, create_engine, func, URL
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from app.database.setup import (get_session, get_course_table, get_student_group_table, get_student_table,
                                get_course_student_table, get_metadata_obj)


user_db_url = URL.create(
    "postgresql",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(user_db_url)

metadata_obj = get_metadata_obj(engine)

student_table = get_student_table(metadata_obj)
student_group_table = get_student_group_table(metadata_obj)
course_table = get_course_table(metadata_obj)
course_student_table = get_course_student_table(metadata_obj)

session = get_session(engine)


def add_student(first_name: str, last_name: str, courses: list, group: str = None):

    with session:
        group_id = session.scalars(
            select(student_group_table.c.group_id).where(student_group_table.c.group_name == group)).first()
        student_id = session.execute(
            insert(student_table).values(group_id=group_id, first_name=first_name, last_name=last_name)
        ).inserted_primary_key[0]

        for course_name in courses:
            course_id = session.scalars(select(course_table.c.course_id)
                                        .where(course_table.c.course_name == course_name)).first()
            session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))

        session.commit()

    return student_id


def get_student(student_id: int) -> dict:
    with session:
        name_and_group_data = session.execute(
            select(student_table.c['first_name', 'last_name'], student_group_table.c.group_name)
            .join(student_group_table, student_group_table.c.group_id == student_table.c.group_id)
            .where(student_table.c.student_id == student_id)
        ).first()

        courses_row = session.execute(select(course_table.c.course_name)
                                      .join(course_student_table,
                                            course_student_table.c.course_id == course_table.c.course_id)
                                      .where(course_student_table.c.student_id == student_id))

        courses = [course[0] for course in courses_row]

        if not name_and_group_data:
            name_and_group_data = session.execute(select(student_table.c['first_name', 'last_name'])
                                                  .where(student_table.c.student_id == student_id)).first()

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
         groups = session.execute(select(student_group_table.c.group_name)
                                  .join_from(student_table, student_group_table, isouter=True)
                                  .group_by(student_group_table.c.group_name)
                                  .having(func.count(student_table.c.student_id) <= students_count)
                                  ).all()
     return [group[0] if group[0] else "no_group" for group in groups]


def get_students_for_course(course_name: str) -> list:
    with session:
        students_for_course = session.execute(
            select(student_table.c.first_name, student_table.c.last_name)
            .join(course_student_table, course_student_table.c.student_id == student_table.c.student_id)
            .join(course_table, course_student_table.c.course_id == course_table.c.course_id)
            .where(course_table.c.course_name == course_name)
        ).all()

    return [f"{first_name} {last_name}" for first_name, last_name in students_for_course]


def get_list_of_courses() -> list:
    with session:
        all_courses = session.execute(select(course_table.c.course_name)).all()

    return [course_name[0] for course_name in all_courses]


def get_list_of_groups() -> list:
    with session:
        all_groups = session.execute(select(student_group_table.c.group_name)).all()

    return [group[0] for group in all_groups]


def delete_student(student_id: int):
    with session:
        session.execute(delete(student_table).where(student_table.c.student_id == student_id))
        session.commit()


def check_student_id(student_id: int):
    with session:
        is_student = bool(session.execute(
            select(student_table.c.student_id).where(student_table.c.student_id == student_id)
        ).all())

    return is_student


def check_course_id(course_id: int):
    with session:
        is_course = bool(
            session.execute(select(course_table.c.course_id).where(course_table.c.course_id == course_id)).all())
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
