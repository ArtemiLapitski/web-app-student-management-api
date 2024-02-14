from pydantic import BaseModel, validator
from .schemas_validation import (student_count_validation, course_name_validation, name_validation,
                                 courses_list_validation, group_validation)
from typing import Optional


class StudentCountToValidate(BaseModel):
    student_count_lte: int

    validate_student_count = validator('student_count_lte')(student_count_validation)


class CourseNameToValidate(BaseModel):
    course: str

    validate_course_name = validator('course', allow_reuse=True)(course_name_validation)


class StudentToCreate(BaseModel):
    first_name: str
    last_name: str
    courses: list
    group: Optional[str] = None

    validate_first_name = validator('first_name', allow_reuse=True)(name_validation)
    validate_last_name = validator('last_name', allow_reuse=True)(name_validation)
    validate_course_names = validator('courses', allow_reuse=True)(courses_list_validation)
    validate_group = validator('group')(group_validation)


class StudentToRetrieve(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    courses: list
    group: Optional[str] = None
