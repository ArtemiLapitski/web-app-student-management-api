import pytest


student_count_lte_error_params = [
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
        -15,
        b'{"validation_error":{"query_params":[{"loc":["student_count_lte"],"msg":"Amo'
        b'unt of students cannot be negative","type":"value_error"}]}}\n'
    )
]


@pytest.mark.parametrize('student_count_lte, error', student_count_lte_error_params)
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


new_student_courses_validation = {"first_name": "George", "last_name": "Washington",
                                  "courses": ["Science", "Physics", "PE"]}
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


student_id_error_params = [
    (
        'abc',
        b'{"validation_error":{"path_params":[{"loc":["student_id"],"msg":"value is no'
        b't a valid integer","type":"type_error.integer"}]}}\n'
    ),
    (
        -2,
        b'{"message": "Student under id \'-2\' does not exist"}\n'
    ),
    (
        100500,
        b'{"message": "Student under id \'100500\' does not exist"}\n'
    )
]


@pytest.mark.parametrize('student_id, error', student_id_error_params)
def test_delete_student_id_validation(db_setup, client, db_create_tables, student_id, error):
    response = client.delete(f"students/{student_id}")
    assert response.data == error


@pytest.mark.parametrize('student_id, error', student_id_error_params)
def test_add_course_student_id_validation(db_setup, client, db_create_tables, student_id, error):
    response = client.put(f"students/{student_id}/courses/1")
    assert response.data == error


@pytest.mark.parametrize('student_id, error', student_id_error_params)
def test_delete_course_student_id_validation(db_setup, client, db_create_tables, student_id, error):
    response = client.delete(f"students/{student_id}/courses/1")
    assert response.data == error


course_id_error_params = [
    (
        'abc',
        b'{"validation_error":{"path_params":[{"loc":["course_id"],"msg":"value is no'
        b't a valid integer","type":"type_error.integer"}]}}\n'
    ),
    (
        -2,
        b'{"message": "Course under id \'-2\' does not exist"}\n'
    ),
    (
        100500,
        b'{"message": "Course under id \'100500\' does not exist"}\n'
    )
]


@pytest.mark.parametrize('course_id, error', course_id_error_params)
def test_add_course_id_validation(db_setup, client, db_create_tables, course_id, error):
    response = client.put(f"students/1/courses/{course_id}")
    assert response.data == error


@pytest.mark.parametrize('course_id, error', course_id_error_params)
def test_delete_course_id_validation(db_setup, client, db_create_tables, course_id, error):
    response = client.delete(f"students/1/courses/{course_id}")
    assert response.data == error


def test_no_course_for_student_validation(db_setup, client, db_create_tables):
    response = client.delete(f"students/1/courses/1")
    assert response.data == b'{"message": "This course is not assigned to student"}\n'


def test_course_exists_for_student_validation(db_setup, client, db_create_tables):
    response = client.put(f"students/1/courses/2")
    assert response.data == b'{"message": "This course is already assigned to student"}\n'
