import json
from tests.mocks import students_for_physics_mocked


def test_1(client, db, mocker):
    mocker.patch('app.database.connection.get_session', return_value=db)
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    print(students_for_course)
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


def test_2(client, db, mocker):
    mocker.patch('app.database.connection.get_session', return_value=db)
    response = client.put('students/2/courses/9')
    print(response)


def test_3(client, db):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


