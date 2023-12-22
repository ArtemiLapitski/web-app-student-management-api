from random import choice, randint
from string import ascii_uppercase, digits
from config import (STUDENTS_PER_GROUP_MIN, STUDENTS_PER_GROUP_MAX, COURSES_PER_STUDENT_MAX, COURSES_PER_STUDENT_MIN,
                    COURSES, NAMES, SURNAMES)


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

    courses_by_students = {student: [] for student in students}
    for student in students:
        courses_amount = randint(COURSES_PER_STUDENT_MIN, COURSES_PER_STUDENT_MAX)
        while len(courses_by_students[student]) < courses_amount:
            course = choice(COURSES)
            if course not in courses_by_students[student]:
                courses_by_students[student].append(course)

    return courses_by_students


def get_courses_and_group_by_students(courses_by_students: dict, students_by_groups: dict):
    courses_and_group_by_students = {student: {'courses': courses} for student, courses in courses_by_students.items()}
    for group, students in students_by_groups.items():
        for student in students:
            courses_and_group_by_students[student]['group'] = group

    return courses_and_group_by_students


def generate_test_data():
    generated_students = generate_students()
    generated_groups = generate_groups()

    students_by_groups = assign_students_to_groups(generated_students, generated_groups)
    courses_by_students = assign_courses_to_students(generated_students)
    courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

    return {'generated_students': generated_students,
            'generated_groups': generated_groups,
            'students_by_groups': students_by_groups,
            'courses_by_students': courses_by_students,
            'courses_and_group_by_students': courses_and_group_by_students
            }
