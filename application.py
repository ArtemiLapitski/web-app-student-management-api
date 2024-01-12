from sqlalchemy import create_engine, URL
from config import (DB_HOST, DB_NAME, DB_PORT, DB_SUPERUSER_USERNAME, DB_SUPERUSER_PASSWORD)
from app.database.setup import get_session
from app.database.models import CourseModel


db_url = URL.create(
    "postgresql",
    username=DB_SUPERUSER_USERNAME,
    password=DB_SUPERUSER_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(db_url)

prod_session = get_session(engine)


def add_course(course_name):
    with prod_session:
        prod_session.add(CourseModel(course_name=course_name))
        prod_session.commit()
