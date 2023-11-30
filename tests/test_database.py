# from app import add_urls, USER_PASSWORD, USER_USERNAME, SUPERUSER_USERNAME, SUPERUSER_PASSWORD
import pytest
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker


def test_db():
    # testing_url = URL.create(
    #     "postgresql",
    #     username=SUPERUSER_USERNAME,
    #     password=SUPERUSER_PASSWORD,
    #     host="localhost",
    #     port=5432
    # )
    # engine = create_engine(testing_url)
    # connection = engine.connect()
    # with connection:
    #     connection.execution_options(isolation_level="AUTOCOMMIT")
    #     connection.execute(text("CREATE DATABASE testdb"))

    SUPERUSER_USERNAME = 'postgres'
    SUPERUSER_PASSWORD = '1996'
    # USER_USERNAME = 'supervisor_test'
    # USER_PASSWORD = 'supervisor_test'


    # superuser_url = URL.create(
    #     "postgresql",
    #     username=SUPERUSER_USERNAME,
    #     password=SUPERUSER_PASSWORD,
    #     host="localhost",
    #     port=5432
    # )
    #
    # engine = create_engine(superuser_url)
    #
    # with engine.connect() as connection:
    #     connection.execution_options(isolation_level="AUTOCOMMIT")
    #     connection.execute(text("CREATE DATABASE testdb"))
    #     connection.execute(text("CREATE ROLE students_admin_test"))
    #     connection.execute(text(f"CREATE USER {USER_USERNAME} PASSWORD '{USER_PASSWORD}'"))
    #     connection.execute(text(f"GRANT students_admin_test TO {USER_USERNAME}"))
    #
    # superuser_studentsdb_url = URL.create(
    #     "postgresql",
    #     username=SUPERUSER_USERNAME,
    #     password=SUPERUSER_PASSWORD,
    #     host="localhost",
    #     port=5432,
    #     database="testdb"
    # )
    #
    # engine = create_engine(superuser_studentsdb_url)
    #
    # with engine.connect() as connection:
    #     connection.execute(text("GRANT ALL ON SCHEMA public TO students_admin"))
    #     connection.commit()
    #
    user_studentsdb_url = URL.create(
        "postgresql",
        username=SUPERUSER_USERNAME,
        password=SUPERUSER_PASSWORD,
        host="localhost",
        port=5432,
        database="testdb"
    )

    engine = create_engine(user_studentsdb_url)

    connection = engine.connect()

    with connection:
        with open("app/create_tables.sql") as file:
            query = text(file.read())
            connection.execute(query)
            connection.commit()




