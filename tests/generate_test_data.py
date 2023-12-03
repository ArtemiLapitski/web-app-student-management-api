from random import choice, randint
from string import ascii_uppercase, digits
from sqlalchemy import insert, select, Table


STUDENTS_PER_GROUP_MIN = 10
STUDENTS_PER_GROUP_MAX = 30
COURSES_PER_STUDENT_MIN = 1
COURSES_PER_STUDENT_MAX = 3

COURSES = ['Physical Education', 'Science', 'Art', 'Mathematics', 'English', 'Music', 'Chemistry', 'Algebra', 'Physics',
           'Geography']
NAMES = ['Luca', 'Sasha', 'Amaya', 'Chace', 'Amiah', 'Essence', 'Shyann', 'Jackson', 'Jamar', 'Emanuel', 'Kristin',
         'Brenna', 'Gaige', 'Brianna', 'Quinn', 'Colten', 'Raphael', 'Keyon', 'Kennedi', 'Mackenzie']
SURNAMES = ['Schaefer', 'Sharp', 'Newton', 'Armstrong', 'Reynolds', 'Hamilton', 'Romero', 'Rush', 'Alvarez',
            'Williamson', 'Fletcher', 'Cannon', 'Blackwell', 'Mora', 'Ford', 'Lowe', 'Hutchinson', 'Pineda', 'Chaney',
            'Best']


def generate_groups() -> list:

    groups = []
    while len(groups) != 10:
        group = "".join([
                choice(ascii_uppercase),
                choice(ascii_uppercase),
                "-",
                choice(digits),
                choice(digits)
                ])
        if group not in groups:
            groups.append(group)

    return groups


def generate_students() -> list:

    students = [(i, choice(NAMES), choice(SURNAMES)) for i, _ in enumerate(range(200), start=1)]

    return students


def assign_students_to_groups(students: list, groups: list) -> dict:

    students_copy = students.copy()

    students_by_groups = {}
    for group in groups:
        group_size = randint(STUDENTS_PER_GROUP_MIN, STUDENTS_PER_GROUP_MAX)
        if len(students_copy) >= group_size:
            students_by_groups[group] = [students_copy.pop() for _ in range(group_size)]

    if students_copy:
        students_by_groups['no_group'] = students_copy

    return students_by_groups


def assign_courses_to_students(students: list) -> dict:

    courses_by_students = {student: {'courses': []} for student in students}
    for student in students:
        courses_amount = randint(COURSES_PER_STUDENT_MIN, COURSES_PER_STUDENT_MAX)
        while len(courses_by_students[student]['courses']) < courses_amount:
            course = choice(COURSES)
            if course not in courses_by_students[student]['courses']:
                courses_by_students[student]['courses'].append(course)

    return courses_by_students


def get_courses_and_group_by_students(courses_by_students: dict, students_by_groups: dict):
    for group, students in students_by_groups.items():
        for student in students:
            courses_by_students[student]['group'] = group

    return courses_by_students


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


# def add_test_data()