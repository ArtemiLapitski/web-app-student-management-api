from os import path, environ
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get("SECRET_KEY")

DB_SUPERUSER_USERNAME = environ.get("DB_SUPERUSER_USERNAME")
DB_SUPERUSER_PASSWORD = environ.get("DB_SUPERUSER_PASSWORD")
DB_USERNAME = environ.get("DB_USERNAME")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_NAME = environ.get("DB_NAME")
DB_PORT = int(environ.get("DB_PORT"))
DB_ROLE = environ.get("DB_ROLE")
DB_HOST = environ.get("DB_HOST")

DB_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DB_SUPERUSER_URL = f'postgresql://{DB_SUPERUSER_USERNAME}:{DB_SUPERUSER_PASSWORD}@{DB_HOST}:{DB_PORT}'

WORKING_DIR = path.dirname(__file__)
CREATE_TABLES_SQL_FILE_PATH = path.join(WORKING_DIR, 'app', 'database', 'create_tables.sql')

STUDENTS_PER_GROUP_MIN = 10
STUDENTS_PER_GROUP_MAX = 30
COURSES_PER_STUDENT_MIN = 1
COURSES_PER_STUDENT_MAX = 3
NUMBER_OF_STUDENTS = 200
COURSES = ['Physical Education', 'Science', 'Art', 'Mathematics', 'English', 'Music', 'Chemistry', 'Algebra', 'Physics',
           'Geography']
NAMES = ['Luca', 'Sasha', 'Amaya', 'Chace', 'Amiah', 'Essence', 'Shyann', 'Jackson', 'Jamar', 'Emanuel', 'Kristin',
         'Brenna', 'Gaige', 'Brianna', 'Quinn', 'Colten', 'Raphael', 'Keyon', 'Kennedi', 'Mackenzie']
SURNAMES = ['Schaefer', 'Sharp', 'Newton', 'Armstrong', 'Reynolds', 'Hamilton', 'Romero', 'Rush', 'Alvarez',
            'Williamson', 'Fletcher', 'Cannon', 'Blackwell', 'Mora', 'Ford', 'Lowe', 'Hutchinson', 'Pineda', 'Chaney',
            'Best']
