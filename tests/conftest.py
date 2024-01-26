import pytest
from main import create_app, create_api
from app.urls import add_urls
from tests.mocks import groups_mock, courses_mock, data_by_student_mock
from config import DB_URL
from sqlalchemy import create_engine, URL, text
from app.database.setup import create_db_and_user, create_tables, get_session, add_data
from config import (DB_USERNAME, DB_PASSWORD, DB_ROLE, DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
                    DB_SUPERUSER_USERNAME, DB_PORT, CREATE_TABLES_SQL_FILE_PATH)
from app.database.models import db


@pytest.fixture(scope="session")
def db_setup(request):
    create_db_and_user(superuser_username=DB_SUPERUSER_USERNAME,
                       superuser_password=DB_SUPERUSER_PASSWORD,
                       username=DB_USERNAME,
                       password=DB_PASSWORD,
                       db_name=DB_NAME,
                       role=DB_ROLE,
                       port=DB_PORT,
                       host=DB_HOST)

    engine = create_engine(DB_URL)

    create_tables(engine, CREATE_TABLES_SQL_FILE_PATH)

    session = get_session(engine)

    with session:
        add_data(session, groups=groups_mock, courses=courses_mock, data_by_student=data_by_student_mock)

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


@pytest.fixture(scope="session")
def client(request):
    app = create_app()
    app.config['TESTING'] = True
    db.init_app(app)
    api = create_api(app)
    add_urls(api)
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return client


@pytest.fixture(scope='function')
def session(client, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db._make_scoped_session(options=options)

    db.session = session

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
