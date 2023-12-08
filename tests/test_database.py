from sqlalchemy import select
from docker.database import get_session
from docker.generate_test_data import COURSES

SUPERUSER_USERNAME='postgres'
SUPERUSER_PASSWORD='1996'
USERNAME='supervisor_test'
PASSWORD='supervisor_test'
DB_NAME='studentsdb_test'
ROLE='students_admin_test'
PORT=5432
HOST='localhost'


def test_courses(setup_db, create_test_tables, add_test_data):
    engine = setup_db
    course_table, student_group_table, student_table, course_student_table = create_test_tables
    generated_students = add_test_data['students']
    generated_groups = add_test_data['groups']
    students_by_groups = add_test_data['students_by_groups']
    courses_by_students = add_test_data['courses_by_students']
    courses_and_group_by_students = add_test_data['courses_and_group_by_students']

    session = get_session(engine)

    with session:
        courses = session.execute(select(course_table.c.course_name)).all()
        groups = session.execute(select(student_group_table.c.group_name)).all()
        students = session.execute(select(student_table.c.first_name, student_table.c.last_name)).all()
        # students_by_groups = session.execute(select(student_table.c.first_name, student_table.c.last_name)).all()

    courses = [course_name[0] for course_name in courses]
    groups = [group_name[0] for group_name in groups]
    students = [(student[0], student[1]) for student in students]
    generated_students_without_enum = [(student[1], student[2]) for student in generated_students]
    # print(generated_students_without_enum)

    assert courses == COURSES
    assert groups == generated_groups
    assert students == generated_students_without_enum



