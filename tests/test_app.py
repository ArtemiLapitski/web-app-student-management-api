import json


student_count_lte = 15
course = 'Physics'


def test_groups(client, setup_db, get_test_data, add_test_data):

    response = client.get('groups', query_string={'student_count_lte': student_count_lte})
    actual = json.loads(response.data)

    students_by_group = get_test_data['students_by_group']
    groups_with_lte_student_count = [group for group, students in students_by_group.items()
                                     if (len(students) <= student_count_lte) and (group != 'no_group')]

    assert set(actual) == set(groups_with_lte_student_count)


def test_courses_by_students(client, setup_db, get_test_data, add_test_data):

    response = client.get('students', query_string={'course': course})
    actual = json.loads(response.data)

    courses_by_student = get_test_data['courses_by_student']
    students_for_course = [' '.join([student[1], student[2]])
                           for student, courses in courses_by_student.items() if course in courses]

    assert set(actual) == set(students_for_course)


groups_mock = ['ZF-86', 'FD-64']

courses_mock = ['Physical Education',
           'Science',
           'Art',
           'Mathematics',
           'English',
           'Music',
           'Chemistry',
           'Algebra',
           'Physics',
           'Geography']

students_mock = [(1, 'Jackson', 'Mora'), (2, 'Luca', 'Rush'), (3, 'Amaya', 'Schaefer')]

data_by_student_mock = {(1, 'Jackson', 'Mora'): {
                                 'courses': ['Art'],
                                 'group': 'ZF-86'},
                            (2, 'Luca', 'Rush'): {
                                'courses': ['Chemistry', 'Art', 'English'],
                                'group': 'FD-64'},
                            (3, 'Amaya', 'Schaefer'): {
                                'courses': ['Geography', 'Algebra'],
                                'group': 'no_group'}
                            }


def test_add_course_to_student(client, setup_db, get_test_data, add_test_data, mocker):
    mocker.patch('app.generate_data.get_courses', return_value=courses_mock)
    mocker.patch('app.generate_data.generate_students', return_value=students_mock)
    mocker.patch('app.generate_data.generate_groups', return_value=groups_mock)
    mocker.patch('app.generate_data.get_data_by_student', return_value=data_by_student_mock)

    response = client.get('students', query_string={'course': course})
    actual = json.loads(response.data)
    print(actual)

    # response = client.post('students/3/courses/4', query_string={'course': course})
    #
    # actual = json.loads(response.data)
    #
    # courses_by_student = get_test_data['courses_by_student']
    #
    # students_for_course = [' '.join([student[1], student[2]])
    #                        for student, courses in courses_by_student.items() if course in courses]
    #
    # assert set(actual) == set(students_for_course)