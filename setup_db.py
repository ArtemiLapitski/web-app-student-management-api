from app.database.setup import (create_db_and_user, create_tables, add_data, get_session)
from os import environ
from config import CREATE_TABLES_SQL_FILE_PATH, DB_URL
from app.generate_data import generate_test_data
from sqlalchemy import create_engine

# to delete
DB_SUPERUSER_USERNAME = environ['DB_SUPERUSER_USERNAME']
DB_SUPERUSER_PASSWORD = environ['DB_SUPERUSER_PASSWORD']
DB_USERNAME = environ['DB_USERNAME']
DB_PASSWORD = environ['DB_PASSWORD']
DB_NAME = environ['DB_NAME']
DB_ROLE = environ['DB_ROLE']
DB_PORT = int(environ['DB_PORT'])

# DB_HOST = "host.docker.internal"
DB_HOST = 'localhost'


if __name__ == "__main__":
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

    generated_test_data = generate_test_data()

    session = get_session(engine)

    with session:
        add_data(session, **generated_test_data)
