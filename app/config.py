import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.environ.get('SECRET_KEY')

DATABASE_URL: str = os.environ.get('DATABASE_URL')

SUPERUSER_USERNAME: str = os.environ.get('SUPERUSER_USERNAME')

SUPERUSER_PASSWORD: str = os.environ.get('SUPERUSER_PASSWORD')

USER_USERNAME: str = os.environ.get('USER_USERNAME')

USER_PASSWORD: str = os.environ.get('USER_PASSWORD')


COURSES = ['Physical Education', 'Science', 'Art', 'Mathematics', 'English', 'Music', 'Chemistry', 'Algebra', 'Physics',
           'Geography']

NAMES = ['Luca', 'Sasha', 'Amaya', 'Chace', 'Amiah', 'Essence', 'Shyann', 'Jackson', 'Jamar', 'Emanuel', 'Kristin',
         'Brenna', 'Gaige', 'Brianna', 'Quinn', 'Colten', 'Raphael', 'Keyon', 'Kennedi', 'Mackenzie']

SURNAMES = ['Schaefer', 'Sharp', 'Newton', 'Armstrong', 'Reynolds', 'Hamilton', 'Romero', 'Rush', 'Alvarez',
            'Williamson', 'Fletcher', 'Cannon', 'Blackwell', 'Mora', 'Ford', 'Lowe', 'Hutchinson', 'Pineda', 'Chaney',
            'Best']

LOWER_BOUND_STUDENTS_PER_GROUP = 10

UPPER_BOUND_STUDENTS_PER_GROUP = 30

LOWER_BOUND_COURSES_PER_STUDENT = 1

UPPER_BOUND_COURSES_PER_STUDENT = 3
