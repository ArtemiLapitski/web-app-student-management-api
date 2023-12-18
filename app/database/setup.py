from sqlalchemy import URL, text, insert, select, create_engine, Table, MetaData, func
from sqlalchemy.orm import sessionmaker
from app.generate_test_data import (assign_students_to_groups, assign_courses_to_students, generate_students,
                                get_courses_and_group_by_students, generate_groups, COURSES)


# ADD TO SESSION and create db outbupt annotations
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

    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)

    course_table = metadata_obj.tables["course"]
    student_table = metadata_obj.tables["student"]
    student_group_table = metadata_obj.tables["student_group"]
    course_student_table = metadata_obj.tables["course_student"]

    return course_table, student_group_table, student_table, course_student_table


def get_session(engine):
    Session = sessionmaker(engine)
    session = Session()

    return session


def add_courses(courses_list: list, course_table: Table, session):
    courses_list_of_dict = [{'course_name': course_name} for course_name in courses_list]
    with session:
        session.execute(insert(course_table).values(courses_list_of_dict))
        session.commit()


def add_groups(groups_list: list, student_group_table: Table, session):
    groups_list_of_dict = [{'group_name': group} for group in groups_list]
    with session:
        session.execute(insert(student_group_table).values(groups_list_of_dict))
        session.commit()


def add_students(courses_and_group_by_students: dict,
                 student_group_table: Table,
                 student_table: Table,
                 course_table: Table,
                 course_student_table: Table,
                 session):
    with session:
        for student_name, data in courses_and_group_by_students.items():
            group = data['group']
            if group != 'no_group':
                group_id = session.scalars(
                    select(student_group_table.c.group_id).where(student_group_table.c.group_name == group)).first()
                student_id = session.execute(insert(student_table).values(
                    group_id=group_id, first_name=student_name[1], last_name=student_name[2])).inserted_primary_key[0]
            else:
                student_id = session.execute(
                    insert(student_table).values(first_name=student_name[1], last_name=student_name[2])).inserted_primary_key[0]
            for course_name in data['courses']:
                course_id = session.scalars(
                    select(course_table.c.course_id).where(course_table.c.course_name == course_name)).first()
                session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))
        session.commit()


def add_and_retrieve_test_data(student_group_table: Table,
                        course_table: Table,
                        student_table: Table,
                        course_student_table: Table,
                        session):

    generated_students = generate_students()
    generated_groups = generate_groups()

    students_by_groups = assign_students_to_groups(generated_students, generated_groups)
    courses_by_students = assign_courses_to_students(generated_students)
    courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

    add_groups(generated_groups, student_group_table, session)
    add_courses(COURSES, course_table, session)
    add_students(courses_and_group_by_students, student_group_table, student_table, course_table, course_student_table, session)

    return {'generated_students': generated_students,
            'generated_groups': generated_groups,
            'students_by_groups': students_by_groups,
            'courses_by_students': courses_by_students,
            'courses_and_group_by_students': courses_and_group_by_students
            }

#
# def get_groups_lte_student_count(students_count: int,
#                                 student_group_table: Table,
#                                 student_table: Table,
#                                 session) -> list:
#     with session:
#         groups = session.execute(select(student_group_table.c.group_name)
#                                  .join_from(student_table, student_group_table, isouter=True)
#                                  .group_by(student_group_table.c.group_name)
#                                  .having(func.count(student_table.c.student_id) <= students_count)
#                                  ).all()
#     return [group[0] if group[0] else "no_group" for group in groups]
#
#
# def get_students_for_course(course_name: str,
#                             course_table: Table,
#                             student_table: Table,
#                             course_student_table: Table,
#                             session) -> list:
#     with session:
#         students_for_course = session.execute(select(student_table.c.first_name, student_table.c.last_name)
#                                               .join(course_student_table,
#                                                     course_student_table.c.student_id == student_table.c.student_id)
#                                               .join(course_table, course_student_table.c.course_id == course_table.c.course_id)
#                                               .where(course_table.c.course_name == course_name)).all()
#
#     return [f"{first_name} {last_name}" for first_name, last_name in students_for_course]

