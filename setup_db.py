from app.database.setup import (create_db, create_tables, add_data, get_session)
from os import environ
from config import CREATE_TABLES_SQL_FILE_PATH
from app.generate_test_data import generate_test_data

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
    engine = create_db(superuser_username=DB_SUPERUSER_USERNAME,
                       superuser_password=DB_SUPERUSER_PASSWORD,
                       username=DB_USERNAME,
                       password=DB_PASSWORD,
                       db_name=DB_NAME,
                       role=DB_ROLE,
                       port=DB_PORT,
                       host=DB_HOST)

    create_tables(engine, CREATE_TABLES_SQL_FILE_PATH)

    session = get_session(engine)

    generated_test_data = generate_test_data()
#
#
#
#     # add_test_data(
#     #     session,
#     #     **generated_test_data
#     # )
#
    add_data(session, generated_test_data['data_by_student'])
#
#
# from sqlalchemy import URL, create_engine, text
#
# superuser_url = URL.create(
#     "postgresql",
#     username=DB_SUPERUSER_USERNAME,
#     password=DB_SUPERUSER_PASSWORD,
#     host=DB_HOST,
#     port=DB_PORT
# )
# engine = create_engine(superuser_url)
# with engine.connect() as conn:
#     conn.execution_options(isolation_level="AUTOCOMMIT")
#     conn.execute(text(f"DROP DATABASE {DB_NAME} WITH (FORCE)"))
#     conn.execute(text(f"DROP USER {DB_USERNAME}"))
#     conn.execute(text(f"DROP ROLE {DB_ROLE}"))