from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import Session
from config import (DB_USERNAME, DB_PASSWORD, DB_ROLE, DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
                    DB_SUPERUSER_USERNAME, DB_PORT, CREATE_TABLES_SQL_FILE_PATH)
from pytest import fixture
from app.database.setup import (create_db, create_tables, add_data, get_session)
from app.generate_data import generate_test_data
from main import create_app, create_api
from app.urls import add_urls
from tests.mocks import groups_mock, courses_mock, data_by_student_mock
# from app.database.connection import engine


@fixture(scope='session')
def db_setup(request):
    db_engine = create_db(DB_SUPERUSER_USERNAME,
                       DB_SUPERUSER_PASSWORD,
                       DB_USERNAME,
                       DB_PASSWORD,
                       DB_NAME,
                       DB_ROLE,
                       DB_PORT,
                       DB_HOST)

    create_tables(db_engine, CREATE_TABLES_SQL_FILE_PATH)
    db_session = get_session(db_engine)
    with db_session:
        add_data(db_session, groups=groups_mock, courses=courses_mock, data_by_student=data_by_student_mock)

    def teardown():
        superuser_url = URL.create(
            "postgresql",
            username=DB_SUPERUSER_USERNAME,
            password=DB_SUPERUSER_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        engine = create_engine(superuser_url)
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text(f"DROP DATABASE {DB_NAME} WITH (FORCE)"))
            conn.execute(text(f"DROP USER {DB_USERNAME}"))
            conn.execute(text(f"DROP ROLE {DB_ROLE}"))

    request.addfinalizer(teardown)

    return db_engine


@fixture(scope='function')
def db_session(db_setup):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = db_setup.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()

    # def rollback():
    #     session.close()
    #     transaction.rollback()
    #     connection.close()
    #
    # request.addfinalizer(rollback)
    #
    # return session



# @fixture(scope='function')
# def db_session(request):
#
#     def rollback():
#         session.rollback()
#         session.close()
#
#     request.addfinalizer(rollback)
#
#     return session



# @fixture(scope='function')
# def db_session(db_setup, request):
#     session = get_session(db_setup)
#
#     def rollback():
#         session.rollback()
#         session.close()
#
#     request.addfinalizer(rollback)
#
#     return session


# @fixture(scope='function')
# def db_session(db_setup, request):
#     session = get_session(db_setup)
#
#
#     yield session
#
#     session.rollback()
#     session.close()


# @fixture(scope='module')
# def get_test_data():
#     return generate_test_data()
#
#
# @fixture(scope='module')
# def add_test_data(setup_db, get_test_data):
#     engine = setup_db
#     session = get_session(engine)
#     add_data(session, **get_test_data)


# @fixture(scope='module')
# def add_mocked_data(setup_db):
#     engine = setup_db
#     session = get_session(engine)
#     add_data(session, groups=groups_mock, courses=courses_mock, data_by_student=data_by_students_mock)
#

@fixture()
def app():
    app = create_app()
    return app


@fixture()
def client(app):
    api = create_api(app)
    add_urls(api)
    return app.test_client()
