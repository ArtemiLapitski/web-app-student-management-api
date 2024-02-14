from flask_restful import Resource
from flask import abort
from app.database.crud import (add_student, get_groups_lte_student_count, get_students_for_course, delete_student,
                               get_student, add_course_to_student, delete_student_from_course)
from app.database.validation import check_student_id, check_course_id, check_course_for_student
from app.schema.schemas import StudentCountToValidate, CourseNameToValidate, StudentToCreate, StudentToRetrieve
from flask_pydantic import validate


class Groups(Resource):
    @validate()
    def get(self, query: StudentCountToValidate):
        student_count_lte = query.student_count_lte
        return get_groups_lte_student_count(student_count_lte)


class Students(Resource):
    @validate()
    def get(self, query: CourseNameToValidate):
        course_name = query.course
        return get_students_for_course(course_name)

    @validate()
    def post(self, body: StudentToCreate):
        student_id = add_student(**body.dict())
        return StudentToRetrieve(**get_student(student_id)).dict(), 201

    @validate()
    def delete(self, student_id: int):
        is_student = check_student_id(student_id)
        if is_student:
            delete_student(student_id)
            return {'mssg': f"Student under id '{student_id}' has been deleted"}
        else:
            abort(400, f"Student under id '{student_id}' does not exist")


class StudentsCourses(Resource):
    @validate()
    def put(self, student_id: int, course_id: int):
        is_student = check_student_id(student_id)
        if not is_student:
            abort(400, f"Student under id '{student_id}' does not exist")

        is_course = check_course_id(course_id)
        if not is_course:
            abort(400, f"Course under id '{course_id}' does not exist")

        is_course_for_student = check_course_for_student(student_id, course_id)
        if is_course_for_student:
            abort(400, "This course is already assigned to student")

        add_course_to_student(student_id=student_id, course_id=course_id)
        return StudentToRetrieve(**get_student(student_id)).dict(), 201

    @validate()
    def delete(self, student_id: int, course_id: int):
        is_student = check_student_id(student_id)
        if not is_student:
            abort(400, f"Student under id '{student_id}' does not exist")

        is_course = check_course_id(course_id)
        if not is_course:
            abort(400, f"Course under id '{course_id}' does not exist")

        is_course_for_student = check_course_for_student(student_id, course_id)
        if not is_course_for_student:
            abort(400, "This course is not assigned to student")

        delete_student_from_course(student_id=student_id, course_id=course_id)
        return {'mssg': f"Course under id '{course_id}' has been deleted"}
