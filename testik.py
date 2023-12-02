from app import session, course_table, student_table, student_group_table, course_student_table
from sqlalchemy import text, delete, select, insert
from app.schemas import StudentIdToValidate

# get coourses for first and last name


def get_courses_for_student(student_id: int) -> list:
    with session:
        courses = session.execute(select(course_table.c.course_name)
                                 .join(course_student_table, course_table.c.course_id == course_student_table.c.course_id)
                                 .join(student_table, student_table.c.student_id == course_student_table.c.student_id)
                                 .where(student_table.c.student_id == student_id)).all()
    return [course_name[0] for course_name in courses]


def get_course_id(course_name: str) -> int:
    return session.scalars(select(course_table.c.course_id).where(course_table.c.course_name == course_name)).first()


# student_id = 2
# course_name = 'Mathematics'
#
# with session:
#     is_student = bool(session.execute(select(student.c.student_id).where(student.c.student_id == student_id)).all())
#
# courses = get_courses_for_student(student_id)
# if is_student and course_name not in courses:
#     course_id = get_course_id(course_name)
#     session.execute(insert(course_student).values(course_id=course_id, student_id=student_id))
#     session.commit()

# print(StudentIdToValidate(student_id=2))


def check_course_id(course_id: int):
    with session:
        is_course_id = bool(
            session.execute(select(course_table.c.course_id).where(course_table.c.course_id == course_id)).all())
    return is_course_id


# print(check_course_id(10, 201))
def check_course_for_student(student_id: int, course_id: int):
    with session:
        courses_for_student = session.execute(select(course_student_table.c.course_id)
                                              .where(course_student_table.c.student_id == student_id)).all()
    return course_id in [course_id[0] for course_id in courses_for_student]


def get_student(student_id: int) -> dict:
    with session:
        name_and_group_data = session.execute(select(student_table.c['first_name', 'last_name'],
                                                     student_group_table.c.group_name)
                                       .join(student_group_table,
                                             student_group_table.c.group_id == student_table.c.group_id)
                                       .where(student_table.c.student_id == student_id)).first()

        courses_row = session.execute(select(course_table.c.course_name)
                                  .join(course_student_table,
                                        course_student_table.c.course_id == course_table.c.course_id)
                                  .where(course_student_table.c.student_id == student_id))

        courses = [course[0] for course in courses_row]

        if not name_and_group_data:
            name_and_group_data = session.execute(select(student_table.c['first_name', 'last_name'])
                                                  .where(student_table.c.student_id == student_id)).first()

            student_data = {'first_name': name_and_group_data[0],
                            'last_name': name_and_group_data[1],
                            'group': 'no_group',
                            'courses': courses
                            }
        else:
            student_data = {'first_name': name_and_group_data[0],
                            'last_name': name_and_group_data[1],
                            'group': name_and_group_data[2],
                            'courses': courses
                            }

    return student_data

# print(get_student_data(1))
# what to do with null groups?


def add_course_to_student(student_id: int, course_id: int):
    with session:
        session.execute(insert(course_student_table).values(course_id=course_id, student_id=student_id))
        session.commit()


# add_course_to_student(1, 3)


def delete_student_from_course(student_id: int, course_id: int):
    with session:
        session.execute(delete(course_student_table)
                        .where(course_student_table.c.student_id == student_id)
                        .where(course_student_table.c.course_id == course_id))
        session.commit()

# delete_student_from_course(student_id=208, course_id=6)


print(type(session))
