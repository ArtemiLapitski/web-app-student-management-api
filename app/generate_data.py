from random import choice, randint
from string import ascii_uppercase, digits
from config import (STUDENTS_PER_GROUP_MIN, STUDENTS_PER_GROUP_MAX, COURSES_PER_STUDENT_MAX, COURSES_PER_STUDENT_MIN,
                    COURSES, NAMES, SURNAMES, NUMBER_OF_STUDENTS)


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

    students = [(i, choice(NAMES), choice(SURNAMES)) for i, _ in enumerate(range(NUMBER_OF_STUDENTS), start=1)]

    return students


def get_courses() -> list:
    return COURSES


def assign_students_to_groups(students: list, groups: list) -> dict:

    students_copy = students.copy()

    students_by_group = {}
    for group in groups:
        group_size = randint(STUDENTS_PER_GROUP_MIN, STUDENTS_PER_GROUP_MAX)
        if len(students_copy) >= group_size:
            students_by_group[group] = [students_copy.pop() for _ in range(group_size)]

    if students_copy:
        students_by_group['no_group'] = students_copy

    return students_by_group


def assign_courses_to_students(students: list, courses: list) -> dict:

    courses_by_student = {student: [] for student in students}
    for student in students:
        courses_amount = randint(COURSES_PER_STUDENT_MIN, COURSES_PER_STUDENT_MAX)
        while len(courses_by_student[student]) < courses_amount:
            course = choice(courses)
            if course not in courses_by_student[student]:
                courses_by_student[student].append(course)

    return courses_by_student


def get_data_by_student(courses_by_students: dict, students_by_groups: dict) -> dict:
    data_by_student = {student: {'courses': courses} for student, courses in courses_by_students.items()}

    for group, students in students_by_groups.items():

        if group != 'no_group':
            for student in students:
                data_by_student[student]['group'] = group

    return data_by_student


def generate_test_data():
    generated_students = generate_students()
    generated_groups = generate_groups()
    courses = get_courses()

    students_by_group = assign_students_to_groups(generated_students, generated_groups)
    courses_by_student = assign_courses_to_students(generated_students, courses)

    data_by_student = get_data_by_student(courses_by_student, students_by_group)

    return {
            'groups': generated_groups,
            'courses': courses,
            'data_by_student': data_by_student
            }
