from flask import Flask
from flask_restful import Api
from app.urls import add_urls
from config import SECRET_KEY, DB_URL
from app.database.db import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SECRET_KEY'] = SECRET_KEY
    return app


def init_db(app):
    return db.init_app(app)


def create_api(app):
    api = Api(app)
    return api


if __name__ == '__main__':
    app = create_app()
    init_db(app)
    api = create_api(app)
    add_urls(api)
    app.run(debug=True)


# app = create_app()
# init_db(app)
# api = create_api(app)
# add_urls(api)
# #
# with app.app_context():
#     from app.database.models import GroupModel, StudentModel, CourseModel, CourseStudentModel
#     from sqlalchemy import or_, func
#     from app.schema.schemas import StudentToRetrieve
#
#     # is_group = db.session.query(StudentModel.query.filter(StudentModel.student_id == 1)
#     #                             .filter(StudentModel.group_id != None).exists()).scalar()
#     #
#     # print(is_group)
#
#     def get_student(student_id: int) -> dict:
#         is_group = db.session.query(StudentModel.query.filter(StudentModel.student_id == student_id)
#                                     .filter(StudentModel.group_id != None).exists()).scalar()
#
#         if is_group:
#             student = db.session.query(StudentModel.first_name, StudentModel.last_name, GroupModel.group_name,
#                                        func.array_agg(CourseModel.course_name)) \
#                 .filter(CourseStudentModel.course_id == CourseModel.course_id) \
#                 .filter(GroupModel.group_id == StudentModel.group_id) \
#                 .filter(StudentModel.student_id == student_id) \
#                 .filter(CourseStudentModel.student_id == StudentModel.student_id) \
#                 .group_by(StudentModel.first_name, StudentModel.last_name, GroupModel.group_name).first()
#         else:
#             student = db.session.query(StudentModel.first_name, StudentModel.last_name, None,
#                                         func.array_agg(CourseModel.course_name))\
#                 .filter(CourseStudentModel.course_id == CourseModel.course_id)\
#                 .filter(StudentModel.student_id == student_id)\
#                 .filter(CourseStudentModel.student_id == StudentModel.student_id)\
#                 .group_by(StudentModel.first_name, StudentModel.last_name).first()
#
#         return {
#             'student_id': student_id,
#             'first_name': student[0],
#             'last_name': student[1],
#             'group': student[2],
#             'courses': student[3]
#         }
#
#
#     # print(get_student(5))
#
#     # print(StudentToRetrieve(**get_student(5)).dict())

