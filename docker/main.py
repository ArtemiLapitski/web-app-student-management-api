from database import create_db, add_groups, add_courses, add_students
from generate_test_data import (assign_students_to_groups, assign_courses_to_students, generate_students,
                                get_courses_and_group_by_students, generate_groups, COURSES)
from os import environ
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


# SUPERUSER_USERNAME = environ['SUPERUSER_USERNAME']
# SUPERUSER_PASSWORD = environ['SUPERUSER_PASSWORD']
# USERNAME = environ['USERNAME']
# PASSWORD = environ['PASSWORD']
# DB_NAME = environ['DB_NAME']
# ROLE = environ['ROLE']
# PORT = int(environ['PORT'])
# HOST = "host.docker.internal"

SUPERUSER_USERNAME='postgres'
SUPERUSER_PASSWORD='1996'
USERNAME='supervisor'
PASSWORD='supervisor'
DB_NAME='studentsdb'
ROLE='students_admin'
PORT=5432
HOST='localhost'


engine = create_db(superuser_username=SUPERUSER_USERNAME,
                   superuser_password=SUPERUSER_PASSWORD,
                   username=USERNAME,
                   password=PASSWORD,
                   db_name=DB_NAME,
                   role=ROLE,
                   port=PORT,
                   host=HOST)


Session = sessionmaker(engine)
session = Session()


metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)


course_table = metadata_obj.tables["course"]
student_table = metadata_obj.tables["student"]
student_group_table = metadata_obj.tables["student_group"]
course_student_table = metadata_obj.tables["course_student"]


students_list = generate_students()
groups_list = generate_groups()

students_by_groups = assign_students_to_groups(students_list, groups_list)
courses_by_students = assign_courses_to_students(students_list)
data_for_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

add_groups(groups_list, student_group_table, session)
add_courses(COURSES, course_table, session)
add_students(data_for_students, student_group_table, student_table, course_table, course_student_table, session)



# create_groups(groups_list, student_group_table)
# create_courses(COURSES, course_table)
# create_students(data_for_students, student_group_table, student_table, course_table, course_student_table)