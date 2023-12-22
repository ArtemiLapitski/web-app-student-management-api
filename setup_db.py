from app.database.setup import (create_db, create_tables, add_test_data, get_session, get_course_table,
                                get_course_student_table, get_student_table, get_student_group_table, get_metadata_obj)
from os import environ
from config import CREATE_TABLES_FILE_PATH

from app.generate_test_data import generate_test_data

SUPERUSER_USERNAME = environ['DB_SUPERUSER_USERNAME']
SUPERUSER_PASSWORD = environ['DB_SUPERUSER_PASSWORD']
USERNAME = environ['DB_USERNAME']
PASSWORD = environ['DB_PASSWORD']
DB_NAME = environ['DB_NAME']
ROLE = environ['DB_ROLE']
PORT = int(environ['DB_PORT'])
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

    create_tables(engine, CREATE_TABLES_FILE_PATH)

    metadata_obj = get_metadata_obj(engine)

    course_table = get_course_table(metadata_obj)
    student_group_table = get_student_group_table(metadata_obj)
    student_table = get_student_table(metadata_obj)
    course_student_table = get_course_student_table(metadata_obj)

    generated_test_data = generate_test_data()

    session = get_session(engine)

    add_test_data(
        session,
        student_group_table,
        course_table,
        student_table,
        course_student_table,
        **generated_test_data
    )
