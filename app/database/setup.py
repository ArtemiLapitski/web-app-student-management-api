from sqlalchemy import URL, text, create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from config import CREATE_TABLES_SQL_FILE_PATH


def create_db_and_user(
        superuser_username: str,
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


def get_session(engine: Engine) -> Session:
    Session = sessionmaker(engine)
    session = Session()
    return session


def add_courses(session: Session, courses: list):
    with session:
        for course in courses:
            session.add(CourseModel(course_name=course))
        session.commit()


def add_groups(session: Session, groups: list):
    with session:
        for group in groups:
            session.add(GroupModel(group_name=group))
        session.commit()


def add_students(session: Session, data_by_student: dict):
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


def add_data(session: Session, groups: list, courses: list, data_by_student: dict):
    add_courses(session, courses)
    add_groups(session, groups)
    add_students(session, data_by_student)


def create_tables_with_data(engine: Engine, session: Session, groups: list, courses: list, data_by_student: dict):
    with engine.connect() as conn:
        with open(CREATE_TABLES_SQL_FILE_PATH) as file:
            query = text(file.read())
            conn.execute(query)
            conn.commit()

    with session:
        add_data(session, groups=groups, courses=courses, data_by_student=data_by_student)


def drop_tables(engine: Engine):
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"DROP TABLE course_student"))
        conn.execute(text(f"DROP TABLE student"))
        conn.execute(text(f"DROP TABLE course"))
        conn.execute(text(f"DROP TABLE student_group"))
