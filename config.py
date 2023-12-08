from os import path, environ
from dotenv import load_dotenv


WORKING_DIR = path.dirname(__file__)
CREATE_TABLES_FILE_PATH = path.join(WORKING_DIR, 'docker', 'create_tables.sql')

TEST_USERNAME = 'supervisor_test'
TEST_PASSWORD = 'supervisor_test'
TEST_DB_NAME = 'studentsdb_test'
TEST_ROLE = 'students_admin_test'
HOST = 'localhost'

DOTENV_PATH = path.join(WORKING_DIR, 'docker', '.env')
load_dotenv(DOTENV_PATH)

SECRET_KEY = environ.get("SECRET_KEY")
SUPERUSER_USERNAME = environ.get("SUPERUSER_USERNAME")
SUPERUSER_PASSWORD = environ.get("SUPERUSER_PASSWORD")
PORT = environ.get("PORT")
