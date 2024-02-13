from flask_restful import Resource
from flask import abort
from app.database.crud import (add_student, get_groups_lte_student_count, get_students_for_course, delete_student,
                               get_student, add_course_to_student, delete_student_from_course)
from app.database.validation import check_student_id
from flask import request
# from app.schema.schemas import StudentCountToValidate
from app.schema.schemas import (StudentCountToValidate, CourseNameToValidate, StudentToCreate, StudentIdToValidate,
                                CourseToAdd, CourseToDelete)
from flask_pydantic import validate
# from app.exceptions import StudentIdNotFound


class Groups(Resource):
    @validate()
    def get(self, query: StudentCountToValidate):
        student_count_lte = query.student_count_lte
        return get_groups_lte_student_count(student_count_lte)

    # def get(self):
    #     student_count_lte = request.args.get("student_count_lte")
    #     student_count = StudentCountToValidate(student_count_lte=student_count_lte).student_count_lte
    #
    #     return get_groups_lte_student_count(student_count)


class Students(Resource):
    @validate()
    def get(self, query: CourseNameToValidate):

        course_name = query.course
        # course_name = CourseNameToValidate(course=course_name).course

        return get_students_for_course(course_name)

    @validate()
    def post(self, body: StudentToCreate):
        student_id = add_student(**body.dict())
        return get_student(student_id)

    @validate()
    def delete(self, student_id: int):

        is_student = check_student_id(student_id)
        if is_student:
            delete_student(student_id)
            return {'mssg': f"Student with id '{student_id}' has been deleted"}
        else:
            abort(400, f"Student under id '{student_id}' does not exist.")




        # delete_student(student_id)
        # return {'mssg': f"Student with {student_id} id has been deleted"}

    # def delete(self, student_id):
    #
    #     student_id = StudentIdToValidate(student_id=student_id)
    #     delete_student(student_id.student_id)
    #     return {'mssg': f"Student with {student_id} id has been deleted"}


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
