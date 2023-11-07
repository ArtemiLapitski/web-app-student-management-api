from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from sqlalchemy import create_engine, Table
# from app import COURSES, courses


# def get_session(engine):
#     Session = sessionmaker(engine)
#     return Session()
# session = get_session(engine)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
session = Session()


def add_courses(courses_list: list, courses: Table):
    courses_list_of_dict = [{'course_name': course} for course in courses_list]
    with session:
        session.execute(insert(courses).values(courses_list_of_dict))
        session.commit()


def add_groups(groups_list: list, student_groups: Table):
    groups_list_of_dict = [{'group_name': group} for group in groups_list]
    with session:
        session.execute(insert(student_groups).values(groups_list_of_dict))
        session.commit()


def add_students(courses_and_group_by_students: dict,
                 student_groups: Table,
                 students: Table,
                 courses: Table,
                 courses_students: Table):
    with session:
        for student, data in courses_and_group_by_students.items():
            group = data['group']
            if group != 'no_group':
                group_id = session.execute(
                    select(student_groups.c.group_id).where(student_groups.c.group_name == group)).first()[0]
                student_id = session.execute(insert(students).values(
                    group_id=group_id, first_name=student[1], last_name=student[2])).inserted_primary_key[0]
            else:
                student_id = session.execute(
                    insert(students).values(first_name=student[1], last_name=student[2])).inserted_primary_key[0]
            for course in data['courses']:
                course_id = session.execute(
                    select(courses.c.course_id).where(courses.c.course_name == course)).first()[0]
                session.execute(insert(courses_students).values(course_id=course_id, student_id=student_id))

        session.commit()






# add_groups(groups_list)
# add_courses(COURSES)
# add_students()
