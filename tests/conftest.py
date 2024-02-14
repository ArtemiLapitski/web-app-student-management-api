import pytest
from main import create_app, create_api
from app.urls import add_urls
from tests.mocks import groups_mock, courses_mock, data_by_student_mock
from config import DB_URL
from sqlalchemy import create_engine, URL, text
from app.database.setup import create_db_and_user, get_session, create_tables_with_data, drop_tables
from config import (DB_USERNAME, DB_PASSWORD, DB_ROLE, DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
                    DB_SUPERUSER_USERNAME, DB_PORT)
from app.database.db import db


@pytest.fixture(scope="session")
def db_setup():
    create_db_and_user(superuser_username=DB_SUPERUSER_USERNAME,
                       superuser_password=DB_SUPERUSER_PASSWORD,
                       username=DB_USERNAME,
                       password=DB_PASSWORD,
                       db_name=DB_NAME,
                       role=DB_ROLE,
                       port=DB_PORT,
                       host=DB_HOST)

    yield
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


@pytest.fixture(scope="session")
def client():
    app = create_app()
    db.init_app(app)
    api = create_api(app)
    add_urls(api)

    client = app.test_client()

    return client


@pytest.fixture(scope="session")
def db_engine():
    return create_engine(DB_URL)


@pytest.fixture(scope="session")
def db_session(db_engine):
    return get_session(db_engine)


@pytest.fixture(scope="function")
def db_create_tables(db_engine, db_session):
    create_tables_with_data(session=db_session, engine=db_engine, groups=groups_mock, courses=courses_mock,
                            data_by_student=data_by_student_mock)
    yield
    drop_tables(db_engine)
