from sqlalchemy import create_engine, URL, text

SUPERUSER_USERNAME = 'postgres'
SUPERUSER_PASSWORD = '1996'
USER_USERNAME = 'supervisor'
USER_PASSWORD = 'supervisor'


superuser_url = URL.create(
    "postgresql",
    username=SUPERUSER_USERNAME,
    password=SUPERUSER_PASSWORD,
    host="host.docker.internal",
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
    host="host.docker.internal",
    port=5432,
    database="studentsdb"
)

engine = create_engine(superuser_studentsdb_url)

with engine.connect() as connection:
    connection.execute(text("GRANT ALL ON SCHEMA public TO students_admin"))
    connection.commit()




user_studentsdb_url = URL.create(
    "postgresql",
    username=USER_USERNAME,
    password=USER_PASSWORD,
    host="host.docker.internal",
    port=5432,
    database="studentsdb"
)

engine = create_engine(user_studentsdb_url)


with engine.connect() as connection:
    with open("create_tables.sql") as file:
                query = text(file.read())
                connection.execute(query)
                connection.commit()
