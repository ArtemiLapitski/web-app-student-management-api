from sqlalchemy import URL, text, insert, select, create_engine
from sqlalchemy.orm import sessionmaker
from config import COURSES
from app.database.models import StudentModel, GroupModel, CourseModel, course_student_table


def create_db(superuser_username: str,
              superuser_password: str,
              username: str,
              password: str,
              db_name: str,
              role: str,
              port: int,
              host: str):

    superuser_url = URL.create(
        "postgresql",
        username=superuser_username,
        password=superuser_password,
        host=host,
        port=port
    )
    engine = create_engine(superuser_url)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"CREATE DATABASE {db_name}"))
        conn.execute(text(f"CREATE ROLE {role}"))
        conn.execute(text(f"CREATE USER {username} PASSWORD '{password}'"))
        conn.execute(text(f"GRANT {role} TO {username}"))

    superuser_db_url = URL.create(
        "postgresql",
        username=superuser_username,
        password=superuser_password,
        host=host,
        port=port,
        database=db_name
    )
    engine = create_engine(superuser_db_url)
    with engine.connect() as conn:
        conn.execute(text(f"GRANT ALL ON SCHEMA public TO {role}"))
        conn.commit()

    user_db_url = URL.create(
        "postgresql",
        username=username,
        password=password,
        host=host,
        port=port,
        database=db_name
    )
    engine = create_engine(user_db_url)

    return engine


def create_tables(engine, sql_file_path: str):

    with engine.connect() as conn:
        with open(sql_file_path) as file:
            query = text(file.read())
            conn.execute(query)
            conn.commit()


def get_session(engine):
    Session = sessionmaker(engine)
    session = Session()

    return session


def add_courses(courses_list: list, session):
    courses_list_of_dict = [{'course_name': course_name} for course_name in courses_list]
    with session:
        session.execute(insert(CourseModel).values(courses_list_of_dict))
        session.commit()


def add_groups(groups: list, session):
    groups_list_of_dict = [{'group_name': group} for group in groups]
    with session:
        session.execute(insert(GroupModel).values(groups_list_of_dict))
        session.commit()


def add_students_and_course_student(courses_and_group_by_students: dict, session):
    with session:
        for student_name, data in courses_and_group_by_students.items():
            group = data['group']
            if group != 'no_group':
                group_id = session.scalars(
                    select(GroupModel.group_id).where(GroupModel.group_name == group)).first()
                student_id = session.execute(insert(StudentModel).values(
                    group_id=group_id, first_name=student_name[1], last_name=student_name[2])).inserted_primary_key[0]
            else:
                student_id = session.execute(
                    insert(StudentModel)
                    .values(first_name=student_name[1], last_name=student_name[2])).inserted_primary_key[0]
            for course_name in data['courses']:
                course_id = session.scalars(
                    select(CourseModel.course_id).where(CourseModel.course_name == course_name)).first()
                session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))
        session.commit()


def add_test_data(
    session,
    generated_groups: list,
    courses_and_group_by_students: dict,
    **kwargs
):

    add_groups(generated_groups, session)
    add_courses(COURSES, session)
    add_students_and_course_student(courses_and_group_by_students, session)


