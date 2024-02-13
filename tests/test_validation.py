import json
import pytest


params = [
    (
        None,
        b'{"validation_error":{"query_params":[{"loc":["student_count_lte"],"msg":"fie'
        b'ld required","type":"value_error.missing"}]}}\n'
    ),
    (
        "ten",
        b'{"validation_error":{"query_params":[{"loc":["student_count_lte"],"msg":"val'
        b'ue is not a valid integer","type":"type_error.integer"}]}}\n'
    ),
    (
        '-15',
        b'{"validation_error":{"query_params":[{"loc":["student_count_lte"],"msg":"Amo'
        b'unt of students cannot be negative","type":"value_error"}]}}\n'
    )
]


@pytest.mark.parametrize('student_count_lte, error', params)
def test_student_count_validation(db_setup, client, db_create_tables, student_count_lte, error):
    response = client.get('groups', query_string={'student_count_lte': student_count_lte})
    assert response.data == error


no_course_error = b'{"validation_error":{"query_params":[{"loc":["course"],' \
                  b'"msg":"\'matan\' course does not exist","type":"value_error"}]}}\n'


def test_course_name_validation(db_setup, client, db_create_tables):
    response = client.get('students', query_string={'course': 'matan'})
    assert response.data == no_course_error


new_student = {"first_name": "George!", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]}


name_error_params = [
    (
        {"first_name": "George!", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["first_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "Geo rge", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["first_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "George1", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["first_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "George", "last_name": "Washington!", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["last_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "George", "last_name": "Washington ", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["last_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "George", "last_name": "Washington1", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["last_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    )
]


@pytest.mark.parametrize('student, error', name_error_params)
def test_create_student_name_validation(db_setup, client, db_create_tables, student, error):
    response = client.post('students', json=student)
    assert response.data == error


courses_error_params = [
    (
        {"first_name": "George", "last_name": "Washington", "courses": ["PE", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["last_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "George", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["last_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    ),
    (
        {"first_name": "George", "last_name": "Washington", "courses": ["Art", "Science", "Physics"]},
        b'{"validation_error":{"body_params":[{"loc":["last_name"],"msg":"Numbers, sp'
        b'aces or special characters are not allowed","type":"value_error"}]}}\n'
    )
]


new_student_courses_validation = {"first_name": "George", "last_name": "Washington", "courses": ["Science", "Physics", "PE"]}
courses_error = (b'{"validation_error":{"body_params":[{"loc":["courses"],"msg":"\'PE\' cours'
                 b'e does not exist","type":"value_error"}]}}\n')


def test_create_student_courses_validation(db_setup, client, db_create_tables):
    response = client.post('students', json=new_student_courses_validation)
    assert response.data == courses_error


new_student_group_validation = {"first_name": "George", "last_name": "Washington",
                                "courses": ["Science", "Physics"], "group": "some_group"}
group_error = (b'{"validation_error":{"body_params":[{"loc":["group"],"msg":"\'some_group\''
               b' group does not exist","type":"value_error"}]}}\n')


def test_create_student_group_validation(db_setup, client, db_create_tables):
    response = client.post('students', json=new_student_group_validation)
    assert response.data == group_error


# DONE
# def student_count_validation(cls, v):
#     if v < 0:
#         raise ValueError("Amount of students cannot be negative")
#     else:
#         return v

# DONE
# def course_name_validation(cls, v):
#     all_courses = get_list_of_courses()
#     if not v.replace(' ', '').isalpha():
#         raise ValueError("Course name should not contain numbers or special characters")
#     if v not in all_courses:
#         raise ValueError(f"'{v}' course does not exist")
#     else:
#         return v


# DONE
# def name_validation(cls, v):
#     if not v.isalpha():
#         raise ValueError("Numbers, spaces or special characters are not allowed")
#     else:
#         return v.title()
#
## DONE
# def course_names_validation(cls, v):
#     all_courses = get_list_of_courses()
#     for course_name in v:
#         if course_name not in all_courses:
#             raise ValueError(f"'{course_name}' course does not exist")
#         elif not course_name.replace(' ', '').isalpha():
#             raise ValueError("Course name should not contain numbers or special characters")
#         else:
#             return v
#
### DONE
# def group_validation(cls, v):
#     all_groups = get_list_of_groups()
#     if v != 'no_group' and v not in all_groups:
#         raise ValueError(f"'{v}' group does not exist")
#     else:
#         return v
#
#
# def student_id_validation(cls, v):
#     is_student = check_student_id(v)
#     if not is_student:
#         raise ValueError(f"Student with '{v}' id does not exist")
#     else:
#         return v
#
#
# def course_id_validation(cls, v):
#     is_course = check_course_id(v)
#     if not is_course:
#         raise ValueError(f"Course with '{v}' id does not exist")
#     else:
#         return v
#
#
# def no_course_for_student_validation(self):
#     student_id = self.student_id
#     course_id = self.course_id
#     is_course_for_student = check_course_for_student(student_id, course_id)
#     if is_course_for_student:
#         raise ValueError(f"This course is already assigned to student")
#
#
# def course_exists_for_student_validation(self):
#     student_id = self.student_id
#     course_id = self.course_id
#     is_course_for_student = check_course_for_student(student_id, course_id)
#     if not is_course_for_student:
#         raise ValueError(f"This course is not assigned to student")