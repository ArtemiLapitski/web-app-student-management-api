import pytest
from app import (GROUP_SIZES, COURSES_AMOUNT_PER_STUDENT, assign_students_to_groups, assign_courses_to_students,
                 generate_students, get_courses_and_group_by_students, generate_groups)

group_sizes_for_testing = GROUP_SIZES.copy()
group_sizes_for_testing.append(0)

students = generate_students()


@pytest.mark.parametrize('execution_number', range(100))
def test_generate_students(execution_number):
    students_for_test = generate_students()
    assert len(students_for_test) == 200


@pytest.mark.parametrize('execution_number', range(100))
def test_generate_groups(execution_number):
    groups_for_test = generate_groups()
    assert len(set(groups_for_test)) == 10


@pytest.mark.parametrize('execution_number', range(100))
def test_assign_students_to_groups(execution_number):
    groups = generate_groups()
    students_by_groups = assign_students_to_groups(students, groups)

    total_students = []
    for group, students_per_group in students_by_groups.items():
        total_students.append(len(students_per_group))
        if group != "no_group":
            assert len(students_per_group) in group_sizes_for_testing

    assert sum(total_students) == 200


@pytest.mark.parametrize('execution_number', range(100))
def test_assign_courses_to_students(execution_number):
    courses_by_students = assign_courses_to_students(students)

    for _, courses in courses_by_students.items():
        assert len(courses) in (1, 2, 3)
        assert len(courses) == len(set(courses))
    assert len(courses_by_students.keys()) == 200


@pytest.mark.parametrize('execution_number', range(100))
def test_get_courses_and_group_by_students(execution_number):
    groups = generate_groups()
    students_by_groups = assign_students_to_groups(students, groups)
    courses_by_students = assign_courses_to_students(students)
    courses_and_group_by_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

    groups = []
    list_of_students = []
    for student, data in courses_and_group_by_students.items():
        groups.append(data['group'])
        assert len(data['courses']) in (1, 2, 3)
        list_of_students.append(student)
    assert set(students_by_groups.keys()) == set(groups)
    assert len(list_of_students) == 200



