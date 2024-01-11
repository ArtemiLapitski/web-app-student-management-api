# from sqlalchemy import URL, create_engine, text
# from sqlalchemy.orm import Session
# from config import (DB_USERNAME, DB_PASSWORD, DB_ROLE, DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
#                     DB_SUPERUSER_USERNAME, DB_PORT, CREATE_TABLES_SQL_FILE_PATH)
# from app.database.setup import (create_db, create_tables, add_data, get_session)
# from main import create_app, create_api
# from app.urls import add_urls
# from tests.mocks import groups_mock, courses_mock, data_by_student_mock
# import pytest
#
#
#
# @pytest.fixture(scope='session')
# def db_setup(request):
#     db_engine = create_db(DB_SUPERUSER_USERNAME,
#                        DB_SUPERUSER_PASSWORD,
#                        DB_USERNAME,
#                        DB_PASSWORD,
#                        DB_NAME,
#                        DB_ROLE,
#                        DB_PORT,
#                        DB_HOST)
#
#     create_tables(db_engine, CREATE_TABLES_SQL_FILE_PATH)
#     db_session = get_session(db_engine)
#     with db_session:
#         add_data(db_session, groups=groups_mock, courses=courses_mock, data_by_student=data_by_student_mock)
#
#     def teardown():
#         superuser_url = URL.create(
#             "postgresql",
#             username=DB_SUPERUSER_USERNAME,
#             password=DB_SUPERUSER_PASSWORD,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#         engine = create_engine(superuser_url)
#         with engine.connect() as conn:
#             conn.execution_options(isolation_level="AUTOCOMMIT")
#             conn.execute(text(f"DROP DATABASE {DB_NAME} WITH (FORCE)"))
#             conn.execute(text(f"DROP USER {DB_USERNAME}"))
#             conn.execute(text(f"DROP ROLE {DB_ROLE}"))
#
#     request.addfinalizer(teardown)
#
#     return db_engine
#
#     # yield db_engine
#     # drop_database(f'postgresql://{"postgres"}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
#
#
# @pytest.fixture(scope='function')
# def db_session(db_setup):
#     """Returns an sqlalchemy session, and after the test tears down everything properly."""
#     connection = db_setup.connect()
#     # begin the nested transaction
#     transaction = connection.begin()
#     # use the connection with the already started transaction
#     session = Session(bind=connection)
#
#     yield session
#     session.rollback()
#     connection.close()




import pytest
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database.models import Base
from config import (DB_USERNAME, DB_PASSWORD, DB_ROLE, DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
                    DB_SUPERUSER_USERNAME, DB_PORT, CREATE_TABLES_SQL_FILE_PATH)
from pytest import fixture
from app.database.setup import (create_db, create_tables, add_data, get_session)
from main import create_app, create_api
from app.urls import add_urls
from tests.mocks import groups_mock, courses_mock, data_by_student_mock
from sqlalchemy_utils import database_exists, create_database, drop_database

from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def db_engine():
    TEST_DB_URL = f'postgresql://{"postgres"}:{DB_SUPERUSER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    engine = create_engine(TEST_DB_URL)
    if not database_exists(TEST_DB_URL):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    db_session = get_session(engine)
    with db_session:
        add_data(db_session, groups=groups_mock, courses=courses_mock, data_by_student=data_by_student_mock)

    yield engine
    drop_database(TEST_DB_URL)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()








@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture()
def client(app):
    api = create_api(app)
    add_urls(api)
    return app.test_client()
