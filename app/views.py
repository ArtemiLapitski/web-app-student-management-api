from flask_restful import Resource
from app import (add_student, get_groups_lte_student_count, get_students_for_course, delete_student,
                 get_student, add_course_to_student, delete_student_from_course)
from sqlalchemy import select, func
from flask_pydantic import validate
from flask import request, jsonify
# from app import StudentCountToValidate
from .schemas import (StudentCountToValidate, CourseNameToValidate, StudentToCreate, StudentIdToValidate,
                      CourseToAdd, CourseToDelete)
import json


class Groups(Resource):

    def get(self):
        student_count_lte = request.args.get("student_count_lte")
        student_count = StudentCountToValidate(student_count_lte=student_count_lte).student_count_lte

        return get_groups_lte_student_count(student_count)


class Students(Resource):
    def get(self):

        course_param = request.args.get("course")
        course_name = CourseNameToValidate(course=course_param).course

        return get_students_for_course(course_name)

    def post(self):

        student_data = request.get_json()
        student_data_validated = StudentToCreate(**student_data)
        student_data_validated_dict = student_data_validated.model_dump()
        student_id = add_student(**student_data_validated_dict)

        return get_student(student_id)

    def delete(self, student_id):

        student_id = StudentIdToValidate(student_id=student_id)
        delete_student(student_id.student_id)
        return {'mssg': f"Student with {student_id} id has been deleted"}


class StudentsCourses(Resource):

    def put(self, student_id, course_id):
        data = CourseToAdd(student_id=student_id, course_id=course_id)
        add_course_to_student(student_id=data.student_id, course_id=data.course_id)
        get_student(student_id)
        return get_student(student_id)

    def delete(self, student_id, course_id):
        data = CourseToDelete(student_id=student_id, course_id=course_id)
        delete_student_from_course(student_id=data.student_id, course_id=data.course_id)
        return {'mssg': f"Course with {course_id} id has been deleted"}




