from sqlalchemy import select, func, literal_column
from app.database.setup import get_session
from config import COURSES

# SUPERUSER_USERNAME='postgres'
# SUPERUSER_PASSWORD='1996'
# USERNAME='supervisor_test'
# PASSWORD='supervisor_test'
# DB_NAME='studentsdb_test'
# ROLE='students_admin_test'
# PORT=5432
# HOST='localhost'


def test_students(setup_db, create_test_tables, add_test_data):
    engine = setup_db
    _, _, student_table, _ = create_test_tables
    generated_students = add_test_data['generated_students']

    session = get_session(engine)

    with (session):
        students_from_db = session.execute(select(student_table.c.student_id, student_table.c.first_name,
                                          student_table.c.last_name)).all()

    assert students_from_db == generated_students
    assert len(students_from_db) == 200


def test_groups(setup_db, create_test_tables, add_test_data):
    engine = setup_db
    _, student_group_table, _, _ = create_test_tables
    generated_groups = add_test_data['generated_groups']

    session = get_session(engine)

    with (session):
        groups_from_db = session.execute(select(student_group_table.c.group_name)).all()

    groups_from_db_list = [group[0] for group in groups_from_db]

    assert groups_from_db_list == generated_groups
    assert len(groups_from_db) == 10


def test_courses(setup_db, create_test_tables, add_test_data):
    engine = setup_db
    course_table, _, _, _ = create_test_tables

    session = get_session(engine)

    with session:
        courses = session.execute(select(course_table.c.course_name)).all()

    courses = [course_name[0] for course_name in courses]

    assert courses == COURSES


def test_students_by_groups(setup_db, create_test_tables, add_test_data):
    engine = setup_db
    _, student_group_table, student_table, _ = create_test_tables
    students_by_groups = add_test_data['students_by_groups']

    students_by_groups_new = {}
    for group, students in students_by_groups.items():
        student_list_new = []
        for student in students:
            student_list_new.append(f"{student[1]} {student[2]}")
        student_list_new.reverse()
        students_by_groups_new[group] = student_list_new

    session = get_session(engine)

    with session:

        students_by_groups_from_db = session.execute(select(
            student_group_table.c.group_name,
            func.array_agg(func.concat(student_table.c.first_name, ' ', student_table.c.last_name)))
            .join(student_table, student_table.c.group_id == student_group_table.c.group_id)
            .group_by(student_group_table.c.group_name)
            ).all()

        students_without_group = session.execute(select(student_table.c.first_name, student_table.c.last_name)
                                                 .where(student_table.c.group_id == None)).all()

    students_without_group = [f"{student[0]} {student[1]}" for student in students_without_group]
    students_by_groups_from_db = {data[0]: data[1] for data in students_by_groups_from_db}

    students_without_group.reverse()
    students_by_groups_from_db['no_group'] = students_without_group

    assert students_by_groups_new == students_by_groups_from_db


# def test_courses_by_students(setup_db, create_test_tables, add_test_data):
#     engine = setup_db
#     course_table, student_group_table, student_table, course_student_table = create_test_tables
#     generated_students = add_test_data['generated_students']
#     courses_by_students = add_test_data['courses_by_students']
#
#     session = get_session(engine)
#
#     with (session):
#         courses_by_students_from_bd = session.execute(
#             select(
#                 course_student_table.c.student_id,
#                 func.array_agg(course_table.c.course_name)
#             )
#             .join(course_table, course_table.c.course_id == course_student_table.c.course_id)
#             .group_by(course_student_table.c.student_id)
#         ).all()
#
#         print(courses_by_students_from_bd)
#         print(len(courses_by_students_from_bd))
#         print(courses_by_students.items())
#         print(len(courses_by_students.items()))



def test_courses_by_students(setup_db, create_test_tables, add_test_data):
    engine = setup_db
    course_table, student_group_table, student_table, course_student_table = create_test_tables
    generated_students = add_test_data['generated_students']
    courses_by_students = add_test_data['courses_by_students']

    session = get_session(engine)

    with (session):
        courses_by_students_from_bd = session.execute(
            select(
                func.concat(student_table.c.first_name, ' ', student_table.c.last_name),
                func.array_agg(course_table.c.course_name)
            )
            .select_from(course_student_table)
            .join(course_table, course_table.c.course_id == course_student_table.c.course_id)
            .join(student_table, course_student_table.c.student_id == student_table.c.student_id)
            .group_by(func.concat(student_table.c.first_name, ' ', student_table.c.last_name))

        ).all()

    print(courses_by_students_from_bd)
    print(len(courses_by_students_from_bd))
    print(courses_by_students.items())
    print(len(courses_by_students.items()))