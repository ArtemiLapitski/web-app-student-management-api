# from app import COURSES
from app import get_list_of_courses, get_list_of_groups, check_student_id, check_course_id, check_course_for_student

all_courses = get_list_of_courses()
all_groups = get_list_of_groups()


def student_count_validation(cls, v):
    if v < 0:
        raise ValueError("Amount of students cannot be negative")
    else:
        return v


def course_name_validation(cls, v):
    if not v.replace(' ', '').isalpha():
        raise ValueError("Course name should not contain numbers or special characters")
    if v not in all_courses:
        raise ValueError(f"'{v}' course does not exist")
    else:
        return v


def name_validation(cls, v):
    if not v.isalpha():
        raise ValueError("Numbers, spaces or special characters are not allowed")
    else:
        return v.title()


def course_names_validation(cls, v):
    for course_name in v:
        if course_name not in all_courses:
            raise ValueError(f"'{course_name}' course does not exist")
        elif not course_name.replace(' ', '').isalpha():
            raise ValueError("Course name should not contain numbers or special characters")
        else:
            return v


def group_validation(cls, v):
    if v != 'no_group' and v not in all_groups:
        raise ValueError(f"'{v}' group does not exist")
    else:
        return v


def student_id_validation(cls, v):
    is_student = check_student_id(v)
    if not is_student:
        raise ValueError(f"Student with '{v}' id does not exist")
    else:
        return v


def course_id_validation(cls, v):
    is_course = check_course_id(v)
    if not is_course:
        raise ValueError(f"Course with '{v}' id does not exist")
    else:
        return v


def no_course_for_student_validation(self):
    student_id = self.student_id
    course_id = self.course_id
    is_course_for_student = check_course_for_student(student_id, course_id)
    if is_course_for_student:
        raise ValueError(f"This course is already assigned to student")


def course_exists_for_student_validation(self):
    student_id = self.student_id
    course_id = self.course_id
    is_course_for_student = check_course_for_student(student_id, course_id)
    if not is_course_for_student:
        raise ValueError(f"This course is not assigned to student")

