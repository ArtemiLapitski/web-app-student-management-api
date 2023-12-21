import app.database.crud
# from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from app.database.setup import get_session, get_table_object
from app.database.setup import create_group_table, create_student_table
from sqlalchemy import MetaData
# from app.database.tables import session, course_table, student_table, course_student_table, student_group_table

# 'postgresql://supervisor_test:supervisor_test@localhost:5432/studentsdb_test'

# create_student_table, create_group_table
def test_mock_engine(client, mocker, setup_db, create_test_tables, generate_and_add_data):

    engine = setup_db
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)
    group = create_group_table(metadata_obj)
    student = create_student_table(metadata_obj)

    session = get_session(engine)

    mocker.patch('app.database.crud.session', return_value=session)
    mocker.patch('app.database.crud.create_group_table', return_value=group)
    mocker.patch('app.database.crud.create_student_table', return_value=student)

    # mocker.patch('app.database.crud.course_table', return_value=course_table)

    # course_table = get_table_object(engine, 'course')
    # student_group_table = get_table_object(engine, 'student_group')
    # student_table = get_table_object(engine, 'student')
    # course_student_table = get_table_object(engine, 'course_student')

    # mocker.patch('app.database.crud.user_db_url', return_value='postgresql://supervisor_test:supervisor_test@localhost:5432/studentsdb_test')

    # mocker.patch.object(app.database.crud, 'DB_USERNAME', 'supervisor_test')

    # mocker.patch('app.database.crud.course_table', return_value=course_table)
    # mocker.patch('app.database.crud.student_table', return_value=student_table)
    # mocker.patch('app.database.crud.course_student_table', return_value=course_student_table)
    # mocker.patch('app.database.crud.student_group_table', return_value=student_group_table)
    response = client.get('groups', query_string={'student_count_lte': '15'})
    # assert response.content_type == 'application/json'
    # report = json.loads(response.data)
    print(response.data)
    # assert report == report_desc_json


def test_mock_constants(client, setup_db, create_test_tables, mocker):
    # mocker.patch.object(app.database.crud, 'DB_USERNAME', TEST_DB_USERNAME)
    mocker.patch('app.database.crud.DB_USERNAME', return_value=TEST_DB_USERNAME)
    # mocker.patch('report.report.extract_from_db', return_value=extract_from_db)
    response = client.get('groups', query_string={'student_count_lte': '15'})
    # assert response.content_type == 'application/json'
    # report = json.loads(response.data)
    print(response.data)
    # assert report == report_desc_json