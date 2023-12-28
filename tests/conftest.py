from sqlalchemy import URL, create_engine, text
from config import (DB_USERNAME, DB_PASSWORD, DB_ROLE, DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
                    DB_SUPERUSER_USERNAME, DB_PORT, CREATE_TABLES_SQL_FILE_PATH)
from pytest import fixture
from app.database.setup import (create_db, create_tables, add_test_data, get_session)
from app.generate_test_data import generate_test_data
from main import create_app, create_api
from app.urls import add_urls


@fixture(scope='module')
def setup_db(request):
    engine = create_db(DB_SUPERUSER_USERNAME,
                       DB_SUPERUSER_PASSWORD,
                       DB_USERNAME,
                       DB_PASSWORD,
                       DB_NAME,
                       DB_ROLE,
                       DB_PORT,
                       DB_HOST)

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

    return engine


@fixture(scope='module')
def create_test_tables(setup_db):

    engine = setup_db

    create_tables(engine, CREATE_TABLES_SQL_FILE_PATH)


@fixture(scope='module')
def generate_and_get_data():

    return generate_test_data()


@fixture(scope='module')
def add_data(setup_db, create_test_tables, generate_and_get_data):
    engine = setup_db

    session = get_session(engine)

    generated_test_data = generate_and_get_data

    add_test_data(
        session,
        **generated_test_data
    )


@fixture()
def app():
    app = create_app()
    return app


@fixture()
def client(app):
    api = create_api(app)
    add_urls(api)
    return app.test_client()
