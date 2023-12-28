import json

student_count_lte = 15
course = 'Physics'


def test_groups(client, setup_db, create_test_tables, generate_and_get_data, add_data):

    response = client.get('groups', query_string={'student_count_lte': student_count_lte})

    actual = json.loads(response.data)

    students_by_groups = generate_and_get_data['students_by_groups']

    groups_with_lte_student_count = [group for group, students in students_by_groups.items() if len(students) <= student_count_lte]

    assert set(actual) == set(groups_with_lte_student_count)


def test_courses_by_students(client, setup_db, create_test_tables, generate_and_get_data, add_data):

    response = client.get('students', query_string={'course': course})

    actual = json.loads(response.data)

    courses_by_students = generate_and_get_data['courses_by_students']

    students_for_course = [' '.join([student[1], student[2]])
                           for student, courses in courses_by_students.items() if course in courses]

    assert set(actual) == set(students_for_course)


courses_and_group_by_students_mocked = {(1, 'Jackson', 'Mora'): {
                                             'courses': ['Art'],
                                             'group': 'ZF-86'},
                                        (2, 'Luca', 'Rush'): {
                                            'courses': ['Chemistry', 'Art', 'English'],
                                            'group': 'FD-64'},
                                        (3, 'Amaya', 'Schaefer'): {
                                            'courses': ['Mathematics', 'Geography', 'Algebra'],
                                            'group': 'no_group'}
                                        }
# groups = ['ZF-86', 'FD-64']


def test_add_course_to_student(client, setup_db, create_test_tables, generate_and_get_data, add_data):

    response = client.post('students/1/courses/4', query_string={'course': course})

    actual = json.loads(response.data)

    courses_by_students = generate_and_get_data['courses_by_students']

    students_for_course = [' '.join([student[1], student[2]])
                           for student, courses in courses_by_students.items() if course in courses]

    assert set(actual) == set(students_for_course)