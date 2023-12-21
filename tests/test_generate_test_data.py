import pytest
from app.generate_test_data import generate_students, generate_groups, assign_students_to_groups, \
    assign_courses_to_students, get_courses_and_group_by_students
from config import STUDENTS_PER_GROUP_MAX, STUDENTS_PER_GROUP_MIN, COURSES


@pytest.mark.parametrize('execution_number', range(100))
def test_generate_students(execution_number):
    students_for_test = generate_students()
    assert len(students_for_test) == 200


@pytest.mark.parametrize('execution_number', range(100))
def test_generate_groups(execution_number):
    groups_for_test = generate_groups()
    assert len(set(groups_for_test)) == 10


def test_courses():
    assert len(set(COURSES)) == 10


@pytest.mark.parametrize('execution_number', range(100))
def test_assign_students_to_groups(execution_number):
    students = generate_students()
    groups = generate_groups()
    students_by_groups = assign_students_to_groups(students, groups)

    amount_of_students_per_group = []
    for group, students in students_by_groups.items():
        amount_of_students_per_group.append(len(students))
        if group != "no_group":
            assert STUDENTS_PER_GROUP_MIN <= len(students) <= STUDENTS_PER_GROUP_MAX

    assert sum(amount_of_students_per_group) == 200


@pytest.mark.parametrize('execution_number', range(100))
def test_assign_courses_to_students(execution_number):
    students = generate_students()
    courses_by_students = assign_courses_to_students(students)

    for _, courses in courses_by_students.items():
        assert len(courses) in (1, 2, 3)
        assert len(courses) == len(set(courses))

    assert len(courses_by_students.keys()) == 200


@pytest.mark.parametrize('execution_number', range(100))
def test_courses_in_courses_and_group_by_students(execution_number):
    groups = generate_groups()
    students = generate_students()

    students_by_groups = assign_students_to_groups(students, groups)
    courses_by_students = assign_courses_to_students(students)

    courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

    for student, data in courses_and_group_by_students.items():
        assert data['courses'] == courses_by_students[student]


@pytest.mark.parametrize('execution_number', range(100))
def test_groups_in_courses_and_group_by_students(execution_number):
    groups = generate_groups()
    students = generate_students()

    students_by_groups = assign_students_to_groups(students, groups)
    courses_by_students = assign_courses_to_students(students)

    courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

    group_student_tuples = [(data['group'], student) for student, data in courses_and_group_by_students.items()]

    students_by_group_recreated = {}
    for group, student in group_student_tuples:
        if group not in students_by_group_recreated.keys():
            students_by_group_recreated[group] = []
        students_by_group_recreated[group].append(student)

    for group, students in students_by_group_recreated.items():
        if group is not 'no_group':
            students.reverse()
            students_by_group_recreated[group] = students

    assert students_by_group_recreated == students_by_groups


@pytest.mark.parametrize('execution_number', range(100))
def test_courses_in_courses_and_group_by_students(execution_number):
    groups = generate_groups()
    students = generate_students()

    students_by_groups = assign_students_to_groups(students, groups)
    courses_by_students = assign_courses_to_students(students)

    courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

    assert len(courses_and_group_by_students.keys()) == len(courses_by_students.keys())







