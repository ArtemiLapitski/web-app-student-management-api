from app.database.setup import (create_db_and_user, create_tables_with_data, get_session)
from os import environ
from app.generate_data import generate_test_data
from sqlalchemy import create_engine


DB_SUPERUSER_USERNAME = environ['DB_SUPERUSER_USERNAME']
DB_SUPERUSER_PASSWORD = environ['DB_SUPERUSER_PASSWORD']
DB_USERNAME = environ['DB_USERNAME']
DB_PASSWORD = environ['DB_PASSWORD']
DB_NAME = environ['DB_NAME']
DB_ROLE = environ['DB_ROLE']
DB_PORT = int(environ['DB_PORT'])
DB_HOST = "host.docker.internal"


DB_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


if __name__ == "__main__":
    create_db_and_user(superuser_username=DB_SUPERUSER_USERNAME,
                       superuser_password=DB_SUPERUSER_PASSWORD,
                       username=DB_USERNAME,
                       password=DB_PASSWORD,
                       db_name=DB_NAME,
                       role=DB_ROLE,
                       port=DB_PORT,
                       host=DB_HOST)

    generated_data = generate_test_data()

    engine = create_engine(DB_URL)
    session = get_session(engine)

    create_tables_with_data(engine, session, **generated_data)
