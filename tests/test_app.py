from app.database.setup import (get_session, get_metadata_obj, get_student_table, get_student_group_table)
from sqlalchemy import select, func, URL
import json
from config import (TEST_DB_USERNAME, TEST_DB_PASSWORD, TEST_DB_NAME, DB_HOST, DB_PORT)

student_count_lte = 15


def test_option1_mock_engine(client, mocker, setup_db, create_test_tables, generate_and_add_data):
    engine = setup_db
    mocker.patch('app.database.crud.create_engine', return_value=engine)

    response = client.get('groups', query_string={'student_count_lte': student_count_lte})

    actual = json.loads(response.data)

    session = get_session(engine)

    metadata_obj = get_metadata_obj(engine)

    student_group_table = get_student_group_table(metadata_obj)
    student_table = get_student_table(metadata_obj)

    with session:
        groups = session.execute(select(student_group_table.c.group_name)
                                 .join_from(student_table, student_group_table, isouter=True)
                                 .group_by(student_group_table.c.group_name)
                                 .having(func.count(student_table.c.student_id) <= student_count_lte)
                                 ).all()

    expected = [group[0] if group[0] is not None else 'no_group' for group in groups]

    assert expected == actual


def test_option2_mock_session_and_metadata(client, mocker, setup_db, create_test_tables, generate_and_add_data):

    engine = setup_db
    metadata_obj = get_metadata_obj(engine)

    session = get_session(engine)

    mocker.patch('app.database.crud.session', return_value=session)
    mocker.patch('app.database.crud.get_metadata_obj', return_value=metadata_obj)

    response = client.get('groups', query_string={'student_count_lte': '15'})

    actual = json.loads(response.data)

    student_group_table = get_student_group_table(metadata_obj)
    student_table = get_student_table(metadata_obj)

    with session:
        groups = session.execute(select(student_group_table.c.group_name)
                                 .join_from(student_table, student_group_table, isouter=True)
                                 .group_by(student_group_table.c.group_name)
                                 .having(func.count(student_table.c.student_id) <= student_count_lte)
                                 ).all()

    expected = [group[0] if group[0] is not None else 'no_group' for group in groups]

    assert expected == actual


test_db_url = URL.create(
    "postgresql",
    username=TEST_DB_USERNAME,
    password=TEST_DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=TEST_DB_NAME
)


def test_option3_mock_url(client, setup_db, create_test_tables, mocker):

    mocker.patch('app.database.crud.URL.create', return_value=test_db_url)
    response = client.get('groups', query_string={'student_count_lte': '15'})

    actual = json.loads(response.data)

    engine = setup_db
    metadata_obj = get_metadata_obj(engine)
    student_group_table = get_student_group_table(metadata_obj)
    student_table = get_student_table(metadata_obj)
    session = get_session(engine)

    with session:
        groups = session.execute(select(student_group_table.c.group_name)
                                 .join_from(student_table, student_group_table, isouter=True)
                                 .group_by(student_group_table.c.group_name)
                                 .having(func.count(student_table.c.student_id) <= student_count_lte)
                                 ).all()

    expected = [group[0] if group[0] is not None else 'no_group' for group in groups]

    assert expected == actual
