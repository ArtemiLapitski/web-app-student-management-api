from sqlalchemy import select, func
from app.database.setup import get_session, get_table_object
from config import COURSES
from pytest import mark
from app.generate_test_data import generate_groups

# SUPERUSER_USERNAME='postgres'
# SUPERUSER_PASSWORD='1996'
# USERNAME='supervisor_test'
# PASSWORD='supervisor_test'
# DB_NAME='studentsdb_test'
# ROLE='students_admin_test'
# PORT=5432
# HOST='localhost'


def test_students(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db
    student_table = get_table_object(engine, 'student')
    generated_students = generate_and_add_data['generated_students']

    session = get_session(engine)

    with (session):
        students_from_db = session.execute(select(student_table.c.student_id, student_table.c.first_name,
                                          student_table.c.last_name)).all()

    assert students_from_db == generated_students
    assert len(students_from_db) == 200


def test_groups(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db
    student_group_table = get_table_object(engine, 'student_group')
    generated_groups = generate_and_add_data['generated_groups']

    session = get_session(engine)

    with (session):
        groups_from_db = session.execute(select(student_group_table.c.group_name)).all()

    groups_from_db_list = [group[0] for group in groups_from_db]

    assert groups_from_db_list == generated_groups
    assert len(groups_from_db) == 10


def test_courses(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db

    course_table = get_table_object(engine, 'course')
    session = get_session(engine)

    with session:
        courses = session.execute(select(course_table.c.course_name)).all()

    courses = [course_name[0] for course_name in courses]

    assert courses == COURSES


# @mark.parametrize('execution_number', range(100))
def test_students_by_groups(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db

    student_group_table = get_table_object(engine, 'student_group')
    student_table = get_table_object(engine, 'student')

    # _, student_group_table, student_table, _ = create_test_tables
    students_by_groups = generate_and_add_data['students_by_groups']

    for group, students in students_by_groups.items():
        students_no_id = [' '.join(student[1:]) for student in students]
        students_no_id.reverse()
        students_by_groups[group] = students_no_id

    # print(students_by_groups)
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

    # try:
    assert students_by_groups == students_by_groups_from_db_dict
    # except AssertionError:
    #     print('from db', students_by_groups_from_db_dict['no_group'], students_without_group)
    #     print('print_new')
    #     print('from generated', students_by_groups['no_group'])
    #     raise AssertionError




# @mark.parametrize('execution_number', range(100))
def test_courses_by_students(setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db

    course_table = get_table_object(engine, 'course')
    student_table = get_table_object(engine, 'student')
    course_student_table = get_table_object(engine, 'course_student')

    courses_by_students = generate_and_add_data['courses_by_students']

    session = get_session(engine)

    with (session):
        courses_by_students_from_bd = session.execute(
            select(
                func.concat(student_table.c.student_id, ' ', student_table.c.first_name, ' ', student_table.c.last_name),
                func.array_agg(course_table.c.course_name)
            )
            .select_from(course_student_table)
            .join(course_table, course_table.c.course_id == course_student_table.c.course_id)
            .join(student_table, course_student_table.c.student_id == student_table.c.student_id)
            .group_by(func.concat(student_table.c.student_id, ' ', student_table.c.first_name, ' ', student_table.c.last_name))

        ).all()

    courses_by_students_from_bd = {(int(student.split()[0]), student.split()[1], student.split()[2]): courses for student, courses in courses_by_students_from_bd}
    # courses_by_students_from_bd = sorted(courses_by_students_from_bd.items(), key=lambda item: item[0])
    # print(courses_by_students_from_bd)

    # courses_by_students = [(student, courses) for student, courses in courses_by_students.items()]
    #
    # print(courses_by_students)
    # print(courses_by_students_from_bd)

    assert courses_by_students_from_bd == courses_by_students
