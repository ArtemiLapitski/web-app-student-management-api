import json
from tests.mocks import students_for_physics_mocked, groups_with_student_count_lte_15_mocked


def test_students_for_physics_1(client, db_setup, db_session):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


def test_add_course_to_student(client, db_setup, db_session):
    response = client.put('students/2/courses/9')
    # assert json.loads(response.data) == add_course_to_student_response
    # students_for_physics_mocked.append('Kennedi Blackwell')
    #
    # students_for_course = client.get('students', query_string={'course': 'Physics'})
    # students_for_course = json.loads(students_for_course.data)
    #
    # assert students_for_course == students_for_physics_mocked
#
#
def test_students_for_physics_2(client, db_setup, db_session):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


