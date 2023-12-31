from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class GroupModel(Base):
    __tablename__ = 'student_group'

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(5), nullable=False, unique=True)


class StudentModel(Base):
    __tablename__ = 'student'

    student_id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey('student_group.group_id'))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)


class CourseModel(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)


# course_student_table = Table(
#     "course_student",
#     Base.metadata,
#     Column("course_id", ForeignKey("course.course_id"), primary_key=True),
#     Column("student_id", ForeignKey("student.student_id"), primary_key=True),
# )
class CourseStudentModel(Base):
    __tablename__ = 'course_student'

    course_id = Column(Integer, ForeignKey('course.course_id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'), primary_key=True)
    # course = relationship("CourseModel", backref="student")
    # student = relationship("StudentModel", backref="course")