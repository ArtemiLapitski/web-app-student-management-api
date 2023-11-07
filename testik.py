from app.database import connect_db
from app import courses, COURSES, add_courses


session = connect_db()

add_courses(session, COURSES, courses)