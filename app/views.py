from flask_restful import Resource
from app import session, student_groups, courses_students, courses, students
from sqlalchemy import select, func




# with session:
#     group_id = session.execute(select(students.c.group_id).group_by(students.c.group_id)