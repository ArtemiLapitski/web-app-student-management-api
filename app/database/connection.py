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

#
# from app.database.models import GroupModel, StudentModel, CourseStudentModel, CourseModel
# from sqlalchemy import func
# #
#
# groups = (session.query(GroupModel.group_name)
#           .join(StudentModel)
#           .having(func.count(StudentModel.student_id) <= 40)
#           .group_by(GroupModel.group_name).all())
#
# print(groups)
# courses = session.query(CourseModel.course_name
#                         ).filter(CourseStudentModel.course_id == CourseModel.course_id
#                                  ).filter(CourseStudentModel.student_id == 3).all()
#
# print(courses)

# #
# def add_student(first_name: str, last_name: str, courses: list, group: str = None):
#
#     with session:
#         # group_id = session.scalars(
#         #     select(GroupModel.group_id).where(GroupModel.group_name == group)).first()
#         # student_id = session.execute(
#         #     insert(StudentModel).values(group_id=group_id, first_name=first_name, last_name=last_name)
#         # ).inserted_primary_key[0]
#         group_id = session.query(GroupModel).filter_by(group_name=group).first().group_id
#         student = StudentModel(group_id=group_id, first_name=first_name, last_name=last_name)
#         session.add(student)
#         session.commit()
#         print(student.student_id)
#
#         for course_name in courses:
#             # course_id = session.scalars(select(CourseModel.course_id)
#             #                             .where(CourseModel.course_name == course_name)).first()
#
#             # session.execute(insert(CourseStudentModel).values(course_id=course_id, student_id=student_id))
#             course_id = session.query(CourseModel).filter_by(course_name=course_name).first().course_id
#             session.add(CourseStudentModel(course_id=course_id, student_id=student.student_id))
#
#         session.commit()
#         # print(student.student_id)
#         return student.student_id
#
# add_student(first_name="Artemi", last_name="Lapitski", courses=["Mathematics", "Science", "English"], group="RW-15")


# from app.database.models import GroupModel
# group_id = session.query(GroupModel).filter_by(group_name='RW-15').first().group_id
# print(group_id)
#
#
# from app.database.models import StudentModel
# # instance = session.query(StudentModel).filter_by(student_id=201).first()
# # print(instance)
# session.add(StudentModel(first_name='Artemi', last_name='Lapitski', group_id=None))
# session.commit()

#

#
#
# def get_id_or_create_course(session, model, **kwargs):
#     instance = session.query(model).filter_by(**kwargs).first()
#     if instance:
#         return instance
#     else:
#         instance = model(**kwargs)
#         session.add(instance)
#         session.commit()
#         return instance.course_id
#
#
# def get_id_or_create_group(session, model, **kwargs):
#     instance = session.query(model).filter_by(**kwargs).first()
#     if instance:
#         return instance
#     else:
#         instance = model(**kwargs)
#         session.add(instance)
#         session.commit()
#         return instance.group_id
#
#
# result = get_id_or_create_course(session, CourseModel, course_name='Science')
#
# # print(result)
# from app.database.models import CourseStudentModel, CourseModel, GroupModel, StudentModel
# # student = StudentModel(first_name='Artemi', last_name='Lapitski', group_id=1)
# # session.add(student)
#
# # course = CourseModel(course_name='Physics')
# # session.add(course)
# # session.commit()
# #
# # instance = CourseStudentModel(course_id=2, student_id=1)
# #
# # session.add(instance)
#
#
#
#
# # create worked, how to delete and if it cascades?
# instance = session.query(StudentModel).filter_by(student_id=1).first()
# # student = StudentModel(student_id=1)
# session.delete(instance)
#
#
# session.commit()

