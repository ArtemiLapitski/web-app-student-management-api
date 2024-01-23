from sqlalchemy import URL, text, create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel


def create_db_and_user(superuser_username: str,
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

    db_superuser_url = URL.create(
        "postgresql",
        username=superuser_username,
        password=superuser_password,
        host=host,
        port=port,
        database=db_name
    )
    engine = create_engine(db_superuser_url)
    with engine.connect() as conn:
        conn.execute(text(f"GRANT ALL ON SCHEMA public TO {role}"))
        conn.commit()

    # db_user_url = URL.create(
    #     "postgresql",
    #     username=username,
    #     password=password,
    #     host=host,
    #     port=port,
    #     database=db_name
    # )
    # engine = create_engine(db_user_url)
    #
    # return engine


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


# def get_id_or_create_course(session, model, course_name):
#     instance = session.query(model).filter_by(course_name=course_name).first()
#
#     if not instance:
#         instance = model(course_name=course_name)
#         session.add(instance)
#         session.commit()
#
#     return instance.course_id
#
#
# def get_id_or_create_group(session, model, group_name):
#
#     if not group_name:
#         return None
#
#     else:
#         instance = session.query(model).filter_by(group_name=group_name).first()
#
#         if not instance:
#             instance = model(group_name=group_name)
#             session.add(instance)
#             session.commit()
#
#         return instance.group_id


def add_courses(session, courses: list):
    with session:
        for course in courses:
            session.add(CourseModel(course_name=course))
        session.commit()


def add_groups(session, groups: list):
    with session:
        for group in groups:
            session.add(GroupModel(group_name=group))
        session.commit()


def add_students(session, data_by_student: dict):
    with session:
        for student_name, data in data_by_student.items():

            group_name = data.get('group')
            if not group_name:
                group_id = None
            else:
                group_id = session.query(GroupModel.group_id).filter_by(group_name=group_name).first()[0]

            student = StudentModel(first_name=student_name[1], last_name=student_name[2], group_id=group_id)
            session.add(student)
            session.commit()

            for course_name in data['courses']:
                course_id = session.query(CourseModel.course_id).filter_by(course_name=course_name).first()[0]
                session.add(CourseStudentModel(course_id=course_id, student_id=student.student_id))

        session.commit()


def add_data(session, groups: list, courses: list, data_by_student: dict):
    add_courses(session, courses)
    add_groups(session, groups)
    add_students(session, data_by_student)
