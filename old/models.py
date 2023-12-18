# from sqlalchemy import MetaData
# from app import engine





# with session:
#     with open("create_tables.sql") as file:
#         query = text(file.read())
#         session.execute(query)
#         session.commit()

# metadata_obj = MetaData()
# metadata_obj.reflect(bind=engine)
#
# courses = metadata_obj.tables["courses"]
# students = metadata_obj.tables["students"]
# student_groups = metadata_obj.tables["student_groups"]
# courses_students = metadata_obj.tables["courses_students"]



























# from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine
# from sqlalchemy.orm import declarative_base
# from datetime import datetime
#
# Base = declarative_base()
#
#
# class GroupModel(Base):
#     __tablename__ = 'groups'
#     group_id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False, unique=True)
#
#
# class StudentModel(Base):
#     __tablename__ = 'students'
#
#     student_id = Column(Integer, primary_key=True)
#     group_id = Column(ForeignKey('groups.group_id'))
#     first_name = Column(String(100), nullable=False)
#     last_name = Column(String(100), nullable=False)
#
#
# class CourseModel(Base):
#     __tablename__ = 'courses'
#
#     course_id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False, unique=True)
#     description = Column(Text)

