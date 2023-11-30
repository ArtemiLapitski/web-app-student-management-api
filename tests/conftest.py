from main import create_app, create_api
from app import add_urls, USER_PASSWORD, USER_USERNAME
import pytest
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture()
def client(app):
    api = create_api(app)
    add_urls(api)
    return app.test_client()


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

