from app.database.validation import get_list_of_courses, get_list_of_groups


def student_count_validation(cls, v):
    if v < 0:
        raise ValueError("Amount of students cannot be negative")
    else:
        return v


def course_name_validation(cls, v):
    all_courses = get_list_of_courses()
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


def courses_list_validation(cls, v):
    all_courses = get_list_of_courses()
    for course_name in v:
        if course_name not in all_courses:
            raise ValueError(f"'{course_name}' course does not exist")
        elif not course_name.replace(' ', '').isalpha():
            raise ValueError("Course name should not contain numbers or special characters")
    return v


def group_validation(cls, v):
    all_groups = get_list_of_groups()
    if v != 'no_group' and v not in all_groups:
        raise ValueError(f"'{v}' group does not exist")
    else:
        return v
