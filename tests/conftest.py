from sqlalchemy import URL, create_engine, text
from app.database.setup import (create_db, create_tables, get_session, add_test_data, get_student_table,
                                get_course_student_table, get_student_group_table, get_course_table, get_metadata_obj)
from pytest import fixture
from config import (TEST_DB_USERNAME, TEST_DB_PASSWORD, TEST_DB_ROLE, TEST_DB_NAME, DB_HOST, DB_SUPERUSER_PASSWORD,
                    DB_SUPERUSER_USERNAME, DB_PORT, CREATE_TABLES_FILE_PATH)
from app.generate_test_data import generate_test_data
from main import create_app, create_api
from app.urls import add_urls


@fixture()
def app():
    app = create_app()
    return app


@fixture()
def client(app):
    api = create_api(app)
    add_urls(api)
    return app.test_client()


@fixture(scope='module')
def setup_db(request):
    engine = create_db(DB_SUPERUSER_USERNAME,
                       DB_SUPERUSER_PASSWORD,
                       TEST_DB_USERNAME,
                       TEST_DB_PASSWORD,
                       TEST_DB_NAME,
                       TEST_DB_ROLE,
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
            conn.execute(text(f"DROP DATABASE {TEST_DB_NAME} WITH (FORCE)"))
            conn.execute(text(f"DROP USER {TEST_DB_USERNAME}"))
            conn.execute(text(f"DROP ROLE {TEST_DB_ROLE}"))

    request.addfinalizer(teardown)

    return engine


@fixture(scope='module')
def create_test_tables(setup_db):

    engine = setup_db

    create_tables(engine, CREATE_TABLES_FILE_PATH)


@fixture(scope='module')
def generate_and_add_data(setup_db, create_test_tables):
    engine = setup_db

    metadata_obj = get_metadata_obj(engine)

    course_table = get_course_table(metadata_obj)
    student_group_table = get_student_group_table(metadata_obj)
    student_table = get_student_table(metadata_obj)
    course_student_table = get_course_student_table(metadata_obj)

    session = get_session(engine)

    generated_test_data = generate_test_data()

    add_test_data(
        session,
        student_group_table,
        course_table,
        student_table,
        course_student_table,
        **generated_test_data
    )

    return generated_test_data
