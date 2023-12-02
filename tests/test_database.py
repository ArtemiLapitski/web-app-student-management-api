
from sqlalchemy import URL, create_engine, text, MetaData, select
# from docker.database import create_db
from app import (assign_students_to_groups, assign_courses_to_students, generate_students,
                                get_courses_and_group_by_students, generate_groups, COURSES)
from database import (add_students, add_groups, add_courses)
from sqlalchemy.orm import sessionmaker

SUPERUSER_USERNAME='postgres'
SUPERUSER_PASSWORD='1996'
USERNAME='supervisor_test'
PASSWORD='supervisor_test'
DB_NAME='studentsdb_test'
ROLE='students_admin_test'
PORT=5432
HOST='localhost'

def test_db():
    # engine = create_db(SUPERUSER_USERNAME,
    #                    SUPERUSER_PASSWORD,
    #                    USERNAME,
    #                    PASSWORD,
    #                    DB_NAME,
    #                    ROLE,
    #                    PORT,
    #                    HOST)

    superuser_url = URL.create(
        "postgresql",
        username=SUPERUSER_USERNAME,
        password=SUPERUSER_PASSWORD,
        host=HOST,
        port=PORT
    )
    engine = create_engine(superuser_url)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
        conn.execute(text(f"CREATE ROLE {ROLE}"))
        conn.execute(text(f"CREATE USER {USERNAME} PASSWORD '{PASSWORD}'"))
        conn.execute(text(f"GRANT {ROLE} TO {USERNAME}"))
    #
    # superuser_db_url = URL.create(
    #     "postgresql",
    #     username=SUPERUSER_USERNAME,
    #     password=SUPERUSER_PASSWORD,
    #     host=HOST,
    #     port=PORT,
    #     database=DB_NAME
    # )
    # engine = create_engine(superuser_db_url)
    # with engine.connect() as conn:
    #     conn.execute(text(f"GRANT ALL ON SCHEMA public TO {ROLE}"))
    #     conn.commit()
    #
    # user_db_url = URL.create(
    #     "postgresql",
    #     username=USERNAME,
    #     password=PASSWORD,
    #     host=HOST,
    #     port=PORT,
    #     database=DB_NAME
    # )
    # engine = create_engine(user_db_url)
    # with engine.connect() as conn:
    #     with open("create_tables.sql") as file:
    #         query = text(file.read())
    #         conn.execute(query)
    #         conn.commit()
    #
    # # return engine
    #
    # Session = sessionmaker(engine)
    # session = Session()
    #
    # metadata_obj = MetaData()
    # metadata_obj.reflect(bind=engine)
    #
    # course_table = metadata_obj.tables["course"]
    # student_table = metadata_obj.tables["student"]
    # student_group_table = metadata_obj.tables["student_group"]
    # course_student_table = metadata_obj.tables["course_student"]
    #
    # students_list = generate_students()
    # groups_list = generate_groups()
    #
    # students_by_groups = assign_students_to_groups(students_list, groups_list)
    # courses_by_students = assign_courses_to_students(students_list)
    # data_for_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)
    #
    # add_groups(groups_list, student_group_table, session)
    # add_courses(COURSES, course_table, session)
    # add_students(data_for_students, student_group_table, student_table, course_table, course_student_table, session)
    #
    # with session:
    #     all_courses = session.execute(select(course_table.c.course_name)).all()
    #
    # all_courses = [course_name[0] for course_name in all_courses]
    #
    # assert all_courses == COURSES




