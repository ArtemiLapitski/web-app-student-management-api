from sqlalchemy import text
from app import (generate_students, assign_courses_to_students, assign_students_to_groups,
                 get_courses_and_group_by_students, generate_groups, COURSES, course_table, student_table,
                 student_group_table, course_student_table, create_courses, create_students, create_groups, session)
from sqlalchemy import select
# session = get_session()

# with session:
#     with open("app/create_tables.sql") as file:
#         query = text(file.read())
#         session.execute(query)
#         session.commit()


# with session:
#     with open("app/drop_and_create.sql") as file:
#         query = text(file.read())
#         session.execute(query)
#         session.commit()


students_list = generate_students()
groups_list = generate_groups()

students_by_groups = assign_students_to_groups(students_list, groups_list)
courses_by_students = assign_courses_to_students(students_list)
data_for_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

create_groups(groups_list, student_group_table)
create_courses(COURSES, course_table)
create_students(data_for_students, student_group_table, student_table, course_table, course_student_table)


