from sqlalchemy import select, func
from app.database.setup import create_db_and_user, create_tables, get_session, add_data
from config import COURSES
from app.database.models import StudentModel, GroupModel, CourseModel, CourseStudentModel, db
from tests.mocks import groups_mock, courses_mock, data_by_student_mock, students_mock, students_by_group_mock, \
    courses_by_student_mock


def test_students(db_setup, client):

    students_from_db = db.session.execute(select(StudentModel.student_id, StudentModel.first_name,
                                      StudentModel.last_name)).all()

    assert students_from_db == students_mock
    assert len(students_from_db) == 200


def test_groups(db_setup, client):

    groups_from_db = db.session.execute(select(GroupModel.group_name)).all()

    groups_from_db_list = [group[0] for group in groups_from_db]

    assert groups_from_db_list == groups_mock
    assert len(groups_from_db) == 10


def test_courses(db_setup, client):

    courses = db.session.execute(select(CourseModel.course_name)).all()

    courses = [course_name[0] for course_name in courses]

    assert courses == courses_mock


def test_students_by_groups(db_setup, client):

    for group, students in students_by_group_mock.items():
        students_name_only = [' '.join(student[1:]) for student in students]
        students_name_only.reverse()
        students_by_group_mock[group] = students_name_only

    students_by_groups_from_db = db.session.execute(select(
        GroupModel.group_name,
        func.array_agg(func.concat(StudentModel.first_name, ' ', StudentModel.last_name)))
        .join(StudentModel, StudentModel.group_id == GroupModel.group_id)
        .group_by(GroupModel.group_name)
        ).all()
    students_by_groups_from_db = {data[0]: data[1] for data in students_by_groups_from_db}
    
    students_without_group = db.session.execute(select(StudentModel.first_name, StudentModel.last_name)
                                             .where(StudentModel.group_id == None)).all()
    if students_without_group:
        students_without_group_strings = [' '.join(student) for student in students_without_group]
        students_without_group_strings.reverse()
        students_by_groups_from_db['no_group'] = students_without_group_strings

    assert students_by_groups_from_db == students_by_group_mock


def test_courses_by_students(db_setup, client):

    courses_by_students_from_bd = db.session.execute(
        select(
            func.concat(StudentModel.student_id,
                        ' ',
                        StudentModel.first_name,
                        ' ',
                        StudentModel.last_name
                        ),
            func.array_agg(CourseModel.course_name)
        )
        .select_from(CourseStudentModel)
        .join(CourseModel, CourseModel.course_id == CourseStudentModel.course_id)
        .join(StudentModel, CourseStudentModel.student_id == StudentModel.student_id)
        .group_by(func.concat(StudentModel.student_id,
                              ' ',
                              StudentModel.first_name,
                              ' ',
                              StudentModel.last_name))

    ).all()

    courses_by_students_from_bd = {(int(student.split()[0]), student.split()[1], student.split()[2]): courses
                                   for student, courses in courses_by_students_from_bd}

    assert courses_by_students_from_bd == courses_by_student_mock
