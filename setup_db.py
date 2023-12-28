from app.database.setup import (create_db, create_tables, add_test_data, get_session)
from os import environ
from config import CREATE_TABLES_SQL_FILE_PATH
from app.generate_test_data import generate_test_data

SUPERUSER_USERNAME = environ['DB_SUPERUSER_USERNAME']
SUPERUSER_PASSWORD = environ['DB_SUPERUSER_PASSWORD']
USERNAME = environ['DB_USERNAME']
PASSWORD = environ['DB_PASSWORD']
DB_NAME = environ['DB_NAME']
ROLE = environ['DB_ROLE']
PORT = int(environ['DB_PORT'])

HOST = "host.docker.internal"


if __name__ == "__main__":
    engine = create_db(superuser_username=SUPERUSER_USERNAME,
                       superuser_password=SUPERUSER_PASSWORD,
                       username=USERNAME,
                       password=PASSWORD,
                       db_name=DB_NAME,
                       role=ROLE,
                       port=PORT,
                       host=HOST)

    create_tables(engine, CREATE_TABLES_SQL_FILE_PATH)

    session = get_session(engine)

    generated_test_data = generate_test_data()

    add_test_data(
        session,
        **generated_test_data
    )
