import json
from tests.mocks import students_for_physics_mocked, groups_with_student_count_lte_15_mocked


def test_groups(db_setup, client, db_create_tables):
    groups_with_student_count_lte_15 = client.get('groups', query_string={'student_count_lte': 15})
    groups_with_student_count_lte_15 = json.loads(groups_with_student_count_lte_15.data)
    assert groups_with_student_count_lte_15 == groups_with_student_count_lte_15_mocked


def test_students_for_course(db_setup, client, db_create_tables):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


create_new_student_response = {'student_id': 201,
                               'first_name': 'George',
                               'last_name': 'Washington',
                               'group': None,
                               'courses': ['Science', 'Art', 'Physics']
                               }


def test_add_student(db_setup, client, db_create_tables):

    data = {"first_name": "George", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]}
    response = client.post('students', content_type='application/json', data=json.dumps(data))

    print(response)
    # response = json.loads(response.data)
    # assert response == create_new_student_response


def test_delete_student(db_setup, client, db_create_tables):

    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert "Chace Blackwell" in students_for_course

    response = client.delete('students/1')
    response = json.loads(response.data)
    assert response == {'mssg': 'Student with student_id=1 id has been deleted'}

    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert "Chace Blackwell" not in students_for_course


add_course_to_student_response = {'student_id': '2',
                                  'first_name': 'Kennedi',
                                  'last_name': 'Blackwell',
                                  'group': None,
                                  'courses': ['Music', 'Physics']}


def test_add_course_to_student(db_setup, client, db_create_tables):
    response = client.put('students/2/courses/9')
    assert json.loads(response.data) == add_course_to_student_response
    new_students_for_physics_mocked = students_for_physics_mocked.copy()
    new_students_for_physics_mocked.append('Kennedi Blackwell')

    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)

    assert students_for_course == new_students_for_physics_mocked


def test_delete_student_from_course(db_setup, client, db_create_tables):
    response = client.delete('students/1/courses/9')
    response = json.loads(response.data)
    assert response == {'mssg': 'Course with 9 id has been deleted'}

    new_students_for_physics_mocked = students_for_physics_mocked.copy()
    new_students_for_physics_mocked.remove('Chace Blackwell')

    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)

    assert students_for_course == new_students_for_physics_mocked

