from database import create_db, create_tables, add_test_data_to_db, get_session
from os import environ


SUPERUSER_USERNAME = environ['SUPERUSER_USERNAME']
SUPERUSER_PASSWORD = environ['SUPERUSER_PASSWORD']
USERNAME = environ['USERNAME']
PASSWORD = environ['PASSWORD']
DB_NAME = environ['DB_NAME']
ROLE = environ['ROLE']
PORT = int(environ['PORT'])
HOST = "host.docker.internal"


if __name__ == "__main__":
    engine = create_db(superuser_username=SUPERUSER_USERNAME,
                       superuser_password=SUPERUSER_PASSWORD,
                       username=USERNAME,
                       password=PASSWORD,
                       db_name=DB_NAME,
                       role=ROLE,
                       port=PORT,
                       host=HOST)


    course_table, student_group_table, student_table, course_student_table = (
        create_tables(engine, 'create_tables.sql'))

    session = get_session(engine)
    add_test_data_to_db(student_group_table,
                        course_table,
                        student_table,
                        course_student_table,
                        session)
