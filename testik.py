from sqlalchemy import URL


TEST_DB_USERNAME = 'supervisor_test'
TEST_DB_PASSWORD = 'supervisor_test'
TEST_DB_NAME = 'studentsdb_test'
TEST_DB_ROLE = 'students_admin_test'
DB_HOST = 'localhost'


superuser_db_url = URL.create(
    "postgresql",
    username=TEST_DB_USERNAME,
    password=TEST_DB_PASSWORD,
    host=DB_HOST,
    port=5432,
    database=TEST_DB_NAME
)


print(superuser_db_url)

'postgresql://supervisor_test:supervisor_test@localhost:5432/studentsdb_test'

# print(help(URL.create))