import json
from tests.mocks import students_for_physics_mocked
from app.database.models import CourseModel
from sqlalchemy import select


def test_1(db_setup, client, session):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


def test_2(db_setup, client, session):
    response = client.put('students/2/courses/9')
    print(response)


def test_3(db_setup, client, session):
    students_for_course = client.get('students', query_string={'course': 'Physics'})
    students_for_course = json.loads(students_for_course.data)
    assert students_for_course == students_for_physics_mocked


def test_add_course(db_setup, client, session):
    course = CourseModel(course_name="some_course")
    session.add(course)
    session.commit()


def test_check_course_wasnt_added(db_setup, client, session):
    all_courses = session.execute(select(CourseModel.course_name)).all()

    print([course_name[0] for course_name in all_courses])
    assert [course_name[0] for course_name in all_courses] == ['Physical Education', 'Science', 'Art', 'Mathematics',
                                                               'English', 'Music', 'Chemistry', 'Algebra', 'Physics',
                                                               'Geography']
