# from docker.database import create_db, create_tables, add_test_data_to_db, get_session
from app.database.setup import create_db, create_tables, add_and_retrieve_test_data, get_session
from os import environ
# to delete
from sqlalchemy import URL, create_engine, text


SUPERUSER_USERNAME = environ['DB_SUPERUSER_USERNAME']
SUPERUSER_PASSWORD = environ['DB_SUPERUSER_PASSWORD']
USERNAME = environ['DB_USERNAME']
PASSWORD = environ['DB_PASSWORD']
DB_NAME = environ['DB_NAME']
ROLE = environ['DB_ROLE']
PORT = int(environ['DB_PORT'])
HOST = "host.docker.internal"

# to delete
# SUPERUSER_USERNAME='postgres'
# SUPERUSER_PASSWORD='1996'
# USERNAME='supervisor'
# PASSWORD='supervisor'
# DB_NAME='studentsdb'
# ROLE='students_admin'
# PORT=5432
# HOST = 'localhost'


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
        create_tables(engine, 'app/database/create_tables.sql'))

    session = get_session(engine)
    add_and_retrieve_test_data(student_group_table,
                               course_table,
                               student_table,
                               course_student_table,
                               session)

    # to delete
    # superuser_url = URL.create(
    #     "postgresql",
    #     username=SUPERUSER_USERNAME,
    #     password=SUPERUSER_PASSWORD,
    #     host=HOST,
    #     port=PORT
    # )
    # engine = create_engine(superuser_url)
    # with engine.connect() as conn:
    #     conn.execution_options(isolation_level="AUTOCOMMIT")
    #     conn.execute(text(f"DROP DATABASE {DB_NAME} WITH (FORCE)"))
    #     conn.execute(text(f"DROP USER {USERNAME}"))
    #     conn.execute(text(f"DROP ROLE {ROLE}"))
