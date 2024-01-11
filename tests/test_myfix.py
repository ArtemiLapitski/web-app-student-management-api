import json
from tests.mocks import students_for_physics_mocked


def test_1(client, db_session):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


def test_2(client, db_session):
    client.put('students/2/courses/9')


def test_3(client, db_session):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


