from sqlalchemy import URL, text, insert, select, create_engine
from sqlalchemy.orm import sessionmaker
from config import COURSES
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel


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


# def add_courses(courses_list: list, session):
#     courses_list_of_dict = [{'course_name': course_name} for course_name in courses_list]
#     with session:
#         session.execute(insert(CourseModel).values(courses_list_of_dict))
#         session.commit()
#
#
# def add_groups(groups: list, session):
#     groups_list_of_dict = [{'group_name': group} for group in groups]
#     with session:
#         session.execute(insert(GroupModel).values(groups_list_of_dict))
#         session.commit()


# def add_students_and_course_student(courses_and_group_by_students: dict, session):
#     with session:
#         for student_name, data in courses_and_group_by_students.items():
#             group = data['group']
#             if group != 'no_group':
#                 group_id = session.scalars(
#                     select(GroupModel.group_id).where(GroupModel.group_name == group)).first()
#                 student_id = session.execute(insert(StudentModel).values(
#                     group_id=group_id, first_name=student_name[1], last_name=student_name[2])).inserted_primary_key[0]
#             else:
#                 student_id = session.execute(
#                     insert(StudentModel)
#                     .values(first_name=student_name[1], last_name=student_name[2])).inserted_primary_key[0]
#             for course_name in data['courses']:
#                 course_id = session.scalars(
#                     select(CourseModel.course_id).where(CourseModel.course_name == course_name)).first()
#                 session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))
#         session.commit()

def get_id_or_create_course(session, model, course_name):
    instance = session.query(model).filter_by(course_name=course_name).first()

    if not instance:
        instance = model(course_name=course_name)
        session.add(instance)
        session.commit()

    return instance.course_id


def get_id_or_create_group(session, model, group_name):

    if not group_name:
        return None

    else:
        instance = session.query(model).filter_by(group_name=group_name).first()

        if not instance:
            instance = model(group_name=group_name)
            session.add(instance)
            session.commit()

        return instance.group_id


def add_data(session, data_by_student: dict):
    with session:
        for student_name, data in data_by_student.items():

            # group = data['group']
            # if group != 'no_group':
            #     group_id = get_id_or_create_group(session, GroupModel, group_name=group)
            #     student = StudentModel(group_id=group_id, first_name=student_name[1], last_name=student_name[2])
            # else:
            #     student = StudentModel(first_name=student_name[1], last_name=student_name[2])
            # session.add(student)
            # session.commit()

            group_name = data.get('group')
            group_id = get_id_or_create_group(session, GroupModel, group_name=group_name)
            student = StudentModel(first_name=student_name[1], last_name=student_name[2], group_id=group_id)
            session.add(student)
            session.commit()

            for course_name in data['courses']:
                course_id = get_id_or_create_course(session, CourseModel, course_name=course_name)
                session.add(CourseStudentModel(course_id=course_id, student_id=student.student_id))

        session.commit()




