from flask_restful import Resource
from app import session, student_groups, courses_students, courses, students
from sqlalchemy import select, func
from flask_pydantic import validate
from flask import request
# from app import StudentCountToValidate
from .schemas import StudentCountToValidate


# , query: StudentCountToValidate
class GroupsPerStudentCount(Resource):
    # @validate()
    def get(self):
        student_count = request.args.get("students")
        result = StudentCountToValidate(students=student_count)
        # student_count = query.students
        # if student_count:
        #     with session:
        #         groups = session.execute(select(student_groups.c.group_name)
        #                                  .join_from(students, student_groups, isouter=True)
        #                                  .group_by(student_groups.c.group_name)
        #                                  .having(func.count(students.c.student_id) <= int(student_count))
        #                                  ).all()
        #     return [group[0] if group[0] else "no_group" for group in groups]
        # else:
        #     return 'nothing'



#






# with session:
#     results = session.execute(select(student_groups.c.group_name)
#         .join_from(students, student_groups, isouter=True).group_by(student_groups.c.group_name)
#         .having(func.count(students.c.student_id) <= 15)).all()
#     print(results)
#     print([result[0] if result[0] else 'no_group' for result in results])
