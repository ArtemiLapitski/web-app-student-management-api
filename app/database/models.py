from app.database.db import db


class GroupModel(db.Model):
    __tablename__ = 'student_group'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(5), nullable=False, unique=True)


class StudentModel(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.ForeignKey('student_group.group_id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)


class CourseModel(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)


class CourseStudentModel(db.Model):
    __tablename__ = 'course_student'

    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
