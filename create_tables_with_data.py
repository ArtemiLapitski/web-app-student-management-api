from sqlalchemy import text
from app import (generate_students, assign_courses_to_students, assign_students_to_groups,
                 get_courses_and_group_by_students, generate_groups, COURSES, courses, students, student_groups,
                 courses_students, add_courses, add_students, add_groups, session)
from sqlalchemy import select
# session = get_session()

# with session:
#     with open("app/create_tables.sql") as file:
#         query = text(file.read())
#         session.execute(query)
#         session.commit()


with session:
    with open("app/drop_and_create.sql") as file:
        query = text(file.read())
        session.execute(query)
        session.commit()


students_list = generate_students()
groups_list = generate_groups()

students_by_groups = assign_students_to_groups(students_list, groups_list)
courses_by_students = assign_courses_to_students(students_list)
data_for_students = get_courses_and_group_by_students(courses_by_students, students_by_groups)

add_groups(groups_list, student_groups)
add_courses(COURSES, courses)
add_students(data_for_students, student_groups, students, courses, courses_students)


