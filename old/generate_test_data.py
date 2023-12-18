from app import (NAMES, SURNAMES, COURSES, LOWER_BOUND_STUDENTS_PER_GROUP,
                 UPPER_BOUND_STUDENTS_PER_GROUP, LOWER_BOUND_COURSES_PER_STUDENT, UPPER_BOUND_COURSES_PER_STUDENT)
import random
import string


def generate_groups() -> list:

    characters = string.ascii_uppercase
    digits = string.digits

    groups = []
    while len(groups) != 10:
        group = "".join([
                random.choice(characters),
                random.choice(characters),
                "-",
                random.choice(digits),
                random.choice(digits)
                ])
        if group not in groups:
            groups.append(group)

    return groups


def generate_students() -> list:

    students = [(i, random.choice(NAMES), random.choice(SURNAMES)) for i, _ in enumerate(range(200), start=1)]

    return students


def assign_students_to_groups(students: list, groups: list) -> dict:

    students_copy = students.copy()

    students_by_groups = {}
    for group in groups:
        group_size = random.randint(LOWER_BOUND_STUDENTS_PER_GROUP, UPPER_BOUND_STUDENTS_PER_GROUP)
        if len(students_copy) >= group_size:
            students_by_groups[group] = [students_copy.pop() for _ in range(group_size)]

    if students_copy:
        students_by_groups['no_group'] = students_copy

    return students_by_groups


def assign_courses_to_students(students: list) -> dict:

    courses_by_students = {student: {'courses': []} for student in students}
    for student in students:
        courses_amount = random.randint(LOWER_BOUND_COURSES_PER_STUDENT, UPPER_BOUND_COURSES_PER_STUDENT)
        while len(courses_by_students[student]['courses']) < courses_amount:
            course = random.choice(COURSES)
            if course not in courses_by_students[student]['courses']:
                courses_by_students[student]['courses'].append(course)

    return courses_by_students


def get_courses_and_group_by_students(courses_by_students: dict, students_by_groups: dict):
    for group, students in students_by_groups.items():
        for student in students:
            courses_by_students[student]['group'] = group

    return courses_by_students












#
# students = generate_students()
# groups = generate_groups()
#
# students_by_groups = assign_students_to_groups(students, groups)
#
# courses_by_students = assign_courses_to_students(students)
#
#
# courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)
#
# print(courses_and_group_by_students)



#
# groups = []
# for student, data in courses_and_group_by_students.items():
#     groups.append(data['group'])
#     # assert len(data['courses']) in (1, 2, 3)
#
# for group, students in students_by_groups.items():
#     print(group, len(students))
#
# print(set(groups))
# assert len(set(groups)) in [10, 11]



