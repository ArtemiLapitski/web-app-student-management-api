from sqlalchemy import select, func
from app.database.setup import (get_session, get_course_table, get_student_group_table, get_student_table,
                                get_course_student_table, get_metadata_obj)
from config import COURSES


def test_students(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db
    metadata_obj = get_metadata_obj(engine)

    student_table = get_student_table(metadata_obj)
    generated_students = generate_and_add_data['generated_students']

    session = get_session(engine)

    with (session):
        students_from_db = session.execute(select(student_table.c.student_id, student_table.c.first_name,
                                          student_table.c.last_name)).all()

    assert students_from_db == generated_students
    assert len(students_from_db) == 200


def test_groups(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db
    metadata_obj = get_metadata_obj(engine)

    student_group_table = get_student_group_table(metadata_obj)

    generated_groups = generate_and_add_data['generated_groups']

    session = get_session(engine)

    with (session):
        groups_from_db = session.execute(select(student_group_table.c.group_name)).all()

    groups_from_db_list = [group[0] for group in groups_from_db]

    assert groups_from_db_list == generated_groups
    assert len(groups_from_db) == 10


def test_courses(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db

    metadata_obj = get_metadata_obj(engine)

    course_table = get_course_table(metadata_obj)

    session = get_session(engine)

    with session:
        courses = session.execute(select(course_table.c.course_name)).all()

    courses = [course_name[0] for course_name in courses]

    assert courses == COURSES


def test_students_by_groups(setup_db, create_test_tables, generate_and_add_data):

    students_by_groups = generate_and_add_data['students_by_groups']

    for group, students in students_by_groups.items():
        students_name_only = [' '.join(student[1:]) for student in students]
        students_name_only.reverse()
        students_by_groups[group] = students_name_only

    engine = setup_db

    metadata_obj = get_metadata_obj(engine)

    student_group_table = get_student_group_table(metadata_obj)
    student_table = get_student_table(metadata_obj)

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

    students_by_groups_from_db_dict = {data[0]: data[1] for data in students_by_groups_from_db}
    if students_without_group:
        students_without_group_strings = [' '.join(student) for student in students_without_group]
        students_without_group_strings.reverse()
        students_by_groups_from_db_dict['no_group'] = students_without_group_strings

    assert students_by_groups == students_by_groups_from_db_dict


def test_courses_by_students(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db

    metadata_obj = get_metadata_obj(engine)

    course_table = get_course_table(metadata_obj)
    student_table = get_student_table(metadata_obj)
    course_student_table = get_course_student_table(metadata_obj)

    session = get_session(engine)

    with (session):
        courses_by_students_from_bd = session.execute(
            select(
                func.concat(student_table.c.student_id,
                            ' ',
                            student_table.c.first_name,
                            ' ',
                            student_table.c.last_name
                            ),
                func.array_agg(course_table.c.course_name)
            )
            .select_from(course_student_table)
            .join(course_table, course_table.c.course_id == course_student_table.c.course_id)
            .join(student_table, course_student_table.c.student_id == student_table.c.student_id)
            .group_by(func.concat(student_table.c.student_id,
                                  ' ',
                                  student_table.c.first_name,
                                  ' ',
                                  student_table.c.last_name))

        ).all()

    courses_by_students_from_bd = {(int(student.split()[0]), student.split()[1], student.split()[2]): courses for student, courses in courses_by_students_from_bd}

    courses_by_students = generate_and_add_data['courses_by_students']

    assert courses_by_students_from_bd == courses_by_students
