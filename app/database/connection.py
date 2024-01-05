from sqlalchemy import create_engine, URL
from config import (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT)
from app.database.setup import get_session


db_url = URL.create(
    "postgresql",
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(db_url)

session = get_session(engine)

# #
# from app.database.models import GroupModel, StudentModel, CourseStudentModel, CourseModel

# # # create worked, how to delete and if it cascades?
# instance = session.query(StudentModel).filter_by(student_id=1).first()
# # # student = StudentModel(student_id=1)
# session.delete(instance)
# session.delete(StudentModel)
# #
# session.commit()

