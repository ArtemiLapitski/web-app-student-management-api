# from main import create_app, create_api
# from app import add_urls, USER_PASSWORD, USER_USERNAME
# import pytest
# from sqlalchemy import URL, create_engine, text
# from sqlalchemy.orm import sessionmaker
#
#
# @pytest.fixture()
# def app():
#     app = create_app()
#     return app
#
#
# @pytest.fixture()
# def client(app):
#     api = create_api(app)
#     add_urls(api)
#     return app.test_client()


# @pytest.fixture(scope="module")
# def mock_database_path():
#     testing_url = URL.create(
#         "postgresql",
#         username=USER_USERNAME,
#         password=USER_PASSWORD,
#         host="localhost",
#         port=5432
#     )
#     engine = create_engine(testing_url)
#     connection = engine.connect()
#     with connection:
#         connection.execution_options(isolation_level="AUTOCOMMIT")
#         connection.execute(text("CREATE DATABASE testdb"))
#
#     Session = sessionmaker(engine)
#     session = Session()
#
#     return session

from sqlalchemy import URL, create_engine, text
from docker.database import create_db, create_tables, get_session, add_test_data_to_db
from pytest import fixture
from config import (CREATE_TABLES_FILE_PATH, TEST_USERNAME, TEST_PASSWORD, TEST_ROLE, TEST_DB_NAME, HOST,
                    SUPERUSER_PASSWORD, SUPERUSER_USERNAME, PORT)


@fixture(scope='function')
def setup_db(request):
    engine = create_db(SUPERUSER_USERNAME,
                       SUPERUSER_PASSWORD,
                       TEST_USERNAME,
                       TEST_PASSWORD,
                       TEST_DB_NAME,
                       TEST_ROLE,
                       PORT,
                       HOST)

    def teardown():
        superuser_url = URL.create(
            "postgresql",
            username=SUPERUSER_USERNAME,
            password=SUPERUSER_PASSWORD,
            host=HOST,
            port=PORT
        )
        engine = create_engine(superuser_url)
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text(f"DROP DATABASE {TEST_DB_NAME} WITH (FORCE)"))
            conn.execute(text(f"DROP USER {TEST_USERNAME}"))
            conn.execute(text(f"DROP ROLE {TEST_ROLE}"))

    request.addfinalizer(teardown)

    return engine


@fixture(scope='function')
def create_test_tables(setup_db):

    engine = setup_db

    course_table, student_group_table, student_table, course_student_table = (
        create_tables(engine, CREATE_TABLES_FILE_PATH))

    return course_table, student_group_table, student_table, course_student_table


@fixture(scope='function')
def add_test_data(setup_db, create_test_tables):

    engine = setup_db

    course_table, student_group_table, student_table, course_student_table = create_test_tables

    session = get_session(engine)

    test_data = add_test_data_to_db(student_group_table,
                                    course_table,
                                    student_table,
                                    course_student_table,
                                    session
                                    )

    return test_data
