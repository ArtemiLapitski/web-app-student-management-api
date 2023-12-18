from sqlalchemy import create_engine, URL, text
from app.config import SUPERUSER_PASSWORD, SUPERUSER_USERNAME, USER_PASSWORD, USER_USERNAME


superuser_url = URL.create(
    "postgresql",
    username=SUPERUSER_USERNAME,
    password=SUPERUSER_PASSWORD,
    host="localhost",
    port=5432
)

engine = create_engine(superuser_url)


with engine.connect() as connection:
    connection.execution_options(isolation_level="AUTOCOMMIT")
    connection.execute(text("CREATE DATABASE studentsdb"))
    connection.execute(text("CREATE ROLE students_admin"))
    connection.execute(text(f"CREATE USER {USER_USERNAME} PASSWORD '{USER_PASSWORD}'"))
    connection.execute(text(f"GRANT students_admin TO {USER_USERNAME}"))


superuser_studentsdb_url = URL.create(
    "postgresql",
    username=SUPERUSER_USERNAME,
    password=SUPERUSER_PASSWORD,
    host="localhost",
    port=5432,
    database="studentsdb"
)

engine = create_engine(superuser_studentsdb_url)

with engine.connect() as connection:
    connection.execute(text("GRANT ALL ON SCHEMA public TO students_admin"))
    connection.commit()


# user_studentsdb_url = URL.create(
#     "postgresql",
#     username=USER_USERNAME,
#     password=USER_PASSWORD,
#     host="localhost",
#     port=5432,
#     database="studentsdb"
# )
#
# engine = create_engine(user_studentsdb_url)

# CREATE TABLES AND ADD RANDOMLY GENERATED DATA TO DB USING user_studentsdb_url in this .py file in root folder


# engine = create_engine(user_studentsdb_url)
#
# with engine.connect() as connection:
#     with open("app/sql_files/create_tables.sql") as file:
#                 query = text(file.read())
#                 connection.execute(query)
#                 connection.commit()